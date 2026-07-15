<script setup>
/**
 * 部品名: 歩み — ヒーローエリア
 * 用途: ページ冒頭のタイトル・紹介文・肖像・桜装飾・AI導線を表示する
 */
import { pageImageUrl, PROFILE_HERO_IMAGE } from '../../../lib/pageImages.js'
import TopAiCard from '../top/TopAiCard.vue'

const emit = defineEmits(['open-ai'])

const heroImg = pageImageUrl(PROFILE_HERO_IMAGE)
</script>

<template>
  <!-- 歩みページのファーストビュー（デザイン準拠のヒーロー） -->
  <section class="profile-hero" aria-label="歩み紹介">
    <div class="profile-hero__bg" aria-hidden="true">
      <div class="profile-hero__sakura">
        <span v-for="n in 6" :key="n" class="profile-hero__petal" :class="`profile-hero__petal--${n}`" />
      </div>
    </div>

    <div class="profile-hero__inner">
      <div class="profile-hero__copy">
        <p class="profile-hero__eyebrow">PROFILE · MISORA HIBARI</p>
        <div class="profile-hero__title-row">
          <h1 class="profile-hero__title">歩み</h1>
          <p class="profile-hero__sub">美空ひばりプロフィール</p>
        </div>
        <p class="profile-hero__desc">
          1937年横浜生まれ。8歳で初舞台を踏み、昭和歌謡を代表する存在として<br />
          五十二年の生涯を歌とともに歩みました。
        </p>
      </div>

      <div class="profile-hero__aside">
        <div class="profile-hero__visual">
          <img
            :src="heroImg"
            alt=""
            class="profile-hero__photo"
            width="360"
            decoding="async"
          />
        </div>

        <div class="profile-hero__ai">
          <TopAiCard @open-ai="emit('open-ai')" />
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.profile-hero {
  position: relative;
  margin-bottom: var(--sp-7);
  padding: var(--sp-7) var(--sp-6);
  border-radius: var(--site-radius-lg);
  overflow: hidden;
  min-height: 380px;
}
.profile-hero__bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 55% 40%, rgba(252, 232, 236, 0.5) 0%, transparent 55%),
    linear-gradient(135deg, var(--site-bg-warm) 0%, var(--site-bg-pink) 45%, var(--site-surface-muted) 100%);
  border: 1px solid var(--site-border);
}
.profile-hero__visual {
  flex: 0 1 360px;
  width: min(360px, 100%);
  max-width: 360px;
  min-width: 0;
  align-self: stretch;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  overflow: hidden;
}
.profile-hero__photo {
  display: block;
  width: 100%;
  max-width: 360px;
  height: 100%;
  object-fit: contain;
  object-position: left bottom;
  transform: scale(1.18);
  transform-origin: left bottom;
  filter: drop-shadow(var(--site-shadow-md));
}
.profile-hero__aside {
  display: flex;
  align-items: stretch;
  gap: var(--sp-4);
  flex: 0 1 auto;
  min-width: 0;
  max-width: 100%;
  margin-left: auto;
}
.profile-hero__ai {
  display: flex;
  flex: 0 1 320px;
  width: min(320px, 100%);
  max-width: 320px;
  min-width: 0;
}
.profile-hero__ai :deep(.top-ai-card) {
  width: 100%;
  max-width: none;
  height: 100%;
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
  display: flex;
  align-items: center;
  gap: var(--sp-6);
  z-index: 1;
}
.profile-hero__copy {
  flex: 1 1 auto;
  min-width: 0;
  max-width: 400px;
}
.profile-hero__title-row {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: var(--sp-3) var(--sp-4);
  margin-bottom: var(--sp-4);
}
.profile-hero__eyebrow {
  margin: 0 0 var(--sp-3);
  font-family: var(--ff-latin);
  font-style: italic;
  font-size: var(--font-size-caption);
  letter-spacing: 0.28em;
  color: var(--kin-600);
}
.profile-hero__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: clamp(2.5rem, 4.2vw, 3.25rem);
  font-weight: 800;
  letter-spacing: 0.12em;
  color: var(--site-text);
  line-height: 1.1;
}
.profile-hero__sub {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: clamp(0.9375rem, 1.6vw, 1.125rem);
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--murasaki-700);
  white-space: nowrap;
}
.profile-hero__desc {
  margin: 0;
  font-size: var(--font-size-button);
  line-height: 2;
  color: var(--site-text-muted);
  letter-spacing: 0.04em;
}

@media (max-width: 1023px) {
  .profile-hero__inner {
    flex-direction: column;
    align-items: stretch;
  }

  .profile-hero__copy {
    max-width: none;
  }

  .profile-hero__title-row {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--sp-2);
  }

  .profile-hero__sub {
    white-space: normal;
  }

  .profile-hero__aside {
    flex-direction: column;
    margin-left: 0;
    order: 2;
    align-items: stretch;
  }

  .profile-hero__visual {
    width: 100%;
    max-width: 360px;
    min-height: 280px;
    margin: 0 auto;
    align-self: center;
  }

  .profile-hero__photo {
    width: 100%;
    max-width: 360px;
    height: 100%;
    min-height: 280px;
    object-position: left bottom;
    transform: scale(1.12);
    transform-origin: left bottom;
  }

  .profile-hero__ai {
    width: 100%;
    max-width: none;
    flex-basis: auto;
  }
}
</style>
