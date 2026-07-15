<script setup>
/**
 * 部品名: Music Memory Book — 年別アルバム詳細
 */
import { computed } from 'vue'
import MemoryBookAlbumCover from './MemoryBookAlbumCover.vue'
import MemoryBookBreadcrumb from './MemoryBookBreadcrumb.vue'
import MemoryBookPremiumBand from './MemoryBookPremiumBand.vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'
import { aosAttrs } from '../../../lib/aos.js'

const props = defineProps({
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
  data: { type: Object, required: true },
  coverDesignId: { type: Number, default: 1 },
  isPremium: { type: Boolean, default: false },
})

const iconMap = {
  flower: 'flower',
  chat: 'chat',
  music: 'disc',
}

const emit = defineEmits(['back', 'open-detail', 'open-fanclub', 'open-premium', 'export-pdf', 'share', 'open-recap', 'change-cover', 'retry'])

const crumbs = computed(() => [
  { label: 'Music Memory Book', action: 'top' },
  { label: '年別アルバム', action: 'top' },
  { label: `${props.data.year}年の思い出` },
])

function onCrumb(action) {
  if (action === 'top') emit('back')
}

function openItem(item) {
  emit('open-detail', item.id)
}

function onPremiumAction(action) {
  if (props.isPremium) {
    emit(action)
    return
  }
  emit('open-premium')
}
</script>

<template>
  <div class="mmb-year">
    <div v-if="loading && !data.timeline.length" class="mmb-state mmb-state--loading">
      読み込み中です…
    </div>

    <div v-else-if="error" class="mmb-state mmb-state--error">
      <p>{{ error }}</p>
      <UiButton variant="outline" size="sm" @click="emit('retry')">もう一度お試しください</UiButton>
    </div>

    <template v-else>
    <div v-if="!isPremium" class="mmb-year__limit-banner" role="note">
      一般会員の方は閲覧のみ可能です。PDF保存・シェア・AI振り返り・表紙変更はプレミアム会員限定です。
    </div>

    <MemoryBookBreadcrumb :items="crumbs" @navigate="onCrumb" />

    <header class="mmb-year__head" v-bind="aosAttrs()">
      <h1 class="mmb-year__title">{{ data.year }}年のMusic Memories</h1>
      <p class="mmb-year__lead">
        {{ data.year }}年のあなたの美空ひばりとの思い出をまとめたアルバムです。<br />
        1年間の活動を振り返り、かけがえのない思い出を残しましょう。
      </p>
    </header>

    <div class="mmb-year__layout">
      <!-- Left: album -->
      <aside class="mmb-year__aside" v-bind="aosAttrs(80)">
        <MemoryBookAlbumCover :year="data.year" :design-id="coverDesignId" size="lg" />
        <UiButton
          variant="outline"
          size="sm"
          class="mmb-year__cover-btn"
          :class="{ 'mmb-year__btn--locked': !isPremium }"
          @click="onPremiumAction('change-cover')"
        >
          {{ isPremium ? 'アルバムの表紙を変更する' : '表紙変更（プレミアム限定）' }}
        </UiButton>
      </aside>

      <!-- Right: timeline -->
      <div class="mmb-year__main">
        <div class="mmb-year__summary" v-bind="aosAttrs(100)">
          <div class="mmb-year__stat">
            <span class="mmb-year__stat-label">献花</span>
            <span class="mmb-year__stat-val">{{ data.summary.flowers }}<small>件</small></span>
          </div>
          <div class="mmb-year__stat">
            <span class="mmb-year__stat-label">思い出投稿</span>
            <span class="mmb-year__stat-val">{{ data.summary.posts }}<small>件</small></span>
          </div>
          <div class="mmb-year__stat">
            <span class="mmb-year__stat-label">お気に入り楽曲</span>
            <span class="mmb-year__stat-val">{{ data.summary.songs }}<small>曲</small></span>
          </div>
          <div class="mmb-year__stat">
            <span class="mmb-year__stat-label">AIとの会話</span>
            <span class="mmb-year__stat-val">{{ data.summary.aiChats }}<small>件</small></span>
          </div>
        </div>

        <section class="mmb-year__timeline" aria-label="月別タイムライン">
          <p v-if="!data.timeline.length" class="mmb-year__empty">この年の思い出はまだありません。</p>
          <article
            v-for="(item, i) in data.timeline"
            :key="item.id"
            class="mmb-year__entry"
            v-bind="aosAttrs(120 + i * 60)"
          >
            <div class="mmb-year__entry-month">{{ item.monthLabel }}</div>
            <button type="button" class="mmb-year__entry-card" @click="openItem(item)">
              <div class="mmb-year__entry-body">
                <span class="mmb-year__entry-cat">{{ item.categoryLabel }}</span>
                <h2 class="mmb-year__entry-title">{{ item.title }}</h2>
                <p class="mmb-year__entry-date">日付：{{ item.date }}</p>
                <p class="mmb-year__entry-desc">{{ item.description }}</p>
              </div>
              <div class="mmb-year__entry-visual">
                <div class="mmb-year__entry-icon">
                  <UiIco :name="iconMap[item.icon] || 'bookmark'" :size="28" color="var(--murasaki-600)" />
                </div>
                <span class="mmb-year__entry-arrow" aria-hidden="true">›</span>
              </div>
            </button>
          </article>
        </section>

        <div class="mmb-year__actions" v-bind="aosAttrs(400)">
          <UiButton
            variant="outline"
            size="md"
            :class="{ 'mmb-year__btn--locked': !isPremium }"
            @click="onPremiumAction('export-pdf')"
          >
            {{ isPremium ? 'このアルバムをPDFで保存' : 'PDF保存（プレミアム限定）' }}
          </UiButton>
          <UiButton
            variant="outline"
            size="md"
            :class="{ 'mmb-year__btn--locked': !isPremium }"
            @click="onPremiumAction('share')"
          >
            <UiIco name="share" :size="14" />
            {{ isPremium ? 'アルバムをシェアする' : 'シェア（プレミアム限定）' }}
          </UiButton>
          <UiButton
            variant="primary"
            size="md"
            :class="{ 'mmb-year__btn--locked': !isPremium }"
            @click="onPremiumAction('open-recap')"
          >
            {{ isPremium ? 'AIによる1年の振り返りを見る' : 'AI振り返り（プレミアム限定）' }}
          </UiButton>
        </div>
      </div>
    </div>

    <MemoryBookPremiumBand v-if="!isPremium" compact @open-fanclub="emit('open-fanclub')" />
    </template>
  </div>
