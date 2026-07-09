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
} from '../../../api/openChat.js'
import { useMemberAccess } from '../../../composables/useMemberAccess.js'
import { MEMBERSHIP_LABELS, PERMISSION } from '../../../constants/membership.js'

const emit = defineEmits(['need-auth'])

const { isLoggedIn, canUse } = useMemberAccess()

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
  messages.value = []
  lastMessageId.value = null
  showMembers.value = false
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
  if (!text || !activeRoomId.value || sending.value) return

  sending.value = true
  error.value = ''
  try {
    const data = await sendOpenChatMessage(activeRoomId.value, text)
    if (data?.message) {
      messages.value = [...messages.value, data.message]
      lastMessageId.value = data.message.message_id
      draft.value = ''
      const idx = rooms.value.findIndex((r) => r.room_id === activeRoomId.value)
      if (idx >= 0) {
        rooms.value[idx] = {
          ...rooms.value[idx],
          is_joined: true,
          last_message_preview: text.length > 60 ? `${text.slice(0, 60)}…` : text,
          last_message_at: data.message.created_at,
        }
      }
      await nextTick()
      scrollToBottom()
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

watch(activeRoomId, async () => {
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
  await loadRooms()
  if (activeRoom.value?.is_joined) {
    await loadMessages(true)
    startPolling()
  }
})

onUnmounted(() => {
  stopPolling()
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
          <h3 class="open-chat__rooms-title">オープンチャット</h3>
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
                  <span class="open-chat__room-name">{{ room.name }}</span>
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
                  <p class="open-chat__text">{{ msg.body }}</p>
                  <time class="open-chat__time">{{ formatTime(msg.created_at) }}</time>
                </div>
              </article>
            </div>

            <form class="open-chat__composer" @submit.prevent="handleSend">
              <textarea
                v-model="draft"
                class="open-chat__input"
                rows="2"
                maxlength="2000"
                placeholder="メッセージを入力（Enterで送信、Shift+Enterで改行）"
                :disabled="sending"
                @keydown="onKeydown"
              />
              <UiButton variant="primary" size="md" type="submit" :disabled="sending || !draft.trim()">
                {{ sending ? '送信中…' : '送信' }}
              </UiButton>
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
  margin: 0 0 var(--sp-3);
  font-family: var(--ff-mincho);
  font-size: 15px;
  color: var(--murasaki-700);
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
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
  padding: 14px 18px;
  border-top: 1px solid var(--site-border);
  background: var(--site-surface);
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
