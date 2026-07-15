<script setup>
/**
 * 部品名: 思い出 — ヒーローエリア
 * 用途: ページ冒頭のコピー・肖像・AIカードを表示する（歩み／ゆかりの地と同レイアウト）
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

      <div class="memories-hero__aside">
        <div class="memories-hero__visual">
          <img
            :src="heroImg"
            alt=""
            class="memories-hero__photo"
            width="360"
            decoding="async"
          />
        </div>

        <div class="memories-hero__ai">
          <TopAiCard @open-ai="emit('open-ai')" />
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.memories-hero {
  position: relative;
  margin-bottom: var(--sp-7);
  padding: var(--sp-7) var(--sp-5);
  border-radius: var(--site-radius-lg);
  overflow: hidden;
  min-height: 380px;
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
  display: flex;
  align-items: center;
  gap: var(--sp-6);
  z-index: 1;
}
.memories-hero__copy {
  flex: 1 1 auto;
  min-width: 240px;
  max-width: 400px;
}
.memories-hero__eyebrow {
  margin: 0 0 10px;
  font-family: var(--ff-latin);
  font-size: var(--font-size-caption);
  letter-spacing: 0.28em;
  color: var(--kin-600);
}
.memories-hero__title {
  margin: 0 0 10px;
  font-family: var(--ff-mincho);
  font-size: clamp(2rem, 4vw, 2.625rem);
  font-weight: 800;
  letter-spacing: 0.1em;
  color: var(--site-text);
  line-height: 1.2;
}
.memories-hero__subtitle {
  margin: 0 0 14px;
  font-family: var(--ff-mincho);
  font-size: clamp(0.9375rem, 1.6vw, 1.125rem);
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--murasaki-700);
  line-height: 1.5;
}
.memories-hero__desc {
  margin: 0 0 var(--sp-5);
  font-size: var(--font-size-button);
  line-height: 1.85;
  color: var(--site-text-muted);
}
.memories-hero__scroll {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--ff-latin);
  font-size: var(--font-size-badge);
  letter-spacing: 0.3em;
  color: var(--kin-600);
}
.memories-hero__scroll-line {
  display: block;
  width: 1px;
  height: 32px;
  background: linear-gradient(180deg, var(--kin-500), transparent);
}
.memories-hero__aside {
  display: flex;
  align-items: stretch;
  gap: var(--sp-4);
  flex: 0 1 auto;
  min-width: 0;
  max-width: 100%;
  margin-left: auto;
}
.memories-hero__visual {
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
.memories-hero__photo {
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
.memories-hero__ai {
  display: flex;
  flex: 0 1 320px;
  width: min(320px, 100%);
  max-width: 320px;
  min-width: 0;
}
.memories-hero__ai :deep(.top-ai-card) {
  width: 100%;
  max-width: none;
  height: 100%;
}

@media (max-width: 1023px) {
  .memories-hero__inner {
    flex-direction: column;
    align-items: stretch;
  }

  .memories-hero__copy {
    max-width: none;
  }

  .memories-hero__aside {
    flex-direction: column;
    margin-left: 0;
    order: 2;
    align-items: stretch;
  }

  .memories-hero__visual {
    width: 100%;
    max-width: 360px;
    min-height: 280px;
    margin: 0 auto;
    align-self: center;
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

  .memories-hero__ai {
    width: 100%;
    max-width: none;
    flex-basis: auto;
  }

  .memories-hero__scroll {
    display: none;
  }
}
</style>
