<script setup>
/**
 * 部品名: ホーム — ヒーローエリア
 * 用途: 全幅背景動画・コピー・CTA（script 連動パララックス）
 */
import { onBeforeUnmount, onMounted, ref } from 'vue'
import UiButton from '../../ui/UiButton.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'
import { useHeroParallax } from '../../../composables/useHeroParallax.js'
import { whenSiteReady, prefersReducedMotion } from '../../../composables/useSiteReady.js'

const emit = defineEmits(['open-auth', 'open-ai', 'scroll-enjoy'])

const heroVideoSrc = HIBARU_DATA.homeHeroVideo?.src || HIBARU_DATA.homePromoVideo.src

const heroRef = ref(null)
const videoFailed = ref(false)
const { heroStyle, heroActive } = useHeroParallax(heroRef)

const revealTitle = ref(false)
const revealSub = ref(false)
const revealCta = ref(false)

let revealTimers = []
let cleanupReady = null

function startHeroReveal() {
  if (prefersReducedMotion()) {
    revealTitle.value = true
    revealSub.value = true
    revealCta.value = true
    return
  }
  revealTimers.push(window.setTimeout(() => { revealTitle.value = true }, 280))
  revealTimers.push(window.setTimeout(() => { revealSub.value = true }, 520))
  revealTimers.push(window.setTimeout(() => { revealCta.value = true }, 780))
}

onMounted(() => {
  cleanupReady = whenSiteReady(startHeroReveal)
})

onBeforeUnmount(() => {
  cleanupReady?.()
  revealTimers.forEach(clearTimeout)
  revealTimers = []
})
</script>

<template>
  <section
    ref="heroRef"
    class="home-hero"
    :class="{ 'home-hero--active': heroActive }"
    :style="heroStyle"
    aria-label="メインビジュアル"
  >
    <div v-if="videoFailed" class="home-hero__fallback" aria-hidden="true" />

    <video
      v-show="!videoFailed"
      class="home-hero__video"
      autoplay
      muted
      loop
      playsinline
      preload="auto"
      aria-hidden="true"
      @error="videoFailed = true"
    >
      <source :src="heroVideoSrc" type="video/mp4" />
    </video>

    <div class="home-hero__overlay" aria-hidden="true" />
    <div class="home-hero__light" aria-hidden="true" />

    <div class="home-hero__inner">
      <div class="home-hero__copy">
        <h1
          class="home-hero__title home-hero-reveal"
          :class="{ 'is-revealed': revealTitle }"
        >
          永遠の歌声、<br />
          美空ひばりとともに。
        </h1>
        <p
          class="home-hero__sub home-hero-reveal"
          :class="{ 'is-revealed': revealSub }"
        >
          美空ひばりの魅力を、もっと深く、もっと身近に。<br />
          ここだけの体験を、あなたに。
        </p>
        <div
          class="home-hero__cta home-hero-reveal home-hero-reveal--cta"
          :class="{ 'is-revealed': revealCta }"
        >
          <UiButton
            variant="primary"
            size="lg"
            class="home-cta-btn motion-cta-shine"
            @click="emit('open-auth', 'register')"
          >
            ファンクラブ特典を見る
          </UiButton>
          <UiButton
            variant="outline"
            size="lg"
            class="home-cta-btn home-cta-btn--outline"
            @click="emit('open-ai')"
          >
            AIひばり
          </UiButton>
        </div>
      </div>
    </div>

    <button
      type="button"
      class="home-hero__scroll home-hero__scroll-cue"
      aria-label="下へスクロール"
      @click="emit('scroll-enjoy')"
    >
      <span class="home-hero__scroll-icon" aria-hidden="true">⌄</span>
    </button>
  </section>
</template>

<style scoped>
.home-hero {
  position: relative;
  width: 100vw;
  max-width: none;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  margin-bottom: var(--sp-8);
  min-height: calc(100vh - 148px);
  max-height: 820px;
  border-radius: 0;
  overflow: hidden;
}

