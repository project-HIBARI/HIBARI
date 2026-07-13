<script setup>
/**
 * 部品名: ディスコグラフィ — ページネーション
 * 用途: 楽曲一覧のページ切り替えコントロール
 */
import UiButton from '../../ui/UiButton.vue'
import { aosAttrs } from '../../../lib/aos.js'

const props = defineProps({
  page: { type: Number, default: 1 },
  totalPages: { type: Number, default: 1 },
  totalItems: { type: Number, default: 0 },
  pageSize: { type: Number, default: 8 },
})

const emit = defineEmits(['update:page'])

function goTo(p) {
  if (p >= 1 && p <= props.totalPages) {
    emit('update:page', p)
  }
}
</script>

<template>
  <!-- 一覧ページの前後・番号ナビ -->
  <nav
    v-if="totalPages > 1"
    class="disco-pagination"
    aria-label="ページナビゲーション"
    v-bind="aosAttrs()"
  >
    <UiButton variant="ghost" size="sm" aos :disabled="page <= 1" @click="goTo(page - 1)">
      ‹ 前へ
    </UiButton>

    <div class="disco-pagination__pages">
      <button
        v-for="p in totalPages"
        :key="p"
        type="button"
        class="disco-pagination__page"
        :class="{ 'disco-pagination__page--active': p === page }"
        :aria-label="p + 'ページ目'"
        :aria-current="p === page ? 'page' : undefined"
        @click="goTo(p)"
      >
        {{ p }}
      </button>
    </div>

    <UiButton variant="ghost" size="sm" aos :disabled="page >= totalPages" @click="goTo(page + 1)">
      次へ ›
    </UiButton>

    <span class="disco-pagination__info">
      {{ totalItems }} 曲中 {{ (page - 1) * pageSize + 1 }}—{{ Math.min(page * pageSize, totalItems) }} 曲
    </span>
  </nav>
</template>

<style scoped>
.disco-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: var(--sp-3);
  margin-bottom: var(--sp-7);
  padding: var(--sp-4);
  background: var(--site-surface-muted);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
}
.disco-pagination__pages {
  display: flex;
  gap: 6px;
}
.disco-pagination__page {
  width: 36px;
  height: 36px;
  border: 1px solid var(--site-border-strong);
  border-radius: var(--site-radius-sm);
  background: var(--site-surface);
  font-family: var(--ff-mono);
  font-size: 13px;
  color: var(--site-text-muted);
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s, color 0.2s;
}
.disco-pagination__page:hover {
  border-color: var(--murasaki-400);
  color: var(--murasaki-700);
}
.disco-pagination__page--active {
  background: var(--murasaki-700);
  border-color: var(--murasaki-800);
  color: #fff;
}
.disco-pagination__info {
  width: 100%;
  text-align: center;
  font-family: var(--ff-mono);
  font-size: 11px;
  color: var(--site-text-muted);
  letter-spacing: 0.06em;
}
</style>
