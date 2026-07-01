<script setup>
/**
 * 部品名: 日本地図（ゆかりの地ピン）
 * 役割: 緯度経度を簡易投影してピンと選択ハイライトを表示
 */
import { ref, computed } from 'vue'

const props = defineProps({
  places: { type: Array, required: true },
  selected: { type: Object, default: null },
  /** light=ライトテーマ / dark=従来のダーク地図 */
  theme: { type: String, default: 'light' },
})

const emit = defineEmits(['select'])

const hover = ref(null)

const minLat = 30.5
const maxLat = 45.8
const minLng = 128.5
const maxLng = 146
const W = 720
const H = 800
const PAD = 60

function proj(lat, lng) {
  return {
    x: ((lng - minLng) / (maxLng - minLng)) * (W - PAD * 2) + PAD,
    y: H - ((lat - minLat) / (maxLat - minLat)) * (H - PAD * 2) - PAD,
  }
}

const islands = [
  {
    name: 'Hokkaidō',
    d: 'M 510 100 C 540 85, 585 90, 615 120 C 640 150, 640 190, 620 215 C 600 240, 565 250, 540 240 C 520 260, 495 255, 480 235 C 460 215, 455 185, 470 160 C 455 140, 465 110, 510 100 Z',
  },
  {
    name: 'Honshū',
    d: 'M 175 620 C 180 590, 210 575, 245 575 C 275 575, 298 570, 320 555 C 350 550, 378 540, 395 520 C 412 500, 420 480, 438 465 C 460 450, 485 445, 500 425 C 520 405, 528 380, 520 355 C 515 335, 500 325, 480 325 C 455 325, 430 340, 410 360 C 388 380, 365 395, 338 410 C 310 425, 280 440, 260 460 C 240 478, 225 498, 215 520 C 205 545, 195 565, 180 585 C 170 600, 170 612, 175 620 Z M 502 340 C 515 332, 525 342, 520 355 M 438 465 C 450 455, 462 458, 458 470',
  },
  {
    name: 'Kyūshū',
    d: 'M 130 660 C 145 645, 170 648, 185 665 C 200 680, 198 710, 185 728 C 172 745, 148 748, 132 735 C 118 720, 115 690, 130 660 Z',
  },
  {
    name: 'Shikoku',
    d: 'M 215 660 C 240 653, 268 660, 280 675 C 285 690, 270 702, 248 702 C 228 702, 212 692, 210 675 C 210 667, 212 662, 215 660 Z',
  },
  {
    name: 'Okinawa',
    d: 'M 60 760 C 68 755, 78 760, 75 770 C 70 780, 58 778, 56 770 Z',
  },
]

const chainDots = [
  [95, 745],
  [85, 755],
  [75, 758],
  [68, 758],
]

const selPos = computed(() => (props.selected ? proj(props.selected.lat, props.selected.lng) : null))

const isLight = computed(() => props.theme === 'light')

const colors = computed(() =>
  isLight.value
    ? {
        wrap: { background: '#f5f0e8', border: '1px solid rgba(90, 60, 40, 0.15)' },
        sea0: '#e8eef4',
        sea1: '#dce6ee',
        grid: 'rgba(122, 80, 136, 0.08)',
        dots: 'rgba(201, 169, 97, 0.12)',
        land0: '#f0e6d8',
        land1: '#e8dcc8',
        coast: '#c9a961',
        road: 'rgba(122, 80, 136, 0.15)',
        labelBg: 'rgba(255,255,255,0.92)',
        labelBorder: '#c9a961',
        title: '#3a2b22',
        sub: '#a8873f',
        meta: '#8a7568',
        compass: '#f5f0e8',
        pin: '#a8262b',
        pinHi: '#c0342f',
        pinGlow: '#7a5088',
        calloutBg: '#ffffff',
        calloutText: '#3a2b22',
        calloutSub: '#a8873f',
        line: '#c9a961',
      }
    : {
        wrap: { background: '#0d0806', border: '1px solid #3a2a1a' },
        sea0: '#0f0a07',
        sea1: '#050302',
        grid: 'rgba(201,169,97,0.06)',
        dots: 'rgba(201,169,97,0.08)',
        land0: '#2a1d14',
        land1: '#1a120c',
        coast: '#8a6a3a',
        road: '#3a2a1a',
        labelBg: '#050302',
        labelBorder: '#c9a961',
        title: '#f4ede0',
        sub: '#c9a961',
        meta: '#8a6a3a',
        compass: '#050302',
        pin: '#8b1a1a',
        pinHi: '#c0342f',
        pinGlow: '#8b1a1a',
        calloutBg: '#0d0806',
        calloutText: '#f4ede0',
        calloutSub: '#c9a961',
        line: '#c9a961',
      },
)

