<script setup>
/**
 * 部品名: ゆかりの地 — 関連楽曲
 * 用途: スポットと結びつく楽曲の紹介（再生なし）
 */
import SectionTitle from '../../ui/SectionTitle.vue'
import UiCard from '../../ui/UiCard.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const songs = HIBARU_DATA.placeRelatedSongs
</script>

<template>
  <!-- ゆかりの地に関連する楽曲 -->
  <section class="places-songs" aria-label="関連楽曲">
    <SectionTitle title="ゆかりの地に関連する楽曲" sub="Related Songs" size="md" />

    <div class="places-songs__list">
      <UiCard v-for="s in songs" :key="s.id" tone="white" padding="md" class="places-songs__card">
        <div class="places-songs__head">
          <span class="places-songs__note" aria-hidden="true">♪</span>
          <h3 class="places-songs__title">{{ s.song }}</h3>
        </div>
        <p class="places-songs__place">{{ s.placeName }}</p>
        <p class="places-songs__desc">{{ s.description }}</p>
      </UiCard>
    </div>
  </section>
</template>

<style scoped>
.places-songs {
  margin-bottom: var(--sp-7);
}
.places-songs__list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--sp-4);
}
.places-songs__head {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  margin-bottom: 6px;
}
.places-songs__note {
  font-size: var(--font-size-body);
  color: var(--murasaki-500);
}
.places-songs__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-emphasis);
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--site-text);
}
.places-songs__place {
  margin: 0 0 8px;
  font-family: var(--ff-mono);
  font-size: var(--font-size-badge);
  letter-spacing: 0.1em;
  color: var(--kin-600);
}
.places-songs__desc {
  margin: 0;
  font-size: var(--font-size-caption);
  line-height: 1.75;
  color: var(--site-text-muted);
}

@media (max-width: 768px) {
  .places-songs__list {
    grid-template-columns: 1fr;
  }
}
</style>
