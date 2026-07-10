<script setup>
/**
 * 部品名: サイト起動イントロビデオ
 * 用途: 初回アクセス時に全画面プロモーションを表示し、ホームへフェード遷移
 */
import { ref, onMounted, onUnmounted } from 'vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'
import { SITE_NAME, HIBARI_FANCLUB_NAME } from '../../constants/site.js'

const emit = defineEmits(['complete'])

defineProps({
  leaving: { type: Boolean, default: false },
})

const videoSrc = HIBARU_DATA.homePromoVideo?.src || HIBARU_DATA.homeHeroVideo?.src
const videoRef = ref(null)
const videoFailed = ref(false)
const canSkip = ref(false)

const DISPLAY_MS = 5500
const FADE_MS = 680

let displayTimer = null
let skipTimer = null

function finish() {
  if (displayTimer) {
    clearTimeout(displayTimer)
    displayTimer = null
  }
  emit('complete')
}

function onVideoError() {
  videoFailed.value = true
}

function tryPlay() {
  const el = videoRef.value
  if (!el) return
  el.play().catch(() => {
    videoFailed.value = true
  })
}

onMounted(() => {
  skipTimer = window.setTimeout(() => {
    canSkip.value = true
  }, 800)

  displayTimer = window.setTimeout(finish, DISPLAY_MS)

  window.setTimeout(tryPlay, 60)

  const el = videoRef.value
  if (el) {
    el.addEventListener('ended', () => {
      window.setTimeout(finish, 400)
    })
  }
})

onUnmounted(() => {
  if (displayTimer) clearTimeout(displayTimer)
  if (skipTimer) clearTimeout(skipTimer)
})
</script>

<template>
  <div
    class="site-intro"
    :class="{ 'site-intro--leaving': leaving }"
    role="dialog"
    aria-label="プロモーション映像"
    aria-modal="true"
  >
    <div class="site-intro__backdrop" aria-hidden="true" />

    <video
      v-if="!videoFailed"
      ref="videoRef"
      class="site-intro__video"
      :src="videoSrc"
      autoplay
      muted
      playsinline
      preload="auto"
      aria-hidden="true"
      @error="onVideoError"
    />

    <div v-else class="site-intro__fallback" aria-hidden="true">
      <p class="site-intro__fallback-label">{{ SITE_NAME }}</p>
      <p class="site-intro__fallback-title">{{ HIBARI_FANCLUB_NAME }}</p>
    </div>

    <div class="site-intro__veil" aria-hidden="true" />

    <p class="site-intro__brand">{{ SITE_NAME }}</p>
    <p class="site-intro__brand-sub">{{ HIBARI_FANCLUB_NAME }}</p>

    <button
      v-if="canSkip"
      type="button"
      class="site-intro__skip"
      @click="finish"
    >
      スキップ
    </button>
  </div>
</template>

<style scoped>
.site-intro {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  opacity: 1;
  transition: opacity 0.68s ease;
}
.site-intro--leaving {
  opacity: 0;
  pointer-events: none;
}
.site-intro__backdrop {
  position: absolute;
  inset: 0;
  background: linear-gradient(160deg, #2a1520 0%, #1a0a12 45%, #120810 100%);
}
.site-intro__video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 30%;
}
.site-intro__fallback {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  background:
    radial-gradient(ellipse at 50% 35%, rgba(122, 80, 136, 0.35) 0%, transparent 55%),
    linear-gradient(160deg, #2a1520 0%, #1a0a12 100%);
}
.site-intro__fallback-label {
  margin: 0;
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.28em;
  color: rgba(255, 255, 255, 0.72);
}
.site-intro__fallback-title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: clamp(28px, 5vw, 40px);
  letter-spacing: 0.2em;
  color: rgba(255, 251, 247, 0.95);
}
.site-intro__veil {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(20, 10, 18, 0.15) 0%,
    rgba(20, 10, 18, 0.08) 40%,
    rgba(250, 248, 244, 0.12) 100%
  );
  pointer-events: none;
}
.site-intro__brand {
  position: absolute;
  bottom: 56px;
  left: 50%;
  transform: translateX(-50%);
  margin: 0;
  font-family: var(--ff-latin);
  font-size: clamp(18px, 3vw, 24px);
  font-weight: 600;
  letter-spacing: 0.14em;
  color: rgba(255, 255, 255, 0.92);
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.35);
  white-space: nowrap;
}
.site-intro__brand-sub {
  position: absolute;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 11px;
  letter-spacing: 0.16em;
  color: rgba(255, 255, 255, 0.72);
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.35);
  white-space: nowrap;
}
.site-intro__skip {
  position: absolute;
  right: 20px;
  bottom: 20px;
  padding: 8px 14px;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  letter-spacing: 0.08em;
  color: rgba(255, 255, 255, 0.88);
  background: rgba(30, 16, 24, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.28);
  border-radius: 999px;
  cursor: pointer;
  backdrop-filter: blur(6px);
  transition: background 0.35s ease, border-color 0.35s ease, opacity 0.35s ease;
}
.site-intro__skip:hover {
  background: rgba(90, 50, 100, 0.55);
  border-color: rgba(255, 255, 255, 0.45);
}

@media (max-width: 767px) {
  .site-intro__brand {
    bottom: 72px;
    font-size: 16px;
  }
  .site-intro__brand-sub {
    bottom: 48px;
    font-size: 10px;
  }
  .site-intro__skip {
    right: 16px;
    bottom: 16px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .site-intro__video {
    display: none;
  }
  .site-intro {
    transition-duration: 0.2s;
  }
}
</style>
