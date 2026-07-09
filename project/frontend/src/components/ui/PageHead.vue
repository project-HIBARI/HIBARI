<script setup>
/**
 * 部品名: ページ見出し（大字＋欧文サブタイトル）
 * 用途: 各固定ページのタイトルブロック（ライトテーマ）
 */
defineProps({
  kanji: String,
  title: String,
  sub: String,
  /** light: ライト背景 / legacy: ダーク領域（思い出・献花） */
  tone: { type: String, default: 'light' },
})
</script>

<template>
  <header class="page-head motion-page-title" :class="`page-head--${tone}`">
    <div class="page-head__row">
      <span class="page-head__kanji">{{ kanji }}</span>
      <div>
        <h1 class="page-head__title">{{ title }}</h1>
        <div class="page-head__sub">{{ sub }}</div>
      </div>
    </div>
    <hr class="page-head__rule" />
  </header>
</template>

<style scoped>
.page-head {
  margin-bottom: 48px;
}
.page-head__row {
  display: flex;
  align-items: baseline;
  gap: 20px;
}
.page-head__kanji {
  font-family: var(--ff-mincho);
  font-size: 72px;
  font-weight: 800;
  line-height: 1;
}
.page-head__title {
  font-family: var(--ff-mincho);
  font-size: 34px;
  margin: 0;
  letter-spacing: 0.08em;
}
.page-head__sub {
  font-family: var(--ff-latin);
  font-style: italic;
  font-size: 13px;
  margin-top: 5px;
  letter-spacing: 0.2em;
}
.page-head__rule {
  margin-top: 20px;
  border: 0;
  height: 4px;
  border-top: 1px solid var(--kin-500);
  border-bottom: 1px solid var(--kin-500);
}
.page-head--light .page-head__kanji {
  color: var(--murasaki-500);
}
.page-head--light .page-head__title {
  color: var(--site-text);
}
.page-head--light .page-head__sub {
  color: var(--kin-600);
}
.page-head--legacy .page-head__kanji {
  color: var(--beni-500);
}
.page-head--legacy .page-head__title {
  color: var(--paper-100);
}
.page-head--legacy .page-head__sub {
  color: var(--kin-500);
}

@media (max-width: 767px) {
  .page-head {
    margin-bottom: 28px;
  }
  .page-head__row {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  .page-head__kanji {
    font-size: clamp(40px, 14vw, 72px);
  }
  .page-head__title {
    font-size: clamp(22px, 6vw, 34px);
  }
  .page-head__sub {
    font-size: 11px;
    letter-spacing: 0.12em;
  }
  .page-head__rule {
    margin-top: 14px;
  }
}
</style>
