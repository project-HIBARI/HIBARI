<script setup>
/**
 * 部品名: Music Memory Book — 思い出詳細
 */
import MemoryBookBreadcrumb from './MemoryBookBreadcrumb.vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'
import { MEMORY_BOOK_DETAIL_SAMPLE } from '../../../data/memoryBookData.js'
import { aosAttrs } from '../../../lib/aos.js'

const memory = MEMORY_BOOK_DETAIL_SAMPLE

const emit = defineEmits(['back', 'back-year', 'open-fanclub', 'coming-soon'])

const crumbs = [
  { label: 'Music Memory Book', action: 'top' },
  { label: '年別アルバム一覧', action: 'top' },
  { label: `${memory.year}年のMusic Memories`, action: 'year' },
  { label: '思い出の詳細' },
]

function onCrumb(action) {
  if (action === 'top') emit('back')
  if (action === 'year') emit('back-year')
}
</script>

<template>
  <div class="mmb-detail">
    <div class="mmb-detail__toolbar">
      <UiButton variant="ghost" size="sm" @click="emit('back-year')">
        ‹ 戻る
      </UiButton>
      <div class="mmb-detail__edit">
        <button type="button" class="mmb-detail__edit-btn" @click="emit('coming-soon', 'edit')">編集</button>
        <span class="mmb-detail__edit-sep">|</span>
        <button type="button" class="mmb-detail__edit-btn mmb-detail__edit-btn--danger" @click="emit('coming-soon', 'delete')">削除</button>
      </div>
    </div>

    <MemoryBookBreadcrumb :items="crumbs" @navigate="onCrumb" />

    <header class="mmb-detail__head" v-bind="aosAttrs()">
      <h1 class="mmb-detail__title">思い出の詳細</h1>
      <p class="mmb-detail__lead">あなたの大切な思い出をいつでも見返すことができます。</p>
    </header>

    <div class="mmb-detail__layout">
      <main class="mmb-detail__main">
        <article class="mmb-detail__card" v-bind="aosAttrs(80)">
          <span class="mmb-detail__cat">{{ memory.categoryLabel }}</span>
          <h2 class="mmb-detail__memory-title">{{ memory.title }}</h2>
          <dl class="mmb-detail__meta-row">
            <div><dt>日付</dt><dd>{{ memory.dateDisplay }}</dd></div>
            <div><dt>場所</dt><dd>{{ memory.location }}</dd></div>
            <div><dt>公開範囲</dt><dd>{{ memory.visibility }}</dd></div>
          </dl>
          <p class="mmb-detail__body">{{ memory.body }}</p>

          <figure class="mmb-detail__hero-img">
            <img :src="memory.mainImage" :alt="memory.title" class="mmb-detail__hero-photo" decoding="async" />
            <div class="mmb-detail__ribbon" aria-hidden="true" />
          </figure>

          <section class="mmb-detail__photos" aria-label="添付写真">
            <h3 class="mmb-detail__photos-title">添付写真</h3>
            <div class="mmb-detail__photos-grid">
              <figure v-for="(ph, i) in memory.photos" :key="i" class="mmb-detail__photo">
                <img :src="ph.src" :alt="ph.alt" loading="lazy" decoding="async" />
                <figcaption>{{ ph.alt }}</figcaption>
              </figure>
            </div>
          </section>

          <aside class="mmb-detail__ai" aria-label="AIからのメッセージ">
            <div class="mmb-detail__ai-head">
              <UiIco name="chat" :size="16" color="var(--murasaki-700)" />
              <h3>AIからのメッセージ</h3>
            </div>
            <p class="mmb-detail__ai-body">{{ memory.aiMessage }}</p>
            <p class="mmb-detail__ai-note">※ AIからのメッセージは自動生成された内容です</p>
          </aside>
        </article>

        <nav class="mmb-detail__pager" aria-label="思い出ナビゲーション" v-bind="aosAttrs(200)">
          <UiButton variant="outline" size="sm" :disabled="!memory.prevId" @click="emit('coming-soon', 'prev')">
            前の思い出
          </UiButton>
          <UiButton variant="ghost" size="sm" @click="emit('back-year')">一覧に戻る</UiButton>
          <UiButton variant="outline" size="sm" @click="emit('coming-soon', 'next')">
            次の思い出
          </UiButton>
        </nav>
      </main>

      <aside class="mmb-detail__sidebar" v-bind="aosAttrs(120)">
        <section class="mmb-detail__panel">
          <h3 class="mmb-detail__panel-title">この思い出の情報</h3>
          <dl class="mmb-detail__panel-dl">
            <div><dt>日付</dt><dd>{{ memory.dateDisplay }}</dd></div>
            <div><dt>場所</dt><dd>{{ memory.location }}</dd></div>
            <div><dt>カテゴリ</dt><dd>{{ memory.categoryLabel }}</dd></div>
            <div><dt>公開範囲</dt><dd>{{ memory.visibility }}</dd></div>
            <div><dt>メモ</dt><dd>{{ memory.memo }}</dd></div>
          </dl>
        </section>

        <section class="mmb-detail__panel">
          <h3 class="mmb-detail__panel-title">関連項目</h3>
          <ul class="mmb-detail__links">
            <li><button type="button" @click="emit('coming-soon', 'same-day')">同じ日の思い出をすべて見る</button></li>
            <li><button type="button" @click="emit('coming-soon', 'same-place')">同じ場所の思い出をすべて見る</button></li>
            <li><button type="button" @click="emit('coming-soon', 'same-cat')">同じカテゴリの思い出をすべて見る</button></li>
          </ul>
        </section>

        <section class="mmb-detail__panel mmb-detail__panel--accent">
          <h3 class="mmb-detail__panel-title">アルバム内での位置</h3>
          <p class="mmb-detail__album-ref">{{ memory.year }}年のMusic Memories</p>
          <p class="mmb-detail__album-month">{{ memory.monthLabel }}の思い出</p>
          <p class="mmb-detail__album-pos">{{ memory.totalInMonth }}件中{{ memory.indexInMonth }}件目</p>
          <UiButton variant="outline" size="sm" class="mmb-detail__month-btn" @click="emit('back-year')">
            この月の一覧を見る
          </UiButton>
        </section>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.mmb-detail__toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--sp-4);
}

