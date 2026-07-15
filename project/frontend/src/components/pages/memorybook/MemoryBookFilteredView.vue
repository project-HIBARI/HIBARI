<script setup>
/**
 * 部品名: Music Memory Book — 関連思い出一覧
 */
import MemoryBookBreadcrumb from './MemoryBookBreadcrumb.vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'
import { aosAttrs } from '../../../lib/aos.js'
import { computed } from 'vue'

const props = defineProps({
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
  data: { type: Object, required: true },
  backLabel: { type: String, default: '詳細に戻る' },
})

const emit = defineEmits(['back', 'open-detail', 'retry', 'empty-action'])

const iconMap = {
  flower: 'flower',
  chat: 'chat',
  music: 'disc',
}

const crumbs = computed(() => {
  if (props.data.mode === 'category') {
    return [
      { label: 'Music Memory Book', action: 'top' },
      { label: props.data.title },
    ]
  }
  return [
    { label: 'Music Memory Book', action: 'top' },
    { label: '思い出の詳細', action: 'detail' },
    { label: '関連する思い出' },
  ]
})

function onCrumb(action) {
  if (action === 'top' || action === 'detail') emit('back')
}
</script>

<template>
  <div class="mmb-filter">
    <div v-if="loading && !data.timeline.length" class="mmb-state mmb-state--loading">
      読み込み中です…
    </div>

    <div v-else-if="error" class="mmb-state mmb-state--error">
      <p>{{ error }}</p>
      <UiButton variant="outline" size="sm" @click="emit('retry')">もう一度お試しください</UiButton>
    </div>

    <template v-else>
      <div class="mmb-filter__toolbar">
        <UiButton variant="ghost" size="sm" @click="emit('back')">‹ {{ backLabel }}</UiButton>
      </div>

      <MemoryBookBreadcrumb :items="crumbs" @navigate="onCrumb" />

      <header class="mmb-filter__head" v-bind="aosAttrs()">
        <h1 class="mmb-filter__title">{{ data.title }}</h1>
        <p class="mmb-filter__lead">{{ data.lead }}</p>
        <p class="mmb-filter__count">{{ data.total }}<small>件</small></p>
      </header>

      <section class="mmb-filter__list" aria-label="関連する思い出一覧">
        <p v-if="!data.timeline.length" class="mmb-filter__empty">
          {{ data.emptyMessage }}
          <UiButton
            v-if="data.emptyActionLabel"
            variant="outline"
            size="sm"
            class="mmb-filter__empty-btn"
            @click="emit('empty-action', data.emptyAction)"
          >
            {{ data.emptyActionLabel }}
          </UiButton>
        </p>

        <article
          v-for="(item, i) in data.timeline"
          :key="item.id"
          class="mmb-filter__entry"
          v-bind="aosAttrs(80 + i * 40)"
        >
          <button type="button" class="mmb-filter__card" @click="emit('open-detail', item.id)">
            <div class="mmb-filter__body">
              <span class="mmb-filter__cat">{{ item.categoryLabel }}</span>
              <h2 class="mmb-filter__entry-title">{{ item.title }}</h2>
              <p class="mmb-filter__date">日付：{{ item.dateDisplay || item.date }}</p>
              <p class="mmb-filter__desc">{{ item.description }}</p>
            </div>
            <div class="mmb-filter__visual">
              <div class="mmb-filter__icon">
                <UiIco :name="iconMap[item.icon] || 'bookmark'" :size="24" color="var(--murasaki-600)" />
              </div>
              <span class="mmb-filter__arrow" aria-hidden="true">›</span>
            </div>
          </button>
        </article>
      </section>
    </template>
  </div>
</template>

<style scoped>
.mmb-filter__toolbar {
  margin-bottom: var(--sp-4);
}

.mmb-filter__head {
  margin-bottom: var(--sp-6);
}

.mmb-filter__title {
  margin: 0 0 8px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.5rem, 2.6vw, 1.875rem);
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--murasaki-800);
}

.mmb-filter__lead {
  margin: 0 0 12px;
  font-size: var(--font-size-small);
  line-height: 1.9;
  color: var(--site-text-muted);
}

.mmb-filter__count {
  margin: 0;
  font-family: var(--ff-latin);
  font-size: var(--font-size-heading);
  font-weight: 700;
  color: var(--murasaki-700);
}

.mmb-filter__count small {
  font-size: var(--font-size-caption);
  font-family: var(--ff-mincho);
  margin-left: 4px;
}

.mmb-filter__list {
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
}

.mmb-filter__card {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--sp-5);
  width: 100%;
  padding: var(--sp-5) var(--sp-6);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
  cursor: pointer;
  text-align: left;
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}

.mmb-filter__card:hover {
  transform: translateX(4px);
  box-shadow: var(--site-shadow-md);
  border-color: rgba(122, 80, 136, 0.25);
}

.mmb-filter__cat {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 999px;
  background: var(--murasaki-100);
  font-family: var(--ff-mincho);
  font-size: var(--font-size-badge);
  letter-spacing: 0.06em;
  color: var(--murasaki-700);
  margin-bottom: 8px;
}

.mmb-filter__entry-title {
  margin: 0 0 8px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-emphasis);
  font-weight: 700;
  color: var(--site-text);
  line-height: 1.5;
}

.mmb-filter__date {
  margin: 0 0 6px;
  font-family: var(--ff-mono);
  font-size: var(--font-size-caption);
  color: var(--site-text-light);
}

.mmb-filter__desc {
  margin: 0;
  font-size: var(--font-size-button);
  line-height: 1.8;
  color: var(--site-text-muted);
}

.mmb-filter__visual {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--sp-3);
  min-width: 72px;
}

.mmb-filter__icon {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: var(--site-surface-muted);
  border: 1px solid var(--site-border);
  display: flex;
  align-items: center;
  justify-content: center;
}

.mmb-filter__arrow {
  font-size: var(--font-size-subtitle);
  color: var(--murasaki-500);
}

.mmb-filter__empty,
.mmb-state {
  padding: var(--sp-8) var(--sp-6);
  text-align: center;
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--site-border);
  background: var(--site-surface);
}

.mmb-filter__empty {
  color: var(--site-text-muted);
  font-size: var(--font-size-small);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--sp-4);
}

.mmb-filter__empty-btn {
  margin-top: var(--sp-2);
}

.mmb-state--loading {
  color: var(--site-text-muted);
  font-size: var(--font-size-small);
}

.mmb-state--error p {
  margin: 0 0 var(--sp-4);
  color: var(--beni-600);
  font-size: var(--font-size-small);
}
</style>
