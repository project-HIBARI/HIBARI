<script setup>
/**
 * 部品名: Music Memory Book — TOP
 */
import { computed } from 'vue'
import MemoryBookAlbumCover from './MemoryBookAlbumCover.vue'
import MemoryBookPremiumBand from './MemoryBookPremiumBand.vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'
import { pageImageUrl, PROFILE_HERO_IMAGE } from '../../../lib/pageImages.js'
import { aosAttrs } from '../../../lib/aos.js'

const props = defineProps({
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
  summary: { type: Object, default: null },
  categories: { type: Array, default: () => [] },
  years: { type: Array, default: () => [] },
  getCoverDesign: { type: Function, required: true },
  coversByYear: { type: Object, default: () => ({}) },
})

const heroImg = pageImageUrl(PROFILE_HERO_IMAGE)

const iconMap = {
  flower: 'flower',
  chat: 'chat',
  music: 'disc',
  calendar: 'calendar',
}

const emit = defineEmits(['open-year', 'open-detail', 'open-fanclub', 'open-category', 'retry'])

const displaySummary = computed(() => props.summary ?? {
  total: 0,
  startedAt: '—',
  categories: { flowers: 0, posts: 0, songs: 0, aiChats: 0 },
})

const currentYear = computed(() => props.summary?.currentYear ?? {
  year: new Date().getFullYear(),
  total: 0,
})

const yearAlbums = computed(() =>
  props.years.length
    ? props.years
    : [{ year: new Date().getFullYear(), total: 0, tone: 'purple' }],
)

function coverDesignForYear(year) {
  void props.coversByYear
  return props.getCoverDesign(year)
}

const heroCoverDesign = computed(() => coverDesignForYear(currentYear.value.year))
</script>

