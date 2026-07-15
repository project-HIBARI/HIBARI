<script setup>
/**
 * 部品名: 献花 — ヒーローエリア（3カラム）
 * 用途: コピー・肖像・献花統計カードを表示する
 */
import { computed } from 'vue'
import { pageImageUrl, PROFILE_HERO_IMAGE } from '../../../lib/pageImages.js'
import { useCountUp } from '../../../composables/useCountUp.js'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'

const props = defineProps({
  totalCount: { type: Number, default: 128456 },
  monthlyCount: { type: Number, default: 5842 },
})

const emit = defineEmits(['open-offer', 'scroll-wall'])

const heroImg = pageImageUrl(PROFILE_HERO_IMAGE)

const totalDisplay = useCountUp(() => props.totalCount)
const monthlyDisplay = useCountUp(() => props.monthlyCount)

const statCards = computed(() => [
  {
    title: 'これまでの献花数',
    count: totalDisplay.value.toLocaleString(),
    unit: '件',
    desc: 'たくさんの想いをありがとうございます。',
    buttonLabel: '献花を見る',
    variant: 'primary',
    action: 'scroll',
  },
  {
    title: '今月の献花',
    count: monthlyDisplay.value.toLocaleString(),
    unit: '件',
    desc: '今月もたくさんの想いが寄せられています。',
    buttonLabel: '今月の献花を見る',
    variant: 'outline',
    action: 'scroll',
  },
])

function onCardAction(action) {
  if (action === 'scroll') emit('scroll-wall')
}
</script>

<template>
  <section class="msg-hero" aria-labelledby="message-hero-title">
    <div class="msg-hero__bg" aria-hidden="true" />

    <div class="msg-hero__inner">
      <div class="msg-hero__copy">
        <p class="msg-hero__eyebrow">FLOWER OFFERING · MISORA HIBARI</p>
        <div class="msg-hero__title-row">
          <h1 id="message-hero-title" class="msg-hero__title">献花</h1>
          <span class="msg-hero__title-icon" aria-hidden="true">
            <UiIco name="flower" :size="22" color="var(--murasaki-600)" />
          </span>
        </div>
        <p class="msg-hero__subtitle">美空ひばりへの感謝と想いを花に託して。</p>
        <p class="msg-hero__desc">
          いつでも、どこからでも、あなたの想いを届けることができます。<br />
          花とメッセージを添えて、美空ひばりへの感謝を表しましょう。<br />
          みなさんの想いが、未来へと歌い継がれていきます。
        </p>
        <UiButton
          variant="gold"
          size="md"
          class="msg-hero__cta"
          aria-label="献花する"
          @click="emit('open-offer')"
        >
          献花する
        </UiButton>
        <p class="msg-hero__scroll" aria-hidden="true">
          <span class="msg-hero__scroll-line" />
          SCROLL
        </p>
      </div>

      <div class="msg-hero__visual">
        <img
          :src="heroImg"
          alt=""
          class="msg-hero__photo"
          width="360"
          decoding="async"
        />
      </div>

      <div class="msg-hero__stats">
        <article
          v-for="(card, i) in statCards"
          :key="i"
          class="msg-hero__card"
        >
          <h2 class="msg-hero__card-title">{{ card.title }}</h2>
          <p class="msg-hero__card-count" aria-live="polite">
            <span class="msg-hero__card-icon" aria-hidden="true">🌸</span>
            <span class="msg-hero__card-num">{{ card.count }}</span>
            <span class="msg-hero__card-unit">{{ card.unit }}</span>
          </p>
          <hr class="hr-gold msg-hero__card-rule" />
          <p class="msg-hero__card-desc">{{ card.desc }}</p>
          <UiButton
            :variant="card.variant"
            size="md"
            class="msg-hero__card-btn"
            @click="onCardAction(card.action)"
          >
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
  margin-bottom: var(--sp-7);
  padding: var(--sp-6) var(--sp-5);
  border-radius: var(--site-radius-lg);
  overflow: hidden;
}

.msg-hero__bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 15% 40%, rgba(252, 232, 236, 0.85) 0%, transparent 50%),
    radial-gradient(ellipse at 85% 30%, rgba(245, 235, 224, 0.7) 0%, transparent 45%),
    radial-gradient(ellipse at 50% 100%, rgba(201, 169, 97, 0.12) 0%, transparent 55%),
    repeating-radial-gradient(circle at 90% 80%, rgba(201, 169, 97, 0.06) 0 1px, transparent 1px 24px),
    linear-gradient(135deg, var(--site-bg-warm) 0%, var(--site-bg-pink) 50%, var(--site-surface-muted) 100%);
  border: 1px solid var(--site-border);
}

