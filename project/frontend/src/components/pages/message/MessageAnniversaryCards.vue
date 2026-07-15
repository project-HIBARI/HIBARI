<script setup>
/**
 * 部品名: 献花ページ — 誕生日／不死鳥忌カード
 */
import { daysUntil } from '../../../utils/hibaru.js'
import { aosAttrs } from '../../../lib/aos.js'

const daysBd = daysUntil(5, 29)
const daysMem = daysUntil(6, 24)

const cards = [
  {
    en: 'BIRTHDAY',
    jp: '誕生日',
    date: '五月二十九日',
    days: daysBd,
    active: daysBd < daysMem,
    count: '1,482',
    status: daysBd < daysMem ? '開設中' : `あと${daysBd}日`,
  },
  {
    en: 'FUSHICHŌ MEMORIAL',
    jp: '不死鳥忌',
    date: '六月二十四日',
    days: daysMem,
    active: daysMem <= daysBd,
    count: daysMem <= daysBd ? '3,201' : '—',
    status: daysMem <= daysBd ? '開設中' : `あと${daysMem}日`,
  },
]
</script>

<template>
  <section class="msg-anniv" aria-label="記念日の献花">
    <article
      v-for="(s, i) in cards"
      :key="i"
      class="msg-anniv__card"
      :class="{ 'msg-anniv__card--active': s.active }"
      v-bind="aosAttrs(i * 100)"
    >
      <div class="msg-anniv__en">{{ s.en }}</div>
      <div class="msg-anniv__date">{{ s.date }}</div>
      <div class="msg-anniv__jp">{{ s.jp }}</div>
      <hr class="hr-gold msg-anniv__rule" />
      <div class="msg-anniv__count">
        献花 <span class="msg-anniv__count-num">{{ s.count }}</span> 件 · {{ s.status }}
      </div>
      <div v-if="!s.active" class="msg-anniv__days">
        {{ s.days }}<span class="msg-anniv__days-unit"> 日後</span>
      </div>
    </article>
  </section>
</template>

<style scoped>
.msg-anniv {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--sp-6);
  margin-bottom: var(--sp-7);
}

.msg-anniv__card {
  text-align: center;
  padding: var(--sp-7) var(--sp-6);
  border-radius: 24px;
  border: 1px solid color-mix(in srgb, var(--site-border) 85%, transparent);
  background: color-mix(in srgb, var(--site-surface) 70%, transparent);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 10px 32px rgba(59, 47, 42, 0.05);
  transition: transform 0.35s ease, box-shadow 0.35s ease;
}

.msg-anniv__card:hover {
  transform: translateY(-3px);
  box-shadow: 0 16px 40px rgba(59, 47, 42, 0.08);
}

.msg-anniv__card--active {
  background:
    radial-gradient(ellipse at 50% 0%, rgba(252, 232, 236, 0.55) 0%, transparent 60%),
    color-mix(in srgb, var(--site-surface) 75%, transparent);
  border-color: color-mix(in srgb, var(--kin-500) 45%, var(--site-border));
}

.msg-anniv__en {
  font-family: var(--ff-latin);
  font-size: var(--font-size-caption);
  letter-spacing: 0.4em;
  color: var(--kin-600);
}

.msg-anniv__date {
  font-family: var(--ff-mincho);
  font-size: clamp(2rem, 6vw, 3rem);
  font-weight: 800;
  margin: 12px 0 6px;
  letter-spacing: 0.04em;
  color: var(--site-text);
}

.msg-anniv__jp {
  font-size: var(--font-size-button);
  color: var(--site-text-muted);
}

.msg-anniv__rule {
  margin: 20px auto;
  width: 60px;
}

.msg-anniv__count {
  font-family: var(--ff-mono);
  font-size: var(--font-size-caption);
  color: var(--site-text-light);
  letter-spacing: 0.2em;
}

.msg-anniv__count-num {
  color: var(--kin-600);
  font-size: var(--font-size-small);
}

.msg-anniv__days {
  margin-top: 12px;
  font-family: var(--ff-latin);
  font-size: 3rem;
  font-weight: 700;
  color: var(--murasaki-600);
  line-height: 1;
}

.msg-anniv__days-unit {
  font-size: var(--font-size-small);
  font-family: var(--ff-mincho);
}

@media (max-width: 640px) {
  .msg-anniv {
    grid-template-columns: 1fr;
  }
}
</style>
