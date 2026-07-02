<script setup>
/**
 * 部品名: 献花ページ — 誕生日／不死鳥忌カード
 * 用途: 献花ページ上部で記念日カード2枚を表示する
 */
import { daysUntil } from '../../../utils/hibaru.js'

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
  <section class="msg-anniv">
    <article
      v-for="(s, i) in cards"
      :key="i"
      class="msg-anniv__card"
      :class="{ 'msg-anniv__card--active': s.active }"
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
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--site-border);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
}
.msg-anniv__card--active {
  background: linear-gradient(135deg, var(--site-bg-pink) 0%, var(--site-surface) 100%);
  border-color: var(--kin-500);
}
.msg-anniv__en {
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.4em;
  color: var(--kin-600);
}
.msg-anniv__date {
  font-family: var(--ff-mincho);
  font-size: clamp(32px, 6vw, 48px);
  font-weight: 800;
  margin: 12px 0 6px;
  letter-spacing: 0.04em;
  color: var(--site-text);
}
.msg-anniv__jp {
  font-size: 13px;
  color: var(--site-text-muted);
}
.msg-anniv__rule {
  margin: 20px auto;
  width: 60px;
}
.msg-anniv__count {
  font-family: var(--ff-mono);
  font-size: 11px;
  color: var(--site-text-light);
  letter-spacing: 0.2em;
}
.msg-anniv__count-num {
  color: var(--kin-600);
  font-size: 14px;
}
.msg-anniv__days {
  margin-top: 12px;
  font-family: var(--ff-latin);
  font-size: 48px;
  font-weight: 700;
  color: var(--murasaki-600);
  line-height: 1;
}
.msg-anniv__days-unit {
  font-size: 14px;
  font-family: var(--ff-mincho);
}

@media (max-width: 480px) {
  .msg-anniv {
    grid-template-columns: 1fr;
  }
}
</style>
