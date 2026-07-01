<script setup>
/**
 * 部品名: ホーム — ヒーローエリア
 * 用途: メインコピー・CTA・ビジュアル・AIカード・80周年バッジを表示する
 */
import heroImg from '../../../assets/hero.png'
import UiButton from '../../ui/UiButton.vue'
import TopAiCard from './TopAiCard.vue'

const emit = defineEmits(['open-auth', 'scroll-enjoy', 'open-ai'])
</script>

<template>
  <!-- ファーストビューとして表示するホーム用ヒーロー -->
  <section class="home-hero" aria-label="メインビジュアル">
    <div class="home-hero__bg" aria-hidden="true" />

    <div class="home-hero__inner">
      <div class="home-hero__copy">
        <p class="home-hero__eyebrow">MISORA HIBARI OFFICIAL FAN SITE</p>
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

      <div class="home-hero__visual">
        <div class="home-hero__visual-frame">
          <img :src="heroImg" alt="美空ひばり" class="home-hero__photo" />
          <div class="home-hero__mic" aria-hidden="true" />
          <div class="home-hero__polaroids" aria-hidden="true">
            <span class="home-hero__polaroid home-hero__polaroid--1" />
            <span class="home-hero__polaroid home-hero__polaroid--2" />
            <span class="home-hero__polaroid home-hero__polaroid--3" />
          </div>
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
  margin: 0 0 var(--sp-8);
  padding: var(--sp-7) var(--sp-5);
  border-radius: var(--site-radius-lg);
  overflow: hidden;
}
.home-hero__bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 20% 30%, rgba(252, 232, 236, 0.9) 0%, transparent 55%),
    radial-gradient(ellipse at 80% 20%, rgba(245, 235, 224, 0.8) 0%, transparent 50%),
    linear-gradient(135deg, var(--site-bg-warm) 0%, var(--site-bg-pink) 40%, var(--site-surface-muted) 100%);
  border: 1px solid var(--site-border);
  border-radius: inherit;
}
.home-hero__inner {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 1.1fr auto;
  gap: var(--sp-6);
  align-items: center;
}
.home-hero__copy {
  z-index: 1;
}
.home-hero__eyebrow {
  margin: 0 0 var(--sp-4);
  font-family: var(--ff-latin);
  font-style: italic;
  font-size: 12px;
  letter-spacing: 0.28em;
  color: var(--kin-600);
}
.home-hero__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: clamp(28px, 3.2vw, 42px);
  font-weight: 800;
  line-height: 1.45;
  letter-spacing: 0.06em;
  color: var(--site-text);
}
.home-hero__sub {
  margin: var(--sp-5) 0 0;
  font-size: 14px;
  line-height: 2;
  color: var(--site-text-muted);
  letter-spacing: 0.04em;
}
.home-hero__cta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: var(--sp-6);
}
.home-hero__visual {
  position: relative;
  display: flex;
  justify-content: center;
}
.home-hero__visual-frame {
  position: relative;
  width: min(100%, 340px);
}
.home-hero__photo {
  width: 100%;
  height: auto;
  display: block;
  border-radius: var(--site-radius-lg);
  border: 3px solid rgba(255, 255, 255, 0.9);
  box-shadow: var(--site-shadow-md);
  object-fit: cover;
  aspect-ratio: 4 / 5;
}
.home-hero__mic {
  position: absolute;
  bottom: 12%;
  left: -8%;
  width: 48px;
  height: 120px;
  background: linear-gradient(180deg, #c8c8c8 0%, #888 40%, #666 100%);
  border-radius: 24px 24px 8px 8px;
  box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.15);
}
.home-hero__mic::before {
  content: '';
  position: absolute;
  top: 8px;
  left: 50%;
  transform: translateX(-50%);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: repeating-radial-gradient(circle, #555 0 2px, #777 2px 4px);
  border: 2px solid #999;
}
.home-hero__polaroids {
  position: absolute;
  top: -8%;
  right: -12%;
  width: 120px;
  height: 140px;
}
.home-hero__polaroid {
  position: absolute;
  width: 64px;
  height: 76px;
  background: #fff;
  border: 1px solid var(--site-border);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.home-hero__polaroid::after {
  content: '';
  position: absolute;
  top: 6px;
  left: 6px;
  right: 6px;
  bottom: 18px;
  background: linear-gradient(135deg, var(--site-bg-pink), var(--site-surface-muted));
}
.home-hero__polaroid--1 {
  top: 0;
  right: 0;
  transform: rotate(8deg);
}
.home-hero__polaroid--2 {
  top: 24px;
  right: 36px;
  transform: rotate(-6deg);
}
.home-hero__polaroid--3 {
  top: 48px;
  right: 8px;
  transform: rotate(4deg);
}
.home-hero__side {
  display: flex;
  flex-direction: column;
  gap: var(--sp-5);
  align-items: flex-end;
}
.home-hero__anniversary {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid var(--kin-500);
  border-radius: var(--site-radius-md);
  box-shadow: var(--site-shadow);
}
.home-hero__anniversary-ring {
  width: 64px;
  height: 64px;
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
  font-size: 22px;
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
  line-height: 1.6;
  letter-spacing: 0.08em;
  color: var(--site-text-muted);
}

@media (max-width: 1024px) {
  .home-hero__inner {
    grid-template-columns: 1fr;
    gap: var(--sp-7);
  }
  .home-hero__side {
    flex-direction: row;
    flex-wrap: wrap;
    align-items: stretch;
    justify-content: center;
  }
  .home-hero__visual {
    order: -1;
  }
}

@media (max-width: 767px) {
  .home-hero {
    padding: var(--sp-5) var(--sp-4);
    margin-bottom: var(--sp-6);
  }
  .home-hero__mic,
  .home-hero__polaroids {
    display: none;
  }
  .home-hero__side {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
