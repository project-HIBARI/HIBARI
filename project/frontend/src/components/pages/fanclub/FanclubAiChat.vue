<script setup>
/**
 * 部品名: ファンクラブ AIチャット
 * 用途: 美空ひばりAIとの対話（バックエンド /api/chat 連携）
 * 機能: ルーム一覧 / メッセージ履歴 / 新規チャット / 送信
 */
import { ref, onMounted, nextTick } from 'vue'
import UiIco from '../../ui/UiIco.vue'
import UiButton from '../../ui/UiButton.vue'
import { fetchRooms, fetchMessages, sendChatMessage } from '../../../lib/chatApi.js'

const emit = defineEmits(['need-login'])

const rooms = ref([])
const messages = ref([])
const currentRoomId = ref(null)
const currentRoomName = ref('新しいチャット')
const input = ref('')
const loading = ref(false)
const roomsLoading = ref(false)
const error = ref('')
const messagesRef = ref(null)

async function loadRooms() {
  roomsLoading.value = true
  try {
    rooms.value = await fetchRooms()
    error.value = ''
  } catch (e) {
    if (e.status === 401) {
      emit('need-login')
      error.value = 'チャットをご利用いただくにはログインが必要です。'
    } else {
      error.value = e.message || 'ルームの取得に失敗しました。'
    }
  } finally {
    roomsLoading.value = false
  }
}

async function selectRoom(room) {
  currentRoomId.value = room.ai_chat_room_id
  currentRoomName.value = room.room_name
  loading.value = true
  try {
    const list = await fetchMessages(room.ai_chat_room_id)
    messages.value = list.map((m) => ({
      role: m.sender === 'user' ? 'user' : 'ai',
      text: m.content,
    }))
    error.value = ''
    await scrollToBottom()
  } catch (e) {
    if (e.status === 401) emit('need-login')
    error.value = e.message || 'メッセージの取得に失敗しました。'
  } finally {
    loading.value = false
  }
}

function startNewChat() {
  currentRoomId.value = null
  currentRoomName.value = '新しいチャット'
  messages.value = []
  error.value = ''
}

