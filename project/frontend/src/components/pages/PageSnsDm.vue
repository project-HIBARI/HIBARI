<script setup>
/**
 * ページ: SNS ダイレクトメッセージ（一覧 + 詳細）
 */
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import UiButton from '../ui/UiButton.vue'
import UiIco from '../ui/UiIco.vue'
import SnsReportModal from '../modals/SnsReportModal.vue'
import StoryAvatar from '../ui/StoryAvatar.vue'
import { useAuth } from '../../composables/useAuth.js'
import { useSnsDmUnread } from '../../composables/useSnsDmUnread.js'
import {
  fetchDmThreads,
  getOrCreateDmThread,
  fetchDmThread,
  markDmThreadRead,
  acceptDmRequest,
  rejectDmRequest,
  sendDmInThread,
  sendDm,
  deleteDmMessage,
  searchDmUsers,
  uploadDmMedia,
  toggleSnsBlock,
} from '../../api/sns.js'

const props = defineProps({
  targetAccountId: { type: Number, default: null },
  /** 通知等、外部から特定のスレッドを直接開くためのトリガー */
  targetThreadId: { type: Number, default: null },
})

const emit = defineEmits(['need-auth', 'open-chat', 'open-profile'])

const { isLoggedIn } = useAuth()
const { refresh: refreshUnread } = useSnsDmUnread()

const box = ref('inbox')
const threads = ref([])
const threadsLoading = ref(true)
const threadsError = ref('')
const threadsNextBeforeId = ref(null)
const loadingMoreThreads = ref(false)

const activeThreadId = ref(null)
const activeThread = ref(null)
const messages = ref([])
const threadLoading = ref(false)
const threadError = ref('')
const nextBeforeId = ref(null)
const loadingOlder = ref(false)
const reportTarget = ref(null)
const blockBusy = ref(false)

function onReportUser() {
  if (!activeThread.value) return
  reportTarget.value = { type: 'user', id: activeThread.value.other.account_id }
}

function onReportMessage(messageId) {
  reportTarget.value = { type: 'dm_message', id: messageId }
}

async function onBlockUser() {
  if (!activeThread.value || blockBusy.value) return
  if (!window.confirm(`${activeThread.value.other.name}さんをブロックしますか？`)) return
  blockBusy.value = true
  try {
    await toggleSnsBlock(activeThread.value.other.account_id)
    closeThread()
    loadThreads()
  } catch (err) {
    threadError.value = err?.message || 'ブロックに失敗しました'
  } finally {
    blockBusy.value = false
  }
}

async function onAcceptRequest() {
  if (!activeThreadId.value) return
  try {
    await acceptDmRequest(activeThreadId.value)
    await openThread(activeThreadId.value)
    await loadThreads()
  } catch (err) {
    threadError.value = err?.message || 'リクエストの承認に失敗しました'
  }
}

async function onRejectRequest() {
  if (!activeThreadId.value) return
  try {
    await rejectDmRequest(activeThreadId.value)
    closeThread()
    box.value = 'requests'
    await loadThreads()
  } catch (err) {
    threadError.value = err?.message || 'リクエストの削除に失敗しました'
  }
}

const messageInput = ref('')
const sending = ref(false)
const messagesEndRef = ref(null)

const showSearch = ref(false)
const searchQuery = ref('')
const searchResults = ref([])
const searching = ref(false)

const MAX_MESSAGE = 2000

async function loadThreads({ append = false } = {}) {
  if (append) {
    if (!threadsNextBeforeId.value || loadingMoreThreads.value) return
    loadingMoreThreads.value = true
  } else {
    threadsLoading.value = true
    threadsError.value = ''
  }
  try {
    const data = await fetchDmThreads(box.value, {
      beforeId: append ? threadsNextBeforeId.value : null,
    })
    threads.value = append ? [...threads.value, ...(data.threads || [])] : (data.threads || [])
    threadsNextBeforeId.value = data.next_before_id || null
  } catch (err) {
    threadsError.value = err?.message || 'DM一覧の取得に失敗しました'
  } finally {
    threadsLoading.value = false
    loadingMoreThreads.value = false
  }
}

function onBoxChange(next) {
  box.value = next
  threadsNextBeforeId.value = null
  loadThreads()
}

async function scrollToBottom() {
  await nextTick()
  messagesEndRef.value?.scrollIntoView({ block: 'end' })
}