<template>
  <div class="mmb-top">
    <div v-if="loading && !summary" class="mmb-state mmb-state--loading">
      読み込み中です…
    </div>

    <div v-else-if="error" class="mmb-state mmb-state--error">
      <p>{{ error }}</p>
      <UiButton variant="outline" size="sm" @click="emit('retry')">もう一度お試しください</UiButton>
    </div>

    <template v-else>
    <!-- Hero -->
    <section class="mmb-top__hero" aria-labelledby="mmb-top-title">
      <div class="mmb-top__hero-bg" aria-hidden="true" />

      <div class="mmb-top__hero-inner">
        <div class="mmb-top__hero-copy" v-bind="aosAttrs()">
          <p class="mmb-top__eyebrow">MEMORY BOOK · MISORA HIBARI</p>
          <h1 id="mmb-top-title" class="mmb-top__title">Music Memory Book</h1>
          <p class="mmb-top__lead">
            あなたの美空ひばりとの思い出を、ひとつのアルバムに。<br />
            献花、思い出の投稿、お気に入りの楽曲、AIとの会話をまとめて、<br />
            あなただけの音楽の思い出を残しましょう。
          </p>
        </div>

        <div class="mmb-top__hero-photo" v-bind="aosAttrs(60)">
          <img
            :src="heroImg"
            alt=""
            class="mmb-top__hero-photo-img"
            width="360"
            decoding="async"
          />
        </div>

        <aside class="mmb-top__hero-aside" v-bind="aosAttrs(120)" aria-label="あなたのアルバム">
          <article class="mmb-top__hero-tile mmb-top__stats-card">
            <span class="mmb-top__stats-badge">
              <UiIco name="crown" :size="14" color="var(--kin-600)" />
              プレミアム会員限定
            </span>
            <h2 class="mmb-top__stats-label">あなたの思い出総数</h2>
            <p class="mmb-top__stats-num">
              {{ displaySummary.total }}<span class="mmb-top__stats-unit">件</span>
            </p>
            <hr class="hr-gold mmb-top__stats-rule" />
            <p class="mmb-top__stats-since">はじめた日：{{ displaySummary.startedAt }}</p>
          </article>

          <div class="mmb-top__hero-tile mmb-top__hero-album" aria-hidden="true">
            <MemoryBookAlbumCover
              :year="currentYear.year"
              :design-id="heroCoverDesign"
              size="lg"
            />
          </div>
        </aside>
      </div>
    </section>

    <!-- Category cards -->
    <section class="mmb-top__categories" aria-label="思い出カテゴリ">
      <button
        v-for="(cat, i) in categories"
        :key="cat.id"
        type="button"
        class="mmb-top__cat"
        :class="`mmb-top__cat--${cat.tone}`"
        v-bind="aosAttrs(i * 80)"
        @click="emit('open-category', cat.id)"
      >
        <div class="mmb-top__cat-icon">
          <UiIco :name="iconMap[cat.icon] || 'bookmark'" :size="20" color="var(--murasaki-700)" />
        </div>
        <h2 class="mmb-top__cat-title">{{ cat.title }}</h2>
        <p v-if="cat.count != null" class="mmb-top__cat-count">{{ cat.count }}<span>{{ cat.id === 'songs' ? '曲' : '件' }}</span></p>
        <p class="mmb-top__cat-desc">{{ cat.desc }}</p>
        <span class="mmb-top__cat-link">詳しく見る ›</span>
      </button>
    </section>

    <!-- This year -->
    <section class="mmb-top__year-card" v-bind="aosAttrs(120)" aria-label="今年のMusic Memories">
      <div class="mmb-top__year-inner">
        <div class="mmb-top__year-copy">
          <p class="mmb-top__year-eyebrow">THIS YEAR</p>
          <h2 class="mmb-top__year-title">{{ currentYear.year }}年のMusic Memories</h2>
          <ul class="mmb-top__year-stats">
            <li>献花：<strong>{{ displaySummary.categories.flowers }}</strong>件</li>
            <li>投稿：<strong>{{ displaySummary.categories.posts }}</strong>件</li>
            <li>楽曲：<strong>{{ displaySummary.categories.songs }}</strong>曲</li>
            <li>AI会話：<strong>{{ displaySummary.categories.aiChats }}</strong>件</li>
            <li>思い出総数：<strong>{{ currentYear.total }}</strong>件</li>
          </ul>
          <UiButton variant="primary" size="md" @click="emit('open-year', currentYear.year)">
            {{ currentYear.year }}年のアルバムを見る
            <UiIco name="arrow" :size="14" color="#fff" />
          </UiButton>
        </div>
        <MemoryBookAlbumCover
          :year="currentYear.year"
          :design-id="heroCoverDesign"
          size="md"
        />
      </div>
    </section>

    <!-- Shelf -->
    <section class="mmb-top__shelf" aria-label="年別アルバム一覧">
      <h2 class="mmb-top__shelf-title" v-bind="aosAttrs()">年別アルバム一覧</h2>
      <p class="mmb-top__shelf-desc">本棚のように、年ごとの思い出アルバムが並びます。</p>
      <div class="mmb-top__shelf-row">
        <button
          v-for="(y, i) in yearAlbums"
          :key="y.year"
          type="button"
          class="mmb-top__shelf-item"
          v-bind="aosAttrs(i * 80)"
          @click="emit('open-year', y.year)"
        >
          <MemoryBookAlbumCover
            :year="y.year"
            :design-id="coverDesignForYear(y.year)"
            size="sm"
          />
          <p class="mmb-top__shelf-label">{{ y.year }}年 Music Memories</p>
          <p class="mmb-top__shelf-count">{{ y.total }}件の思い出</p>
        </button>
      </div>
    </section>

    <MemoryBookPremiumBand @open-fanclub="emit('open-fanclub')" />
    </template>
  </div>
</template>

<style scoped>
.mmb-top__hero {
  position: relative;
  margin-bottom: var(--sp-8);
  padding: var(--sp-6) var(--sp-5);
  border-radius: var(--site-radius-lg);
  overflow: hidden;
}

