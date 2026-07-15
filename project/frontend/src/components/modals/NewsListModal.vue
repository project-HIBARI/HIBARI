<script setup>
/**
 * 月刊ニュースレター一覧（会員限定）
 */
import ModalShell from './ModalShell.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'
import { MEMBERSHIP_LABELS } from '../../constants/membership.js'
import { useMemberAccess } from '../../composables/useMemberAccess.js'

const emit = defineEmits(['close'])

const { membership } = useMemberAccess()
</script>

<template>
  <ModalShell title="✦ 月刊ニュースレター" @close="emit('close')">
    <p class="news-modal__badge">{{ MEMBERSHIP_LABELS[membership] }}向けコンテンツ</p>
    <ul class="news-modal__list">
      <li v-for="(n, i) in HIBARU_DATA.news" :key="i" class="news-modal__item">
        <time class="news-modal__date">{{ n.date }}</time>
        <span v-if="n.label" class="news-modal__label">{{ n.label }}</span>
        <h3 class="news-modal__title">{{ n.title }}</h3>
      </li>
    </ul>
  </ModalShell>
</template>

<style scoped>
.news-modal__badge {
  display: inline-block;
  margin: 0 0 16px;
  padding: 4px 12px;
  font-size: var(--font-size-caption);
  color: var(--murasaki-700);
  background: var(--murasaki-100);
  border: 1px solid var(--murasaki-400);
  border-radius: 999px;
}
.news-modal__list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.news-modal__item {
  padding: 14px 0;
  border-bottom: 1px solid var(--site-border);
}
.news-modal__date {
  font-family: var(--ff-mono);
  font-size: var(--font-size-caption);
  color: var(--site-text-light);
}
.news-modal__label {
  display: inline-block;
  margin-left: 8px;
  padding: 2px 8px;
  font-size: var(--font-size-badge);
  color: var(--murasaki-700);
  background: var(--murasaki-100);
  border-radius: 4px;
}
.news-modal__title {
  margin: 6px 0 0;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-body);
  color: var(--site-text);
}
</style>