.home-hero__video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  max-width: none;
  object-fit: cover;
  object-position: 58% 22%;
  z-index: 0;
  pointer-events: none;
  opacity: 1;
  filter: contrast(1.05);
}

.home-hero__fallback {
  position: absolute;
  inset: 0;
  z-index: 0;
  background:
    linear-gradient(118deg, rgba(255, 249, 246, 0.95) 0%, rgba(248, 236, 228, 0.88) 42%, rgba(93, 58, 107, 0.22) 100%),
    radial-gradient(ellipse 80% 60% at 70% 30%, rgba(201, 169, 97, 0.18), transparent 70%);
}

.home-hero__overlay {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}

.home-hero__inner {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: minmax(280px, 1fr);
  justify-items: start;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--sp-8) var(--sp-6);
  min-height: inherit;
}

.home-hero__copy {
  position: relative;
  width: fit-content;
  max-width: 720px;
  padding: 28px 32px;
}

.home-hero__copy::before {
  content: '';
  position: absolute;
  z-index: -1;
  inset: -24px -20px -24px -24px;
  background: linear-gradient(
    105deg,
    rgba(255, 251, 247, 0.78) 0%,
    rgba(255, 249, 246, 0.42) 58%,
    rgba(255, 255, 255, 0) 100%
  );
  border-radius: var(--site-radius-md);
  pointer-events: none;
}

.home-hero__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: clamp(34px, 4.2vw, 48px);
  font-weight: 800;
  line-height: 1.5;
  letter-spacing: 0.08em;
  color: var(--site-text);
  text-shadow:
    0 1px 2px rgba(255, 255, 255, 0.95),
    0 0 20px rgba(255, 251, 247, 0.65);
}

.home-hero__sub {
  margin: var(--sp-6) 0 0;
  font-size: 14px;
  line-height: 2.1;
  color: var(--site-text-muted);
  letter-spacing: 0.05em;
  text-shadow: 0 1px 10px rgba(255, 255, 255, 0.85);
}

.home-hero__cta {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: var(--sp-7);
}

.home-hero__scroll {
  position: absolute;
  z-index: 3;
  left: 50%;
  bottom: 24px;
  padding: 6px 12px;
  border: 0;
  background: transparent;
  cursor: pointer;
  color: var(--murasaki-600);
}

.home-hero__scroll-icon {
  display: block;
  font-size: 22px;
  line-height: 1;
  text-shadow: 0 1px 8px rgba(255, 255, 255, 0.8);
}

@media (max-width: 1100px) {
  .home-hero__inner {
    padding-top: var(--sp-7);
    padding-bottom: var(--sp-7);
  }
  .home-hero__copy::before {
    inset: -20px -16px -20px -20px;
  }
}

@media (max-width: 767px) {
  .home-hero {
    min-height: min(72vh, 640px);
    max-height: none;
    margin-bottom: var(--sp-6);
  }
  .home-hero__inner {
    padding: var(--sp-6) var(--sp-4);
  }
  .home-hero__copy {
    width: 100%;
    max-width: 100%;
    padding: 20px 16px;
  }
  .home-hero__copy::before {
    inset: -12px -8px -12px -12px;
    background: linear-gradient(
      180deg,
      rgba(255, 251, 247, 0.82) 0%,
      rgba(255, 249, 246, 0.5) 70%,
      rgba(255, 255, 255, 0) 100%
    );
  }
  .home-hero__title {
    font-size: clamp(28px, 8vw, 36px);
  }
  .home-hero__cta {
    flex-direction: column;
    align-items: stretch;
  }
}

@media (prefers-reduced-motion: reduce) {
  .home-hero__video {
    display: none;
  }
  .home-hero__overlay {
    background: linear-gradient(118deg, #fff9f6 0%, var(--site-bg-pink) 38%, #f8f0ea 100%);
    opacity: 1 !important;
  }
  .home-hero__light {
    display: none;
  }
}
</style>
