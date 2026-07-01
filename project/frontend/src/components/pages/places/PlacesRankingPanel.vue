<script setup>
/**
 * 部品名: ゆかりの地 — 人気ランキング
 * 用途: 訪問人気の高いスポットを3〜5件表示
 */
import { computed } from 'vue'
import SectionTitle from '../../ui/SectionTitle.vue'
import UiCard from '../../ui/UiCard.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const emit = defineEmits(['select'])

const items = computed(() =>
  HIBARU_DATA.placeRanking.map((r) => {
    const place = HIBARU_DATA.places.find((p) => p.id === r.placeId)
    return { ...r, place }
  }).filter((x) => x.place),
)

const medals = ['🥇', '🥈', '🥉']
</script>

<template>
  <!-- 人気スポットランキング -->
  <section class="places-rank" aria-label="人気スポットランキング">
    <SectionTitle title="人気スポット" sub="Popular Places" size="md" />

    <div class="places-rank__list">
      <button
        v-for="item in items"
        :key="item.placeId"
        type="button"
        class="places-rank__item"
        :aria-label="item.label + 'の詳細'"
        @click="emit('select', item.place)"
      >
        <UiCard tone="white" padding="sm" class="places-rank__card">
          <span class="places-rank__medal" aria-hidden="true">
            {{ item.rank <= 3 ? medals[item.rank - 1] : item.rank }}
          </span>
          <div class="places-rank__body">
            <span class="places-rank__name">{{ item.label }}</span>
            <span class="places-rank__area">{{ item.place?.prefecture }}</span>
          </div>
          <span class="places-rank__score">{{ item.score }}</span>
        </UiCard>
      </button>
    </div>
  </section>
</template>

<style scoped>
.places-rank {
  margin-bottom: var(--sp-7);
}
.places-rank__list {
  display: flex;
  flex-direction: column;
  gap: var(--sp-3);
}
.places-rank__item {
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
  text-align: left;
  width: 100%;
}
.places-rank__card {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
  transition: transform 0.2s, box-shadow 0.2s;
}
.places-rank__item:hover .places-rank__card {
  transform: translateX(4px);
  box-shadow: var(--site-shadow-md);
}
.places-rank__medal {
  flex-shrink: 0;
  width: 36px;
  text-align: center;
  font-size: 20px;
  font-family: var(--ff-latin);
  font-weight: 700;
  color: var(--kin-600);
}
.places-rank__body {
  flex: 1;
  min-width: 0;
}
.places-rank__name {
  display: block;
  font-family: var(--ff-mincho);
  font-size: 15px;
  font-weight: 700;
  color: var(--site-text);
  letter-spacing: 0.04em;
}
.places-rank__area {
  display: block;
  margin-top: 2px;
  font-size: 11px;
  color: var(--site-text-muted);
}
.places-rank__score {
  flex-shrink: 0;
  font-family: var(--ff-mono);
  font-size: 14px;
  font-weight: 700;
  color: var(--murasaki-600);
}
.places-rank__item:focus-visible .places-rank__card {
  outline: 2px solid var(--murasaki-500);
  outline-offset: 2px;
}
</style>
