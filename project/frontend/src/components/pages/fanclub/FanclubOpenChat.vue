<script setup>
/**
 * ファンクラブ オープンチャット（会員同士のグループチャット）
 */
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import MemberGate from '../../common/MemberGate.vue'
import UiButton from '../../ui/UiButton.vue'
import {
  fetchOpenChatRooms,
  joinOpenChatRoom,
  leaveOpenChatRoom,
  fetchOpenChatMessages,
  sendOpenChatMessage,
  fetchOpenChatMembers,
  uploadOpenChatMedia,
} from '../../../api/openChat.js'
import { useMemberAccess } from '../../../composables/useMemberAccess.js'
import { useOpenChatNotifications } from '../../../composables/useOpenChatNotifications.js'
import { MEMBERSHIP_LABELS, PERMISSION } from '../../../constants/membership.js'

const emit = defineEmits(['need-auth'])

const { isLoggedIn, canUse } = useMemberAccess()
const {
  totalUnread,
  notificationsEnabled,
  notificationPermission,
  setActiveRoomId,
  refresh: refreshNotifications,
  enableNotifications,
  disableNotifications,
} = useOpenChatNotifications()

const POLL_MS = 4000

const loading = ref(true)
const error = ref('')
const rooms = ref([])
const activeRoomId = ref(null)
const messages = ref([])
const members = ref([])
const draft = ref('')
const sending = ref(false)
const joining = ref(false)
const showMembers = ref(false)
const messagesLoading = ref(false)
const lastMessageId = ref(null)
const pendingMedia = ref(null)
const fileInputRef = ref(null)

const messagesEl = ref(null)
let pollTimer = null

const activeRoom = computed(() => rooms.value.find((r) => r.room_id === activeRoomId.value) || null)

const canUseChat = computed(() => isLoggedIn.value && canUse(PERMISSION.OPEN_CHAT))

function formatTime(value) {
  if (!value) return ''
  const part = String(value).slice(11, 16)
  return part || String(value).slice(0, 10)
}

function membershipLabel(value) {
  return MEMBERSHIP_LABELS[value] || '会員'
}

function roomUnreadCount(room) {
  return room.unread_count || 0
}

function clearPendingMedia() {
  if (pendingMedia.value?.previewUrl) {
    URL.revokeObjectURL(pendingMedia.value.previewUrl)
  }
  pendingMedia.value = null
  if (fileInputRef.value) fileInputRef.value.value = ''
}

function onPickMedia(event) {
  const file = event.target.files?.[0]
  if (!file) return

  const isImage = file.type.startsWith('image/')
  const isVideo = file.type.startsWith('video/')
  if (!isImage && !isVideo) {
    error.value = '画像または動画ファイルを選択してください'
    return
  }

  clearPendingMedia()
  pendingMedia.value = {
    file,
    kind: isImage ? 'image' : 'video',
    previewUrl: URL.createObjectURL(file),
    name: file.name,
  }
}

async function toggleNotifications() {
  if (notificationsEnabled.value) {
    disableNotifications()
    return
  }
  const ok = await enableNotifications()
  if (!ok) {
    error.value = 'ブラウザの通知が許可されませんでした。設定から通知を有効にしてください。'
  }
}

async function loadRooms() {
  loading.value = true
  error.value = ''
  try {
    const data = await fetchOpenChatRooms()
    rooms.value = data?.rooms || []
    if (!activeRoomId.value && rooms.value.length) {
      const joined = rooms.value.find((r) => r.is_joined)
      activeRoomId.value = (joined || rooms.value[0]).room_id
    }
  } catch (err) {
    error.value = err.message || 'ルーム一覧の取得に失敗しました'
    rooms.value = []
  } finally {
    loading.value = false
  }
}