.mmb-top__hero-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 15% 40%, rgba(252, 232, 236, 0.85) 0%, transparent 50%),
    radial-gradient(ellipse at 85% 30%, rgba(245, 235, 224, 0.7) 0%, transparent 45%),
    radial-gradient(ellipse at 50% 100%, rgba(201, 169, 97, 0.12) 0%, transparent 55%),
    repeating-radial-gradient(circle at 90% 80%, rgba(201, 169, 97, 0.06) 0 1px, transparent 1px 24px),
    linear-gradient(135deg, var(--site-bg-warm) 0%, var(--site-bg-pink) 50%, var(--site-surface-muted) 100%);
  border: 1px solid var(--site-border);
  box-shadow: var(--site-shadow-md);
}

.mmb-top__hero-inner {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px minmax(456px, 472px);
  gap: var(--sp-6);
  align-items: stretch;
  min-width: 0;
}

.mmb-top__hero-copy {
  align-self: center;
  min-width: 0;
}

.mmb-top__eyebrow {
  margin: 0 0 12px;
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.35em;
  color: var(--kin-600);
}

.mmb-top__title {
  margin: 0 0 16px;
  font-family: var(--ff-mincho);
  font-size: clamp(32px, 3.5vw, 44px);
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--murasaki-800);
  line-height: 1.35;
}

.mmb-top__lead {
  margin: 0;
  font-size: 14px;
  line-height: 2;
  color: var(--site-text-muted);
}

.mmb-top__hero-photo {
  position: relative;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  align-self: stretch;
  overflow: hidden;
}

.mmb-top__hero-photo-img {
  display: block;
  width: 360px;
  height: 100%;
  min-height: 300px;
  object-fit: contain;
  object-position: center bottom;
  transform: scale(1.14);
  transform-origin: center bottom;
  filter: drop-shadow(var(--site-shadow-md));
}

.mmb-top__hero-aside {
  display: grid;
  grid-template-columns: repeat(2, 220px);
  gap: var(--sp-4);
  align-self: center;
  min-width: 0;
}

.mmb-top__hero-tile {
  box-sizing: border-box;
  width: 220px;
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--site-border);
  background: color-mix(in srgb, var(--site-surface) 92%, transparent);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: var(--site-shadow);
}

.mmb-top__stats-card {
  padding: var(--sp-5) var(--sp-4);
  text-align: center;
}

.mmb-top__hero-album {
  padding: 0;
  background: transparent;
  border: 0;
  box-shadow: none;
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
}

.mmb-top__hero-album :deep(.mmb-cover--with-design) {
  filter: none;
}

.mmb-top__stats-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: 999px;
  background: var(--murasaki-100);
  border: 1px solid rgba(122, 80, 136, 0.2);
  font-family: var(--ff-mincho);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--murasaki-700);
  margin-bottom: var(--sp-4);
}

.mmb-top__stats-label {
  margin: 0 0 var(--sp-3);
  font-family: var(--ff-mincho);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--site-text);
}

.mmb-top__stats-num {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: clamp(32px, 3vw, 40px);
  font-weight: 800;
  letter-spacing: 0.02em;
  color: var(--murasaki-700);
  line-height: 1.1;
}

.mmb-top__stats-rule {
  width: 48px;
  margin: var(--sp-3) auto;
}

.mmb-top__stats-unit {
  font-size: 18px;
  font-weight: 700;
  margin-left: 4px;
}

.mmb-top__stats-since {
  margin: 0;
  font-family: var(--ff-mono);
  font-size: 12px;
  color: var(--site-text-light);
}

.mmb-top__categories {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: var(--sp-4);
  margin-bottom: var(--sp-8);
}

.mmb-top__cat {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
  padding: var(--sp-5);
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--site-border);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
  cursor: pointer;
  transition: transform 0.35s ease, box-shadow 0.35s ease, border-color 0.35s ease;
  min-height: 200px;
}

.mmb-top__cat:hover {
  transform: translateY(-4px);
  box-shadow: var(--site-shadow-md);
  border-color: rgba(122, 80, 136, 0.25);
}

.mmb-top__cat-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--murasaki-100);
  margin-bottom: var(--sp-4);
}

.mmb-top__cat--pink .mmb-top__cat-icon { background: var(--site-bg-pink); }
.mmb-top__cat--gold .mmb-top__cat-icon { background: rgba(201, 169, 97, 0.15); }

