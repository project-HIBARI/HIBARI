<script setup>
/**
 * 部品名: ストーリービューア（フルスクリーン）
 */
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import UiIco from '../../ui/UiIco.vue'
import { useAuth } from '../../../composables/useAuth.js'
import { useToast } from '../../../composables/useToast.js'
import { recordSnsStoryView, fetchSnsStoryViewers, deleteSnsStory, sendDm } from '../../../api/sns.js'

const props = defineProps({
  groups: { type: Array, required: true },
  initialGroupIndex: { type: Number, default: 0 },
})

const emit = defineEmits(['close', 'open-profile', 'deleted', 'need-auth'])

const MAX_REPLY = 300
const REACTION_EMOJI = ['❤️', '🔥', '👏', '😂', '😢', '😮']
const replyInput = ref('')
const replySending = ref(false)
const replySent = ref(false)
const reactionSending = ref(false)
const reactionSent = ref(null)
const reactionError = ref(false)

const { user, isLoggedIn } = useAuth()
const { showToast } = useToast()

const groupIndex = ref(props.initialGroupIndex)
const storyIndex = ref(0)
const progress = ref(0)
const paused = ref(false)
const showViewers = ref(false)
const viewers = ref([])
const viewersLoading = ref(false)
const videoEl = ref(null)
const videoPlayFailed = ref(false)

const IMAGE_DURATION_MS = 5000
const VIDEO_FALLBACK_DURATION_MS = 15000
let timer = null
let lastTick = 0
let touchStartX = 0
let touchStartY = 0

const currentGroup = computed(() => props.groups[groupIndex.value] || null)
const currentStory = computed(() => currentGroup.value?.stories?.[storyIndex.value] || null)
const isOwner = computed(() => currentGroup.value && user.value && currentGroup.value.account_id === user.value.account_id)

function stopTimer() {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

function startTimer(durationMs) {
  stopTimer()
  progress.value = 0
  lastTick = Date.now()
  timer = setInterval(() => {
    if (paused.value) {
      lastTick = Date.now()
      return
    }
    const now = Date.now()
    const elapsed = now - lastTick
    lastTick = now
    progress.value += (elapsed / durationMs) * 100
    if (progress.value >= 100) {
      goNext()
    }
  }, 50)
}

function loadCurrent() {
  if (!currentStory.value) {
    emit('close')
    return
  }
  replyInput.value = ''
  replySent.value = false
  reactionSent.value = null
  reactionError.value = false
  videoPlayFailed.value = false
  const isVideo = currentStory.value.media_type === 'video'
  const durationMs = isVideo ? VIDEO_FALLBACK_DURATION_MS : IMAGE_DURATION_MS
  startTimer(durationMs)
  if (!isOwner.value) {
    recordSnsStoryView(currentStory.value.story_id).catch(() => {})
    currentStory.value.viewed_by_viewer = true
  }
  if (isVideo) {
    nextTick(() => {
      const el = videoEl.value
      if (!el) return
      el.currentTime = 0
      const playPromise = el.play()
      if (playPromise && typeof playPromise.catch === 'function') {
        playPromise.catch(() => {
          videoPlayFailed.value = true
        })
      }
    })
  }
}

function playVideoManually() {
  const el = videoEl.value
  if (!el) return
  el.play()
    .then(() => {
      videoPlayFailed.value = false
    })
    .catch(() => {
      videoPlayFailed.value = true
    })
}

async function sendReply() {
  if (!isLoggedIn.value) {
    emit('need-auth', { mode: 'login' })
    return
  }
  const body = replyInput.value.trim()
  if (!body || replySending.value || !currentStory.value || isOwner.value) return
  replySending.value = true
  paused.value = true
  try {
    await sendDm({
      recipient_id: currentGroup.value.account_id,
      message_type: 'story_reply',
      body,
      shared_story_id: currentStory.value.story_id,
    })
    replyInput.value = ''
    replySent.value = true
  } catch {
    // 送信失敗時は入力内容を保持
  } finally {
    replySending.value = false
    paused.value = false
  }
}

async function sendReaction(emoji) {
  if (!isLoggedIn.value) {
    emit('need-auth', { mode: 'login' })
    return
  }
  if (reactionSending.value || !currentStory.value || isOwner.value) return
  reactionSending.value = true
  reactionError.value = false
  paused.value = true
  try {
    await sendDm({
      recipient_id: currentGroup.value.account_id,
      message_type: 'story_reaction',
      reaction_emoji: emoji,
      shared_story_id: currentStory.value.story_id,
    })
    reactionSent.value = emoji
    showToast(`${emoji} を送信しました`)
  } catch {
    reactionError.value = true
    showToast('リアクションの送信に失敗しました', { tone: 'error' })
  } finally {
    reactionSending.value = false
    paused.value = false
  }
}

function goNext() {
  if (storyIndex.value < (currentGroup.value?.stories?.length || 0) - 1) {
    storyIndex.value += 1
    loadCurrent()
  } else if (groupIndex.value < props.groups.length - 1) {
    groupIndex.value += 1
    storyIndex.value = 0
    loadCurrent()
  } else {
    emit('close')
  }
}

function goPrev() {
  if (storyIndex.value > 0) {
    storyIndex.value -= 1
    loadCurrent()
  } else if (groupIndex.value > 0) {
    groupIndex.value -= 1
    storyIndex.value = (props.groups[groupIndex.value]?.stories?.length || 1) - 1
    loadCurrent()
  } else {
    loadCurrent()
  }
}

function onPointerDown() {
  paused.value = true
}
function onPointerUp() {
  paused.value = false
}

function onTouchStart(e) {
  onPointerDown()
  const t = e.touches[0]
  touchStartX = t.clientX
  touchStartY = t.clientY
}

function onTouchEnd(e) {
  onPointerUp()
  const t = e.changedTouches[0]
  const dx = t.clientX - touchStartX
  const dy = t.clientY - touchStartY
  if (Math.abs(dy) > 80 && Math.abs(dy) > Math.abs(dx)) {
    e.preventDefault()
    emit('close')
    return
  }
  if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy)) {
    e.preventDefault()
    if (dx < 0) goNext()
    else goPrev()
  }
}

