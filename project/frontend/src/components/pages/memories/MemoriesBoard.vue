<script setup>
/**
 * 部品名: 思い出掲示板 — 投稿リスト
 * 用途: 思い出ページでファン投稿をカード形式で表示する
 */
defineProps({
  items: { type: Array, required: true },
})

const emit = defineEmits(['like'])
</script>

<template>
  <div class="mem-board">
    <article v-for="m in items" :key="m.id" class="mem-board__item">
      <div class="mem-board__song">♪ {{ m.song }}</div>
      <h3 class="mem-board__title">{{ m.title }}</h3>
      <p class="mem-board__body">{{ m.body }}</p>
      <footer class="mem-board__foot">
        <span class="mem-board__author">{{ m.author }}（{{ m.age }}歳・{{ m.location }}）</span>
        <div class="mem-board__actions">
          <button type="button" class="mem-board__like" aria-label="いいね" @click="emit('like', m.id)">
            ♡ {{ m.displayLikes }}
          </button>
          <span class="mem-board__meta">💬 {{ m.comments }}</span>
          <span class="mem-board__meta">{{ m.date }}</span>
        </div>
      </footer>
    </article>
  </div>
</template>

<style scoped>
.mem-board {
  display: flex;
  flex-direction: column;
  gap: var(--sp-5);
}
.mem-board__item {
  position: relative;
  border: 1px solid var(--site-border);
  border-left: 4px solid var(--murasaki-500);
  border-radius: var(--site-radius-md);
  padding: var(--sp-5);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
}
.mem-board__song {
  position: absolute;
  top: -11px;
  right: 20px;
  background: var(--murasaki-700);
  color: var(--kin-400);
  padding: 3px 12px;
  font-family: var(--ff-mono);
  font-size: 10px;
  letter-spacing: 0.15em;
  border: 1px solid var(--kin-500);
  border-radius: var(--site-radius-sm);
}
.mem-board__title {
  font-family: var(--ff-mincho);
  font-size: 18px;
  margin: 0 0 12px;
  letter-spacing: 0.06em;
  color: var(--site-text);
}
.mem-board__body {
  font-size: 14px;
  line-height: 2;
  color: var(--site-text-muted);
  margin: 0;
}
.mem-board__foot {
  margin-top: var(--sp-4);
  padding-top: 12px;
  border-top: 1px solid var(--site-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}
.mem-board__author {
  font-size: 12px;
  color: var(--site-text-light);
}
.mem-board__actions {
  display: flex;
  gap: 16px;
  align-items: center;
}
.mem-board__like {
  background: transparent;
  border: 0;
  cursor: pointer;
  color: var(--murasaki-600);
  display: flex;
  align-items: center;
  gap: 5px;
  font-family: var(--ff-mono);
  font-size: 12px;
}
.mem-board__meta {
  color: var(--site-text-light);
  font-family: var(--ff-mono);
  font-size: 12px;
}

@media (max-width: 480px) {
  .mem-board__item {
    padding: var(--sp-4);
  }
  .mem-board__song {
    position: static;
    display: inline-block;
    margin-bottom: 10px;
  }
  .mem-board__foot {
    flex-direction: column;
    align-items: flex-start;
  }
  .mem-board__actions {
    width: 100%;
    flex-wrap: wrap;
    gap: 10px;
  }
}
</style>
