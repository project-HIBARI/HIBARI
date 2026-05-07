<script setup>
/**
 * 部品名: ゆかりの地 — 一覧＋詳細パネル
 */
import { HIBARU_DATA } from '../../../data/hibaruData.js'

defineProps({
  selected: { type: Object, required: true },
})

const emit = defineEmits(['select'])
</script>

<template>
  <div>
    <div style="display: flex; flex-direction: column; gap: 2px; max-height: 580px; overflow-y: auto">
      <button
        v-for="(p, i) in HIBARU_DATA.places"
        :key="p.id"
        type="button"
        :style="{
          textAlign: 'left',
          padding: '13px 16px',
          background: selected.id === p.id ? 'var(--beni-800)' : 'rgba(201,169,97,0.04)',
          border: '1px solid rgba(201,169,97,0.22)',
          borderLeft: selected.id === p.id ? '3px solid var(--kin-500)' : '3px solid transparent',
          color: 'var(--paper-100)',
          cursor: 'pointer',
          display: 'grid',
          gridTemplateColumns: '28px 1fr auto',
          gap: '10px',
          alignItems: 'center',
        }"
        :aria-pressed="selected.id === p.id"
        :aria-label="p.name"
        @click="emit('select', p)"
      >
        <span
          :style="{
            fontFamily: 'var(--ff-latin)',
            fontSize: '15px',
            fontWeight: 700,
            color: selected.id === p.id ? 'var(--kin-500)' : 'var(--paper-300)',
          }"
          >{{ String(i + 1).padStart(2, '0') }}</span
        >
        <div>
          <div style="font-family: var(--ff-mincho); font-size: 14px; font-weight: 700">{{ p.name }}</div>
          <div style="font-size: 11px; color: var(--paper-300); margin-top: 2px">{{ p.area }}</div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 4px; align-items: flex-end">
          <span
            v-if="p.visitable"
            style="font-size: 9px; color: #4a9; border: 1px solid #4a9; padding: 2px 5px; letter-spacing: 0.1em"
            >見学可</span
          >
          <span v-else style="font-size: 9px; color: var(--beni-500); border: 1px solid var(--beni-500); padding: 2px 5px; letter-spacing: 0.1em">閉館</span>
        </div>
      </button>
    </div>
    <div style="margin-top: 16px; padding: 20px; background: rgba(139,26,26,0.15); border: 1px solid var(--beni-700)">
      <div style="font-family: var(--ff-mincho); font-size: 17px; font-weight: 700">{{ selected.name }}</div>
      <div style="font-size: 12px; color: var(--kin-500); margin-top: 4px; letter-spacing: 0.1em">{{ selected.area }}</div>
      <p style="font-size: 13px; line-height: 1.9; color: var(--paper-200); margin-top: 10px; margin-bottom: 0">{{ selected.note }}</p>
      <div
        v-if="selected.id === 'kinenkan'"
        style="margin-top: 12px; padding: 12px; background: rgba(201,169,97,0.08); border: 1px solid rgba(201,169,97,0.3); font-size: 12px; color: var(--paper-200); line-height: 1.8"
      >
        <div style="color: var(--kin-500); font-family: var(--ff-mincho); font-weight: 700; margin-bottom: 6px">🗓 イベント情報</div>
        <div>4月29日《春と恋・愛のフィルムコンサート》</div>
        <div>10:30〜12:00 / 13:30〜15:00 · 料金: ¥3,000（要予約）</div>
        <div style="margin-top: 6px">TEL: 03-5422-3358</div>
      </div>
    </div>
  </div>
</template>