function calloutBox() {
  if (!props.selected) return null
  const { x, y } = proj(props.selected.lat, props.selected.lng)
  const boxW = 180
  const boxH = 54
  const above = y > H / 2
  const bx = Math.min(Math.max(x - boxW / 2, 10), W - boxW - 10)
  const by = above ? y - boxH - 24 : y + 24
  return { x, y, bx, by, boxW, boxH, above }
}
</script>

<template>
  <div
    class="japan-map"
    :class="{ 'japan-map--light': isLight }"
    :style="{ aspectRatio: `${W} / ${H}`, ...colors.wrap }"
  >
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" height="100%" style="display: block">
      <defs>
        <pattern id="jpgrid" width="24" height="24" patternUnits="userSpaceOnUse">
          <path d="M 24 0 L 0 0 0 24" fill="none" :stroke="colors.grid" stroke-width="0.5" />
        </pattern>
        <pattern id="jpdots" width="6" height="6" patternUnits="userSpaceOnUse">
          <circle cx="3" cy="3" r="0.4" :fill="colors.dots" />
        </pattern>
        <radialGradient id="jpsea" cx="0.5" cy="0.5" r="0.7">
          <stop offset="0" :stop-color="colors.sea0" />
          <stop offset="1" :stop-color="colors.sea1" />
        </radialGradient>
        <linearGradient id="jpland" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" :stop-color="colors.land0" />
          <stop offset="1" :stop-color="colors.land1" />
        </linearGradient>
        <filter id="pinglow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="3" />
        </filter>
      </defs>

      <rect :width="W" :height="H" fill="url(#jpsea)" />
      <rect :width="W" :height="H" fill="url(#jpgrid)" />
      <rect :width="W" :height="H" fill="url(#jpdots)" />

      <g v-for="lat in [35, 40]" :key="'lat' + lat">
        <line
          :x1="20"
          :x2="W - 20"
          :y1="proj(lat, minLng).y"
          :y2="proj(lat, minLng).y"
          stroke="#c9a961"
          stroke-width="0.3"
          stroke-dasharray="2 6"
          :opacity="isLight ? 0.5 : 0.4"
        />
        <text :x="24" :y="proj(lat, minLng).y - 4" font-family="'JetBrains Mono', monospace" font-size="8" :fill="colors.sub" :opacity="isLight ? 0.8 : 0.6">
          {{ lat }}°N
        </text>
      </g>
      <g v-for="lng in [135, 140]" :key="'lng' + lng">
        <line
          :y1="20"
          :y2="H - 20"
          :x1="proj(minLat, lng).x"
          :x2="proj(minLat, lng).x"
          :stroke="colors.line"
          stroke-width="0.3"
          stroke-dasharray="2 6"
          :opacity="isLight ? 0.5 : 0.4"
        />
        <text :y="H - 22" :x="proj(minLat, lng).x + 4" font-family="'JetBrains Mono', monospace" font-size="8" :fill="colors.sub" :opacity="isLight ? 0.8 : 0.6">
          {{ lng }}°E
        </text>
      </g>

      <path
        v-for="(isle, i) in islands"
        :key="i"
        :d="isle.d"
        fill="url(#jpland)"
        :stroke="colors.coast"
        stroke-width="1"
        stroke-linejoin="round"
      />
      <circle v-for="(cd, i) in chainDots" :key="'cd' + i" :cx="cd[0]" :cy="cd[1]" r="1.5" :fill="colors.road" />

      <g :stroke="colors.road" stroke-width="0.5" fill="none" :opacity="isLight ? 0.5 : 0.7">
        <path d="M 245 575 Q 260 555, 280 555" />
        <path d="M 320 555 Q 340 545, 360 530" />
        <path d="M 395 520 Q 410 500, 430 490" />
        <path d="M 470 445 Q 490 435, 500 425" />
        <path d="M 260 460 Q 275 450, 295 442" />
      </g>

      <g>
        <rect x="20" y="20" width="200" height="58" :fill="colors.labelBg" :stroke="colors.labelBorder" stroke-width="0.8" />
        <text x="30" y="42" font-family="'Shippori Mincho', serif" font-size="16" font-weight="700" :fill="colors.title" letter-spacing="3">ゆかりの地</text>
        <text x="30" y="58" font-family="'Playfair Display', serif" font-style="italic" font-size="10" :fill="colors.sub" letter-spacing="2">PLACES · PILGRIMAGE</text>
        <text x="30" y="72" font-family="'JetBrains Mono', monospace" font-size="8" :fill="colors.meta" letter-spacing="2">{{ places.length }} LOCATIONS</text>
      </g>

      <g :transform="`translate(${W - 70}, 70)`">
        <circle r="28" :fill="colors.compass" :stroke="colors.labelBorder" stroke-width="0.8" />
        <path d="M 0,-20 L 5,0 L 0,20 L -5,0 Z" :fill="colors.pin" />
        <path d="M 0,-20 L 5,0 L 0,0 Z" :fill="colors.sub" />
        <text y="-32" text-anchor="middle" font-family="'Playfair Display', serif" font-size="11" font-style="italic" :fill="colors.sub">N</text>
        <text y="42" text-anchor="middle" font-family="'Playfair Display', serif" font-size="9" font-style="italic" :fill="colors.meta">S</text>
        <text x="-34" y="3" text-anchor="middle" font-family="'Playfair Display', serif" font-size="9" font-style="italic" :fill="colors.meta">W</text>
        <text x="34" y="3" text-anchor="middle" font-family="'Playfair Display', serif" font-size="9" font-style="italic" :fill="colors.meta">E</text>
      </g>

      <g :transform="`translate(40, ${H - 40})`">
        <line x1="0" y1="0" x2="100" y2="0" :stroke="colors.line" stroke-width="1" />
        <line x1="0" y1="-4" x2="0" y2="4" :stroke="colors.line" stroke-width="1" />
        <line x1="50" y1="-3" x2="50" y2="3" :stroke="colors.line" stroke-width="1" />
        <line x1="100" y1="-4" x2="100" y2="4" :stroke="colors.line" stroke-width="1" />
        <text x="0" y="16" font-family="'JetBrains Mono', monospace" font-size="9" :fill="colors.sub">0</text>
        <text x="50" y="16" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="9" :fill="colors.sub">150</text>
        <text x="100" y="16" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="9" :fill="colors.sub">300 km</text>
      </g>

      <g v-if="selPos">
        <circle
          v-for="r in [1, 2, 3]"
          :key="'ring' + r"
          :cx="selPos.x"
          :cy="selPos.y"
          :r="12 + r * 8"
          fill="none"
          stroke="#c0342f"
          stroke-width="1"
          :opacity="0.4 - r * 0.1"
        >
          <animate attributeName="r" :from="12 + r * 8" :to="30 + r * 10" dur="2.4s" :begin="`${r * 0.4}s`" repeatCount="indefinite" />
          <animate attributeName="opacity" :from="0.5 - r * 0.1" to="0" dur="2.4s" :begin="`${r * 0.4}s`" repeatCount="indefinite" />
        </circle>
      </g>

      <g v-if="selected">
        <line
          v-for="p in places.filter((x) => x.id !== selected.id)"
          :key="'ln' + p.id"
          :x1="proj(selected.lat, selected.lng).x"
          :y1="proj(selected.lat, selected.lng).y"
          :x2="proj(p.lat, p.lng).x"
          :y2="proj(p.lat, p.lng).y"
          :stroke="colors.line"
          stroke-width="0.4"
          stroke-dasharray="1 4"
          :opacity="isLight ? 0.35 : 0.25"
        />
      </g>

      <g
        v-for="(p, i) in places"
        :key="p.id"
        style="cursor: pointer"
        @click="emit('select', p)"
        @mouseenter="hover = p.id"
        @mouseleave="hover = null"
      >
        <ellipse
          :cx="proj(p.lat, p.lng).x"
          :cy="proj(p.lat, p.lng).y + 2"
          :rx="selected && selected.id === p.id ? 8 : 4"
          ry="2"
          fill="#000"
          :opacity="isLight ? 0.2 : 0.5"
        />
        <circle
          v-if="(selected && selected.id === p.id) || hover === p.id"
          :cx="proj(p.lat, p.lng).x"
          :cy="proj(p.lat, p.lng).y"
          :r="selected && selected.id === p.id ? 14 : 10"
          :fill="colors.pinGlow"
          opacity="0.25"
          filter="url(#pinglow)"
        />
        <path
          :d="`M ${proj(p.lat, p.lng).x} ${proj(p.lat, p.lng).y - (selected && selected.id === p.id ? 16 : 10)}
              C ${proj(p.lat, p.lng).x - (selected && selected.id === p.id ? 8 : 5)} ${proj(p.lat, p.lng).y - (selected && selected.id === p.id ? 16 : 10)},
                ${proj(p.lat, p.lng).x - (selected && selected.id === p.id ? 10 : 6)} ${proj(p.lat, p.lng).y - (selected && selected.id === p.id ? 6 : 3)},
                ${proj(p.lat, p.lng).x} ${proj(p.lat, p.lng).y + 2}
              C ${proj(p.lat, p.lng).x + (selected && selected.id === p.id ? 10 : 6)} ${proj(p.lat, p.lng).y - (selected && selected.id === p.id ? 6 : 3)},
                ${proj(p.lat, p.lng).x + (selected && selected.id === p.id ? 8 : 5)} ${proj(p.lat, p.lng).y - (selected && selected.id === p.id ? 16 : 10)},
                ${proj(p.lat, p.lng).x} ${proj(p.lat, p.lng).y - (selected && selected.id === p.id ? 16 : 10)} Z`"
          :fill="selected && selected.id === p.id ? colors.pinHi : colors.pin"
          :stroke="colors.sub"
          :stroke-width="selected && selected.id === p.id ? 1.5 : 0.8"
        />
        <circle
          :cx="proj(p.lat, p.lng).x - (selected && selected.id === p.id ? 2 : 1)"
          :cy="proj(p.lat, p.lng).y - (selected && selected.id === p.id ? 11 : 7)"
          :r="selected && selected.id === p.id ? 2 : 1.2"
          :fill="isLight ? '#fff' : '#f4ede0'"
          opacity="0.7"
        />
        <circle
          :cx="proj(p.lat, p.lng).x + 10"
          :cy="proj(p.lat, p.lng).y - 10"
          r="7"
          :fill="colors.sub"
          :stroke="isLight ? '#fff' : '#0d0806'"
          stroke-width="1"
          :opacity="(selected && selected.id === p.id) || hover === p.id ? 1 : 0"
        />
        <text
          :x="proj(p.lat, p.lng).x + 10"
          :y="proj(p.lat, p.lng).y - 7"
          text-anchor="middle"
          font-family="'Playfair Display', serif"
          font-size="8"
          font-weight="700"
          :fill="isLight ? '#3a2b22' : '#0d0806'"
          :opacity="(selected && selected.id === p.id) || hover === p.id ? 1 : 0"
        >
          {{ i + 1 }}
        </text>
      </g>

      <g v-if="selected && calloutBox()">
        <line
          :x1="calloutBox().x"
          :y1="calloutBox().y + (calloutBox().above ? -16 : 4)"
          :x2="calloutBox().x"
          :y2="calloutBox().above ? calloutBox().by + calloutBox().boxH : calloutBox().by"
          :stroke="colors.line"
          stroke-width="1"
        />
        <rect
          :x="calloutBox().bx"
          :y="calloutBox().by"
          :width="calloutBox().boxW"
          :height="calloutBox().boxH"
          :fill="colors.calloutBg"
          :stroke="colors.labelBorder"
          stroke-width="1"
        />
        <text :x="calloutBox().bx + 12" :y="calloutBox().by + 20" font-family="'Shippori Mincho', serif" font-size="14" font-weight="700" :fill="colors.calloutText">
          {{ selected.name }}
        </text>
        <text :x="calloutBox().bx + 12" :y="calloutBox().by + 38" font-family="'Noto Serif JP', serif" font-size="10" :fill="colors.calloutSub">
          {{ selected.area }}
        </text>
        <g v-if="selected.visitable === false">
          <rect :x="calloutBox().bx + calloutBox().boxW - 44" :y="calloutBox().by + 6" width="36" height="14" :fill="colors.pin" />
          <text
            :x="calloutBox().bx + calloutBox().boxW - 26"
            :y="calloutBox().by + 16"
            text-anchor="middle"
            font-family="'Shippori Mincho', serif"
            font-size="9"
            :fill="isLight ? '#fff' : '#f4ede0'"
          >
            閉 館
          </text>
        </g>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.japan-map {
  position: relative;
  width: 100%;
  overflow: hidden;
}
</style>
