<script setup>
/**
 * 部品名: トップ — ニュースティッカー
 */
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const items = [...HIBARU_DATA.news, ...HIBARU_DATA.news]
</script>

<template>
  <div
    style="overflow: hidden; border-top: 1px solid rgba(201,169,97,0.25); border-bottom: 1px solid rgba(201,169,97,0.25); padding: 10px 0; margin-bottom: 64px; background: rgba(10,6,4,0.5)"
  >
    <div
      style="display: flex; gap: 48px; animation: ticker 30s linear infinite; white-space: nowrap; font-family: var(--ff-mincho); font-size: 13px; color: var(--paper-200); letter-spacing: 0.1em"
    >
      <span v-for="(n, i) in items" :key="i" style="flex-shrink: 0">
        <span style="color: var(--kin-500); margin-right: 12px; font-family: var(--ff-mono); font-size: 11px">{{ n.date }}</span>
        {{ n.title }}
        <span style="margin: 0 24px; opacity: 0.3">◆</span>
      </span>
    </div>
  </div>
</template>