function touchThreadPreview(threadId, lastMessage) {
  const idx = threads.value.findIndex((t) => t.thread_id === threadId)
  if (idx < 0) {
    loadThreads()
    return
  }
  const current = threads.value[idx]
  threads.value.splice(idx, 1)
  threads.value.unshift({
    ...current,
    last_message: lastMessage,
    updated_at: lastMessage?.created_at || new Date().toISOString(),
    unread_count: 0,
  })
}

function appendSentMessage(result) {
  const message = result?.message
  if (!message) {
    openThread(result.thread_id || activeThreadId.value)
    return
  }
  if (!activeThreadId.value) activeThreadId.value = result.thread_id
  messages.value = [...messages.value, message]
  touchThreadPreview(activeThreadId.value, {
    body: message.body,
    message_type: message.message_type,
    reaction_emoji: message.reaction_emoji,
    is_mine: true,
    created_at: message.created_at,
  })
  scrollToBottom()
  refreshUnread()
}

async function openThread(threadId) {
  activeThreadId.value = threadId
  threadLoading.value = true
  threadError.value = ''
  try {
    const data = await fetchDmThread(threadId)
    activeThread.value = data
    messages.value = data.messages
    nextBeforeId.value = data.next_before_id
    await markDmThreadRead(threadId)
    const idx = threads.value.findIndex((t) => t.thread_id === threadId)
    if (idx >= 0 && threads.value[idx].unread_count) {
      threads.value[idx] = { ...threads.value[idx], unread_count: 0 }
    }
    refreshUnread()
    scrollToBottom()
  } catch (err) {
    threadError.value = err?.message || 'DMの取得に失敗しました'
  } finally {
    threadLoading.value = false
  }
}

function closeThread() {
  activeThreadId.value = null
  activeThread.value = null
  messages.value = []
  nextBeforeId.value = null
}

async function loadOlderMessages() {
  if (!activeThreadId.value || !nextBeforeId.value || loadingOlder.value) return
  loadingOlder.value = true
  try {
    const data = await fetchDmThread(activeThreadId.value, { beforeId: nextBeforeId.value })
    messages.value = [...data.messages, ...messages.value]
    nextBeforeId.value = data.next_before_id
  } catch (err) {
    threadError.value = err?.message || '過去のメッセージを読み込めませんでした'
  } finally {
    loadingOlder.value = false
  }
}

async function startThreadWith(accountId) {
  if (!isLoggedIn.value) {
    emit('need-auth', { mode: 'login' })
    return
  }
  showSearch.value = false
  threadLoading.value = true
  threadError.value = ''
  try {
    const data = await getOrCreateDmThread(accountId)
    await openThread(data.thread_id)
    await loadThreads()
  } catch (err) {
    threadError.value = err?.message || 'DMの開始に失敗しました'
  } finally {
    threadLoading.value = false
  }
}

async function sendMessage() {
  const body = messageInput.value.trim()
  if (!body || sending.value || !activeThread.value) return
  sending.value = true
  try {
    let result
    if (activeThreadId.value) {
      result = await sendDmInThread(activeThreadId.value, { message_type: 'text', body })
    } else {
      result = await sendDm({ recipient_id: activeThread.value.other.account_id, message_type: 'text', body })
    }
    messageInput.value = ''
    appendSentMessage(result)
  } catch (err) {
    threadError.value = err?.message || 'メッセージの送信に失敗しました'
  } finally {
    sending.value = false
  }
}

async function onImageSelect(e) {
  const file = e.target.files?.[0]
  e.target.value = ''
  if (!file || sending.value || !activeThread.value) return
  sending.value = true
  try {
    const uploaded = await uploadDmMedia(file)
    let result
    if (activeThreadId.value) {
      result = await sendDmInThread(activeThreadId.value, { message_type: 'image', media_path: uploaded.path })
    } else {
      result = await sendDm({
        recipient_id: activeThread.value.other.account_id,
        message_type: 'image',
        media_path: uploaded.path,
      })
    }
    appendSentMessage(result)
  } catch (err) {
    threadError.value = err?.message || '画像の送信に失敗しました'
  } finally {
    sending.value = false
  }
}

