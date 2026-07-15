<script setup>
/**
 * 部品名: ディスコグラフィ — ヒーローエリア
 * 用途: ページ冒頭のコピー・肖像・AIカード・今日の一曲を表示する（歩み／ゆかりの地と同レイアウト）
 */
import { ref, onMounted } from 'vue'
import { pageImageUrl, PROFILE_HERO_IMAGE } from '../../../lib/pageImages.js'
import UiCard from '../../ui/UiCard.vue'
import RecordChip from '../../ui/RecordChip.vue'
import UiIco from '../../ui/UiIco.vue'
import TopAiCard from '../top/TopAiCard.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'
import { todaysSong } from '../../../utils/hibaru.js'
import { fetchSongs } from '../../../api/songs.js'

const stats = HIBARU_DATA.discographyStats
const today = ref(todaysSong())
const heroImg = pageImageUrl(PROFILE_HERO_IMAGE)

const emit = defineEmits(['open-detail', 'open-ai'])

/** YouTube 埋め込み URL を通常の視聴 URL に変換する */
function toWatchUrl(url) {
  const m = /youtube\.com\/embed\/([\w-]+)/.exec(url || '')
  return m ? `https://www.youtube.com/watch?v=${m[1]}` : url
}

/** DB の曲一覧から日付シードで今日の一曲を選び、静的データとマージする */
onMounted(async () => {
  try {
    const songs = await fetchSongs()
    if (!Array.isArray(songs) || songs.length === 0) return
    const d = new Date()
    const seed = d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate()
    const dbSong = songs[seed % songs.length]
    const local = HIBARU_DATA.discography.find((s) => s.songId === dbSong.song_id)
    today.value = {
      ...(local || today.value),
      songId: dbSong.song_id,
      title: dbSong.title,
      romaji: dbSong.romanized_title,
      year: dbSong.release_year,
      lyric: dbSong.lyrics_by ?? local?.lyric,
      music: dbSong.composed_by ?? local?.music,
      arrangement: dbSong.arrangement ?? local?.arrangement,
      note: dbSong.description ?? local?.note,
      no: local?.no || `S-${String(dbSong.song_id).padStart(3, '0')}`,
      audioUrl: toWatchUrl(dbSong.audio_path) || local?.audioUrl,
    }
  } catch (e) {
    // 取得失敗時は静的データのままフォールバック
    console.warn('今日の一曲のDB取得に失敗しました:', e)
  }
})

function onPlayClick() {
  if (!today.value.audioUrl) return
  window.open(today.value.audioUrl, '_blank', 'noopener,noreferrer')
}
</script>

<template>
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
          <li class="disco-hero__stat disco-hero__stat--period">
            <span class="disco-hero__stat-num">{{ stats.yearStart }}—{{ stats.yearEnd }}</span>
            <span class="disco-hero__stat-label">活動期間</span>
          </li>
          <li class="disco-hero__stat">
            <span class="disco-hero__stat-num">{{ stats.singleCount }}</span>
            <span class="disco-hero__stat-label">シングル</span>
          </li>
        </ul>
      </div>

      <div class="disco-hero__aside">
        <div class="disco-hero__visual">
          <img
            :src="heroImg"
            alt=""
            class="disco-hero__photo"
            width="360"
            decoding="async"
          />
        </div>

        <div class="disco-hero__ai">
          <TopAiCard @open-ai="emit('open-ai')" />
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
          class="disco-hero__today-play motion-button"
          :aria-label="today.title + 'を再生'"
          :disabled="!today.audioUrl"
          @click="onPlayClick"
        >
          <UiIco name="play" :size="16" color="var(--murasaki-700)" />
        </button>
      </div>
    </UiCard>
  </section>
</template>

<style scoped>
.disco-hero {
  position: relative;
  margin-bottom: var(--sp-7);
  padding: var(--sp-7) var(--sp-5);
  border-radius: var(--site-radius-lg);
  overflow: hidden;
  min-height: 380px;
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
  display: flex;
  align-items: center;
  gap: var(--sp-6);
  z-index: 1;
  margin-bottom: var(--sp-5);
}
.disco-hero__copy {
  flex: 1 1 auto;
  min-width: 240px;
  max-width: 400px;
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
  letter-spacing: 0.06em;
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
  gap: var(--sp-3);
  flex-wrap: wrap;
}
.disco-hero__stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: var(--sp-3) var(--sp-4);
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  min-width: 80px;
}
.disco-hero__stat-num {
  display: block;
  font-family: var(--ff-latin);
  font-size: clamp(15px, 1.6vw, 20px);
  font-weight: 700;
  color: var(--murasaki-600);
  line-height: 1.2;
  white-space: nowrap;
}
.disco-hero__stat--period .disco-hero__stat-num {
  font-size: clamp(12px, 1.3vw, 16px);
  letter-spacing: -0.02em;
}
.disco-hero__stat-label {
  display: block;
  margin-top: 4px;
  font-family: var(--ff-mincho);
  font-size: 11px;
  letter-spacing: 0.1em;
  color: var(--site-text-muted);
}
.disco-hero__aside {
  display: flex;
  align-items: stretch;
  gap: var(--sp-4);
  flex-shrink: 0;
  margin-left: auto;
}
.disco-hero__visual {
  flex-shrink: 0;
  width: 360px;
  align-self: stretch;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  overflow: hidden;
}
.disco-hero__photo {
  display: block;
  width: 360px;
  height: 100%;
  object-fit: contain;
  object-position: left bottom;
  transform: scale(1.18);
  transform-origin: left bottom;
  filter: drop-shadow(var(--site-shadow-md));
}
.disco-hero__ai {
  display: flex;
  width: 320px;
  flex-shrink: 0;
}
.disco-hero__ai :deep(.top-ai-card) {
  width: 100%;
  max-width: none;
  height: 100%;
}
.disco-hero__today {
  position: relative;
  z-index: 1;
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
  flex: 1 1 auto;
  min-width: 0;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
  text-align: left;
  color: inherit;
  transition: opacity 0.2s;
}
.disco-hero__today-play {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  margin-right: var(--sp-4);
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

@media (max-width: 900px) {
  .disco-hero__inner {
    flex-direction: column;
    align-items: stretch;
  }

  .disco-hero__copy {
    max-width: none;
  }

  .disco-hero__aside {
    flex-direction: column;
    margin-left: 0;
    order: 2;
    align-items: stretch;
  }

  .disco-hero__visual {
    width: 100%;
    max-width: 360px;
    min-height: 280px;
    margin: 0 auto;
    align-self: center;
  }

  .disco-hero__photo {
    width: 100%;
    max-width: 360px;
    height: 100%;
    min-height: 280px;
    object-position: left bottom;
    transform: scale(1.12);
    transform-origin: left bottom;
  }

  .disco-hero__ai {
    width: 100%;
    max-width: none;
  }
}
</style>
