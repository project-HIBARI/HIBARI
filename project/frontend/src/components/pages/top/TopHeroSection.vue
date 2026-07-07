<script setup>
/**
 * 部品名: ホーム — ヒーローエリア
 * 用途: 全幅背景動画・コピー・CTA・AIカード・80周年バッジ
 */
import UiButton from '../../ui/UiButton.vue'
import TopAiCard from './TopAiCard.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const emit = defineEmits(['open-auth', 'scroll-enjoy', 'open-ai'])

const heroVideoSrc = HIBARU_DATA.homeHeroVideo?.src || HIBARU_DATA.homePromoVideo.src
</script>

<template>
  <section class="top-hero" aria-label="メインビジュアル">
    <video
      class="top-hero__video"
      autoplay
      muted
      loop
      playsinline
      preload="auto"
      aria-hidden="true"
    >
      <source :src="heroVideoSrc" type="video/mp4" />
    </video>

    <div class="top-hero__overlay" aria-hidden="true" />

    <div class="top-hero__inner">
      <div class="top-hero__copy">
        <h1 class="top-hero__title">
          永遠の歌声、<br />
          美空ひばりとともに。
        </h1>
        <p class="top-hero__sub">
          美空ひばりの魅力を、もっと深く、もっと身近に。<br />
          ここだけの体験を、あなたに。
        </p>
        <div class="top-hero__cta">
          <UiButton variant="primary" size="lg" @click="emit('open-auth', 'register')">
            新規登録（無料）
          </UiButton>
          <UiButton variant="outline" size="lg" @click="emit('scroll-enjoy')">
            サイトの楽しみ方
          </UiButton>
        </div>
      </div>

      <div class="top-hero__side">
        <TopAiCard @open-ai="emit('open-ai')" />
        <div class="top-hero__anniversary" aria-label="芸能生活80周年記念">
          <div class="top-hero__anniversary-ring">
            <span class="top-hero__anniversary-num">80</span>
            <span class="top-hero__anniversary-unit">周年</span>
          </div>
          <p class="top-hero__anniversary-text">芸能生活<br />80周年<br />記念サイト</p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.top-hero {
  position: relative;
  width: 100%;
  overflow: hidden;
  min-height: clamp(520px, calc(100vh - 168px), 780px);
}

.top-hero__video {
  position: absolute;
  inset: 0;
  z-index: 0;
  width: 100%;
  height: 100%;
  min-width: 100%;
  min-height: 100%;
  object-fit: cover;
  object-position: center 32%;
  pointer-events: none;
  opacity: 1;
  filter: contrast(1.05);
  transform: scale(1.08);
  transform-origin: center center;
}

.top-hero__overlay {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.05) 0%,
    rgba(255, 255, 255, 0.02) 20%,
    transparent 36%
  );
}

.top-hero__inner {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: minmax(280px, 1fr) minmax(260px, 360px);
  gap: clamp(24px, 4vw, 48px);
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  padding: clamp(48px, 6vw, 72px) clamp(24px, 4vw, 56px);
  min-height: inherit;
}

.top-hero__copy {
  position: relative;
  padding: 8px 0;
}

.top-hero__copy::before {
  content: '';
  position: absolute;
  z-index: -1;
  inset: -20px 24px -20px -28px;
  background: linear-gradient(
    102deg,
    rgba(255, 251, 247, 0.42) 0%,
    rgba(255, 249, 246, 0.16) 52%,
    transparent 100%
  );
  pointer-events: none;
}

.top-hero__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: clamp(32px, 4vw, 46px);
  font-weight: 800;
  line-height: 1.52;
  letter-spacing: 0.08em;
  color: var(--site-text);
  text-shadow:
    0 1px 2px rgba(255, 255, 255, 0.9),
    0 0 16px rgba(255, 251, 247, 0.5);
}

.top-hero__sub {
  margin: var(--sp-6) 0 0;
  font-size: 14px;
  line-height: 2;
  color: var(--site-text-muted);
  letter-spacing: 0.05em;
  text-shadow: 0 1px 8px rgba(255, 255, 255, 0.75);
}

.top-hero__cta {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: var(--sp-7);
}

.top-hero__side {
  display: flex;
  flex-direction: column;
  gap: var(--sp-5);
  align-items: stretch;
  justify-self: end;
  width: 100%;
  max-width: 360px;
}

.top-hero__anniversary {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid var(--kin-500);
  border-radius: var(--site-radius-md);
  box-shadow: var(--site-shadow);
  align-self: flex-end;
}

.top-hero__anniversary-ring {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  border: 2px solid var(--kin-500);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle, #fff 0%, var(--site-surface-muted) 100%);
  flex-shrink: 0;
}

.top-hero__anniversary-num {
  font-family: var(--ff-latin);
  font-size: 24px;
  font-weight: 700;
  color: var(--kin-600);
  line-height: 1;
}

.top-hero__anniversary-unit {
  font-family: var(--ff-mincho);
  font-size: 10px;
  color: var(--kin-600);
}

.top-hero__anniversary-text {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 11px;
  line-height: 1.65;
  letter-spacing: 0.08em;
  color: var(--site-text-muted);
}

@media (max-width: 1100px) {
  .top-hero__inner {
    grid-template-columns: 1fr;
    gap: var(--sp-7);
    padding-top: var(--sp-7);
    padding-bottom: var(--sp-7);
  }
  .top-hero__side {
    justify-self: center;
    max-width: 420px;
  }
}

@media (max-width: 767px) {
  .top-hero {
    min-height: min(68vh, 620px);
  }
  .top-hero__inner {
    padding: var(--sp-6) var(--sp-4);
  }
  .top-hero__copy::before {
    inset: -12px -8px -12px -12px;
    background: linear-gradient(
      180deg,
      rgba(255, 251, 247, 0.5) 0%,
      rgba(255, 249, 246, 0.22) 65%,
      transparent 100%
    );
  }
  .top-hero__title {
    font-size: clamp(26px, 7.5vw, 34px);
  }
  .top-hero__cta {
    flex-direction: column;
    align-items: stretch;
  }
  .top-hero__video {
    object-position: center 28%;
    transform: scale(1.12);
  }
}

@media (prefers-reduced-motion: reduce) {
  .top-hero__video {
    display: none;
    transform: none;
  }
  .top-hero__overlay {
    background: linear-gradient(118deg, #fff9f6 0%, var(--site-bg-pink) 38%, #f8f0ea 100%);
  }
}
</style>
