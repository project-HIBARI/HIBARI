<script setup>
/**
 * 部品名: ゆかりの地 — エピソードパネル
 * 用途: スポットにまつわる短いエピソードカードを表示
 */
import SectionTitle from '../../ui/SectionTitle.vue'
import UiCard from '../../ui/UiCard.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const episodes = HIBARU_DATA.placeEpisodes
</script>

<template>
  <!-- ゆかりの地エピソード -->
  <section class="places-episodes" aria-label="ゆかりの地エピソード">
    <SectionTitle title="ゆかりの地エピソード" sub="Episodes" size="md" />

    <div class="places-episodes__grid">
      <UiCard v-for="ep in episodes" :key="ep.id" tone="warm" padding="md" class="places-episodes__card">
        <h3 class="places-episodes__heading">{{ ep.heading }}</h3>
        <p class="places-episodes__body">{{ ep.body }}</p>
        <p class="places-episodes__place">
          <span aria-hidden="true">📍</span>
          {{ ep.placeName }}
        </p>
      </UiCard>
    </div>
  </section>
</template>

<style scoped>
.places-episodes {
  margin-bottom: var(--sp-7);
}
.places-episodes__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--sp-4);
}
.places-episodes__heading {
  margin: 0 0 10px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-body);
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--site-text);
  line-height: 1.45;
}
.places-episodes__body {
  margin: 0 0 var(--sp-3);
  font-size: var(--font-size-button);
  line-height: 1.85;
  color: var(--site-text-muted);
}
.places-episodes__place {
  margin: 0;
  padding-top: var(--sp-3);
  border-top: 1px solid var(--site-border);
  font-size: var(--font-size-caption);
  color: var(--murasaki-700);
  letter-spacing: 0.04em;
}

@media (max-width: 768px) {
  .places-episodes__grid {
    grid-template-columns: 1fr;
  }
}
</style>
