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
  <section class="home-hero" aria-label="メインビジュアル">
    <video
      class="home-hero__video"
      autoplay
      muted
      loop
      playsinline
      preload="auto"
      aria-hidden="true"
    >
      <source :src="heroVideoSrc" type="video/mp4" />
    </video>

    <div class="home-hero__overlay" aria-hidden="true" />

    <div class="home-hero__inner">
      <div class="home-hero__copy">
        <h1 class="home-hero__title">
          永遠の歌声、<br />
          美空ひばりとともに。
        </h1>
        <p class="home-hero__sub">
          美空ひばりの魅力を、もっと深く、もっと身近に。<br />
          ここだけの体験を、あなたに。
        </p>
        <div class="home-hero__cta">
          <UiButton variant="primary" size="lg" @click="emit('open-auth', 'register')">
            新規登録（無料）
          </UiButton>
          <UiButton variant="outline" size="lg" @click="emit('scroll-enjoy')">
            サイトの楽しみ方
          </UiButton>
        </div>
      </div>

      <div class="home-hero__side">
        <TopAiCard @open-ai="emit('open-ai')" />
        <div class="home-hero__anniversary" aria-label="芸能生活80周年記念">
          <div class="home-hero__anniversary-ring">
            <span class="home-hero__anniversary-num">80</span>
            <span class="home-hero__anniversary-unit">周年</span>
          </div>
          <p class="home-hero__anniversary-text">芸能生活<br />80周年<br />記念サイト</p>
        </div>
      </div>
    </div>
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

.home-hero__overlay {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.06) 0%,
    rgba(255, 255, 255, 0.02) 22%,
    transparent 38%
  );
}

.home-hero__inner {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: minmax(280px, 1fr) minmax(280px, 360px);
  gap: var(--sp-7);
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--sp-8) var(--sp-6);
  min-height: inherit;
}

.home-hero__copy {
  position: relative;
  padding: 28px 24px 28px 0;
}

.home-hero__copy::before {
  content: '';
  position: absolute;
  z-index: -1;
  inset: -24px 8px -24px -32px;
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

.home-hero__side {
  display: flex;
  flex-direction: column;
  gap: var(--sp-5);
  align-items: stretch;
  justify-self: end;
  width: 100%;
  max-width: 360px;
}

.home-hero__anniversary {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid var(--kin-500);
  border-radius: var(--site-radius-md);
  box-shadow: var(--site-shadow);
  align-self: flex-end;
}

.home-hero__anniversary-ring {
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

.home-hero__anniversary-num {
  font-family: var(--ff-latin);
  font-size: 24px;
  font-weight: 700;
  color: var(--kin-600);
  line-height: 1;
}

.home-hero__anniversary-unit {
  font-family: var(--ff-mincho);
  font-size: 10px;
  color: var(--kin-600);
}

.home-hero__anniversary-text {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 11px;
  line-height: 1.65;
  letter-spacing: 0.08em;
  color: var(--site-text-muted);
}

@media (max-width: 1100px) {
  .home-hero__inner {
    grid-template-columns: 1fr;
    gap: var(--sp-7);
    padding-top: var(--sp-7);
    padding-bottom: var(--sp-7);
  }
  .home-hero__side {
    justify-self: center;
    max-width: 420px;
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
    padding: 20px 0;
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
  .home-hero__side {
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
  }
}
</style>