async function send() {
  const text = input.value.trim()
  if (!text || loading.value) return

  messages.value.push({ role: 'user', text })
  input.value = ''
  loading.value = true
  error.value = ''
  await scrollToBottom()

  try {
    const data = await sendChatMessage({
      message: text,
      roomId: currentRoomId.value,
    })
    if (data.room_id) currentRoomId.value = Number(data.room_id)
    if (data.room_name) currentRoomName.value = data.room_name
    messages.value.push({ role: 'ai', text: data.message })
    await loadRooms()
  } catch (e) {
    if (e.status === 401) {
      emit('need-login')
      error.value = 'ログインが必要です。ログイン後に再度お試しください。'
    } else {
      error.value = e.message || '送信に失敗しました。'
    }
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}

async function scrollToBottom() {
  await nextTick()
  const el = messagesRef.value
  if (el) el.scrollTop = el.scrollHeight
}

onMounted(() => {
  loadRooms()
})
</script>

<template>
  <div class="fc-chat">
    <aside class="fc-chat__sidebar">
      <div class="fc-chat__sidebar-head">
        <h3 class="fc-chat__sidebar-title">チャット履歴</h3>
        <button type="button" class="fc-chat__new" @click="startNewChat">＋ 新規</button>
      </div>
      <div v-if="roomsLoading" class="fc-chat__sidebar-loading">読み込み中…</div>
      <ul v-else class="fc-chat__rooms">
        <li v-if="rooms.length === 0" class="fc-chat__empty">履歴はまだありません</li>
        <li v-for="room in rooms" :key="room.ai_chat_room_id">
          <button
            type="button"
            class="fc-chat__room"
            :class="{ 'fc-chat__room--active': currentRoomId === room.ai_chat_room_id }"
            @click="selectRoom(room)"
          >
            <span class="fc-chat__room-name">{{ room.room_name }}</span>
            <span class="fc-chat__room-date">{{ room.created_at }}</span>
          </button>
        </li>
      </ul>
    </aside>

    <div class="fc-chat__main">
      <header class="fc-chat__header">
        <UiIco name="chat" :size="20" color="var(--murasaki-700)" />
        <h3 class="fc-chat__title">{{ currentRoomName }}</h3>
      </header>

      <div class="fc-chat__notice">
        このAIは美空ひばりの言葉・歌・生涯をもとにした応答です。実際の本人の発言ではありません。
      </div>

      <div ref="messagesRef" class="fc-chat__messages">
        <div
          v-for="(m, i) in messages"
          :key="i"
          class="fc-chat__row"
          :class="m.role === 'user' ? 'fc-chat__row--user' : 'fc-chat__row--ai'"
        >
          <div class="fc-chat__bubble" :class="m.role === 'user' ? 'fc-chat__bubble--user' : 'fc-chat__bubble--ai'">
            <div v-if="m.role === 'ai'" class="fc-chat__label">AI美空ひばり</div>
            {{ m.text }}
          </div>
        </div>
        <div v-if="loading && messages.length" class="fc-chat__typing">……</div>
        <div v-if="messages.length === 0 && !loading" class="fc-chat__welcome">
          <UiIco name="flower" :size="36" color="var(--murasaki-500)" />
          <p>ひばりさんに、お気軽にお話しかけてください。</p>
        </div>
      </div>

      <p v-if="error" class="fc-chat__error">{{ error }}</p>

      <div class="fc-chat__input-row">
        <input
          v-model="input"
          class="fc-chat__input"
          placeholder="ひばりさんに話しかける…"
          aria-label="メッセージを入力"
          :disabled="loading"
          @keydown.enter.prevent="send"
        />
        <UiButton variant="primary" size="md" :disabled="loading || !input.trim()" @click="send">
          送信
        </UiButton>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fc-chat {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 0;
  min-height: 520px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  overflow: hidden;
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
}
.fc-chat__sidebar {
  border-right: 1px solid var(--site-border);
  background: var(--site-surface-muted);
  display: flex;
  flex-direction: column;
}
.fc-chat__sidebar-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--site-border);
}
.fc-chat__sidebar-title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 13px;
  font-weight: 700;
  color: var(--site-text);
}
.fc-chat__new {
  background: transparent;
  border: 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  color: var(--murasaki-700);
  cursor: pointer;
}
.fc-chat__new:hover {
  text-decoration: underline;
}
.fc-chat__sidebar-loading,
.fc-chat__empty {
  padding: 16px;
  font-size: 12px;
  color: var(--site-text-light);
  text-align: center;
}
.fc-chat__rooms {
  list-style: none;
  margin: 0;
  padding: 8px;
  overflow-y: auto;
  flex: 1;
}
.fc-chat__room {
  display: flex;
  flex-direction: column;
  gap: 2px;
  width: 100%;
  padding: 10px 12px;
  text-align: left;
  background: transparent;
  border: 0;
  border-radius: var(--site-radius-sm);
  cursor: pointer;
  transition: background 0.15s;
}
.fc-chat__room:hover,
.fc-chat__room--active {
  background: var(--murasaki-100);
}
.fc-chat__room-name {
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  color: var(--site-text);
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.fc-chat__room-date {
  font-size: 10px;
  color: var(--site-text-light);
}
.fc-chat__main {
  display: flex;
  flex-direction: column;
  min-height: 0;
}
.fc-chat__header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--site-border);
  background: linear-gradient(135deg, var(--murasaki-100) 0%, var(--site-surface) 100%);
}
.fc-chat__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 16px;
  font-weight: 700;
  color: var(--murasaki-700);
}
.fc-chat__notice {
  padding: 8px 20px;
  font-size: 10px;
  line-height: 1.6;
  color: var(--site-text-muted);
  background: var(--site-bg-pink);
  border-bottom: 1px solid var(--site-border);
}
.fc-chat__messages {
  flex: 1 1 auto;
  overflow-y: auto;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 280px;
  max-height: 400px;
}
.fc-chat__row {
  display: flex;
}
.fc-chat__row--user {
  justify-content: flex-end;
}
.fc-chat__row--ai {
  justify-content: flex-start;
}
.fc-chat__bubble {
  padding: 10px 14px;
  max-width: 80%;
  font-size: 13px;
  line-height: 1.8;
  font-family: var(--ff-serif);
  border-radius: var(--site-radius-md);
}
.fc-chat__bubble--user {
  background: var(--murasaki-700);
  color: #fff;
  border-radius: 12px 12px 4px 12px;
}
.fc-chat__bubble--ai {
  background: var(--site-surface-muted);
  color: var(--site-text);
  border: 1px solid var(--site-border);
  border-radius: 12px 12px 12px 4px;
}
.fc-chat__label {
  font-size: 10px;
  color: var(--kin-600);
  letter-spacing: 0.12em;
  margin-bottom: 4px;
  font-family: var(--ff-mincho);
}
.fc-chat__typing {
  text-align: center;
  color: var(--murasaki-600);
  font-size: 13px;
}
.fc-chat__welcome {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  text-align: center;
  color: var(--site-text-muted);
  font-size: 13px;
}
.fc-chat__error {
  margin: 0;
  padding: 0 20px;
  font-size: 12px;
  color: #c0453b;
}
.fc-chat__input-row {
  display: flex;
  gap: 10px;
  padding: 16px 20px;
  border-top: 1px solid var(--site-border);
  background: var(--site-surface);
}
.fc-chat__input {
  flex: 1;
  min-width: 0;
  padding: 12px 14px;
  font-family: var(--ff-serif);
  font-size: 13px;
  color: var(--site-text);
  background: #f5f2ee;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
  outline: none;
}
.fc-chat__input:focus {
  border-color: var(--murasaki-400);
}

@media (max-width: 767px) {
  .fc-chat {
    grid-template-columns: 1fr;
    min-height: auto;
  }
  .fc-chat__sidebar {
    border-right: 0;
    border-bottom: 1px solid var(--site-border);
    max-height: 160px;
  }
  .fc-chat__messages {
    max-height: 320px;
  }
  .fc-chat__input-row {
    flex-direction: column;
  }
}
</style>
