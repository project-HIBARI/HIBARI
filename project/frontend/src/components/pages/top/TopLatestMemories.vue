<script setup>
/**
 * 部品名: トップ — 新着思い出プレビュー
 */
import { HIBARU_DATA } from '../../../data/hibaruData.js'
import { btnGhost } from '../../../utils/hibaru.js'

const emit = defineEmits(['navigate'])

const preview = HIBARU_DATA.memories.slice(0, 3)
</script>

<template>
  <section style="margin-bottom: 32px">
    <div style="font-family: var(--ff-latin); font-size: 11px; letter-spacing: 0.3em; color: var(--kin-500); margin-bottom: 8px">LATEST</div>
    <h2 style="font-family: var(--ff-mincho); font-size: 26px; margin: 0 0 28px; letter-spacing: 0.08em">新着の思い出</h2>
    <div style="display: flex; flex-direction: column; gap: 14px">
      <div v-for="m in preview" :key="m.id" style="border-left: 2px solid var(--beni-500); padding: 4px 0 4px 18px">
        <div style="font-family: var(--ff-mincho); font-size: 16px; font-weight: 700">{{ m.title }}</div>
        <div style="font-size: 12px; color: var(--paper-300); margin-top: 4px">
          {{ m.author }}（{{ m.age }}歳・{{ m.location }}）· <span style="color: var(--kin-500)">♪ {{ m.song }}</span>
        </div>
      </div>
    </div>
    <button type="button" :style="{ ...btnGhost, marginTop: '20px', fontSize: '12px' }" @click="emit('navigate', 'memories')">すべての思い出を見る ›</button>
  </section>
</template>