async function onDeleteMessage(messageId) {
  if (!window.confirm('このメッセージを削除しますか？')) return
  try {
    await deleteDmMessage(messageId)
    const idx = messages.value.findIndex((m) => m.message_id === messageId)
    if (idx >= 0) {
      messages.value[idx] = {
        ...messages.value[idx],
        message_type: 'deleted',
        body: '',
        media_path: null,
      }
    }
    const last = [...messages.value].reverse().find((m) => m.message_type !== 'deleted')
    if (activeThreadId.value) {
      touchThreadPreview(activeThreadId.value, last ? {
        body: last.body,
        message_type: last.message_type,
        reaction_emoji: last.reaction_emoji,
        is_mine: last.is_mine,
        created_at: last.created_at,
      } : null)
    }
  } catch (err) {
    threadError.value = err?.message || '削除に失敗しました'
  }
}

let searchDebounce = null
function onSearchInput() {
  clearTimeout(searchDebounce)
  const q = searchQuery.value.trim()
  if (!q) {
    searchResults.value = []
    return
  }
  searchDebounce = setTimeout(async () => {
    searching.value = true
    try {
      const data = await searchDmUsers(q)
      searchResults.value = data.users
    } catch {
      searchResults.value = []
    } finally {
      searching.value = false
    }
  }, 300)
}

