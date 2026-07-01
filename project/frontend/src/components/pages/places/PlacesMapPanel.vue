<script setup>
/**
 * 部品名: ゆかりの地 — 地図パネル
 * 用途: 日本地図と現在エリア表示をまとめて表示
 */
import { computed } from 'vue'
import UiCard from '../../ui/UiCard.vue'
import JapanMap from '../../map/JapanMap.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const props = defineProps({
  places: { type: Array, required: true },
  selected: { type: Object, default: null },
  regionKey: { type: String, default: 'all' },
})

const emit = defineEmits(['select'])

const areaLabel = computed(() => {
  const r = HIBARU_DATA.placeRegions.find((x) => x.key === props.regionKey)
  return r ? r.areaLabel : '全国エリア'
})

const visibleCount = computed(() => props.places.length)
</script>

<template>
  <!-- 日本地図エリア -->
  <UiCard tone="warm" padding="md" class="places-map">
    <div class="places-map__head">
      <div>
        <p class="places-map__eyebrow">JAPAN MAP</p>
        <h3 class="places-map__area">{{ areaLabel }}</h3>
      </div>
      <p class="places-map__count">
        <span class="places-map__count-num">{{ visibleCount }}</span>
        <span class="places-map__count-label">スポット表示中</span>
      </p>
    </div>
    <div class="places-map__canvas">
      <JapanMap
        :places="places"
        :selected="selected"
        theme="light"
        @select="emit('select', $event)"
      />
    </div>
  </UiCard>
</template>

<style scoped>
.places-map {
  margin-bottom: var(--sp-6);
}
.places-map__head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--sp-4);
  margin-bottom: var(--sp-4);
  flex-wrap: wrap;
}
.places-map__eyebrow {
  margin: 0 0 4px;
  font-family: var(--ff-latin);
  font-size: 10px;
  letter-spacing: 0.22em;
  color: var(--kin-600);
}
.places-map__area {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--site-text);
}
.places-map__count {
  margin: 0;
  text-align: right;
}
.places-map__count-num {
  display: block;
  font-family: var(--ff-latin);
  font-size: 24px;
  font-weight: 700;
  color: var(--murasaki-600);
  line-height: 1;
}
.places-map__count-label {
  font-size: 11px;
  color: var(--site-text-muted);
  letter-spacing: 0.06em;
}
.places-map__canvas {
  border-radius: var(--site-radius-md);
  overflow: hidden;
  border: 1px solid var(--site-border);
}
</style>
