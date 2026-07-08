<script setup>
/**
 * 部品名: ホーム — ヒーローエリア
 * 用途: 全幅背景動画・コピー・CTA
 */
import UiButton from '../../ui/UiButton.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const emit = defineEmits(['open-auth', 'scroll-enjoy'])

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
  }
}
</style>