async function loadMessages(initial = false) {
  if (!activeRoomId.value || !activeRoom.value?.is_joined) return

  if (initial) messagesLoading.value = true
  try {
    const data = await fetchOpenChatMessages(activeRoomId.value, {
      afterId: initial ? undefined : lastMessageId.value || undefined,
      limit: initial ? 50 : 100,
    })
    const incoming = data?.messages || []
    if (initial) {
      messages.value = incoming
    } else if (incoming.length) {
      const existing = new Set(messages.value.map((m) => m.message_id))
      const merged = [...messages.value]
      for (const msg of incoming) {
        if (!existing.has(msg.message_id)) merged.push(msg)
      }
      messages.value = merged
    }
    if (data?.latest_id) {
      lastMessageId.value = data.latest_id
    } else if (messages.value.length) {
      lastMessageId.value = messages.value[messages.value.length - 1].message_id
    }
    if (incoming.length) {
      await nextTick()
      scrollToBottom()
      await refreshNotifications()
    }
  } catch (err) {
    if (initial) error.value = err.message || 'メッセージの取得に失敗しました'
  } finally {
    messagesLoading.value = false
  }
}

async function loadMembers() {
  if (!activeRoomId.value || !activeRoom.value?.is_joined) return
  try {
    const data = await fetchOpenChatMembers(activeRoomId.value)
    members.value = data?.members || []
  } catch {
    members.value = []
  }
}

function scrollToBottom() {
  const el = messagesEl.value
  if (el) el.scrollTop = el.scrollHeight
}

function startPolling() {
  stopPolling()
  pollTimer = window.setInterval(() => {
    if (activeRoom.value?.is_joined) {
      loadMessages(false)
    }
  }, POLL_MS)
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

async function selectRoom(roomId) {
  if (activeRoomId.value === roomId) return
  activeRoomId.value = roomId
  setActiveRoomId(roomId)
  messages.value = []
  lastMessageId.value = null
  showMembers.value = false
  clearPendingMedia()
  if (activeRoom.value?.is_joined) {
    await loadMessages(true)
  }
}

async function handleJoin() {
  if (!activeRoomId.value) return
  joining.value = true
  error.value = ''
  try {
    await joinOpenChatRoom(activeRoomId.value)
    const idx = rooms.value.findIndex((r) => r.room_id === activeRoomId.value)
    if (idx >= 0) {
      rooms.value[idx] = {
        ...rooms.value[idx],
        is_joined: true,
        member_count: (rooms.value[idx].member_count || 0) + 1,
      }
    }
    await loadMessages(true)
    startPolling()
  } catch (err) {
    error.value = err.message || '参加に失敗しました'
  } finally {
    joining.value = false
  }
}

async function handleLeave() {
  if (!activeRoomId.value) return
  try {
    await leaveOpenChatRoom(activeRoomId.value)
    const idx = rooms.value.findIndex((r) => r.room_id === activeRoomId.value)
    if (idx >= 0) {
      rooms.value[idx] = {
        ...rooms.value[idx],
        is_joined: false,
        member_count: Math.max((rooms.value[idx].member_count || 1) - 1, 0),
      }
    }
    messages.value = []
    lastMessageId.value = null
    showMembers.value = false
    stopPolling()
  } catch (err) {
    error.value = err.message || '退出に失敗しました'
  }
}

async function handleSend() {
  const text = draft.value.trim()
  const media = pendingMedia.value
  if ((!text && !media) || !activeRoomId.value || sending.value) return

  sending.value = true
  error.value = ''
  try {
    let message_type = 'text'
    let media_path = null

    if (media) {
      const uploaded = await uploadOpenChatMedia(activeRoomId.value, media.file)
      message_type = uploaded.media_type
      media_path = uploaded.path
    } else if (!text) {
      return
    }

    const data = await sendOpenChatMessage(activeRoomId.value, {
      body: text,
      message_type,
      media_path,
    })

    if (data?.message) {
      messages.value = [...messages.value, data.message]
      lastMessageId.value = data.message.message_id
      draft.value = ''
      clearPendingMedia()
      const preview =
        message_type === 'text'
          ? (text.length > 60 ? `${text.slice(0, 60)}…` : text)
          : message_type === 'image'
            ? '📷 画像'
            : '🎬 動画'
      const idx = rooms.value.findIndex((r) => r.room_id === activeRoomId.value)
      if (idx >= 0) {
        rooms.value[idx] = {
          ...rooms.value[idx],
          is_joined: true,
          last_message_preview: preview,
          last_message_at: data.message.created_at,
          unread_count: 0,
        }
      }
      await nextTick()
      scrollToBottom()
      await refreshNotifications()
    }
  } catch (err) {
    error.value = err.message || '送信に失敗しました'
  } finally {
    sending.value = false
  }
}

function onKeydown(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    handleSend()
  }
}