function onZoneClick(direction) {
  if (direction === 'prev') goPrev()
  else goNext()
}

async function openViewers() {
  if (!isOwner.value || !currentStory.value) return
  paused.value = true
  showViewers.value = true
  viewersLoading.value = true
  try {
    const data = await fetchSnsStoryViewers(currentStory.value.story_id)
    viewers.value = data.viewers
  } catch {
    viewers.value = []
  } finally {
    viewersLoading.value = false
  }
}

function closeViewers() {
  showViewers.value = false
  paused.value = false
}

async function onDelete() {
  if (!currentStory.value || !window.confirm('このストーリーズを削除しますか？')) return
  try {
    await deleteSnsStory(currentStory.value.story_id)
    emit('deleted', currentStory.value.story_id)
    goNext()
  } catch {
    // 削除失敗時は表示を維持
  }
}

function onKey(e) {
  if (e.key === 'Escape') emit('close')
  if (e.key === 'ArrowRight') goNext()
  if (e.key === 'ArrowLeft') goPrev()
}

function onVisibilityChange() {
  if (document.hidden) {
    paused.value = true
    videoEl.value?.pause()
  } else {
    paused.value = false
    lastTick = Date.now()
    if (currentStory.value?.media_type === 'video') playVideoManually()
  }
}

onMounted(() => {
  loadCurrent()
  window.addEventListener('keydown', onKey)
  document.addEventListener('visibilitychange', onVisibilityChange)
})
onUnmounted(() => {
  stopTimer()
  window.removeEventListener('keydown', onKey)
  document.removeEventListener('visibilitychange', onVisibilityChange)
})
</script>

