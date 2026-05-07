<script setup>
/**
 * 部品名: 献花 — 寄せられたメッセージ一覧
 */
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const flowers = ['白百合', '紅薔薇', '白菊', 'かすみ草', '桔梗', '小手毬']
const flowerEmoji = ['🌸', '🌹', '🌼', '🌿', '🔔', '🍃']

function emojiFor(flower) {
  const i = flowers.indexOf(flower)
  return i >= 0 ? flowerEmoji[i] : '🌸'
}
</script>

<template>
  <div>
    <h3 style="font-family: var(--ff-mincho); font-size: 20px; margin: 0 0 20px">寄せられたメッセージ</h3>
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px">
      <div
        v-for="(m, i) in HIBARU_DATA.messages"
        :key="i"
        style="background: rgba(250,245,234,0.03); border: 1px solid rgba(201,169,97,0.2); padding: 20px; display: grid; grid-template-columns: 36px 1fr; gap: 14px"
      >
        <div style="padding-top: 4px"><span style="font-size: 24px">{{ emojiFor(m.flower) }}</span></div>
        <div>
          <div style="font-size: 14px; line-height: 1.9; color: var(--paper-100)">{{ m.body }}</div>
          <div style="margin-top: 10px; font-size: 11px; color: var(--paper-300); letter-spacing: 0.1em">
            — {{ m.name }} · {{ m.location }} · {{ m.flower }} · <span style="font-family: var(--ff-mono)">{{ m.date }}</span>
          </div>
        </div>
      </div>
    </div>
    <div style="margin-top: 32px; padding: 16px 0; border-top: 1px solid rgba(201,169,97,0.2)">
      <div style="font-family: var(--ff-mincho); font-size: 13px; color: var(--paper-300); letter-spacing: 0.15em">
        年別アーカイブ：
        <button
          v-for="y in [2024, 2023, 2022, 2021, 2020]"
          :key="y"
          type="button"
          style="background: transparent; border: 1px solid rgba(201,169,97,0.3); color: var(--paper-300); padding: 4px 12px; cursor: pointer; font-family: var(--ff-mono); font-size: 11px; margin-left: 8px"
        >
          {{ y }}年
        </button>
      </div>
    </div>
  </div>
</template>
