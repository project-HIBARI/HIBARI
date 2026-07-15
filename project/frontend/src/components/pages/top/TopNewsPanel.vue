<script setup>
/**
 * 部品名: ホーム — 最新ニュース一覧
 */
import { computed } from 'vue'
import UiCard from '../../ui/UiCard.vue'
import MemberGate from '../../common/MemberGate.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'
import { useMemberAccess } from '../../../composables/useMemberAccess.js'

const emit = defineEmits(['navigate', 'need-auth'])

const { canUse, PERMISSION } = useMemberAccess()

const canView = computed(() => canUse(PERMISSION.NEWSLETTER))
const allItems = computed(() => HIBARU_DATA.news.slice(0, 5))
const visibleItems = computed(() => (canView.value ? allItems.value : allItems.value.slice(0, 2)))

function onOpenAll() {
  emit('navigate', 'news')
}
</script>

<template>
  <UiCard tone="white" padding="md" class="top-news">
    <div class="top-news__head home-news__header">
      <h2 class="top-news__heading">最新ニュース</h2>
      <button type="button" class="home-news__link" @click="onOpenAll">
        一覧を見る <span class="home-news__link-arrow">›</span>
      </button>
    </div>

    <ul class="top-news__list">
      <li
        v-for="(n, i) in visibleItems"
        :key="i"
        class="top-news__item home-news__item"
        :class="{ 'top-news__item--locked': !canView && i >= 2 }"
        :style="{ '--news-i': i }"
      >
        <div class="top-news__row">
          <time class="top-news__date">{{ n.date }}</time>
          <span v-if="i === 0 || n.isNew" class="top-news__new">NEW</span>
          <span v-if="n.label" class="top-news__label">{{ n.label }}</span>
        </div>
        <p class="top-news__title-text">{{ n.title }}</p>
      </li>
    </ul>

    <MemberGate
      v-if="!canView"
      :permission="PERMISSION.NEWSLETTER"
      feature="月刊ニュースレター"
      compact
      class="top-news__gate"
      @login="emit('need-auth', 'login')"
      @register="emit('need-auth', 'register')"
      @upgrade="emit('need-auth', 'register-premium')"
    />
  </UiCard>
</template>

<style scoped>
.top-news {
  height: 100%;
  display: flex;
  flex-direction: column;
  min-height: 380px;
}
.top-news__head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: var(--sp-5);
  padding-bottom: var(--sp-3);
  border-bottom: 1px solid var(--site-border);
}
.top-news__heading {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-subtitle);
  font-weight: 700;
  color: var(--site-text);
  letter-spacing: 0.06em;
}
.top-news__list {
  list-style: none;
  margin: 0;
  padding: 0;
  flex: 1;
}
.top-news__item {
  padding: 13px 0;
  border-bottom: 1px solid var(--site-border);
}
.top-news__item:last-child {
  border-bottom: 0;
}
.top-news__row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 5px;
  flex-wrap: wrap;
}
.top-news__date {
  font-family: var(--ff-mono);
  font-size: var(--font-size-caption);
  color: var(--site-text-light);
  letter-spacing: 0.04em;
  transition: color 0.35s ease;
}
.top-news__new {
  display: inline-block;
  padding: 1px 7px;
  font-size: var(--font-size-badge);
  font-family: var(--ff-sans-jp);
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #fff;
  background: var(--beni-500);
  border-radius: 3px;
}
.top-news__label {
  font-size: var(--font-size-badge);
  color: var(--murasaki-700);
  background: var(--murasaki-100);
  padding: 1px 6px;
  border-radius: 3px;
  transition: background 0.35s ease, color 0.35s ease;
}
.top-news__title-text {
  margin: 0;
  font-size: var(--font-size-button);
  line-height: 1.65;
  color: var(--site-text);
}
.top-news__gate {
  margin-top: 12px;
}
.home-news__link {
  background: transparent;
  border: 0;
  padding: 0;
  cursor: pointer;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  color: var(--murasaki-700);
  letter-spacing: 0.04em;
  white-space: nowrap;
}

@media (max-width: 767px) {
  .top-news {
    min-height: auto;
  }
}
</style>
