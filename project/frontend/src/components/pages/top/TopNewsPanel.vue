<script setup>
/**
 * 部品名: ホーム — 最新ニュース一覧
 */
import { computed } from 'vue'
import UiCard from '../../ui/UiCard.vue'
import SectionTitle from '../../ui/SectionTitle.vue'
import MemberGate from '../../common/MemberGate.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'
import { useMemberAccess } from '../../../composables/useMemberAccess.js'

const emit = defineEmits(['open-all', 'need-auth'])

const { canUse, PERMISSION } = useMemberAccess()

const canView = computed(() => canUse(PERMISSION.NEWSLETTER))
const allItems = computed(() => HIBARU_DATA.news.slice(0, 5))
const visibleItems = computed(() => (canView.value ? allItems.value : allItems.value.slice(0, 2)))

function onOpenAll() {
  if (canView.value) {
    emit('open-all')
  } else {
    emit('need-auth', 'login')
  }
}
</script>

<template>
  <UiCard tone="white" padding="md" class="top-news">
    <SectionTitle
      title="最新ニュース"
      size="md"
      link-label="一覧を見る ›"
      @link-click="onOpenAll"
    />

    <ul class="top-news__list">
      <li
        v-for="(n, i) in visibleItems"
        :key="i"
        class="top-news__item"
        :class="{ 'top-news__item--locked': !canView && i >= 2 }"
      >
        <div class="top-news__row">
          <time class="top-news__date">{{ n.date }}</time>
          <span v-if="i === 0 || n.isNew" class="top-news__new">NEW</span>
          <span v-if="n.label" class="top-news__label">{{ n.label }}</span>
        </div>
        <p class="top-news__title">{{ n.title }}</p>
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
  font-size: 12px;
  color: var(--site-text-light);
  letter-spacing: 0.04em;
}
.top-news__new {
  display: inline-block;
  padding: 1px 7px;
  font-size: 9px;
  font-family: var(--ff-sans-jp);
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #fff;
  background: var(--beni-500);
  border-radius: 3px;
}
.top-news__label {
  font-size: 10px;
  color: var(--murasaki-700);
  background: var(--murasaki-100);
  padding: 1px 6px;
  border-radius: 3px;
}
.top-news__title {
  margin: 0;
  font-size: 13px;
  line-height: 1.65;
  color: var(--site-text);
}
.top-news__gate {
  margin-top: 12px;
}

@media (max-width: 767px) {
  .top-news {
    min-height: auto;
  }
}
</style>