.mmb-detail__edit {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.mmb-detail__edit-btn {
  padding: 0;
  border: 0;
  background: transparent;
  color: var(--site-text-muted);
  cursor: pointer;
  font-family: var(--ff-mincho);
}

.mmb-detail__edit-btn:hover {
  color: var(--murasaki-700);
}

.mmb-detail__edit-btn--danger:hover {
  color: var(--beni-600);
}

.mmb-detail__edit-sep {
  color: var(--site-border-strong);
}

.mmb-detail__head {
  margin-bottom: var(--sp-6);
}

.mmb-detail__title {
  margin: 0 0 8px;
  font-family: var(--ff-mincho);
  font-size: clamp(26px, 2.8vw, 32px);
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--murasaki-800);
}

.mmb-detail__lead {
  margin: 0;
  font-size: 14px;
  color: var(--site-text-muted);
}

.mmb-detail__layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 300px;
  gap: var(--sp-7);
  align-items: start;
}

.mmb-detail__card {
  padding: var(--sp-7);
  border-radius: 24px;
  border: 1px solid color-mix(in srgb, var(--kin-500) 28%, var(--site-border));
  background: var(--site-surface);
  box-shadow: var(--site-shadow-md);
}

.mmb-detail__cat {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 999px;
  background: var(--murasaki-100);
  font-family: var(--ff-mincho);
  font-size: 11px;
  letter-spacing: 0.08em;
  color: var(--murasaki-700);
  margin-bottom: 12px;
}

.mmb-detail__memory-title {
  margin: 0 0 var(--sp-5);
  font-family: var(--ff-mincho);
  font-size: clamp(22px, 2.2vw, 28px);
  font-weight: 700;
  line-height: 1.5;
  color: var(--site-text);
}

.mmb-detail__meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16px 32px;
  margin: 0 0 var(--sp-5);
  padding-bottom: var(--sp-5);
  border-bottom: 1px solid var(--site-border);
}

.mmb-detail__meta-row div {
  display: flex;
  gap: 8px;
  font-size: 13px;
}

.mmb-detail__meta-row dt {
  font-family: var(--ff-mincho);
  font-weight: 700;
  color: var(--kin-600);
}

.mmb-detail__meta-row dd {
  margin: 0;
  color: var(--site-text-muted);
}

.mmb-detail__body {
  margin: 0 0 var(--sp-6);
  font-size: 15px;
  line-height: 2.1;
  color: var(--site-text);
  white-space: pre-line;
}

