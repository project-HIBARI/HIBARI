<script setup>
/**
 * ファンクラブ オープンチャット（会員同士のグループチャット）
 */
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import MemberGate from '../../common/MemberGate.vue'
import UiButton from '../../ui/UiButton.vue'
import {
  fetchOpenChatRooms,
  fetchOpenChatRoom,
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
import { PLATFORM_CHAT_ARTISTS } from '../../../data/musicMemoriesData.js'
import {
  resolveOpenChatMediaUrl,
  isOpenChatImageMessage,
  isOpenChatVideoMessage,
} from '../../../lib/openChatMedia.js'

const emit = defineEmits(['need-auth'])

const props = defineProps({
  /** artist_site = ファンクラブサイト内 / platform = Music Memories */
  chatScope: { type: String, default: 'artist_site' },
  platformTheme: { type: Boolean, default: false },
  /** 楽曲チャット等、一覧に出ない特定ルームへ直接遷移したい場合の room_id */
  initialRoomId: { type: [Number, String], default: null },
})

const { isLoggedIn, canUse } = useMemberAccess()
const {
  totalUnread,
  notificationsEnabled,
  notificationPermission,
  setActiveRoomId,
  refresh: refreshNotifications,
  enableNotifications,
  disableNotifications,
} = useOpenChatNotifications(props.chatScope)

const POLL_MS = 4000

const loading = ref(true)
const error = ref('')
const rooms = ref([])
const selectedArtist = ref('all')
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
const bottomAnchor = ref(null)
const isNearBottom = ref(true)
const pendingNewCount = ref(0)
const mobileView = ref('rooms')
const isMobile = ref(false)
let pollTimer = null

const SCROLL_THRESHOLD = 96
const showJumpToBottom = computed(() => pendingNewCount.value > 0 && !isNearBottom.value)

function updateMobile() {
  isMobile.value = window.matchMedia('(max-width: 767px)').matches
  if (!isMobile.value) mobileView.value = 'chat'
}

function showMobileChat() {
  if (isMobile.value) mobileView.value = 'chat'
}

function showMobileRooms() {
  mobileView.value = 'rooms'
}

const activeRoom = computed(() => rooms.value.find((r) => r.room_id === activeRoomId.value) || null)

const artistTabs = computed(() => (props.platformTheme ? PLATFORM_CHAT_ARTISTS : []))

const displayedRooms = computed(() => {
  if (!props.platformTheme || selectedArtist.value === 'all') {
    return rooms.value
  }
  if (selectedArtist.value === 'lounge') {
    return rooms.value.filter((r) => !r.artist_slug)
  }
  return rooms.value.filter((r) => r.artist_slug === selectedArtist.value)
})

const chatTitle = computed(() => (props.platformTheme ? 'Music Memories オープンチャット' : 'オープンチャット'))

const canUseChat = computed(() => isLoggedIn.value && canUse(PERMISSION.OPEN_CHAT))

function formatTime(value) {
  if (!value) return ''
  const part = String(value).slice(11, 16)
  return part || String(value).slice(0, 10)
}

function membershipLabel(value) {
  return MEMBERSHIP_LABELS[value] || '会員'
}

function mediaUrl(msg) {
  return resolveOpenChatMediaUrl(msg)
}

function isImageMessage(msg) {
  return isOpenChatImageMessage(msg)
}

function isVideoMessage(msg) {
  return isOpenChatVideoMessage(msg)
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
    const artist = props.platformTheme && selectedArtist.value === 'hibari'
      ? 'hibari'
      : undefined
    const data = await fetchOpenChatRooms({ scope: props.chatScope, artist })
    rooms.value = data?.rooms || []

    if (props.initialRoomId) {
      const initialId = Number(props.initialRoomId)
      if (!rooms.value.some((r) => r.room_id === initialId)) {
        try {
          const room = await fetchOpenChatRoom(initialId)
          if (room) rooms.value = [room, ...rooms.value]
        } catch {
          /* ルームが取得できない場合は通常一覧のみ表示 */
        }
      }
      if (rooms.value.some((r) => r.room_id === initialId)) {
        activeRoomId.value = initialId
        showMobileChat()
        return
      }
    }

    if (!activeRoomId.value && rooms.value.length) {
      const joined = rooms.value.find((r) => r.is_joined)
      activeRoomId.value = (joined || rooms.value[0]).room_id
      if (!isMobile.value) showMobileChat()
    } else if (activeRoomId.value && !rooms.value.some((r) => r.room_id === activeRoomId.value)) {
      activeRoomId.value = rooms.value[0]?.room_id || null
    }
  } catch (err) {
    error.value = err.message || 'ルーム一覧の取得に失敗しました'
    rooms.value = []
  } finally {
    loading.value = false
  }
}