async function toggleMembers() {
  showMembers.value = !showMembers.value
  if (showMembers.value) {
    await loadMembers()
  }
}

watch(activeRoomId, async (roomId) => {
  setActiveRoomId(roomId)
  if (activeRoom.value?.is_joined) {
    await loadMessages(true)
    startPolling()
  } else {
    stopPolling()
  }
})

onMounted(async () => {
  if (!canUseChat.value) {
    loading.value = false
    return
  }
  setActiveRoomId(activeRoomId.value)
  await loadRooms()
  if (activeRoomId.value) setActiveRoomId(activeRoomId.value)
  if (activeRoom.value?.is_joined) {
    await loadMessages(true)
    startPolling()
  }
  await refreshNotifications()
})

onUnmounted(() => {
  stopPolling()
  setActiveRoomId(null)
  clearPendingMedia()
})
</script>

<template>
  <div class="open-chat">
    <MemberGate
      v-if="!canUseChat"
      :permission="PERMISSION.OPEN_CHAT"
      feature="オープンチャット"
      @login="emit('need-auth', 'login')"
      @register="emit('need-auth', 'register')"
    />

    <template v-else>
      <p v-if="error" class="open-chat__error" role="alert">{{ error }}</p>

      <div class="open-chat__layout">
        <aside class="open-chat__rooms">
          <div class="open-chat__rooms-head">
            <h3 class="open-chat__rooms-title">オープンチャット</h3>
            <span v-if="totalUnread > 0" class="open-chat__rooms-badge">{{ totalUnread }}</span>
          </div>
          <button
            type="button"
            class="open-chat__notify-btn"
            :class="{ 'open-chat__notify-btn--on': notificationsEnabled }"
            @click="toggleNotifications"
          >
            {{ notificationsEnabled ? '🔔 通知オン' : '🔕 通知をオンにする' }}
          </button>
          <p v-if="notificationPermission === 'denied'" class="open-chat__notify-hint">
            ブラウザ設定で通知がブロックされています。
          </p>
          <p v-if="loading" class="open-chat__muted">読み込み中…</p>
          <ul v-else class="open-chat__room-list">
            <li v-for="room in rooms" :key="room.room_id">
              <button
                type="button"
                class="open-chat__room-btn"
                :class="{ 'open-chat__room-btn--active': room.room_id === activeRoomId }"
                @click="selectRoom(room.room_id)"
              >
                <span class="open-chat__room-icon" aria-hidden="true">{{ room.icon_emoji }}</span>
                <span class="open-chat__room-body">
                  <span class="open-chat__room-name-row">
                    <span class="open-chat__room-name">{{ room.name }}</span>
                    <span v-if="roomUnreadCount(room) > 0" class="open-chat__room-unread">
                      {{ roomUnreadCount(room) }}
                    </span>
                  </span>
                  <span class="open-chat__room-preview">
                    {{ room.last_message_preview || room.description }}
                  </span>
                  <span class="open-chat__room-meta">
                    {{ room.member_count }}人参加
                    <span v-if="room.is_joined"> · 参加中</span>
                  </span>
                </span>
              </button>
            </li>
          </ul>
        </aside>

        <section v-if="activeRoom" class="open-chat__panel">
          <header class="open-chat__header">
            <div>
              <h3 class="open-chat__title">
                <span aria-hidden="true">{{ activeRoom.icon_emoji }}</span>
                {{ activeRoom.name }}
              </h3>
              <p class="open-chat__desc">{{ activeRoom.description }}</p>
            </div>
            <div class="open-chat__header-actions">
              <button type="button" class="open-chat__meta-btn" @click="toggleMembers">
                {{ showMembers ? 'チャットに戻る' : `参加者 ${activeRoom.member_count}人` }}
              </button>
              <button
                v-if="activeRoom.is_joined"
                type="button"
                class="open-chat__meta-btn open-chat__meta-btn--leave"
                @click="handleLeave"
              >
                退出
              </button>
            </div>
          </header>

          <div v-if="!activeRoom.is_joined" class="open-chat__join">
            <p>このルームに参加すると、ファン同士でメッセージのやり取りができます。</p>
            <UiButton variant="primary" size="md" :disabled="joining" @click="handleJoin">
              {{ joining ? '参加中…' : 'オープンチャットに参加' }}
            </UiButton>
          </div>

          <template v-else-if="showMembers">
            <ul class="open-chat__member-list">
              <li v-for="member in members" :key="member.account_id" class="open-chat__member">
                <span class="open-chat__member-name">
                  {{ member.display_name }}
                  <span v-if="member.is_own" class="open-chat__member-you">（あなた）</span>
                </span>
                <span class="open-chat__member-plan">{{ membershipLabel(member.membership) }}</span>
              </li>
            </ul>
          </template>

          <template v-else>
            <div ref="messagesEl" class="open-chat__messages">
              <p v-if="messagesLoading" class="open-chat__muted">メッセージを読み込み中…</p>
              <p v-else-if="!messages.length" class="open-chat__muted open-chat__empty">
                まだメッセージはありません。最初の一言を送ってみましょう。
              </p>
              <article
                v-for="msg in messages"
                :key="msg.message_id"
                class="open-chat__bubble-row"
                :class="{ 'open-chat__bubble-row--own': msg.is_own }"
              >
                <div class="open-chat__bubble">
                  <p v-if="!msg.is_own" class="open-chat__author">
                    {{ msg.author_name }}
                    <span class="open-chat__author-plan">{{ membershipLabel(msg.membership) }}</span>
                  </p>
                  <div v-if="msg.message_type === 'image' && msg.media_path" class="open-chat__media">
                    <a :href="msg.media_path" target="_blank" rel="noopener noreferrer">
                      <img :src="msg.media_path" :alt="msg.body || '画像'" class="open-chat__image" />
                    </a>
                  </div>
                  <div v-else-if="msg.message_type === 'video' && msg.media_path" class="open-chat__media">
                    <video :src="msg.media_path" class="open-chat__video" controls playsinline />
                  </div>
                  <p v-if="msg.body" class="open-chat__text">{{ msg.body }}</p>
                  <time class="open-chat__time">{{ formatTime(msg.created_at) }}</time>
                </div>
              </article>
            </div>

            <form class="open-chat__composer" @submit.prevent="handleSend">
              <div class="open-chat__composer-main">
                <div v-if="pendingMedia" class="open-chat__pending">
                  <img
                    v-if="pendingMedia.kind === 'image'"
                    :src="pendingMedia.previewUrl"
                    alt=""
                    class="open-chat__pending-thumb"
                  />
                  <video
                    v-else
                    :src="pendingMedia.previewUrl"
                    class="open-chat__pending-thumb"
                    muted
                  />
                  <span class="open-chat__pending-name">{{ pendingMedia.name }}</span>
                  <button type="button" class="open-chat__pending-remove" @click="clearPendingMedia">×</button>
                </div>
                <textarea
                  v-model="draft"
                  class="open-chat__input"
                  rows="2"
                  maxlength="2000"
                  placeholder="メッセージを入力（Enterで送信、Shift+Enterで改行）"
                  :disabled="sending"
                  @keydown="onKeydown"
                />
              </div>
              <div class="open-chat__composer-actions">
                <input
                  ref="fileInputRef"
                  type="file"
                  class="open-chat__file-input"
                  accept="image/jpeg,image/png,image/gif,image/webp,video/mp4,video/webm,video/quicktime"
                  @change="onPickMedia"
                />
                <button
                  type="button"
                  class="open-chat__attach-btn"
                  title="画像・動画を添付"
                  :disabled="sending"
                  @click="fileInputRef?.click()"
                >
                  📎
                </button>
                <UiButton
                  variant="primary"
                  size="md"
                  type="submit"
                  :disabled="sending || (!draft.trim() && !pendingMedia)"
                >
                  {{ sending ? '送信中…' : '送信' }}
                </UiButton>
              </div>
            </form>
          </template>
        </section>
      </div>
    </template>
  </div>
