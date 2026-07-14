<script setup>
/**
 * 部品名: 思い出 — ヒーローエリア
 * 用途: ページ冒頭のコピー・肖像・AIカード・80周年バッジを表示する
 */
import { pageImageUrl, PROFILE_HERO_IMAGE } from '../../../lib/pageImages.js'
import TopAiCard from '../top/TopAiCard.vue'

const heroImg = pageImageUrl(PROFILE_HERO_IMAGE)

const emit = defineEmits(['open-ai'])
</script>

<template>
  <section class="memories-hero" aria-label="思い出紹介">
    <div class="memories-hero__bg" aria-hidden="true" />

    <div class="memories-hero__inner">
      <div class="memories-hero__copy">
        <p class="memories-hero__eyebrow">MEMORIES · MISORA HIBARI</p>
        <h1 class="memories-hero__title">思い出</h1>
        <p class="memories-hero__subtitle">歌とともに歩んだ、美空ひばりの軌跡。</p>
        <p class="memories-hero__desc">
          舞台の輝き、銀幕の名場面、ファンの心に残る歌声。<br />
          美空ひばりの思い出を、写真と証言とともにたどります。
        </p>

        <p class="memories-hero__scroll" aria-hidden="true">
          <span class="memories-hero__scroll-line" />
          SCROLL
        </p>
      </div>

      <div class="memories-hero__visual">
        <img
          :src="heroImg"
          alt=""
          class="memories-hero__photo"
          width="360"
          decoding="async"
        />
      </div>

      <div class="memories-hero__side">
        <div class="memories-hero__ai">
          <TopAiCard @open-ai="emit('open-ai')" />
        </div>
        <div class="memories-hero__anniversary" aria-label="芸能生活80周年記念">
          <div class="memories-hero__anniversary-ring">
            <span class="memories-hero__anniversary-num">80</span>
            <span class="memories-hero__anniversary-unit">周年</span>
          </div>
          <p class="memories-hero__anniversary-text">芸能生活<br />80周年<br />記念サイト</p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.memories-hero {
  position: relative;
  margin-bottom: var(--sp-7);
  padding: var(--sp-6) var(--sp-5);
  border-radius: var(--site-radius-lg);
  overflow: hidden;
}
.memories-hero__bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 15% 40%, rgba(252, 232, 236, 0.85) 0%, transparent 50%),
    radial-gradient(ellipse at 85% 30%, rgba(245, 235, 224, 0.7) 0%, transparent 45%),
    repeating-radial-gradient(circle at 90% 80%, rgba(201, 169, 97, 0.06) 0 1px, transparent 1px 24px),
    linear-gradient(135deg, var(--site-bg-warm) 0%, var(--site-bg-pink) 50%, var(--site-surface-muted) 100%);
  border: 1px solid var(--site-border);
}
.memories-hero__inner {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px auto;
  gap: var(--sp-6);
  align-items: stretch;
  min-width: 0;
}
.memories-hero__copy {
  align-self: center;
  min-width: 0;
}
.memories-hero__eyebrow {
  margin: 0 0 10px;
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.28em;
  color: var(--kin-600);
}
.memories-hero__title {
  margin: 0 0 14px;
  font-family: var(--ff-mincho);
  font-size: clamp(28px, 3.5vw, 38px);
  font-weight: 800;
  letter-spacing: 0.06em;
  color: var(--site-text);
  line-height: 1.3;
  white-space: nowrap;
}
.memories-hero__subtitle {
  margin: 0 0 14px;
  font-family: var(--ff-mincho);
  font-size: clamp(15px, 1.6vw, 18px);
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--murasaki-700);
  line-height: 1.5;
  white-space: nowrap;
}
.memories-hero__desc {
  margin: 0 0 var(--sp-5);
  font-size: 13px;
  line-height: 1.85;
  color: var(--site-text-muted);
}
.memories-hero__scroll {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--ff-latin);
  font-size: 10px;
  letter-spacing: 0.3em;
  color: var(--kin-600);
}
.memories-hero__scroll-line {
  display: block;
  width: 1px;
  height: 32px;
  background: linear-gradient(180deg, var(--kin-500), transparent);
}
.memories-hero__visual {
  position: relative;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  align-self: stretch;
  overflow: hidden;
}
.memories-hero__photo {
  display: block;
  width: 360px;
  height: 100%;
  object-fit: contain;
  object-position: left bottom;
  transform: scale(1.18);
  transform-origin: left bottom;
  filter: drop-shadow(var(--site-shadow-md));
}
.memories-hero__side {
  display: flex;
  flex-direction: row;
  gap: var(--sp-4);
  align-items: stretch;
  align-self: stretch;
}
.memories-hero__ai {
  display: flex;
  width: 320px;
  flex-shrink: 0;
}
.memories-hero__ai :deep(.top-ai-card) {
  width: 100%;
  max-width: none;
  height: 100%;
}
.memories-hero__anniversary {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid var(--kin-500);
  border-radius: var(--site-radius-md);
  box-shadow: var(--site-shadow);
  flex-shrink: 0;
  align-self: flex-end;
}
.memories-hero__anniversary-ring {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: 2px solid var(--kin-500);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle, #fff 0%, var(--site-surface-muted) 100%);
  flex-shrink: 0;
}
.memories-hero__anniversary-num {
  font-family: var(--ff-latin);
  font-size: 20px;
  font-weight: 700;
  color: var(--kin-600);
  line-height: 1;
}
.memories-hero__anniversary-unit {
  font-family: var(--ff-mincho);
  font-size: 9px;
  color: var(--kin-600);
}
.memories-hero__anniversary-text {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 10px;
  line-height: 1.6;
  letter-spacing: 0.08em;
  color: var(--site-text-muted);
  white-space: nowrap;
}

@media (max-width: 1024px) {
  .memories-hero__inner {
    grid-template-columns: 1fr;
    gap: var(--sp-7);
  }
  .memories-hero__subtitle {
    font-size: clamp(13px, 3.6vw, 17px);
    letter-spacing: 0.03em;
  }
  .memories-hero__side {
    flex-direction: column;
    align-items: stretch;
    justify-content: center;
  }
  .memories-hero__anniversary {
    align-self: flex-start;
  }
  .memories-hero__ai {
    width: 100%;
    max-width: none;
  }
  .memories-hero__visual {
    order: -1;
    min-height: 280px;
  }
  .memories-hero__photo {
    width: 100%;
    max-width: 360px;
    height: 100%;
    min-height: 280px;
    object-position: left bottom;
    transform: scale(1.12);
    transform-origin: left bottom;
  }
  .memories-hero__scroll {
    display: none;
  }
}
</style>