async function onArtistFilterChange(artistId) {
  if (selectedArtist.value === artistId) return
  selectedArtist.value = artistId
  await loadRooms()
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
    const stickToBottom = initial || checkNearBottom()

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
      if (stickToBottom) {
        scrollToBottom(true)
      } else {
        const newFromOthers = incoming.filter((m) => !m.is_own).length
        if (newFromOthers > 0) {
          pendingNewCount.value += newFromOthers
        }
      }
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

function checkNearBottom() {
  const el = messagesEl.value
  if (!el) return true
  return el.scrollHeight - el.scrollTop - el.clientHeight <= SCROLL_THRESHOLD
}

function onMessagesScroll() {
  isNearBottom.value = checkNearBottom()
  if (isNearBottom.value) {
    pendingNewCount.value = 0
  }
}

function scrollToBottom(force = false) {
  if (!force && !isNearBottom.value) return
  const anchor = bottomAnchor.value
  if (anchor) {
    anchor.scrollIntoView({ behavior: force ? 'instant' : 'smooth', block: 'end' })
  } else {
    const el = messagesEl.value
    if (el) el.scrollTop = el.scrollHeight
  }
  isNearBottom.value = true
  pendingNewCount.value = 0
}

function jumpToLatest() {
  scrollToBottom(true)
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
  showMobileChat()
  if (activeRoomId.value === roomId) return
  activeRoomId.value = roomId
  setActiveRoomId(roomId)
  messages.value = []
  lastMessageId.value = null
  pendingNewCount.value = 0
  isNearBottom.value = true
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
    pendingNewCount.value = 0
    isNearBottom.value = true
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
      scrollToBottom(true)
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
  updateMobile()
  window.addEventListener('resize', updateMobile)
  if (!canUseChat.value) {
    loading.value = false
    return
  }
  setActiveRoomId(activeRoomId.value)
  await loadRooms()
  if (activeRoomId.value) setActiveRoomId(activeRoomId.value)
  if (props.initialRoomId && activeRoomId.value) showMobileChat()
  if (activeRoom.value?.is_joined) {
    await loadMessages(true)
    startPolling()
  }
  await refreshNotifications()
})

onUnmounted(() => {
  window.removeEventListener('resize', updateMobile)
  stopPolling()
  setActiveRoomId(null)
  clearPendingMedia()
})
</script>