<template>
  <div class="sns-story-viewer" role="dialog" aria-modal="true" aria-label="ストーリービューア">
    <template v-if="currentStory">
      <div class="sns-story-viewer__bars">
        <span
          v-for="(s, i) in currentGroup.stories"
          :key="s.story_id"
          class="sns-story-viewer__bar"
        >
          <span
            class="sns-story-viewer__bar-fill"
            :style="{ width: i < storyIndex ? '100%' : i === storyIndex ? progress + '%' : '0%' }"
          />
        </span>
      </div>

      <header class="sns-story-viewer__head">
        <button type="button" class="sns-story-viewer__author" @click="emit('open-profile', currentGroup.account_id)">
          <span class="sns-story-viewer__avatar">
            <img v-if="currentGroup.author_avatar_path" :src="currentGroup.author_avatar_path" :alt="currentGroup.author_name" />
            <span v-else>{{ (currentGroup.author_name || '?').charAt(0) }}</span>
          </span>
          <span class="sns-story-viewer__name">{{ currentGroup.author_name }}</span>
        </button>
        <div class="sns-story-viewer__head-actions">
          <button v-if="isOwner" type="button" class="sns-story-viewer__icon-btn" aria-label="削除" @click="onDelete">
            <UiIco name="trash" :size="18" color="var(--beni-600)" />
          </button>
          <button type="button" class="sns-story-viewer__icon-btn" aria-label="閉じる" @click="emit('close')">
            <UiIco name="close" :size="20" />
          </button>
        </div>
      </header>

      <div
        class="sns-story-viewer__media"
        @mousedown="onPointerDown"
        @mouseup="onPointerUp"
        @touchstart="onTouchStart"
        @touchend="onTouchEnd"
      >
        <img v-if="currentStory.media_type === 'image'" :src="currentStory.file_path" :alt="currentStory.caption || 'ストーリーズ'" loading="eager" />
        <video
          v-else
          ref="videoEl"
          :src="currentStory.file_path"
          playsinline
          preload="metadata"
          @ended="goNext"
        />
        <button
          v-if="currentStory.media_type === 'video' && videoPlayFailed"
          type="button"
          class="sns-story-viewer__play-btn"
          aria-label="動画を再生する"
          @click="playVideoManually"
        >
          <UiIco name="play" :size="28" color="#fff" />
        </button>

        <button type="button" class="sns-story-viewer__zone sns-story-viewer__zone--prev" aria-label="前のストーリーズへ" @click="onZoneClick('prev')" />
        <button type="button" class="sns-story-viewer__zone sns-story-viewer__zone--next" aria-label="次のストーリーズへ" @click="onZoneClick('next')" />

        <p v-if="currentStory.caption" class="sns-story-viewer__caption">{{ currentStory.caption }}</p>
      </div>

      <footer v-if="isOwner" class="sns-story-viewer__footer">
        <button type="button" class="sns-story-viewer__viewers-btn" @click="openViewers">
          <UiIco name="eye" :size="16" />
          閲覧者を見る
        </button>
      </footer>
      <footer v-else class="sns-story-viewer__footer">
        <div class="sns-story-viewer__reactions">
          <button
            v-for="emoji in REACTION_EMOJI"
            :key="emoji"
            type="button"
            class="sns-story-viewer__reaction-btn"
            :class="{ 'sns-story-viewer__reaction-btn--sent': reactionSent === emoji }"
            :disabled="reactionSending"
            :aria-label="`${emoji} でリアクションする`"
            @pointerdown="paused = true"
            @pointerup="paused = false"
            @click="sendReaction(emoji)"
          >
            {{ emoji }}
          </button>
        </div>
        <p v-if="reactionSent" class="sns-story-viewer__reaction-sent">{{ reactionSent }} を送信しました</p>
        <p v-else-if="reactionError" class="sns-story-viewer__reaction-error">リアクションを送信できませんでした</p>

        <form v-if="!replySent" class="sns-story-viewer__reply-form" @submit.prevent="sendReply">
          <input
            v-model="replyInput"
            type="text"
            class="sns-story-viewer__reply-input"
            :maxlength="MAX_REPLY"
            placeholder="返信を送信（DMに届きます）"
            :disabled="replySending"
            @focus="paused = true"
            @blur="paused = false"
          />
          <button type="submit" class="sns-story-viewer__reply-send" :disabled="replySending || !replyInput.trim()" aria-label="送信">
            <UiIco name="send" :size="16" color="#fff" />
          </button>
        </form>
        <p v-else class="sns-story-viewer__reply-sent">返信を送信しました</p>
      </footer>

      <div v-if="showViewers" class="sns-story-viewer__viewers-panel">
        <div class="sns-story-viewer__viewers-head">
          <span>閲覧者</span>
          <button type="button" class="sns-story-viewer__icon-btn" aria-label="閉じる" @click="closeViewers">
            <UiIco name="close" :size="16" />
          </button>
        </div>
        <p v-if="viewersLoading" class="sns-story-viewer__viewers-state">読み込み中…</p>
        <p v-else-if="!viewers.length" class="sns-story-viewer__viewers-state">まだ閲覧されていません</p>
        <ul v-else class="sns-story-viewer__viewers-list">
          <li v-for="v in viewers" :key="v.account_id">
            <span class="sns-story-viewer__viewers-avatar">
              <img v-if="v.avatar_path" :src="v.avatar_path" :alt="v.name" />
              <span v-else>{{ (v.name || '?').charAt(0) }}</span>
            </span>
            {{ v.name }}
          </li>
        </ul>
      </div>
    </template>
  </div>