function formatTime(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleString('ja-JP', { month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function messageSummary(msg) {
  if (!msg) return 'メッセージはまだありません'
  if (msg.message_type === 'image') return (msg.is_mine ? 'あなた: ' : '') + '画像を送信しました'
  if (msg.message_type === 'post_share') return (msg.is_mine ? 'あなた: ' : '') + '投稿を共有しました'
  if (msg.message_type === 'story_reply') return (msg.is_mine ? 'あなた: ' : '') + 'ストーリーズに返信しました'
  if (msg.message_type === 'story_reaction') return (msg.is_mine ? 'あなた: ' : '') + `${msg.reaction_emoji || ''} ストーリーズにリアクションしました`.trim()
  return (msg.is_mine ? 'あなた: ' : '') + msg.body
}

watch(
  () => props.targetAccountId,
  (id) => {
    if (id) startThreadWith(id)
  },
  { immediate: true },
)

watch(
  () => props.targetThreadId,
  (id) => {
    if (id) openThread(id)
  },
  { immediate: true },
)

onMounted(() => {
  loadThreads()
})
</script>

<template>
  <div class="sns-dm">
    <p v-if="!isLoggedIn" class="sns-dm__state">DM機能を利用するにはログインしてください。</p>

    <template v-else>
      <div v-if="!activeThread" class="sns-dm__list">
        <header class="sns-dm__list-head">
          <h1 class="sns-dm__title">メッセージ</h1>
          <button type="button" class="sns-dm__icon-btn" aria-label="ユーザーを検索" @click="showSearch = true">
            <UiIco name="search" :size="18" />
          </button>
        </header>

        <nav class="sns-dm__box-tabs">
          <button type="button" :class="{ active: box === 'inbox' }" @click="onBoxChange('inbox')">受信</button>
          <button type="button" :class="{ active: box === 'requests' }" @click="onBoxChange('requests')">リクエスト</button>
        </nav>

        <p v-if="threadsLoading" class="sns-dm__state">読み込み中…</p>
        <template v-else-if="threadsError">
          <p class="sns-dm__state sns-dm__state--error">{{ threadsError }}</p>
          <UiButton variant="outline" size="sm" @click="loadThreads">再試行</UiButton>
        </template>
        <p v-else-if="!threads.length" class="sns-dm__state">
          {{ box === 'requests' ? 'メッセージリクエストはありません' : 'まだDMがありません。ユーザーを検索してメッセージを送ってみましょう。' }}
        </p>
        <ul v-else class="sns-dm__thread-list">
          <li v-for="t in threads" :key="t.thread_id" class="sns-dm__thread-row">
            <StoryAvatar
              :account-id="t.other.account_id"
              :name="t.other.name"
              :avatar-path="t.other.avatar_path"
              :size="44"
              @open-profile="openThread(t.thread_id)"
            />
            <button type="button" class="sns-dm__thread-item" @click="openThread(t.thread_id)">
              <span class="sns-dm__thread-body">
                <span class="sns-dm__thread-name">{{ t.other.name }}</span>
                <span class="sns-dm__thread-preview">{{ messageSummary(t.last_message) }}</span>
              </span>
              <span class="sns-dm__thread-meta">
                <span class="sns-dm__thread-time">{{ formatTime(t.updated_at) }}</span>
                <span v-if="t.unread_count" class="sns-dm__badge">{{ t.unread_count }}</span>
              </span>
            </button>
          </li>
        </ul>
        <div v-if="threadsNextBeforeId" class="sns-dm__more-wrap">
          <UiButton
            variant="outline"
            size="sm"
            :disabled="loadingMoreThreads"
            @click="loadThreads({ append: true })"
          >
            {{ loadingMoreThreads ? '読み込み中…' : 'さらに読み込む' }}
          </UiButton>
        </div>

        <section class="sns-dm__chat-cta">
          <p>みんなで美空ひばりさんの思い出を語りませんか？</p>
          <UiButton variant="gold" size="sm" @click="emit('open-chat')">オープンチャットに参加する</UiButton>
        </section>
      </div>

      <div v-else class="sns-dm__thread">
        <header class="sns-dm__thread-head">
          <button type="button" class="sns-dm__icon-btn" aria-label="戻る" @click="closeThread">
            <UiIco name="arrow" :size="18" color="#f8f4ef" />
          </button>
          <span class="sns-dm__thread-author">
            <StoryAvatar
              :account-id="activeThread.other.account_id"
              :name="activeThread.other.name"
              :avatar-path="activeThread.other.avatar_path"
              :size="32"
              @open-profile="emit('open-profile', activeThread.other.account_id)"
            />
            <button type="button" @click="emit('open-profile', activeThread.other.account_id)">
              {{ activeThread.other.name }}
            </button>
          </span>
          <div class="sns-dm__thread-actions">
            <button type="button" class="sns-dm__icon-btn" aria-label="通報" @click="onReportUser">通報</button>
            <button type="button" class="sns-dm__icon-btn" aria-label="ブロック" :disabled="blockBusy" @click="onBlockUser">ブロック</button>
          </div>
        </header>

        <p v-if="activeThread.status === 'requested'" class="sns-dm__request-note">
          このユーザーからのメッセージリクエストです。返信すると受信一覧に追加されます。
        </p>
        <div v-if="activeThread.status === 'requested'" class="sns-dm__request-actions">
          <UiButton variant="gold" size="sm" @click="onAcceptRequest">承認</UiButton>
          <UiButton variant="outline" size="sm" @click="onRejectRequest">削除</UiButton>
        </div>
        <p v-if="activeThread.blocked" class="sns-dm__request-note sns-dm__request-note--error">
          ブロック中のためメッセージを送受信できません。
        </p>

        <div class="sns-dm__messages">
          <p v-if="threadLoading" class="sns-dm__state">読み込み中…</p>
          <template v-else-if="threadError">
            <p class="sns-dm__state sns-dm__state--error">{{ threadError }}</p>
          </template>
          <p v-else-if="!messages.length" class="sns-dm__state">まだメッセージがありません</p>
          <template v-else>
            <button
              v-if="nextBeforeId"
              type="button"
              class="sns-dm__older-btn"
              :disabled="loadingOlder"
              @click="loadOlderMessages"
            >
              {{ loadingOlder ? '読み込み中…' : '以前のメッセージ' }}
            </button>
            <div
              v-for="m in messages"
              :key="m.message_id"
              class="sns-dm__message"
              :class="{ 'sns-dm__message--mine': m.is_mine }"
            >
              <div class="sns-dm__bubble">
                <p v-if="m.message_type === 'deleted'" class="sns-dm__deleted">メッセージは削除されました</p>
                <img
                  v-else-if="m.message_type === 'image'"
                  :src="m.media_path"
                  alt="送信された画像"
                  loading="lazy"
                  decoding="async"
                />
                <p v-else-if="m.message_type === 'post_share'" class="sns-dm__shared">投稿を共有しました</p>
                <div v-else-if="m.message_type === 'story_reply' || m.message_type === 'story_reaction'" class="sns-dm__story-ref">
                  <div class="sns-dm__story-ref-thumb">
                    <img
                      v-if="m.story_file_path && m.story_media_type === 'image'"
                      :src="m.story_file_path"
                      alt="ストーリーズ"
                      loading="lazy"
                      decoding="async"
                    />
                    <video v-else-if="m.story_file_path && m.story_media_type === 'video'" :src="m.story_file_path" muted playsinline preload="metadata" />
                    <span v-else class="sns-dm__story-ref-fallback" aria-hidden="true">
                      <UiIco name="story-ring" :size="16" />
                    </span>
                    <span v-if="m.story_file_path && m.story_is_expired" class="sns-dm__story-ref-badge">期限切れ</span>
                  </div>
                  <div class="sns-dm__story-ref-body">
                    <p class="sns-dm__story-ref-label">
                      {{ m.message_type === 'story_reaction' ? 'ストーリーズにリアクションしました' : 'ストーリーズに返信しました' }}
                    </p>
                    <p v-if="!m.story_file_path" class="sns-dm__story-ref-expired">このストーリーズは期限切れです</p>
                    <p v-if="m.message_type === 'story_reaction'" class="sns-dm__story-ref-emoji">{{ m.reaction_emoji }}</p>
                    <p v-else-if="m.body" class="sns-dm__story-ref-text">{{ m.body }}</p>
                  </div>
                </div>
                <p v-else>{{ m.body }}</p>
              </div>
              <div class="sns-dm__message-meta">
                <span>{{ formatTime(m.created_at) }}</span>
                <button
                  v-if="m.is_mine && m.message_type !== 'deleted'"
                  type="button"
                  class="sns-dm__delete-btn"
                  @click="onDeleteMessage(m.message_id)"
                >
                  削除
                </button>
                <button
                  v-else-if="m.message_type !== 'deleted'"
                  type="button"
                  class="sns-dm__delete-btn"
                  @click="onReportMessage(m.message_id)"
                >
                  通報
                </button>
              </div>
            </div>
          </template>
          <div ref="messagesEndRef" />
        </div>

        <form v-if="!activeThread.blocked" class="sns-dm__composer" @submit.prevent="sendMessage">
          <label class="sns-dm__image-btn" aria-label="画像を送信">
            <UiIco name="image" :size="18" />
            <input type="file" accept="image/*" hidden @change="onImageSelect" />
          </label>
          <input
            v-model="messageInput"
            type="text"
            class="sns-dm__input"
            :maxlength="MAX_MESSAGE"
            placeholder="メッセージを入力"
            :disabled="sending"
          />
          <button type="submit" class="sns-dm__send-btn" :disabled="sending || !messageInput.trim()" aria-label="送信">
            <UiIco name="send" :size="18" color="#fff" />
          </button>
        </form>
      </div>
    </template>

    <div v-if="showSearch" class="sns-dm__search-overlay">
      <div class="sns-dm__search-panel">
        <div class="sns-dm__search-head">
          <input
            v-model="searchQuery"
            type="text"
            class="sns-dm__search-input"
            placeholder="ユーザー名で検索"
            @input="onSearchInput"
          />
          <button type="button" class="sns-dm__icon-btn" aria-label="閉じる" @click="showSearch = false">
            <UiIco name="close" :size="18" color="#f8f4ef" />
          </button>
        </div>
        <p v-if="searching" class="sns-dm__state">検索中…</p>
        <p v-else-if="searchQuery && !searchResults.length" class="sns-dm__state">該当するユーザーが見つかりません</p>
        <ul v-else class="sns-dm__thread-list">
          <li v-for="u in searchResults" :key="u.account_id">
            <button type="button" class="sns-dm__thread-item" @click="startThreadWith(u.account_id)">
              <span class="sns-dm__avatar">
                <img v-if="u.avatar_path" :src="u.avatar_path" :alt="u.name" />
                <span v-else>{{ (u.name || '?').charAt(0) }}</span>
              </span>
              <span class="sns-dm__thread-name">{{ u.name }}</span>
            </button>
          </li>
        </ul>
      </div>
    </div>

    <SnsReportModal
      v-if="reportTarget"
      :target-type="reportTarget.type"
      :target-id="reportTarget.id"
      @close="reportTarget = null"
    />
  </div>
</template>

<style scoped>
.sns-dm {
  width: 100%;
  max-width: min(640px, 100%);
  margin: 0 auto;
  padding: 16px 0 calc(var(--bottom-nav-height, 66px) + env(safe-area-inset-bottom, 0px) + 24px);
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 65px);
  min-height: calc(100dvh - 65px);
  min-width: 0;
  box-sizing: border-box;
}
.sns-dm__state {
  margin: 0;
  padding: 24px 16px;
  text-align: center;
  font-size: var(--font-size-button);
  color: rgba(248, 244, 239, 0.6);
}
.sns-dm__state--error {
  color: #e08a8a;
}
.sns-dm__list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0 16px;
}
.sns-dm__list-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.sns-dm__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 1.4rem;
  color: #f8f4ef;
}
.sns-dm__icon-btn {
  background: transparent;
  border: 0;
  color: #f8f4ef;
  cursor: pointer;
  padding: 6px;
}
.sns-dm__box-tabs {
  display: flex;
  gap: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}