<template>
  <div
    class="open-chat"
    :class="{
      'open-chat--platform': platformTheme,
      'open-chat--mobile': isMobile,
    }"
  >
    <MemberGate
      v-if="!canUseChat"
      :permission="PERMISSION.OPEN_CHAT"
      :feature="platformTheme ? 'Music Memories オープンチャット' : 'オープンチャット'"
      @login="emit('need-auth', 'login')"
      @register="emit('need-auth', 'register')"
    />

    <template v-else>
      <p v-if="platformTheme && !isMobile" class="open-chat__platform-lead">
        複数アーティストのファンが交流できるプラットフォーム共通のオープンチャットです。
      </p>
      <p v-if="error" class="open-chat__error" role="alert">{{ error }}</p>

      <div class="open-chat__layout">
        <aside
          v-show="!isMobile || mobileView === 'rooms'"
          class="open-chat__rooms"
        >
          <div class="open-chat__rooms-head">
            <h3 class="open-chat__rooms-title">{{ chatTitle }}</h3>
            <span v-if="totalUnread > 0" class="open-chat__rooms-badge">{{ totalUnread }}</span>
          </div>
          <div v-if="artistTabs.length" class="open-chat__artist-tabs" role="tablist" aria-label="アーティストで絞り込み">
            <button
              v-for="tab in artistTabs"
              :key="tab.id"
              type="button"
              class="open-chat__artist-tab"
              :class="{ 'open-chat__artist-tab--active': selectedArtist === tab.id }"
              role="tab"
              :aria-selected="selectedArtist === tab.id"
              @click="onArtistFilterChange(tab.id)"
            >
              {{ tab.label }}
            </button>
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
            <li v-for="room in displayedRooms" :key="room.room_id">
              <button
                type="button"
                class="open-chat__room-btn"
                :class="{ 'open-chat__room-btn--active': room.room_id === activeRoomId }"
                @click="selectRoom(room.room_id)"
              >
                <span class="open-chat__room-icon" aria-hidden="true">{{ room.icon_emoji }}</span>
                <span class="open-chat__room-body">
                  <span v-if="platformTheme && room.artist_name" class="open-chat__room-artist">{{ room.artist_name }}</span>
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

        <section
          v-if="activeRoom"
          v-show="!isMobile || mobileView === 'chat'"
          class="open-chat__panel"
        >
          <header class="open-chat__header">
            <div class="open-chat__header-main">
              <button
                v-if="isMobile"
                type="button"
                class="open-chat__back"
                @click="showMobileRooms"
              >
                ← ルーム一覧
              </button>
              <div>
                <h3 class="open-chat__title">
                  <span aria-hidden="true">{{ activeRoom.icon_emoji }}</span>
                  {{ activeRoom.name }}
                </h3>
                <p class="open-chat__desc">{{ activeRoom.description }}</p>
              </div>
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
            <div class="open-chat__chat-body">
              <div ref="messagesEl" class="open-chat__messages" @scroll="onMessagesScroll">
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
                    <div v-if="isImageMessage(msg)" class="open-chat__media">
                      <a :href="mediaUrl(msg)" target="_blank" rel="noopener noreferrer">
                        <img
                          :src="mediaUrl(msg)"
                          :alt="msg.body || '画像'"
                          class="open-chat__image"
                          loading="lazy"
                          decoding="async"
                        />
                      </a>
                    </div>
                    <div v-else-if="isVideoMessage(msg)" class="open-chat__media">
                      <video
                        :src="mediaUrl(msg)"
                        class="open-chat__video"
                        controls
                        playsinline
                        preload="metadata"
                      />
                    </div>
                    <p v-if="msg.body" class="open-chat__text">{{ msg.body }}</p>
                    <time class="open-chat__time">{{ formatTime(msg.created_at) }}</time>
                  </div>
                </article>
                <button
                  v-if="showJumpToBottom"
                  type="button"
                  class="open-chat__jump-btn"
                  @click="jumpToLatest"
                >
                  新着メッセージ {{ pendingNewCount > 99 ? '99+' : pendingNewCount }}件 ↓
                </button>
                <div ref="bottomAnchor" class="open-chat__bottom-anchor" aria-hidden="true" />
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
            </div>
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
  font-size: var(--font-size-button);
}
.open-chat__layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 0;
  height: min(72vh, 680px);
  max-height: min(72vh, 680px);
  min-height: 480px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  overflow: hidden;
  background: var(--site-surface);
}
.open-chat__rooms {
  display: flex;
  flex-direction: column;
  min-height: 0;
  height: 100%;
  border-right: 1px solid var(--site-border);
  background: var(--site-bg-pink);
  padding: var(--sp-4);
  overflow: hidden;
}
.open-chat__rooms-title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-body);
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
  font-size: var(--font-size-caption);
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
  font-size: var(--font-size-caption);
  font-weight: 700;
  color: var(--murasaki-700);
  cursor: pointer;
}
.open-chat__notify-btn--on {
  background: var(--murasaki-100);
}
.open-chat__notify-hint {
  margin: 0 0 10px;
  font-size: var(--font-size-badge);
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
  flex: 1;
  min-height: 0;
  overflow-y: auto;
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
  font-size: var(--font-size-body);
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
  font-size: var(--font-size-badge);
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.open-chat__room-name {
  font-size: var(--font-size-button);
  font-weight: 700;
  color: var(--site-text);
}
.open-chat__room-preview {
  font-size: var(--font-size-caption);
  line-height: 1.5;
  color: var(--site-text-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.open-chat__room-meta {
  font-size: var(--font-size-badge);
  color: var(--murasaki-700);
}
.open-chat__panel {
  display: flex;
  flex-direction: column;
  min-height: 0;
  height: 100%;
  overflow: hidden;
}
.open-chat__header {
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 18px;
  border-bottom: 1px solid var(--site-border);
  background: linear-gradient(180deg, var(--murasaki-100) 0%, var(--site-surface) 100%);
}
.open-chat__header-main {
  min-width: 0;
  flex: 1;
}
.open-chat__back {
  display: inline-flex;
  align-items: center;
  margin: 0 0 8px;
  padding: 0;
  border: 0;
  background: transparent;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  font-weight: 700;
  color: var(--murasaki-700);
  cursor: pointer;
}
.open-chat__chat-body {
  position: relative;
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}
.open-chat__jump-btn {
  position: sticky;
  bottom: 12px;
  align-self: center;
  margin: 4px auto 0;
  z-index: 2;
  padding: 8px 16px;
  border: 1px solid var(--murasaki-400);
  border-radius: 999px;
  background: #fff;
  box-shadow: var(--site-shadow-md);
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  font-weight: 700;
  color: var(--murasaki-700);
  cursor: pointer;
  white-space: nowrap;
}
.open-chat__jump-btn:hover {
  background: var(--murasaki-100);
}
.open-chat__title {
  margin: 0 0 4px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-body);
  color: var(--murasaki-700);
  display: flex;
  align-items: center;
  gap: 8px;
}
.open-chat__desc {
  margin: 0;
  font-size: var(--font-size-caption);
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
  font-size: var(--font-size-caption);
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
  font-size: var(--font-size-button);
  line-height: 1.8;
}
.open-chat__messages {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  overscroll-behavior: contain;
  padding: 16px 18px 8px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #ece8e4;
  -webkit-overflow-scrolling: touch;
}
.open-chat__bottom-anchor {
  flex-shrink: 0;
  width: 100%;
  height: 1px;
}
.open-chat__bubble-row {
  display: flex;
  justify-content: flex-start;
}
.open-chat__bubble-row--own {
  justify-content: flex-end;
}
.open-chat__bubble {
  max-width: min(75%, 320px);
  min-width: 0;
  padding: 10px 12px;
  border-radius: 18px;
  background: #fff;
  border: none;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
}
.open-chat__bubble-row--own .open-chat__bubble {
  background: #d9ecff;
  border: none;
}
.open-chat__author {
  margin: 0 0 4px;
  font-size: var(--font-size-caption);
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
  font-size: var(--font-size-button);
  line-height: 1.7;
  color: var(--site-text);
  white-space: pre-wrap;
  word-break: break-word;
}
.open-chat__time {
  display: block;
  margin-top: 6px;
  font-size: var(--font-size-badge);
  color: var(--site-text-light);
  text-align: right;
}
.open-chat__composer {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 12px 14px;
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
  font-size: var(--font-size-emphasis);
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
  font-size: var(--font-size-caption);
  color: var(--site-text-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.open-chat__pending-remove {
  border: 0;
  background: transparent;
  font-size: var(--font-size-emphasis);
  line-height: 1;
  cursor: pointer;
  color: var(--site-text-muted);
}
.open-chat__media {
  margin-bottom: 6px;
  min-width: 0;
}
.open-chat__media a {
  display: block;
  line-height: 0;
}
.open-chat__image {
  display: block;
  width: 100%;
  max-width: 100%;
  min-width: 120px;
  min-height: 80px;
  max-height: 280px;
  border-radius: 10px;
  object-fit: contain;
  background: #f3f0ec;
}
.open-chat__bubble-row:not(.open-chat__bubble-row--own) .open-chat__image {
  border: 1px solid rgba(0, 0, 0, 0.08);
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
  font-size: var(--font-size-button);
  line-height: 1.6;
}
.open-chat__member-list {
  list-style: none;
  margin: 0;
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
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
  font-size: var(--font-size-button);
  font-weight: 700;
  color: var(--site-text);
}
.open-chat__member-you {
  font-weight: 500;
  color: var(--site-text-muted);
}
.open-chat__member-plan {
  font-size: var(--font-size-caption);
  color: var(--murasaki-700);
}
.open-chat__muted {
  margin: 0;
  font-size: var(--font-size-caption);
  color: var(--site-text-muted);
}
.open-chat__empty {
  text-align: center;
  padding: 24px 12px;
}

.open-chat__platform-lead {
  margin: 0 0 var(--sp-4);
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-button);
  line-height: 1.7;
  color: rgba(248, 244, 239, 0.72);
}

.open-chat__artist-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
}

.open-chat__artist-tab {
  padding: 5px 10px;
  border: 1px solid var(--site-border);
  border-radius: 999px;
  background: #fff;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  color: var(--site-text-muted);
  cursor: pointer;
}

.open-chat__artist-tab--active {
  background: var(--murasaki-700);
  border-color: var(--murasaki-800);
  color: #fff;
}

.open-chat__room-artist {
  display: block;
  font-size: var(--font-size-badge);
  color: var(--kin-600);
  letter-spacing: 0.06em;
  margin-bottom: 2px;
}

.open-chat--platform .open-chat__layout {
  border-color: rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.04);
}

.open-chat--platform .open-chat__rooms {
  background: rgba(26, 20, 24, 0.55);
  border-right-color: rgba(255, 255, 255, 0.1);
}

.open-chat--platform .open-chat__rooms-title,
.open-chat--platform .open-chat__room-name,
.open-chat--platform .open-chat__title {
  color: #f8f4ef;
}

.open-chat--platform .open-chat__room-preview,
.open-chat--platform .open-chat__room-meta,
.open-chat--platform .open-chat__desc,
.open-chat--platform .open-chat__muted {
  color: rgba(248, 244, 239, 0.55);
}

.open-chat--platform .open-chat__room-btn {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.08);
}