</template>

<style scoped>
.sns-story-viewer {
  position: fixed;
  inset: 0;
  z-index: 500;
  background: #000;
  display: flex;
  flex-direction: column;
  color: #fff;
}
.sns-story-viewer__bars {
  display: flex;
  gap: 4px;
  padding: 8px 8px 0;
}
.sns-story-viewer__bar {
  flex: 1;
  height: 2px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  overflow: hidden;
}
.sns-story-viewer__bar-fill {
  display: block;
  height: 100%;
  background: #fff;
}
.sns-story-viewer__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
}
.sns-story-viewer__author {
  display: flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: 0;
  cursor: pointer;
  color: #fff;
}
.sns-story-viewer__avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--murasaki-700);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}
.sns-story-viewer__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sns-story-viewer__name {
  font-size: 13px;
}
.sns-story-viewer__head-actions {
  display: flex;
  gap: 6px;
}
.sns-story-viewer__icon-btn {
  background: transparent;
  border: 0;
  color: #fff;
  cursor: pointer;
  padding: 4px;
}
.sns-story-viewer__media {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.sns-story-viewer__media img,
.sns-story-viewer__media video {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
.sns-story-viewer__zone {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 35%;
  background: transparent;
  border: 0;
  cursor: pointer;
}
.sns-story-viewer__zone--prev {
  left: 0;
}
.sns-story-viewer__zone--next {
  right: 0;
}
.sns-story-viewer__caption {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 16px;
  margin: 0;
  padding: 0 16px;
  text-align: center;
  font-size: 13px;
  color: #fff;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.6);
}
.sns-story-viewer__play-btn {
  position: absolute;
  top: 50%;
  left: 50%;
  z-index: 2;
  transform: translate(-50%, -50%);
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.sns-story-viewer__footer {
  padding: 12px 16px calc(12px + env(safe-area-inset-bottom, 0px));
}
.sns-story-viewer__reactions {
  display: flex;
  justify-content: space-between;
  gap: 6px;
  margin-bottom: 8px;
}
.sns-story-viewer__reaction-btn {
  flex: 1;
  min-width: 44px;
  min-height: 44px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.08);
  font-size: 20px;
  line-height: 1;
  cursor: pointer;
  transition: transform 0.15s ease, background-color 0.15s ease;
}
.sns-story-viewer__reaction-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.sns-story-viewer__reaction-btn--sent {
  background: rgba(228, 190, 99, 0.25);
  border-color: var(--sns-gold, var(--kin-500));
  transform: scale(1.08);
}
.sns-story-viewer__reaction-sent,
.sns-story-viewer__reaction-error {
  margin: 0 0 8px;
  text-align: center;
  font-size: 12px;
}
.sns-story-viewer__reaction-sent {
  color: rgba(255, 255, 255, 0.7);
}
.sns-story-viewer__reaction-error {
  color: #e08a8a;
}
.sns-story-viewer__reply-form {
  display: flex;
  align-items: center;
  gap: 8px;
}
.sns-story-viewer__reply-input {
  flex: 1;
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: rgba(255, 255, 255, 0.08);
  border-radius: 999px;
  padding: 9px 16px;
  font-size: 13px;
  color: #fff;
}
.sns-story-viewer__reply-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}
.sns-story-viewer__reply-send {
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
.sns-story-viewer__reply-send:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.sns-story-viewer__reply-sent {
  margin: 0;
  text-align: center;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}
.sns-story-viewer__viewers-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 999px;
  color: #fff;
  padding: 8px 16px;
  font-size: 12px;
  cursor: pointer;
}
.sns-story-viewer__viewers-panel {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  max-height: 50%;
  background: rgba(20, 16, 18, 0.96);
  border-radius: 16px 16px 0 0;
  padding: 14px 16px calc(14px + env(safe-area-inset-bottom, 0px));
  overflow-y: auto;
}
.sns-story-viewer__viewers-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  margin-bottom: 10px;
}
.sns-story-viewer__viewers-state {
  margin: 0;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  text-align: center;
  padding: 12px 0;
}
.sns-story-viewer__viewers-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.sns-story-viewer__viewers-list li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}
.sns-story-viewer__viewers-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--murasaki-600);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
}
.sns-story-viewer__viewers-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sns-story-viewer button:focus-visible {
  outline: 2px solid var(--sns-gold, #e4be63);
  outline-offset: 2px;
}
</style>