.mmb-detail__hero-img {
  position: relative;
  margin: 0 0 var(--sp-6);
  padding: var(--sp-6);
  border-radius: var(--site-radius-lg);
  background:
    radial-gradient(ellipse at 50% 0%, rgba(243, 235, 246, 0.8) 0%, transparent 60%),
    var(--site-surface-muted);
  border: 1px solid var(--site-border);
  text-align: center;
}

.mmb-detail__hero-photo {
  max-width: 220px;
  max-height: 280px;
  object-fit: contain;
  filter: drop-shadow(0 12px 24px rgba(61, 36, 80, 0.15));
}

.mmb-detail__ribbon {
  position: absolute;
  top: 24px;
  right: 32px;
  width: 48px;
  height: 80px;
  background: linear-gradient(180deg, var(--murasaki-600), var(--murasaki-800));
  clip-path: polygon(0 0, 100% 0, 100% 85%, 50% 100%, 0 85%);
  opacity: 0.85;
}

.mmb-detail__photos-title {
  margin: 0 0 var(--sp-4);
  font-family: var(--ff-mincho);
  font-size: 15px;
  font-weight: 700;
  color: var(--site-text);
}

.mmb-detail__photos-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--sp-3);
  margin-bottom: var(--sp-6);
}

.mmb-detail__photo {
  margin: 0;
  border-radius: var(--site-radius-md);
  overflow: hidden;
  border: 1px solid var(--site-border);
  background: var(--site-surface-muted);
}

.mmb-detail__photo img {
  display: block;
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
}

.mmb-detail__photo figcaption {
  padding: 6px 8px;
  font-size: 10px;
  color: var(--site-text-muted);
  text-align: center;
}

.mmb-detail__ai {
  padding: var(--sp-5);
  border-radius: var(--site-radius-lg);
  background: linear-gradient(135deg, var(--murasaki-100) 0%, rgba(252, 232, 236, 0.5) 100%);
  border: 1px solid rgba(122, 80, 136, 0.2);
}

.mmb-detail__ai-head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.mmb-detail__ai-head h3 {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 14px;
  font-weight: 700;
  color: var(--murasaki-800);
}

.mmb-detail__ai-body {
  margin: 0 0 10px;
  font-size: 14px;
  line-height: 1.95;
  color: var(--site-text);
  white-space: pre-line;
}

.mmb-detail__ai-note {
  margin: 0;
  font-size: 10px;
  color: var(--site-text-light);
}

.mmb-detail__pager {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--sp-4);
  margin-top: var(--sp-6);
  padding-top: var(--sp-5);
  border-top: 1px solid var(--site-border);
}

.mmb-detail__panel {
  padding: var(--sp-5);
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--site-border);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
  margin-bottom: var(--sp-4);
}

.mmb-detail__panel--accent {
  background: linear-gradient(135deg, var(--site-surface) 0%, var(--murasaki-100) 100%);
  border-color: rgba(122, 80, 136, 0.2);
}

.mmb-detail__panel-title {
  margin: 0 0 var(--sp-4);
  font-family: var(--ff-mincho);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--murasaki-700);
  padding-bottom: var(--sp-3);
  border-bottom: 1px solid var(--site-border);
}

.mmb-detail__panel-dl {
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.mmb-detail__panel-dl div {
  display: grid;
  grid-template-columns: 72px 1fr;
  gap: 8px;
  font-size: 12px;
}

.mmb-detail__panel-dl dt {
  font-family: var(--ff-mincho);
  font-weight: 700;
  color: var(--kin-600);
}

.mmb-detail__panel-dl dd {
  margin: 0;
  color: var(--site-text-muted);
  line-height: 1.6;
}

.mmb-detail__links {
  list-style: none;
  margin: 0;
  padding: 0;
}

.mmb-detail__links button {
  display: block;
  width: 100%;
  padding: 10px 0;
  border: 0;
  border-bottom: 1px solid var(--site-border);
  background: transparent;
  text-align: left;
  font-family: var(--ff-mincho);
  font-size: 12px;
  color: var(--murasaki-700);
  cursor: pointer;
}

.mmb-detail__links button:hover {
  color: var(--murasaki-900);
}

.mmb-detail__album-ref {
  margin: 0 0 4px;
  font-family: var(--ff-mincho);
  font-size: 13px;
  font-weight: 700;
  color: var(--site-text);
}

.mmb-detail__album-month,
.mmb-detail__album-pos {
  margin: 0 0 4px;
  font-size: 12px;
  color: var(--site-text-muted);
}

.mmb-detail__month-btn {
  width: 100%;
  margin-top: var(--sp-4);
}
</style>