.open-chat--platform .open-chat__room-btn--active {
  background: rgba(122, 80, 136, 0.35);
  border-color: rgba(201, 169, 97, 0.4);
}

.open-chat--platform .open-chat__panel {
  background: rgba(20, 16, 20, 0.35);
}

.open-chat--platform .open-chat__messages {
  background: #ece5d8;
}

.open-chat--platform .open-chat__artist-tab {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.14);
  color: rgba(248, 244, 239, 0.72);
}

.open-chat--platform .open-chat__artist-tab--active {
  background: var(--murasaki-600);
  border-color: var(--murasaki-700);
  color: #fff;
}

.open-chat--platform .open-chat__notify-btn {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.18);
  color: #f8f4ef;
}

.open-chat--platform .open-chat__back {
  color: #f8f4ef;
}

@media (max-width: 767px) {
  .open-chat__layout {
    grid-template-columns: 1fr;
    height: min(70dvh, 640px);
    max-height: min(70dvh, 640px);
    min-height: 0;
  }
  .open-chat--mobile .open-chat__rooms,
  .open-chat--mobile .open-chat__panel {
    height: 100%;
    max-height: none;
    border-right: 0;
    border-bottom: 0;
  }
  .open-chat__room-list {
    max-height: none;
  }
  .open-chat__header {
    flex-wrap: wrap;
    align-items: flex-start;
    padding: 12px 14px;
  }
  .open-chat__header-actions {
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
  .open-chat__desc {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
}
</style>