</template>

<style scoped>
.mmb-year__limit-banner {
  margin-bottom: var(--sp-5);
  padding: var(--sp-4) var(--sp-5);
  border-radius: var(--site-radius-lg);
  border: 1px solid rgba(122, 80, 136, 0.18);
  background: rgba(245, 235, 248, 0.65);
  font-size: 13px;
  line-height: 1.75;
  color: var(--site-text-muted);
}

.mmb-year__btn--locked {
  opacity: 0.88;
}

.mmb-year__head {
  margin-bottom: var(--sp-7);
}

.mmb-year__title {
  margin: 0 0 12px;
  font-family: var(--ff-mincho);
  font-size: clamp(28px, 3vw, 36px);
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--murasaki-800);
}

.mmb-year__lead {
  margin: 0;
  font-size: 14px;
  line-height: 1.95;
  color: var(--site-text-muted);
}

.mmb-year__layout {
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr);
  gap: var(--sp-8);
  align-items: start;
}

.mmb-year__aside {
  position: sticky;
  top: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--sp-4);
}

.mmb-year__cover-btn {
  width: 100%;
  max-width: 220px;
}

.mmb-year__summary {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--sp-4);
  margin-bottom: var(--sp-7);
}

.mmb-year__stat {
  padding: var(--sp-4) var(--sp-5);
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--site-border);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
  text-align: center;
}

.mmb-year__stat-label {
  display: block;
  font-family: var(--ff-mincho);
  font-size: 11px;
  letter-spacing: 0.06em;
  color: var(--site-text-muted);
  margin-bottom: 6px;
}

.mmb-year__stat-val {
  font-family: var(--ff-latin);
  font-size: 28px;
  font-weight: 700;
  color: var(--murasaki-700);
  line-height: 1;
}

.mmb-year__stat-val small {
  font-size: 12px;
  font-family: var(--ff-mincho);
  margin-left: 2px;
}

.mmb-year__timeline {
  display: flex;
  flex-direction: column;
  gap: var(--sp-5);
  margin-bottom: var(--sp-7);
  position: relative;
  padding-left: 48px;
}

.mmb-year__timeline::before {
  content: '';
  position: absolute;
  left: 18px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: linear-gradient(180deg, var(--kin-400), var(--murasaki-400));
  opacity: 0.45;
}

.mmb-year__entry {
  position: relative;
}

.mmb-year__entry-month {
  position: absolute;
  left: -48px;
  top: 20px;
  width: 36px;
  font-family: var(--ff-latin);
  font-size: 13px;
  font-weight: 700;
  color: var(--kin-600);
  text-align: right;
}

.mmb-year__entry-card {
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

.mmb-year__entry-card:hover {
  transform: translateX(4px);
  box-shadow: var(--site-shadow-md);
  border-color: rgba(122, 80, 136, 0.25);
}

.mmb-year__entry-cat {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 999px;
  background: var(--murasaki-100);
  font-family: var(--ff-mincho);
  font-size: 10px;
  letter-spacing: 0.06em;
  color: var(--murasaki-700);
  margin-bottom: 8px;
}

.mmb-year__entry-title {
  margin: 0 0 8px;
  font-family: var(--ff-mincho);
  font-size: 17px;
  font-weight: 700;
  color: var(--site-text);
  line-height: 1.5;
}

.mmb-year__entry-date {
  margin: 0 0 6px;
  font-family: var(--ff-mono);
  font-size: 11px;
  color: var(--site-text-light);
}

.mmb-year__entry-desc {
  margin: 0;
  font-size: 13px;
  line-height: 1.8;
  color: var(--site-text-muted);
}

.mmb-year__entry-visual {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--sp-3);
  min-width: 72px;
}

.mmb-year__entry-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  background: var(--site-surface-muted);
  border: 1px solid var(--site-border);
  display: flex;
  align-items: center;
  justify-content: center;
}

.mmb-year__entry-arrow {
  font-size: 22px;
  color: var(--murasaki-500);
}

.mmb-year__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-3);
  padding: var(--sp-5);
  border-radius: var(--site-radius-lg);
  background: var(--site-surface-muted);
  border: 1px dashed var(--site-border-strong);
}

.mmb-year__empty,
.mmb-state {
  padding: var(--sp-8) var(--sp-6);
  text-align: center;
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--site-border);
  background: var(--site-surface);
}

.mmb-year__empty {
  color: var(--site-text-muted);
  font-size: 14px;
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
