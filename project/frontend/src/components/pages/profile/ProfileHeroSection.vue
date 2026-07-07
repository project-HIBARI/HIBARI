<script setup>
/**
 * 部品名: 歩み — ヒーローエリア
 * 用途: ページ冒頭のタイトル・紹介文・肖像・桜装飾・AI導線を表示する
 */
import { pageImageUrl, PAGE_HERO_IMAGE } from '../../../lib/pageImages.js'
import TopAiCard from '../top/TopAiCard.vue'

const emit = defineEmits(['open-ai'])

const heroImg = pageImageUrl(PAGE_HERO_IMAGE)
</script>

<template>
  <!-- 歩みページのファーストビュー（デザイン準拠のヒーロー） -->
  <section class="profile-hero" aria-label="歩み紹介">
    <div class="profile-hero__bg" aria-hidden="true">
      <img :src="heroImg" alt="" class="profile-hero__photo" />
      <div class="profile-hero__sakura">
        <span v-for="n in 6" :key="n" class="profile-hero__petal" :class="`profile-hero__petal--${n}`" />
      </div>
    </div>

    <div class="profile-hero__inner">
      <div class="profile-hero__copy">
        <p class="profile-hero__eyebrow">PROFILE · MISORA HIBARI</p>
        <h1 class="profile-hero__title">歩み</h1>
        <p class="profile-hero__sub">美空ひばりプロフィール</p>
        <p class="profile-hero__desc">
          1937年横浜生まれ。8歳で初舞台を踏み、昭和歌謡を代表する存在として<br />
          五十二年の生涯を歌とともに歩みました。
        </p>
      </div>

      <TopAiCard @open-ai="emit('open-ai')" />
    </div>
  </section>
</template>

<style scoped>
.profile-hero {
  position: relative;
  margin-bottom: var(--sp-7);
  padding: var(--sp-7) var(--sp-5);
  border-radius: var(--site-radius-lg);
  overflow: hidden;
  min-height: 320px;
}
.profile-hero__bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 55% 40%, rgba(252, 232, 236, 0.5) 0%, transparent 55%),
    linear-gradient(135deg, var(--site-bg-warm) 0%, var(--site-bg-pink) 45%, var(--site-surface-muted) 100%);
  border: 1px solid var(--site-border);
}
.profile-hero__photo {
  position: absolute;
  right: 28%;
  top: 50%;
  transform: translateY(-50%);
  width: min(38%, 280px);
  height: auto;
  aspect-ratio: 4 / 5;
  object-fit: cover;
  border-radius: var(--site-radius-lg);
  opacity: 0.22;
  filter: grayscale(0.85) sepia(0.15);
  pointer-events: none;
}
.profile-hero__sakura {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}
.profile-hero__petal {
  position: absolute;
  width: 10px;
  height: 10px;
  background: radial-gradient(circle, #f8c8d4 0%, #e8a0b0 100%);
  border-radius: 50% 0 50% 50%;
  opacity: 0.45;
  transform: rotate(45deg);
}
.profile-hero__petal--1 { top: 12%; left: 18%; }
.profile-hero__petal--2 { top: 28%; left: 42%; opacity: 0.3; transform: rotate(20deg) scale(0.8); }
.profile-hero__petal--3 { top: 8%; right: 35%; opacity: 0.35; }
.profile-hero__petal--4 { bottom: 22%; left: 28%; opacity: 0.25; transform: rotate(-15deg); }
.profile-hero__petal--5 { bottom: 15%; right: 42%; opacity: 0.3; transform: rotate(60deg) scale(0.7); }
.profile-hero__petal--6 { top: 45%; left: 8%; opacity: 0.2; transform: rotate(-30deg) scale(0.6); }
.profile-hero__inner {
  position: relative;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--sp-6);
  align-items: start;
  z-index: 1;
}
.profile-hero__copy {
  max-width: 520px;
}
.profile-hero__eyebrow {
  margin: 0 0 var(--sp-3);
  font-family: var(--ff-latin);
  font-style: italic;
  font-size: 11px;
  letter-spacing: 0.28em;
  color: var(--kin-600);
}
.profile-hero__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: clamp(36px, 4vw, 48px);
  font-weight: 800;
  letter-spacing: 0.12em;
  color: var(--site-text);
  line-height: 1.2;
}
.profile-hero__sub {
  margin: var(--sp-3) 0 var(--sp-4);
  font-family: var(--ff-mincho);
  font-size: 16px;
  letter-spacing: 0.08em;
  color: var(--murasaki-700);
}
.profile-hero__desc {
  margin: 0;
  font-size: 13px;
  line-height: 2;
  color: var(--site-text-muted);
  letter-spacing: 0.04em;
}

@media (max-width: 900px) {
  .profile-hero__inner {
    grid-template-columns: 1fr;
  }
  .profile-hero__photo {
    right: 10%;
    width: min(50%, 200px);
    opacity: 0.15;
  }
}
</style>
