<script setup>
/**
 * 部品名: ディスコグラフィ — ヒーローエリア
 * 用途: ページ冒頭のコピー・統計・今日の一曲ハイライトを表示する
 */
import UiCard from '../../ui/UiCard.vue'
import RecordChip from '../../ui/RecordChip.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'
import { todaysSong } from '../../../utils/hibaru.js'

const stats = HIBARU_DATA.discographyStats
const today = todaysSong()

const emit = defineEmits(['open-detail'])

const chipColors = ['var(--beni-700)', '#3a2a1a', 'var(--murasaki-700)']
</script>

<template>
  <!-- ディスコグラフィページのファーストビュー -->
  <section class="disco-hero" aria-label="ディスコグラフィ紹介">
    <div class="disco-hero__bg" aria-hidden="true" />

    <div class="disco-hero__inner">
      <div class="disco-hero__copy">
        <p class="disco-hero__eyebrow">DISCOGRAPHY · MISORA HIBARI</p>
        <h2 class="disco-hero__title">昭和歌謡の軌跡を、<br />一枚のレコードから。</h2>
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

      <UiCard tone="pink" padding="md" class="disco-hero__today">
        <p class="disco-hero__today-label">TODAY'S SONG · 今日の一曲</p>
        <button
          type="button"
          class="disco-hero__today-btn"
          :aria-label="today.title + 'の詳細を見る'"
          @click="emit('open-detail', today)"
        >
          <RecordChip :no="today.no" :color="chipColors[0]" />
          <div class="disco-hero__today-meta">
            <span class="disco-hero__today-year">{{ today.year }} · {{ today.genre }}</span>
            <span class="disco-hero__today-title">{{ today.title }}</span>
            <span class="disco-hero__today-romaji">{{ today.romaji }}</span>
          </div>
        </button>
      </UiCard>
    </div>
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
  grid-template-columns: 1.2fr 1fr;
  gap: var(--sp-6);
  align-items: center;
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
  font-size: clamp(22px, 3vw, 30px);
  font-weight: 700;
  line-height: 1.5;
  letter-spacing: 0.06em;
  color: var(--site-text);
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
  gap: var(--sp-5);
  flex-wrap: wrap;
}
.disco-hero__stat {
  text-align: center;
  padding: var(--sp-3) var(--sp-4);
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  min-width: 88px;
}
.disco-hero__stat-num {
  display: block;
  font-family: var(--ff-latin);
  font-size: 22px;
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
.disco-hero__today {
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
.disco-hero__today-btn {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
  width: 100%;
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
  font-size: 22px;
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

@media (max-width: 900px) {
  .disco-hero__inner {
    grid-template-columns: 1fr;
  }
}
</style>
