<script setup>
/**
 * 部品名: ディスコグラフィ — ヒーローエリア
 * 用途: ページ冒頭のコピー・肖像・AIカード・80周年バッジ・今日の一曲を表示する
 */
import { pageImageUrl, PAGE_HERO_IMAGE } from '../../../lib/pageImages.js'
import UiCard from '../../ui/UiCard.vue'
import RecordChip from '../../ui/RecordChip.vue'
import UiIco from '../../ui/UiIco.vue'
import TopAiCard from '../top/TopAiCard.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'
import { todaysSong } from '../../../utils/hibaru.js'

const stats = HIBARU_DATA.discographyStats
const today = todaysSong()
const heroImg = pageImageUrl(PAGE_HERO_IMAGE)

const emit = defineEmits(['open-detail', 'open-ai'])

function onPlayClick() {
  if (!today.audioUrl) return
  window.open(today.audioUrl, '_blank', 'noopener,noreferrer')
}
</script>

<template>
  <!-- ディスコグラフィページのファーストビュー（デザイン準拠） -->
  <section class="disco-hero" aria-label="ディスコグラフィ紹介">
    <div class="disco-hero__bg" aria-hidden="true" />

    <div class="disco-hero__inner">
      <div class="disco-hero__copy">
        <p class="disco-hero__eyebrow">DISCOGRAPHY · MISORA HIBARI</p>
        <h1 class="disco-hero__title">ディスコグラフィ</h1>
        <p class="disco-hero__desc">
          デビュー作「悲しき口笛」から遺作「川の流れのように」まで。<br />
          代表曲を年代・ジャンルでたどれるディスコグラフィです。
        </p>

        <ul class="disco-hero__stats" aria-label="収録サマリー">
          <li class="disco-hero__stat">
            <span class="disco-hero__stat-num">{{ stats.totalSongs }}</span>
            <span class="disco-hero__stat-label">代表曲</span>
          </li>
          <li class="disco-hero__stat">
            <span class="disco-hero__stat-num">{{ stats.yearStart }}—{{ stats.yearEnd }}</span>
            <span class="disco-hero__stat-label">活動期間</span>
          </li>
          <li class="disco-hero__stat">
            <span class="disco-hero__stat-num">{{ stats.singleCount }}</span>
            <span class="disco-hero__stat-label">シングル</span>
          </li>
        </ul>
      </div>

      <div class="disco-hero__visual">
        <img :src="heroImg" alt="美空ひばり" class="disco-hero__photo" />
        <div class="disco-hero__mic" aria-hidden="true" />
      </div>

      <div class="disco-hero__side">
        <TopAiCard @open-ai="emit('open-ai')" />
        <div class="disco-hero__anniversary" aria-label="芸能生活80周年記念">
          <div class="disco-hero__anniversary-ring">
            <span class="disco-hero__anniversary-num">80</span>
            <span class="disco-hero__anniversary-unit">周年</span>
          </div>
          <p class="disco-hero__anniversary-text">芸能生活<br />80周年<br />記念サイト</p>
        </div>
      </div>
    </div>

    <UiCard tone="pink" padding="md" class="disco-hero__today">
      <p class="disco-hero__today-label">TODAY'S SONG · 今日の一曲</p>
      <div class="disco-hero__today-row">
        <button
          type="button"
          class="disco-hero__today-btn"
          :aria-label="today.title + 'の詳細を見る'"
          @click="emit('open-detail', today)"
        >
          <RecordChip :no="today.no" color="var(--beni-700)" />
          <div class="disco-hero__today-meta">
            <span class="disco-hero__today-year">{{ today.year }} · {{ today.genre }}</span>
            <span class="disco-hero__today-title">{{ today.title }}</span>
            <span class="disco-hero__today-romaji">{{ today.romaji }}</span>
          </div>
        </button>
        <button
          type="button"
          class="disco-hero__today-play"
          :aria-label="today.title + 'を再生'"
          :disabled="!today.audioUrl"
          @click="onPlayClick"
        >
          <UiIco name="play" :size="13" color="var(--murasaki-700)" />
        </button>
      </div>
    </UiCard>
  </section>
</template>

