<script setup>
/**
 * 部品名: トップ — 3 枚のショートカットカード（曲・憶・花）
 */
const emit = defineEmits(['navigate'])

const cards = [
  { k: '曲', t: 'ディスコグラフィ', d: '実在の楽曲13作。作詞・作曲者、レコード大賞受賞歴を収録。', to: 'disco' },
  { k: '憶', t: '思い出掲示板', d: '「あの公演を観た」「あの歌に救われた」——ファンの証言の集い。', to: 'memories' },
  { k: '花', t: '献花・メッセージ', d: '誕生日・不死鳥忌に、想いをお寄せください。', to: 'message' },
]
</script>

<template>
  <section style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; margin-bottom: 80px" aria-label="コンテンツ一覧">
    <button
      v-for="(c, i) in cards"
      :key="i"
      type="button"
      style="background: rgba(201,169,97,0.05); border: 1px solid rgba(201,169,97,0.3); padding: 32px 28px; text-align: left; cursor: pointer; color: var(--paper-100); display: flex; flex-direction: column; gap: 12px"
      :aria-label="c.t + 'ページへ'"
      @click="emit('navigate', c.to)"
      @mouseenter="(e) => (e.currentTarget.style.background = 'rgba(201,169,97,0.12)')"
      @mouseleave="(e) => (e.currentTarget.style.background = 'rgba(201,169,97,0.05)')"
    >
      <div style="font-family: var(--ff-mincho); font-size: 52px; font-weight: 800; color: var(--beni-500); line-height: 1">{{ c.k }}</div>
      <div style="font-family: var(--ff-mincho); font-size: 19px; font-weight: 700; letter-spacing: 0.1em">{{ c.t }}</div>
      <div style="font-size: 13px; line-height: 1.9; color: var(--paper-300)">{{ c.d }}</div>
      <div style="margin-top: 8px; font-size: 11px; color: var(--kin-500); letter-spacing: 0.2em">見る ›</div>
    </button>
  </section>
</template>
