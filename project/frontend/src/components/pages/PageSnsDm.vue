<script setup>
/**
 * ページ: SNS ダイレクトメッセージ（一覧 + 詳細）
 */
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import UiButton from '../ui/UiButton.vue'
import UiIco from '../ui/UiIco.vue'
import SnsReportModal from '../modals/SnsReportModal.vue'
import { useAuth } from '../../composables/useAuth.js'
import { useSnsDmUnread } from '../../composables/useSnsDmUnread.js'
import {
  fetchDmThreads,
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
})

const emit = defineEmits(['need-auth', 'open-chat', 'open-profile'])

const { isLoggedIn } = useAuth()
const { refresh: refreshUnread } = useSnsDmUnread()

const box = ref('inbox')
const threads = ref([])
const threadsLoading = ref(true)
const threadsError = ref('')

const activeThreadId = ref(null)
const activeThread = ref(null)
const messages = ref([])
const threadLoading = ref(false)
const threadError = ref('')
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

async function loadThreads() {
  threadsLoading.value = true
  threadsError.value = ''
  try {
    const data = await fetchDmThreads(box.value)
    threads.value = data.threads
  } catch (err) {
    threadsError.value = err?.message || 'DM一覧の取得に失敗しました'
  } finally {
    threadsLoading.value = false
  }
}

function onBoxChange(next) {
  box.value = next
  loadThreads()
}

async function scrollToBottom() {
  await nextTick()
  messagesEndRef.value?.scrollIntoView({ block: 'end' })
}

async function openThread(threadId) {
  activeThreadId.value = threadId
  threadLoading.value = true
  threadError.value = ''
  try {
    const data = await fetchDmThread(threadId)
    activeThread.value = data
    messages.value = data.messages
    await markDmThreadRead(threadId)
    refreshUnread()
    loadThreads()
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
}

async function startThreadWith(accountId) {
  showSearch.value = false
  const existing = threads.value.find((t) => t.other.account_id === accountId)
  if (existing) {
    await openThread(existing.thread_id)
    return
  }
  activeThreadId.value = null
  activeThread.value = {
    thread_id: null,
    other: searchResults.value.find((u) => u.account_id === accountId) || { account_id: accountId, name: '', avatar_path: null },
    status: 'accepted',
    blocked: false,
  }
  messages.value = []
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
    if (!activeThreadId.value) {
      activeThreadId.value = result.thread_id
    }
    await openThread(activeThreadId.value)
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
    if (!activeThreadId.value) activeThreadId.value = result.thread_id
    await openThread(activeThreadId.value)
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
    await openThread(activeThreadId.value)
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
  return (msg.is_mine ? 'あなた: ' : '') + msg.body
}

watch(
  () => props.targetAccountId,
  (id) => {
    if (id) startThreadWith(id)
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
          <li v-for="t in threads" :key="t.thread_id">
            <button type="button" class="sns-dm__thread-item" @click="openThread(t.thread_id)">
              <span class="sns-dm__avatar">
                <img v-if="t.other.avatar_path" :src="t.other.avatar_path" :alt="t.other.name" />
                <span v-else>{{ (t.other.name || '?').charAt(0) }}</span>
              </span>
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
          <button type="button" class="sns-dm__thread-author" @click="emit('open-profile', activeThread.other.account_id)">
            <span class="sns-dm__avatar">
              <img v-if="activeThread.other.avatar_path" :src="activeThread.other.avatar_path" :alt="activeThread.other.name" />
              <span v-else>{{ (activeThread.other.name || '?').charAt(0) }}</span>
            </span>
            <span>{{ activeThread.other.name }}</span>
          </button>
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
            <div
              v-for="m in messages"
              :key="m.message_id"
              class="sns-dm__message"
              :class="{ 'sns-dm__message--mine': m.is_mine }"
            >
              <div class="sns-dm__bubble">
                <p v-if="m.message_type === 'deleted'" class="sns-dm__deleted">メッセージは削除されました</p>
                <img v-else-if="m.message_type === 'image'" :src="m.media_path" alt="送信された画像" />
                <p v-else-if="m.message_type === 'post_share'" class="sns-dm__shared">投稿を共有しました</p>
                <p v-else-if="m.message_type === 'story_reply'" class="sns-dm__shared">
                  ストーリーズへの返信：{{ m.body }}
                </p>
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
  max-width: 640px;
  margin: 0 auto;
  padding: 16px 0 calc(var(--bottom-nav-height, 66px) + env(safe-area-inset-bottom, 0px) + 24px);
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 65px);
}
.sns-dm__state {
  margin: 0;
  padding: 24px 16px;
  text-align: center;
  font-size: 13px;
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
  font-size: 13px;
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
.sns-dm__thread-item {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 10px 4px;
  background: transparent;
  border: 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  cursor: pointer;
  text-align: left;
  min-width: 0;
}
.sns-dm__avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--murasaki-700);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}
.sns-dm__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sns-dm__thread-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}
.sns-dm__thread-name {
  font-size: 13px;
  color: #f8f4ef;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.sns-dm__thread-preview {
  font-size: 12px;
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
  font-size: 10px;
  color: rgba(248, 244, 239, 0.4);
}
.sns-dm__badge {
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 999px;
  background: var(--beni-600);
  color: #fff;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
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
  font-size: 12px;
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
  background: transparent;
  border: 0;
  color: #f8f4ef;
  font-size: 14px;
  cursor: pointer;
  flex: 1;
  min-width: 0;
}
.sns-dm__thread-author > span:last-child {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.sns-dm__thread-actions {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}
.sns-dm__thread-actions .sns-dm__icon-btn {
  font-size: 11px;
  color: rgba(248, 244, 239, 0.6);
}
.sns-dm__request-note {
  margin: 8px 16px 0;
  padding: 8px 12px;
  border-radius: var(--site-radius-sm);
  background: rgba(255, 255, 255, 0.06);
  color: rgba(248, 244, 239, 0.7);
  font-size: 11px;
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
  font-size: 13px;
  line-height: 1.6;
  word-break: break-word;
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
.sns-dm__message-meta {
  display: flex;
  gap: 8px;
  margin-top: 2px;
  font-size: 10px;
  color: rgba(248, 244, 239, 0.4);
}
.sns-dm__delete-btn {
  background: transparent;
  border: 0;
  color: rgba(248, 244, 239, 0.4);
  cursor: pointer;
  padding: 0;
  font-size: 10px;
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
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.06);
  border-radius: 999px;
  padding: 9px 16px;
  font-size: 13px;
  color: #f8f4ef;
}
.sns-dm__input::placeholder {
  color: rgba(248, 244, 239, 0.4);
}
.sns-dm__send-btn {
  width: 36px;
  height: 36px;
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
  overflow-y: auto;
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
  font-size: 13px;
  color: #f8f4ef;
}

@media (max-width: 767px) {
  .sns-dm {
    min-height: calc(100vh - 112px);
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
  .sns-dm__thread-item {
    gap: 8px;
  }

  .sns-dm__avatar {
    width: 40px;
    height: 40px;
  }

  .sns-dm__thread-time {
    display: none;
  }
}
</style>