.msg-hero__inner {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 360px) minmax(0, 1fr);
  gap: var(--sp-6);
  align-items: stretch;
  min-width: 0;
}

.msg-hero__copy {
  align-self: center;
  min-width: 0;
}

.msg-hero__eyebrow {
  margin: 0 0 10px;
  font-family: var(--ff-latin);
  font-size: var(--font-size-caption);
  letter-spacing: 0.28em;
  color: var(--kin-600);
}

.msg-hero__title-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

.msg-hero__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: clamp(2rem, 4vw, 2.75rem);
  font-weight: 800;
  letter-spacing: 0.12em;
  color: var(--murasaki-800);
  line-height: 1.2;
}

.msg-hero__title-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--murasaki-100);
  border: 1px solid var(--site-border);
}

.msg-hero__subtitle {
  margin: 0 0 14px;
  font-family: var(--ff-mincho);
  font-size: clamp(0.9375rem, 1.6vw, 1.125rem);
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--murasaki-700);
  line-height: 1.55;
}

.msg-hero__desc {
  margin: 0 0 var(--sp-5);
  font-size: var(--font-size-button);
  line-height: 1.9;
  color: var(--site-text-muted);
}

.msg-hero__cta {
  margin-bottom: var(--sp-5);
}

.msg-hero__scroll {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--ff-latin);
  font-size: var(--font-size-badge);
  letter-spacing: 0.3em;
  color: var(--kin-600);
}

.msg-hero__scroll-line {
  display: block;
  width: 1px;
  height: 32px;
  background: linear-gradient(180deg, var(--kin-500), transparent);
}

.msg-hero__visual {
  position: relative;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  align-self: stretch;
  overflow: hidden;
}

.msg-hero__photo {
  display: block;
  width: 100%;
  max-width: 360px;
  height: 100%;
  object-fit: contain;
  object-position: center bottom;
  transform: scale(1.14);
  transform-origin: center bottom;
  filter: drop-shadow(var(--site-shadow-md));
}

.msg-hero__stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--sp-4);
  align-self: center;
  min-width: 0;
}

.msg-hero__card {
  text-align: center;
  padding: var(--sp-5) var(--sp-4);
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--site-border);
  background: color-mix(in srgb, var(--site-surface) 88%, transparent);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: var(--site-shadow);
}

.msg-hero__card-title {
  margin: 0 0 var(--sp-3);
  font-family: var(--ff-mincho);
  font-size: var(--font-size-button);
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--site-text);
}

.msg-hero__card-count {
  margin: 0;
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 6px;
  line-height: 1.1;
}

.msg-hero__card-icon {
  font-size: var(--font-size-emphasis);
}

.msg-hero__card-num {
  font-family: var(--ff-mincho);
  font-size: clamp(1.625rem, 3vw, 2.125rem);
  font-weight: 800;
  letter-spacing: 0.02em;
  color: var(--murasaki-700);
}

.msg-hero__card-unit {
  font-family: var(--ff-mincho);
  font-size: var(--font-size-small);
  font-weight: 700;
  color: var(--site-text-muted);
}

.msg-hero__card-rule {
  margin: var(--sp-3) auto;
  width: 48px;
}

.msg-hero__card-desc {
  margin: 0 0 var(--sp-4);
  font-size: var(--font-size-caption);
  line-height: 1.75;
  color: var(--site-text-light);
}

.msg-hero__card-btn {
  width: 100%;
}

@media (max-width: 1023px) {
  .msg-hero__inner {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--sp-7);
  }

  .msg-hero__visual {
    order: -1;
    min-height: 280px;
    min-width: 0;
  }

  .msg-hero__photo {
    width: 100%;
    max-width: 360px;
    min-height: 280px;
    transform: scale(1.1);
    margin-inline: auto;
  }

  .msg-hero__stats {
    order: 1;
    width: 100%;
  }

  .msg-hero__scroll {
    display: none;
  }
}

@media (max-width: 640px) {
  .msg-hero__stats {
    grid-template-columns: 1fr;
  }
}
</style>