<style scoped>
.disco-hero {
  position: relative;
  margin-bottom: var(--sp-7);
  padding: var(--sp-6) var(--sp-5);
  border-radius: var(--site-radius-lg);
  overflow: hidden;
}
.disco-hero__bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 15% 40%, rgba(252, 232, 236, 0.85) 0%, transparent 50%),
    radial-gradient(ellipse at 85% 30%, rgba(245, 235, 224, 0.7) 0%, transparent 45%),
    repeating-radial-gradient(circle at 90% 80%, rgba(201, 169, 97, 0.06) 0 1px, transparent 1px 24px),
    linear-gradient(135deg, var(--site-bg-warm) 0%, var(--site-bg-pink) 50%, var(--site-surface-muted) 100%);
  border: 1px solid var(--site-border);
}
.disco-hero__inner {
  position: relative;
  display: grid;
  grid-template-columns: 1fr minmax(200px, 280px) auto;
  gap: var(--sp-6);
  align-items: center;
  margin-bottom: var(--sp-5);
}
.disco-hero__eyebrow {
  margin: 0 0 10px;
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.28em;
  color: var(--kin-600);
}
.disco-hero__title {
  margin: 0 0 14px;
  font-family: var(--ff-mincho);
  font-size: clamp(28px, 3.5vw, 38px);
  font-weight: 800;
  letter-spacing: 0.08em;
  color: var(--site-text);
  line-height: 1.3;
}
.disco-hero__desc {
  margin: 0 0 var(--sp-5);
  font-size: 13px;
  line-height: 1.85;
  color: var(--site-text-muted);
}
.disco-hero__stats {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  gap: var(--sp-4);
  flex-wrap: wrap;
}
.disco-hero__stat {
  text-align: center;
  padding: var(--sp-3) var(--sp-4);
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  min-width: 80px;
}
.disco-hero__stat-num {
  display: block;
  font-family: var(--ff-latin);
  font-size: 20px;
  font-weight: 700;
  color: var(--murasaki-600);
  line-height: 1.2;
}
.disco-hero__stat-label {
  display: block;
  margin-top: 4px;
  font-family: var(--ff-mincho);
  font-size: 11px;
  letter-spacing: 0.1em;
  color: var(--site-text-muted);
}
.disco-hero__visual {
  position: relative;
  display: flex;
  justify-content: center;
}
.disco-hero__photo {
  width: 100%;
  max-width: 260px;
  height: auto;
  aspect-ratio: 4 / 5;
  object-fit: cover;
  border-radius: var(--site-radius-lg);
  border: 3px solid rgba(255, 255, 255, 0.9);
  box-shadow: var(--site-shadow-md);
  filter: grayscale(0.15);
}
.disco-hero__mic {
  position: absolute;
  bottom: 10%;
  left: -6%;
  width: 40px;
  height: 100px;
  background: linear-gradient(180deg, #c8c8c8 0%, #888 40%, #666 100%);
  border-radius: 20px 20px 6px 6px;
  box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.12);
}
.disco-hero__side {
  display: flex;
  flex-direction: column;
  gap: var(--sp-5);
  align-items: flex-end;
}
.disco-hero__anniversary {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid var(--kin-500);
  border-radius: var(--site-radius-md);
  box-shadow: var(--site-shadow);
}
.disco-hero__anniversary-ring {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: 2px solid var(--kin-500);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle, #fff 0%, var(--site-surface-muted) 100%);
  flex-shrink: 0;
}
.disco-hero__anniversary-num {
  font-family: var(--ff-latin);
  font-size: 20px;
  font-weight: 700;
  color: var(--kin-600);
  line-height: 1;
}
.disco-hero__anniversary-unit {
  font-family: var(--ff-mincho);
  font-size: 9px;
  color: var(--kin-600);
}
.disco-hero__anniversary-text {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 10px;
  line-height: 1.6;
  letter-spacing: 0.08em;
  color: var(--site-text-muted);
}
.disco-hero__today {
  position: relative;
  background:
    radial-gradient(ellipse at 100% 0%, rgba(243, 235, 246, 0.8) 0%, transparent 55%),
    var(--site-surface);
}
.disco-hero__today-label {
  margin: 0 0 var(--sp-4);
  font-family: var(--ff-latin);
  font-size: 10px;
  letter-spacing: 0.25em;
  color: var(--kin-600);
}
.disco-hero__today-row {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
}
.disco-hero__today-btn {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
  flex: 1;
  min-width: 0;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
  text-align: left;
  color: inherit;
  transition: opacity 0.2s;
}
.disco-hero__today-btn:hover {
  opacity: 0.85;
}
.disco-hero__today-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}
.disco-hero__today-year {
  font-family: var(--ff-mono);
  font-size: 10px;
  letter-spacing: 0.15em;
  color: var(--kin-600);
}
.disco-hero__today-title {
  font-family: var(--ff-mincho);
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--site-text);
}
.disco-hero__today-romaji {
  font-family: var(--ff-latin);
  font-style: italic;
  font-size: 12px;
  color: var(--site-text-muted);
}
.disco-hero__today-play {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--murasaki-400);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--murasaki-100);
  cursor: pointer;
  padding: 0;
  transition: background 0.2s, border-color 0.2s;
}
.disco-hero__today-play:hover:not(:disabled) {
  background: var(--murasaki-200, #e8dff0);
  border-color: var(--murasaki-500);
}
.disco-hero__today-play:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

@media (max-width: 1024px) {
  .disco-hero__inner {
    grid-template-columns: 1fr;
    gap: var(--sp-7);
  }
  .disco-hero__side {
    flex-direction: row;
    flex-wrap: wrap;
    align-items: stretch;
    justify-content: center;
  }
  .disco-hero__visual {
    order: -1;
  }
  .disco-hero__mic {
    display: none;
  }
}
</style>