</template>

<style scoped>
.open-chat__error {
  margin: 0 0 var(--sp-4);
  padding: 10px 14px;
  border-radius: var(--site-radius-sm);
  background: #fff2f0;
  border: 1px solid #f0c4be;
  color: #a33b2f;
  font-size: 13px;
}
.open-chat__layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: var(--sp-4);
  min-height: 520px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  overflow: hidden;
  background: var(--site-surface);
}
.open-chat__rooms {
  border-right: 1px solid var(--site-border);
  background: var(--site-bg-pink);
  padding: var(--sp-4);
}
.open-chat__rooms-title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 15px;
  color: var(--murasaki-700);
}
.open-chat__rooms-head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: var(--sp-3);
}
.open-chat__rooms-badge {
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  border-radius: 999px;
  background: #c0453b;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.open-chat__notify-btn {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px 10px;
  border: 1px solid var(--murasaki-400);
  border-radius: var(--site-radius-sm);
  background: #fff;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  font-weight: 700;
  color: var(--murasaki-700);
  cursor: pointer;
}
.open-chat__notify-btn--on {
  background: var(--murasaki-100);
}
.open-chat__notify-hint {
  margin: 0 0 10px;
  font-size: 10px;
  line-height: 1.6;
  color: #a33b2f;
}
.open-chat__room-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.open-chat__room-btn {
  display: flex;
  gap: 10px;
  width: 100%;
  padding: 12px;
  border: 1px solid transparent;
  border-radius: var(--site-radius-md);
  background: rgba(255, 255, 255, 0.55);
  text-align: left;
  cursor: pointer;
}
.open-chat__room-btn--active {
  border-color: var(--murasaki-400);
  background: #fff;
  box-shadow: var(--site-shadow-sm);
}
.open-chat__room-icon {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--murasaki-700);
  color: var(--kin-400);
  font-size: 16px;
}
.open-chat__room-body {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}
.open-chat__room-name-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.open-chat__room-unread {
  flex-shrink: 0;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 999px;
  background: #c0453b;
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.open-chat__room-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--site-text);
}
.open-chat__room-preview {
  font-size: 11px;
  line-height: 1.5;
  color: var(--site-text-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.open-chat__room-meta {
  font-size: 10px;
  color: var(--murasaki-700);
}
.open-chat__panel {
  display: flex;
  flex-direction: column;
  min-height: 520px;
}
.open-chat__header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 18px;
  border-bottom: 1px solid var(--site-border);
  background: linear-gradient(180deg, var(--murasaki-100) 0%, var(--site-surface) 100%);
}
.open-chat__title {
  margin: 0 0 4px;
  font-family: var(--ff-mincho);
  font-size: 16px;
  color: var(--murasaki-700);
  display: flex;
  align-items: center;
  gap: 8px;
}
.open-chat__desc {
  margin: 0;
  font-size: 12px;
  line-height: 1.6;
  color: var(--site-text-muted);
}
.open-chat__header-actions {
  display: flex;
  flex-direction: column;
  gap: 6px;
  align-items: flex-end;
}
.open-chat__meta-btn {
  border: 0;
  background: transparent;
  font-size: 11px;
  font-weight: 700;
  color: var(--murasaki-700);
  cursor: pointer;
}
.open-chat__meta-btn--leave {
  color: var(--site-text-muted);
}
.open-chat__join {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 32px 24px;
  text-align: center;
  color: var(--site-text-muted);
  font-size: 13px;
  line-height: 1.8;
}
.open-chat__messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #faf8f6;
}
.open-chat__bubble-row {
  display: flex;
  justify-content: flex-start;
}
.open-chat__bubble-row--own {
  justify-content: flex-end;
}
.open-chat__bubble {
  max-width: min(78%, 520px);
  padding: 10px 14px;
  border-radius: 14px;
  background: #fff;
  border: 1px solid var(--site-border);
  box-shadow: var(--site-shadow-sm);
}
.open-chat__bubble-row--own .open-chat__bubble {
  background: var(--murasaki-100);
  border-color: var(--murasaki-400);
}
.open-chat__author {
  margin: 0 0 4px;
  font-size: 11px;
  font-weight: 700;
  color: var(--murasaki-700);
}
.open-chat__author-plan {
  margin-left: 6px;
  font-weight: 500;
  color: var(--site-text-muted);
}
.open-chat__text {
  margin: 0;
  font-size: 13px;
  line-height: 1.7;
  color: var(--site-text);
  white-space: pre-wrap;
  word-break: break-word;
}
.open-chat__time {
  display: block;
  margin-top: 6px;
  font-size: 10px;
  color: var(--site-text-light);
  text-align: right;
}
.open-chat__composer {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 14px 18px;
  border-top: 1px solid var(--site-border);
  background: var(--site-surface);
}
.open-chat__composer-main {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.open-chat__composer-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
}
.open-chat__file-input {
  display: none;
}
.open-chat__attach-btn {
  width: 40px;
  height: 40px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  background: var(--site-surface-muted);
  font-size: 18px;
  cursor: pointer;
}
.open-chat__attach-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.open-chat__pending {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border: 1px dashed var(--murasaki-400);
  border-radius: var(--site-radius-md);
  background: var(--murasaki-100);
}
.open-chat__pending-thumb {
  width: 56px;
  height: 56px;
  object-fit: cover;
  border-radius: 6px;
  background: #000;
}
.open-chat__pending-name {
  flex: 1;
  font-size: 11px;
  color: var(--site-text-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.open-chat__pending-remove {
  border: 0;
  background: transparent;
  font-size: 18px;
  line-height: 1;
  cursor: pointer;
  color: var(--site-text-muted);
}
.open-chat__media {
  margin-bottom: 6px;
}
.open-chat__image {
  display: block;
  max-width: 100%;
  max-height: 280px;
  border-radius: 10px;
  object-fit: contain;
}
.open-chat__video {
  display: block;
  max-width: 100%;
  max-height: 280px;
  border-radius: 10px;
  background: #000;
}
.open-chat__input {
  width: 100%;
  resize: vertical;
  min-height: 52px;
  max-height: 140px;
  padding: 10px 12px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.6;
}
.open-chat__member-list {
  list-style: none;
  margin: 0;
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.open-chat__member {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 12px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  background: #fff;
}
.open-chat__member-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--site-text);
}
.open-chat__member-you {
  font-weight: 500;
  color: var(--site-text-muted);
}
.open-chat__member-plan {
  font-size: 11px;
  color: var(--murasaki-700);
}
.open-chat__muted {
  margin: 0;
  font-size: 12px;
  color: var(--site-text-muted);
}
.open-chat__empty {
  text-align: center;
  padding: 24px 12px;
}

@media (max-width: 900px) {
  .open-chat__layout {
    grid-template-columns: 1fr;
  }
  .open-chat__rooms {
    border-right: 0;
    border-bottom: 1px solid var(--site-border);
  }
  .open-chat__room-list {
    max-height: 180px;
    overflow-y: auto;
  }
}
</style>
