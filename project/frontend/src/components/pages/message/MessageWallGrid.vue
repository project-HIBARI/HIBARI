<script setup>
/**
 * 部品名: 献花 — 寄せられたメッセージ一覧
 * 用途: 献花ページで寄せられたメッセージをカード一覧で表示する
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
  <section class="msg-wall">
    <h3 class="msg-wall__title">寄せられたメッセージ</h3>
    <div class="msg-wall__grid">
      <article v-for="(m, i) in HIBARU_DATA.messages" :key="i" class="msg-wall__card">
        <div class="msg-wall__emoji" aria-hidden="true">{{ emojiFor(m.flower) }}</div>
        <div>
          <p class="msg-wall__body">{{ m.body }}</p>
          <p class="msg-wall__meta">
            — {{ m.name }} · {{ m.location }} · {{ m.flower }} · <span class="msg-wall__date">{{ m.date }}</span>
          </p>
        </div>
      </article>
    </div>
    <footer class="msg-wall__archive">
      <span class="msg-wall__archive-label">年別アーカイブ：</span>
      <button v-for="y in [2024, 2023, 2022, 2021, 2020]" :key="y" type="button" class="msg-wall__year">
        {{ y }}年
      </button>
    </footer>
  </section>
</template>

<style scoped>
.msg-wall__title {
  font-family: var(--ff-mincho);
  font-size: 20px;
  margin: 0 0 var(--sp-5);
  color: var(--site-text);
}
.msg-wall__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--sp-4);
}
.msg-wall__card {
  background: var(--site-surface);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  padding: var(--sp-4);
  display: grid;
  grid-template-columns: 36px 1fr;
  gap: 14px;
  box-shadow: var(--site-shadow);
}
.msg-wall__emoji {
  padding-top: 4px;
  font-size: 24px;
}
.msg-wall__body {
  font-size: 14px;
  line-height: 1.9;
  color: var(--site-text);
  margin: 0;
}
.msg-wall__meta {
  margin: 10px 0 0;
  font-size: 11px;
  color: var(--site-text-light);
  letter-spacing: 0.1em;
}
.msg-wall__date {
  font-family: var(--ff-mono);
}
.msg-wall__archive {
  margin-top: var(--sp-6);
  padding: var(--sp-4) 0;
  border-top: 1px solid var(--site-border);
}
.msg-wall__archive-label {
  font-family: var(--ff-mincho);
  font-size: 13px;
  color: var(--site-text-muted);
  letter-spacing: 0.15em;
}
.msg-wall__year {
  background: var(--site-surface);
  border: 1px solid var(--site-border);
  color: var(--site-text-muted);
  padding: 4px 12px;
  cursor: pointer;
  font-family: var(--ff-mono);
  font-size: 11px;
  margin-left: 8px;
  border-radius: var(--site-radius-sm);
}
.msg-wall__year:hover {
  border-color: var(--murasaki-400);
  color: var(--murasaki-700);
}

@media (max-width: 480px) {
  .msg-wall__grid {
    grid-template-columns: 1fr;
  }
  .msg-wall__archive {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
  }
  .msg-wall__year {
    margin-left: 0;
  }
}
</style>
