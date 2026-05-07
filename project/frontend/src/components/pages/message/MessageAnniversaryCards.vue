<script setup>
/**
 * 部品名: 献花ページ — 誕生日／不死鳥忌カード
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
  <section style="display: grid; grid-template-columns: 1fr 1fr; gap: 32px; margin-bottom: 56px">
    <div
      v-for="(s, i) in cards"
      :key="i"
      :style="{
        background: s.active ? 'linear-gradient(180deg,rgba(139,26,26,0.35),rgba(139,26,26,0.1))' : 'rgba(201,169,97,0.03)',
        border: `1px solid ${s.active ? 'var(--kin-500)' : 'var(--beni-700)'}`,
        padding: '40px 36px',
        textAlign: 'center',
      }"
    >
      <div
        :style="{
          fontFamily: 'var(--ff-latin)',
          fontSize: '11px',
          letterSpacing: '0.4em',
          color: s.active ? 'var(--kin-500)' : 'var(--beni-500)',
        }"
      >
        {{ s.en }}
      </div>
      <div style="font-family: var(--ff-mincho); font-size: 48px; font-weight: 800; margin: 12px 0 6px; letter-spacing: 0.04em">{{ s.date }}</div>
      <div style="font-size: 13px; color: var(--paper-200)">{{ s.jp }}</div>
      <hr class="hr-gold" style="margin: 20px auto; width: 60px" />
      <div style="font-family: var(--ff-mono); font-size: 11px; color: var(--paper-300); letter-spacing: 0.2em">
        献花 <span style="color: var(--kin-500); font-size: 14px">{{ s.count }}</span> 件 · {{ s.status }}
      </div>
      <div
        v-if="!s.active"
        style="margin-top: 12px; font-family: var(--ff-latin); font-size: 48px; font-weight: 700; color: var(--beni-500); line-height: 1"
      >
        {{ s.days }}<span style="font-size: 14px; font-family: var(--ff-mincho)"> 日後</span>
      </div>
    </div>
  </section>
</template>
