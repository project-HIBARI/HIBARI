<script setup>
/**
 * 部品名: 献花ページ — ヒーローセクション
 * 用途: タイトル・説明・献花統計カード（ダミーデータ）
 */
import { pageImageUrl, PAGE_IMAGES, PAGE_HERO_IMAGE } from '../../../lib/pageImages.js'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'

/** 背景・装飾画像（差し替えは pageImages.js を参照） */
const HERO_ASSETS = {
  background: '/images/message/hero-placeholder.jpg',
  lily: '/images/login/yuri-white.png',
  flowers: pageImageUrl(PAGE_IMAGES.about),
  portrait: pageImageUrl(PAGE_HERO_IMAGE),
}

const statCards = [
  {
    title: 'これまでの献花数',
    count: '128,456',
    unit: '件',
    desc: 'サイト開設以来、全国のファンの皆さまから寄せられた献花とメッセージの総数です。',
    buttonLabel: '献花を見る',
    variant: 'primary',
  },
  {
    title: '今月の献花',
    count: '5,842',
    unit: '件',
    desc: '今月お寄せいただいた献花の件数です。日々の感謝が、静かに積み重なっています。',
    buttonLabel: '今月の献花を見る',
    variant: 'outline',
  },
]
</script>

<template>
  <section class="msg-hero" aria-labelledby="message-hero-title">
    <div class="msg-hero__bg" aria-hidden="true">
      <img :src="HERO_ASSETS.background" alt="" class="msg-hero__bg-photo" decoding="async" />
      <img :src="HERO_ASSETS.lily" alt="" class="msg-hero__deco msg-hero__deco--lily" decoding="async" />
      <img :src="HERO_ASSETS.flowers" alt="" class="msg-hero__deco msg-hero__deco--flowers" decoding="async" />
      <img :src="HERO_ASSETS.portrait" alt="" class="msg-hero__deco msg-hero__deco--portrait" decoding="async" />
      <div class="msg-hero__overlay" />
    </div>

    <div class="msg-hero__inner">
      <div class="msg-hero__copy">
        <p class="msg-hero__icon" aria-hidden="true">
          <UiIco name="flower" :size="20" color="var(--murasaki-600)" />
        </p>
        <h1 id="message-hero-title" class="msg-hero__title">献花</h1>
        <p class="msg-hero__subtitle">美空ひばりへの感謝と想いを花に託して。</p>
        <div class="msg-hero__desc">
          <p>1963年より、美空ひばりへの感謝と想いを花と言葉で綴り続けてきた場所です。</p>
          <p>誕生日・不死鳥忌の記念日をはじめ、いつでもあなたの想いを添えることができます。</p>
          <p>全国のファンの皆さまが紡いできた、やさしい献花の記録をご覧ください。</p>
        </div>
      </div>

      <div class="msg-hero__cards">
        <article v-for="(card, i) in statCards" :key="i" class="msg-hero__card">
          <h2 class="msg-hero__card-title">{{ card.title }}</h2>
          <p class="msg-hero__card-count">
            <span class="msg-hero__card-num">{{ card.count }}</span>
            <span class="msg-hero__card-unit">{{ card.unit }}</span>
          </p>
          <hr class="hr-gold msg-hero__card-rule" />
          <p class="msg-hero__card-desc">{{ card.desc }}</p>
          <UiButton :variant="card.variant" size="md" class="msg-hero__card-btn">
            {{ card.buttonLabel }}
          </UiButton>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.msg-hero {
  position: relative;
  margin: 0 auto var(--sp-7);
  max-width: 1200px;
  border-radius: var(--site-radius-lg);
  overflow: hidden;
  border: 1px solid var(--site-border);
  box-shadow: var(--site-shadow-md);
}

.msg-hero__bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.msg-hero__bg-photo {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.35;
  filter: grayscale(0.15) sepia(0.08);
}

.msg-hero__deco {
  position: absolute;
  object-fit: contain;
  pointer-events: none;
  filter: drop-shadow(var(--site-shadow));
}

.msg-hero__deco--lily {
  left: 4%;
  bottom: 8%;
  width: min(22vw, 180px);
  opacity: 0.55;
}

.msg-hero__deco--flowers {
  right: 38%;
  top: 6%;
  width: min(18vw, 140px);
  opacity: 0.42;
  transform: rotate(-8deg);
}

