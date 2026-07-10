<script setup>
/**
 * 部品名: ホーム — 今日のひばり（日替わりスポットライト）
 * 用途: ディスコグラフィから日替わりで1曲を選び、ホームに動きのある情報を出す
 */
import { computed } from 'vue'
import UiButton from '../../ui/UiButton.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const emit = defineEmits(['navigate'])

function dayOfYear(date) {
  const start = new Date(date.getFullYear(), 0, 0)
  const diff = date - start
  return Math.floor(diff / 86400000)
}

const songs = HIBARU_DATA.discography

const todaySong = computed(() => {
  if (!songs.length) return null
  const index = dayOfYear(new Date()) % songs.length
  return songs[index]
})

const todayLabel = computed(() => {
  const d = new Date()
  return `${d.getMonth() + 1}月${d.getDate()}日の一曲`
})

function onListen() {
  if (todaySong.value?.audioUrl) {
    window.open(todaySong.value.audioUrl, '_blank', 'noopener')
  }
}

function onOpenDisco() {
  emit('navigate', 'disco')
}
</script>

<template>
  <section
    v-if="todaySong"
    class="spotlight home-motion-section"
    aria-label="今日のひばり"
  >
    <div class="spotlight__inner">
      <div class="spotlight__badge">
        <span class="spotlight__badge-dot" aria-hidden="true" />
        {{ todayLabel }}
      </div>
      <div class="spotlight__body">
        <div class="spotlight__meta">
          <span class="spotlight__year">{{ todaySong.year }}</span>
          <h2 class="spotlight__title">{{ todaySong.title }}</h2>
          <p class="spotlight__note">{{ todaySong.note }}</p>
        </div>
        <div class="spotlight__actions">
          <UiButton
            v-if="todaySong.audioUrl"
            variant="primary"
            size="sm"
            class="motion-cta-shine"
            @click="onListen"
          >
            試聴する
          </UiButton>
          <UiButton variant="outline" size="sm" @click="onOpenDisco">
            全曲を見る
          </UiButton>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.spotlight {
  margin: 0 var(--sp-6) var(--sp-8);
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--site-border);
  background: linear-gradient(120deg, rgba(93, 58, 107, 0.06) 0%, rgba(255, 251, 247, 0.4) 55%, rgba(201, 169, 97, 0.08) 100%);
  overflow: hidden;
}
.spotlight__inner {
  padding: var(--sp-6) var(--sp-7);
}
.spotlight__badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--murasaki-700);
  margin-bottom: var(--sp-4);
}
.spotlight__badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--beni-500);
  box-shadow: 0 0 0 4px rgba(190, 60, 70, 0.14);
  animation: spotlight-pulse 2.4s ease-in-out infinite;
}
.spotlight__body {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-6);
  flex-wrap: wrap;
}
.spotlight__meta {
  min-width: 0;
  flex: 1;
}
.spotlight__year {
  display: inline-block;
  font-family: var(--ff-mono);
  font-size: 12px;
  color: var(--site-text-light);
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}
.spotlight__title {
  margin: 0 0 6px;
  font-family: var(--ff-mincho);
  font-size: 24px;
  font-weight: 800;
  color: var(--site-text);
  letter-spacing: 0.05em;
}
.spotlight__note {
  margin: 0;
  font-size: 13px;
  line-height: 1.7;
  color: var(--site-text-muted);
}
.spotlight__actions {
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}

@keyframes spotlight-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.35; }
}

@media (max-width: 767px) {
  .spotlight__inner {
    padding: var(--sp-5) var(--sp-4);
  }
  .spotlight__body {
    flex-direction: column;
    align-items: stretch;
  }
  .spotlight__actions {
    justify-content: stretch;
  }
  .spotlight__actions > * {
    flex: 1;
  }
}

@media (prefers-reduced-motion: reduce) {
  .spotlight__badge-dot {
    animation: none;
  }
}
</style>
