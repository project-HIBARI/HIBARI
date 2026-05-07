<script setup>
/**
 * 部品名: グッズ案内モーダル
 */
import ModalShell from './ModalShell.vue'
import { btnBeni } from '../../utils/hibaru.js'

const emit = defineEmits(['close'])

const goods = [
  { title: '川の流れのように 37周年記念盤', type: 'CD', price: '¥3,300', member: '¥2,970 (会員10%OFF)' },
  { title: '美空ひばり 公式フォトブック 2024', type: '書籍', price: '¥4,400', member: '¥3,960 (会員10%OFF)' },
  { title: '不死鳥コンサート Blu-ray', type: 'BD', price: '¥8,800', member: '¥7,920 (会員10%OFF)' },
]
</script>

<template>
  <ModalShell title="✦ グッズ" @close="emit('close')">
    <div style="display: flex; flex-direction: column; gap: 16px">
      <div
        v-for="(g, i) in goods"
        :key="i"
        style="display: grid; grid-template-columns: 80px 1fr auto; gap: 16px; align-items: center; border: 1px solid rgba(201,169,97,0.25); padding: 20px"
      >
        <div
          style="width: 80px; height: 80px; background: rgba(201,169,97,0.08); display: flex; align-items: center; justify-content: center; border: 1px solid rgba(201,169,97,0.2); font-family: var(--ff-mono); font-size: 10px; color: var(--kin-500); text-align: center"
        >
          {{ g.type }}
        </div>
        <div>
          <div style="font-family: var(--ff-mincho); font-size: 15px; font-weight: 700; margin-bottom: 6px">{{ g.title }}</div>
          <div style="font-family: var(--ff-mono); font-size: 13px; color: var(--paper-200)">{{ g.price }}</div>
          <div style="font-size: 11px; color: var(--kin-500); margin-top: 3px">✦ {{ g.member }}</div>
        </div>
        <button type="button" :style="{ ...btnBeni, fontSize: '11px', padding: '10px 16px', whiteSpace: 'nowrap' }">購入</button>
      </div>
    </div>
    <p style="font-size: 12px; color: var(--paper-300); line-height: 1.8; margin-top: 16px">
      ※ 実際の購入は
      <a href="http://misorahibari-shop.com" target="_blank" rel="noopener noreferrer" style="color: var(--kin-500)">公式ショッピングサイト</a>
      をご利用ください。
    </p>
  </ModalShell>
</template>
