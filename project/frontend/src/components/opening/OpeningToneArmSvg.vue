<script setup>
/**
 * 部品名: トーンアーム SVG
 * 役割: レコードシーンの針アーム（回転は親が transform で付与）
 */
import { computed } from 'vue'

const props = defineProps({
  recordSize: { type: Number, required: true },
})

const armLen = computed(() => props.recordSize * 0.58)
const cwLen = computed(() => props.recordSize * 0.2)
const pivR = computed(() => props.recordSize * 0.03)
const cwR = computed(() => props.recordSize * 0.036)
const aw1 = computed(() => props.recordSize * 0.016)
const aw2 = computed(() => props.recordSize * 0.009)
const hsW = computed(() => props.recordSize * 0.038)
const margin = 20
const svgW = computed(() => Math.max(cwR.value, aw1.value / 2, hsW.value / 2) * 2 + margin * 2)
const svgH = computed(() => cwLen.value + armLen.value + margin * 2)
const ox = computed(() => svgW.value / 2)
const oy = computed(() => cwLen.value + margin)
</script>

<template>
  <svg
    :width="svgW"
    :height="svgH"
    :viewBox="`0 0 ${svgW} ${svgH}`"
    :style="{
      position: 'absolute',
      left: -ox + 'px',
      top: -oy + 'px',
      overflow: 'visible',
      pointerEvents: 'none',
    }"
  >
    <defs>
      <linearGradient id="taBodyGrad" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#9a7a42" />
        <stop offset="0.3" stop-color="#d4b878" />
        <stop offset="0.7" stop-color="#c9a961" />
        <stop offset="1" stop-color="#7a5a28" />
      </linearGradient>
      <radialGradient id="taPivotGrad" cx="38%" cy="32%">
        <stop offset="0" stop-color="#e8d090" />
        <stop offset="1" stop-color="#8a6a3a" />
      </radialGradient>
      <radialGradient id="taCwGrad" cx="35%" cy="32%">
        <stop offset="0" stop-color="#4a3a2a" />
        <stop offset="1" stop-color="#1a1410" />
      </radialGradient>
    </defs>
    <g :transform="`translate(${ox}, ${oy})`">
      <rect :x="-aw1 / 2" :y="-cwLen * 0.9" :width="aw1" :height="cwLen * 0.9" fill="url(#taBodyGrad)" />
      <rect :x="-cwR" :y="-cwLen * 0.95" :width="cwR * 2" :height="cwLen * 0.55" :rx="cwR * 0.25" fill="url(#taCwGrad)" stroke="#5a4a3a" stroke-width="1" />
      <rect :x="-cwR * 0.7" :y="-cwLen * 0.78" :width="cwR * 1.4" :height="cwLen * 0.18" rx="3" fill="#2a1a10" />
      <path
        :d="`M ${-aw1 / 2} 0 L ${-aw2 / 2} ${armLen * 0.82} L ${-hsW / 2} ${armLen * 0.88} L ${hsW / 2} ${armLen * 0.88} L ${aw2 / 2} ${armLen * 0.82} L ${aw1 / 2} 0 Z`"
        fill="url(#taBodyGrad)"
      />
      <circle :cx="aw1 * 1.4" :cy="armLen * 0.1" :r="aw1 * 0.6" fill="#c9a961" />
      <circle :cx="aw1 * 1.4" :cy="armLen * 0.1" :r="aw1 * 0.25" fill="#050302" />
      <circle cx="0" cy="0" :r="pivR" fill="url(#taPivotGrad)" stroke="#7a5a28" stroke-width="1.5" />
      <circle cx="0" cy="0" :r="pivR * 0.35" fill="#050302" />
      <path
        :d="`M ${-aw2 / 2} ${armLen * 0.82} L ${-hsW / 2} ${armLen * 0.88} L ${-hsW * 0.55} ${armLen * 1.0} L ${hsW * 0.55} ${armLen * 1.0} L ${hsW / 2} ${armLen * 0.88} L ${aw2 / 2} ${armLen * 0.82} Z`"
        fill="#5a3a1a"
        stroke="#c9a961"
        stroke-width="0.8"
      />
      <rect :x="-hsW * 0.5" :y="armLen * 1.0" :width="hsW * 1.0" :height="armLen * 0.055" rx="2" fill="#1e120a" stroke="#c9a961" stroke-width="0.6" />
      <line :x1="-hsW * 0.06" :y1="armLen * 1.055" :x2="-hsW * 0.1" :y2="armLen * 1.085" stroke="#c8c8c8" stroke-width="1.2" />
      <ellipse :cx="-hsW * 0.1" :cy="armLen * 1.085" rx="1.8" ry="2.2" fill="#f0f0f0" />
    </g>
  </svg>
</template>