.sns-dm__box-tabs button {
  background: transparent;
  border: 0;
  border-bottom: 2px solid transparent;
  color: rgba(248, 244, 239, 0.6);
  padding: 8px 4px;
  font-size: var(--font-size-button);
  cursor: pointer;
}
.sns-dm__box-tabs button.active {
  color: var(--kin-400);
  border-bottom-color: var(--kin-400);
}
.sns-dm__thread-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
}
.sns-dm__thread-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 4px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}
.sns-dm__thread-item {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
  padding: 0;
  background: transparent;
  border: 0;
  cursor: pointer;
  text-align: left;
}
.sns-dm__thread-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}
.sns-dm__thread-name {
  font-size: var(--font-size-button);
  color: #f8f4ef;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.sns-dm__thread-preview {
  font-size: var(--font-size-caption);
  color: rgba(248, 244, 239, 0.55);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.sns-dm__thread-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
  flex: 0 0 auto;
  max-width: 76px;
}
.sns-dm__thread-time {
  font-size: var(--font-size-badge);
  color: rgba(248, 244, 239, 0.4);
}
.sns-dm__badge {
  min-width: 18px;
  min-height: 18px;
  height: auto;
  padding: 0 5px;
  border-radius: 999px;
  background: var(--beni-600);
  color: #fff;
  font-size: var(--font-size-badge);
  line-height: 1.2;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}
