<script setup>
/**
 * 部品名: 思い出ページ — 交流イベントカード群
 */
import { HIBARU_DATA } from '../../../data/hibaruData.js'
import { btnBeni, btnGhost } from '../../../utils/hibaru.js'

const eventTypes = {
  nodojiman: { label: 'のど自慢', color: 'var(--beni-700)' },
  karaoke: { label: 'カラオケ', color: '#3a5a8a' },
  tour: { label: 'ゆかりの地ツアー', color: '#4a6a3a' },
  photo: { label: 'フォトコンテスト', color: '#6a4a8a' },
}
</script>

<template>
  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; margin-top: 24px">
    <div
      v-for="ev in HIBARU_DATA.events"
      :key="ev.id"
      style="border: 1px solid rgba(201,169,97,0.25); padding: 28px; background: rgba(201,169,97,0.03)"
    >
      <div style="display: flex; gap: 8px; margin-bottom: 14px; flex-wrap: wrap">
        <span
          :style="{
            fontSize: '10px',
            background: (eventTypes[ev.type] || { color: 'var(--ink-500)' }).color,
            color: 'var(--paper-50)',
            padding: '3px 10px',
            letterSpacing: '0.15em',
            fontFamily: 'var(--ff-mincho)',
          }"
          >{{ (eventTypes[ev.type] || { label: ev.type }).label }}</span
        >
        <span
          v-if="ev.partner"
          style="font-size: 10px; border: 1px solid rgba(201,169,97,0.4); color: var(--kin-500); padding: 3px 8px; letter-spacing: 0.1em; font-family: var(--ff-mincho)"
          >{{ ev.partner }}</span
        >
      </div>
      <div style="font-family: var(--ff-mincho); font-size: 18px; font-weight: 700; margin-bottom: 12px">{{ ev.title }}</div>
      <div style="display: grid; grid-template-columns: 60px 1fr; gap: 6px 12px; font-size: 13px; color: var(--paper-200)">
        <span style="color: var(--kin-500); font-family: var(--ff-mincho)">日時</span><span>{{ ev.date }}</span>
        <span style="color: var(--kin-500); font-family: var(--ff-mincho)">会場</span><span>{{ ev.place }}</span>
        <span style="color: var(--kin-500); font-family: var(--ff-mincho)">定員</span><span>{{ ev.capacity }}</span>
        <span style="color: var(--kin-500); font-family: var(--ff-mincho)">料金</span><span>{{ ev.fee }}</span>
      </div>
      <div style="display: flex; gap: 10px; margin-top: 20px; flex-wrap: wrap">
        <button type="button" :style="{ ...btnBeni, fontSize: '12px', padding: '10px 20px' }">申し込む</button>
        <button type="button" :style="{ ...btnGhost, fontSize: '12px', padding: '10px 16px' }">縁ページへ ›</button>
      </div>
    </div>
  </div>
</template>
