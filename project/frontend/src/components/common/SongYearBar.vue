<script setup>
/**
 * 部品名: 楽曲の年代バー
 * 役割: 1920〜1990年を横軸に、楽曲の発売年の位置を金色マーカーで示す
 */
import { computed } from 'vue'

const YEAR_MIN = 1920
const YEAR_MAX = 1990

const props = defineProps({
  year: { type: Number, required: true },
})

const markerPosition = computed(() => {
  const clamped = Math.min(Math.max(props.year, YEAR_MIN), YEAR_MAX)
  return ((clamped - YEAR_MIN) / (YEAR_MAX - YEAR_MIN)) * 100
})
</script>

<template>
  <div class="song-year-bar" role="img" :aria-label="`発売年 ${year}年（${YEAR_MIN}〜${YEAR_MAX}年の年代バー上の位置）`">
    <div class="song-year-bar__track">
      <span class="song-year-bar__marker" :style="{ left: markerPosition + '%' }" aria-hidden="true"></span>
    </div>
    <div class="song-year-bar__labels" aria-hidden="true">
      <span>{{ YEAR_MIN }}</span>
      <span class="song-year-bar__year">{{ year }}</span>
      <span>{{ YEAR_MAX }}</span>
    </div>
  </div>
</template>

<style scoped>
.song-year-bar {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.song-year-bar__track {
  position: relative;
  height: 3px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.15);
}

.song-year-bar__marker {
  position: absolute;
  top: 50%;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--kin-400);
  box-shadow: 0 0 0 2px rgba(217, 189, 125, 0.25);
  transform: translate(-50%, -50%);
}

.song-year-bar__labels {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-badge);
  letter-spacing: 0.03em;
  color: rgba(248, 244, 239, 0.4);
}

.song-year-bar__year {
  color: var(--kin-400);
  font-weight: 600;
}
</style>
