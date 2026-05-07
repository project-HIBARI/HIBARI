<script setup>
/**
 * 部品名: トップ — 今日の一曲 ＋ 記念日カウントダウン
 */
import RecordChip from '../../ui/RecordChip.vue'
import { daysUntil, btnGhost } from '../../../utils/hibaru.js'

defineProps({
  song: { type: Object, required: true },
})

const emit = defineEmits(['navigate'])

const daysBd = daysUntil(5, 29)
const daysMem = daysUntil(6, 24)
const closer =
  daysBd <= daysMem
    ? { label: '誕生日', date: '五月二十九日', days: daysBd }
    : { label: '不死鳥忌', date: '六月二十四日', days: daysMem }
</script>

<template>
  <section style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 48px; margin-bottom: 80px" class="two-col">
    <div style="border: 1px solid rgba(201,169,97,0.3); padding: 32px">
      <div style="font-family: var(--ff-latin); font-size: 11px; letter-spacing: 0.3em; color: var(--kin-500); margin-bottom: 8px">TODAY'S SONG</div>
      <div style="font-family: var(--ff-mincho); font-size: 22px; font-weight: 700; margin-bottom: 20px">今日の一曲</div>
      <div style="display: flex; align-items: center; gap: 24px">
        <RecordChip :no="song.no" color="var(--beni-700)" />
        <div>
          <div style="font-family: var(--ff-mono); font-size: 10px; color: var(--kin-500); letter-spacing: 0.2em">
            {{ song.year }} · {{ song.no }}
          </div>
          <div style="font-family: var(--ff-mincho); font-size: 26px; font-weight: 700; margin: 6px 0 2px">{{ song.title }}</div>
          <div style="font-family: var(--ff-latin); font-style: italic; font-size: 12px; color: var(--paper-300)">{{ song.romaji }}</div>
          <div style="font-size: 12px; color: var(--paper-300); margin-top: 8px">作詞：{{ song.lyric }} / 作曲：{{ song.music }}</div>
          <div v-if="song.note" style="font-size: 12px; color: var(--paper-200); margin-top: 6px">{{ song.note }}</div>
        </div>
      </div>
    </div>
    <div style="background: rgba(139,26,26,0.2); border: 1px solid var(--beni-700); padding: 32px">
      <div style="font-family: var(--ff-latin); font-size: 11px; letter-spacing: 0.3em; color: var(--kin-500); margin-bottom: 8px">ANNIVERSARY</div>
      <div style="font-family: var(--ff-mincho); font-size: 20px; font-weight: 700; margin-bottom: 20px">{{ closer.label }}まで</div>
      <div style="display: flex; align-items: baseline; gap: 12px; margin-bottom: 12px">
        <span style="font-family: var(--ff-latin); font-size: 80px; font-weight: 700; color: var(--beni-500); line-height: 1">{{ closer.days }}</span>
        <span style="font-family: var(--ff-mincho); font-size: 20px">日</span>
      </div>
      <div style="font-family: var(--ff-mincho); font-size: 16px; color: var(--paper-200); margin-bottom: 20px; letter-spacing: 0.2em">{{ closer.date }}</div>
      <div style="display: flex; gap: 12px; font-size: 12px; color: var(--paper-300); font-family: var(--ff-mono)">
        <span>誕生日 5/29 → あと {{ daysBd }}日</span>
        <span style="opacity: 0.4">|</span>
        <span>不死鳥忌 6/24 → あと {{ daysMem }}日</span>
      </div>
      <button type="button" :style="{ ...btnGhost, marginTop: '20px', fontSize: '12px' }" @click="emit('navigate', 'message')">記帳所へ ›</button>
    </div>
  </section>
</template>