.msg-hero__deco--portrait {
  right: 6%;
  bottom: 0;
  width: min(24vw, 220px);
  opacity: 0.28;
  filter: grayscale(0.2) sepia(0.12);
}

.msg-hero__overlay {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(
      105deg,
      color-mix(in srgb, var(--site-surface) 92%, transparent) 0%,
      color-mix(in srgb, var(--site-bg-warm) 88%, transparent) 42%,
      color-mix(in srgb, var(--murasaki-100) 82%, transparent) 100%
    ),
    radial-gradient(
      ellipse at 18% 80%,
      color-mix(in srgb, var(--site-bg-pink) 45%, transparent) 0%,
      transparent 55%
    ),
    radial-gradient(
      ellipse at 72% 20%,
      color-mix(in srgb, var(--murasaki-100) 35%, transparent) 0%,
      transparent 50%
    );
}

.msg-hero__inner {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr);
  gap: var(--sp-7);
  align-items: center;
  padding: var(--sp-8) var(--sp-7);
}

.msg-hero__copy {
  max-width: 520px;
}

.msg-hero__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  margin: 0 0 var(--sp-4);
  border-radius: 50%;
  background: var(--murasaki-100);
  border: 1px solid var(--site-border);
}

.msg-hero__title {
  margin: 0 0 var(--sp-3);
  font-family: var(--ff-mincho);
  font-size: clamp(2.5rem, 4.8vw, 3.5rem);
  font-weight: 800;
  letter-spacing: 0.14em;
  line-height: 1.15;
  color: var(--murasaki-800);
}

.msg-hero__subtitle {
  margin: 0 0 var(--sp-5);
  font-family: var(--ff-mincho);
  font-size: clamp(1rem, 1.8vw, 1.25rem);
  font-weight: 700;
  letter-spacing: 0.08em;
  line-height: 1.65;
  color: var(--murasaki-700);
}

.msg-hero__desc {
  display: flex;
  flex-direction: column;
  gap: var(--sp-3);
}

.msg-hero__desc p {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-button);
  line-height: 2;
  letter-spacing: 0.04em;
  color: var(--site-text-muted);
}

.msg-hero__cards {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--sp-5);
  width: 100%;
  justify-self: end;
}

.msg-hero__card {
  text-align: center;
  padding: var(--sp-6) var(--sp-5);
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--site-border);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
}

.msg-hero__card-title {
  margin: 0 0 var(--sp-3);
  font-family: var(--ff-mincho);
  font-size: var(--font-size-body);
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--site-text);
}

.msg-hero__card-count {
  margin: 0;
  line-height: 1.1;
}

.msg-hero__card-num {
  font-family: var(--ff-mincho);
  font-size: clamp(2.125rem, 4vw, 2.75rem);
  font-weight: 800;
  letter-spacing: 0.04em;
  color: var(--murasaki-700);
}

.msg-hero__card-unit {
  margin-left: 4px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-emphasis);
  font-weight: 700;
  color: var(--site-text-muted);
}

.msg-hero__card-rule {
  margin: var(--sp-4) auto;
  width: 56px;
}

.msg-hero__card-desc {
  margin: 0 0 var(--sp-5);
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  line-height: 1.85;
  letter-spacing: 0.03em;
  color: var(--site-text-light);
}

.msg-hero__card-btn {
  width: 100%;
}

@media (max-width: 768px) {
  .msg-hero {
    margin-bottom: var(--sp-6);
  }

  .msg-hero__inner {
    grid-template-columns: 1fr;
    gap: var(--sp-6);
    padding: var(--sp-6) var(--sp-5);
  }

  .msg-hero__copy {
    max-width: none;
  }

  .msg-hero__cards {
    grid-template-columns: 1fr;
    justify-self: stretch;
  }

  .msg-hero__deco--lily {
    width: 120px;
    opacity: 0.35;
  }

  .msg-hero__deco--flowers {
    width: 90px;
    right: 8%;
    opacity: 0.28;
  }

  .msg-hero__deco--portrait {
    width: 140px;
    opacity: 0.18;
  }

  .msg-hero__title {
    font-size: clamp(2.125rem, 9vw, 2.75rem);
  }

  .msg-hero__subtitle {
    font-size: var(--font-size-body);
  }

  .msg-hero__desc p {
    font-size: var(--font-size-caption);
    line-height: 1.9;
  }

  .msg-hero__card {
    padding: var(--sp-5) var(--sp-4);
  }
}
</style>