.mmb-top__cat-title {
  margin: 0 0 8px;
  font-family: var(--ff-mincho);
  font-size: 15px;
  font-weight: 700;
  color: var(--site-text);
}

.mmb-top__cat-count {
  margin: 0 0 8px;
  font-family: var(--ff-latin);
  font-size: 28px;
  font-weight: 700;
  color: var(--murasaki-700);
  line-height: 1;
}

.mmb-top__cat-count span {
  font-size: 13px;
  font-family: var(--ff-mincho);
  margin-left: 2px;
}

.mmb-top__cat-desc {
  margin: 0 0 auto;
  font-size: 11px;
  line-height: 1.75;
  color: var(--site-text-muted);
  flex: 1;
}

.mmb-top__cat-link {
  margin-top: var(--sp-4);
  font-family: var(--ff-mincho);
  font-size: 11px;
  color: var(--murasaki-600);
  letter-spacing: 0.04em;
}

.mmb-top__year-card {
  margin-bottom: var(--sp-8);
  border-radius: 24px;
  border: 1px solid color-mix(in srgb, var(--murasaki-400) 35%, var(--site-border));
  background:
    radial-gradient(ellipse at 0% 100%, rgba(252, 232, 236, 0.5) 0%, transparent 50%),
    var(--site-surface);
  box-shadow: var(--site-shadow-md);
  overflow: hidden;
}

.mmb-top__year-inner {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--sp-7);
  align-items: center;
  padding: var(--sp-7) var(--sp-8);
}

.mmb-top__year-eyebrow {
  margin: 0 0 8px;
  font-family: var(--ff-latin);
  font-size: 10px;
  letter-spacing: 0.35em;
  color: var(--kin-600);
}

.mmb-top__year-title {
  margin: 0 0 var(--sp-5);
  font-family: var(--ff-mincho);
  font-size: clamp(24px, 2.5vw, 32px);
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--murasaki-800);
}

.mmb-top__year-stats {
  list-style: none;
  margin: 0 0 var(--sp-6);
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 10px 24px;
  font-size: 13px;
  color: var(--site-text-muted);
}

.mmb-top__year-stats strong {
  font-family: var(--ff-latin);
  font-size: 18px;
  color: var(--murasaki-700);
  margin-right: 2px;
}

.mmb-top__shelf-title {
  margin: 0 0 8px;
  font-family: var(--ff-mincho);
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--site-text);
}

.mmb-top__shelf-desc {
  margin: 0 0 var(--sp-6);
  font-size: 13px;
  color: var(--site-text-muted);
}

.mmb-top__shelf-row {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--sp-5);
  padding: var(--sp-6);
  border-radius: var(--site-radius-lg);
  background:
    linear-gradient(180deg, #e8dfd4 0%, #ddd2c4 100%);
  border: 1px solid rgba(90, 60, 40, 0.15);
  box-shadow: inset 0 2px 8px rgba(60, 40, 30, 0.08);
  margin-bottom: var(--sp-2);
}

.mmb-top__shelf-item {
  padding: var(--sp-4) var(--sp-3) var(--sp-5);
  border: 0;
  background: transparent;
  cursor: pointer;
  text-align: center;
  transition: transform 0.3s ease;
}

.mmb-top__shelf-item:hover {
  transform: translateY(-6px);
}

.mmb-top__shelf-item :deep(.mmb-cover) {
  margin: 0 auto var(--sp-3);
}

.mmb-top__shelf-label {
  margin: 0 0 4px;
  font-family: var(--ff-mincho);
  font-size: 12px;
  font-weight: 700;
  color: var(--site-text);
}

.mmb-top__shelf-count {
  margin: 0;
  font-size: 11px;
  color: var(--site-text-muted);
}

.mmb-state {
  padding: var(--sp-8) var(--sp-6);
  text-align: center;
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--site-border);
  background: var(--site-surface);
}

.mmb-state--loading {
  color: var(--site-text-muted);
  font-size: 14px;
}

.mmb-state--error p {
  margin: 0 0 var(--sp-4);
  color: var(--beni-600);
  font-size: 14px;
}
</style>
