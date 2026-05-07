<script setup>
/**
 * 部品名: ページ見出し（大字＋欧文サブタイトル）
 * 用途: 各固定ページのタイトルブロック
 */
defineProps({
  kanji: String,
  title: String,
  sub: String,
})
</script>

<template>
  <header :style="{ marginBottom: '48px' }">
    <div :style="{ display: 'flex', alignItems: 'baseline', gap: '20px' }">
      <span
        :style="{
          fontFamily: 'var(--ff-mincho)',
          fontSize: '72px',
          fontWeight: 800,
          color: 'var(--beni-500)',
          lineHeight: 1,
        }"
      >{{ kanji }}</span>
      <div>
        <h1
          :style="{
            fontFamily: 'var(--ff-mincho)',
            fontSize: '34px',
            margin: 0,
            letterSpacing: '0.08em',
          }"
        >{{ title }}</h1>
        <div
          :style="{
            fontFamily: 'var(--ff-latin)',
            fontStyle: 'italic',
            fontSize: '13px',
            color: 'var(--kin-500)',
            marginTop: '5px',
            letterSpacing: '0.2em',
          }"
        >{{ sub }}</div>
      </div>
    </div>
    <hr class="hr-double" :style="{ marginTop: '20px', borderColor: 'var(--kin-500)' }" />
  </header>
</template>
