<script setup>
/**
 * 部品名: ファンクラブ案内モーダル
 */
import ModalShell from './ModalShell.vue'
import { btnBeni } from '../../utils/hibaru.js'

const emit = defineEmits(['close'])

const plans = [
  {
    name: '一般会員',
    price: '¥500 / 月',
    features: ['月刊ニュースレター', 'チケット先行予約', '掲示板投稿', '月10回AIひばり対話'],
    locked: ['限定コンテンツ', 'AI新曲制作支援', '優先申込'],
  },
  {
    name: 'プレミアム会員',
    price: '¥1,500 / 月',
    features: ['上記すべて', 'プレミアム限定映像', '限定コンテンツ', 'AI新曲制作支援', 'AIひばり無制限', '優先申込 + 割引'],
    locked: [],
  },
]
</script>

<template>
  <ModalShell title="✦ ファンクラブ" @close="emit('close')">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px">
      <div
        v-for="(p, i) in plans"
        :key="p.name"
        :style="{
          border: `1px solid ${i === 1 ? 'var(--kin-500)' : 'rgba(201,169,97,0.3)'}`,
          padding: '24px',
          background: i === 1 ? 'rgba(201,169,97,0.06)' : 'transparent',
          position: 'relative',
        }"
      >
        <div
          v-if="i === 1"
          style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: var(--kin-500); color: var(--sumi); padding: 2px 14px; font-family: var(--ff-mincho); font-size: 11px; font-weight: 700"
        >
          おすすめ
        </div>
        <div style="font-family: var(--ff-mincho); font-size: 17px; font-weight: 700; margin-bottom: 4px">{{ p.name }}</div>
        <div style="font-family: var(--ff-latin); font-size: 24px; font-weight: 700; color: var(--kin-500); margin-bottom: 16px">{{ p.price }}</div>
        <ul style="list-style: none; padding: 0; margin: 0">
          <li
            v-for="f in p.features"
            :key="f"
            style="font-size: 12px; color: var(--paper-200); padding: 4px 0; border-bottom: 1px solid rgba(201,169,97,0.1)"
          >
            ✓ {{ f }}
          </li>
          <li
            v-for="f in p.locked"
            :key="'l' + f"
            style="font-size: 12px; color: var(--paper-400); padding: 4px 0; border-bottom: 1px solid rgba(201,169,97,0.08); text-decoration: line-through; opacity: 0.5"
          >
            🔒 {{ f }}
          </li>
        </ul>
        <button type="button" :style="{ ...btnBeni, width: '100%', justifyContent: 'center', marginTop: '20px', fontSize: '12px' }">入会する</button>
      </div>
    </div>
    <p style="font-size: 12px; color: var(--paper-300); line-height: 1.8">
      ※ 決済はプレースホルダーです。詳細は公式サイト（misorahibari.com）の
      <a href="https://www.misorahibari.com/fanclub.html" target="_blank" rel="noopener noreferrer" style="color: var(--kin-500)">ファンクラブページ</a>
      をご確認ください。
    </p>
  </ModalShell>
</template>