.sns-dm__more-wrap {
  display: flex;
  justify-content: center;
  padding: 4px 0 8px;
}
.sns-dm__chat-cta {
  margin-top: 12px;
  padding: 16px;
  border-radius: var(--site-radius-lg);
  border: 1px solid rgba(201, 169, 97, 0.35);
  background: linear-gradient(135deg, rgba(122, 80, 136, 0.22), rgba(26, 20, 24, 0.5));
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.sns-dm__chat-cta p {
  margin: 0;
  font-size: var(--font-size-caption);
  color: rgba(248, 244, 239, 0.8);
}
.sns-dm__thread {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}
.sns-dm__thread-head {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.sns-dm__thread-author {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  min-width: 0;
}
.sns-dm__thread-author > button {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  background: transparent;
  border: 0;
  color: #f8f4ef;
  font-size: var(--font-size-small);
  cursor: pointer;
  padding: 0;
}
.sns-dm__thread-actions {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}
.sns-dm__thread-actions .sns-dm__icon-btn {
  font-size: var(--font-size-caption);
  color: rgba(248, 244, 239, 0.6);
}
.sns-dm__request-note {
  margin: 8px 16px 0;
  padding: 8px 12px;
  border-radius: var(--site-radius-sm);
  background: rgba(255, 255, 255, 0.06);
  color: rgba(248, 244, 239, 0.7);
  font-size: var(--font-size-caption);
}
.sns-dm__request-note--error {
  color: #e08a8a;
}
.sns-dm__request-actions {
  display: flex;
  gap: 8px;
  margin: 8px 16px 0;
}
.sns-dm__messages {
  flex: 1;
  overflow-y: auto;
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.sns-dm__older-btn {
  align-self: center;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  color: rgba(248, 244, 239, 0.76);
  font-size: var(--font-size-caption);
  padding: 7px 14px;
  cursor: pointer;
}
.sns-dm__older-btn:disabled {
  opacity: 0.55;
  cursor: wait;
}
.sns-dm__message {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  max-width: 78%;
}
.sns-dm__message--mine {
  align-self: flex-end;
  align-items: flex-end;
}
.sns-dm__bubble {
  padding: 8px 12px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.08);
  color: #f8f4ef;
  font-size: var(--font-size-body);
  line-height: 1.6;
  max-width: 100%;
  min-width: 0;
  word-break: break-word;
  overflow-wrap: anywhere;
}
.sns-dm__message--mine .sns-dm__bubble {
  background: var(--murasaki-700);
}
.sns-dm__bubble img {
  max-width: min(220px, 68vw);
  border-radius: 10px;
  display: block;
}
.sns-dm__bubble p {
  margin: 0;
}
.sns-dm__deleted,
.sns-dm__shared {
  font-style: italic;
  color: rgba(248, 244, 239, 0.6);
}
.sns-dm__story-ref {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  min-width: 0;
}
.sns-dm__story-ref-thumb {
  position: relative;
  flex-shrink: 0;
  width: 44px;
  height: 66px;
  border-radius: 8px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
}
.sns-dm__story-ref-thumb img,
.sns-dm__story-ref-thumb video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sns-dm__story-ref-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(248, 244, 239, 0.5);
}
.sns-dm__story-ref-badge {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 1px 0;
  text-align: center;
  font-size: var(--font-size-badge);
  background: rgba(0, 0, 0, 0.6);
  color: rgba(248, 244, 239, 0.85);
}
.sns-dm__story-ref-body {
  min-width: 0;
}
.sns-dm__story-ref-label {
  font-style: italic;
  color: rgba(248, 244, 239, 0.6);
  font-size: var(--font-size-caption);
}
.sns-dm__story-ref-expired {
  font-size: var(--font-size-caption);
  color: rgba(248, 244, 239, 0.45);
}
.sns-dm__story-ref-emoji {
  font-size: var(--font-size-subtitle);
}
.sns-dm__story-ref-text {
  color: #f8f4ef;
  overflow-wrap: anywhere;
  word-break: break-word;
}
.sns-dm__message-meta {
  display: flex;
  gap: 8px;
  margin-top: 2px;
  font-size: var(--font-size-badge);
  color: rgba(248, 244, 239, 0.4);
}
.sns-dm__delete-btn {
  background: transparent;
  border: 0;
  color: rgba(248, 244, 239, 0.4);
  cursor: pointer;
  padding: 0;
  font-size: var(--font-size-badge);
  text-decoration: underline;
}
.sns-dm__composer {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px calc(10px + env(safe-area-inset-bottom, 0px));
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}
.sns-dm__image-btn {
  color: #f8f4ef;
  cursor: pointer;
  padding: 6px;
  flex-shrink: 0;
}
.sns-dm__input {
  flex: 1;
  min-width: 0;
  min-height: 44px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.06);
  border-radius: 999px;
  padding: 9px 16px;
  font-size: var(--font-size-form-input, var(--font-size-small));
  line-height: 1.4;
  color: #f8f4ef;
  box-sizing: border-box;
}
.sns-dm__input::placeholder {
  color: rgba(248, 244, 239, 0.4);
}
.sns-dm__send-btn {
  width: 44px;
  height: 44px;
  min-width: 44px;
  min-height: 44px;
  border-radius: 50%;
  border: 0;
  background: var(--murasaki-700);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
}
.sns-dm__send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.sns-dm__search-overlay {
  position: fixed;
  inset: 0;
  z-index: 200;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 40px 16px;
}
.sns-dm__search-panel {
  width: 100%;
  max-width: 480px;
  background: #1a1418;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--site-radius-lg);
  padding: 16px;
  max-height: 70vh;
  max-height: 70dvh;
  overflow-y: auto;
  box-sizing: border-box;
}
.sns-dm__search-head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}
.sns-dm__search-input {
  flex: 1;
  min-width: 0;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.06);
  border-radius: 999px;
  padding: 8px 14px;
  font-size: var(--font-size-button);
  color: #f8f4ef;
}

@media (max-width: 767px) {
  .sns-dm {
    min-height: calc(100vh - 112px);
    min-height: calc(100dvh - 112px);
  }

  .sns-dm__thread-head {
    padding-inline: 10px;
    gap: 6px;
  }

  .sns-dm__thread-actions .sns-dm__icon-btn {
    padding-inline: 4px;
  }

  .sns-dm__message {
    max-width: 86%;
  }

  .sns-dm__composer {
    position: sticky;
    bottom: calc(var(--bottom-nav-height, 66px) + env(safe-area-inset-bottom, 0px));
    background: rgba(22, 15, 24, 0.98);
    backdrop-filter: blur(10px);
  }
}

@media (max-width: 374px) {
  .sns-dm__thread-row {
    gap: 8px;
  }

  .sns-dm__thread-time {
    display: none;
  }
}
</style>
