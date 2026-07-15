<script setup>
/**
 * 部品名: 日本地図（ゆかりの地ピン）
 * 役割: OpenStreetMap ベースの実地図にスポットピンを表示し、選択・ハイライトする
 */
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  places: { type: Array, required: true },
  selected: { type: Object, default: null },
  /** light=ライトテーマ（Carto Voyager） / dark=ダーク地図 */
  theme: { type: String, default: 'light' },
})

const emit = defineEmits(['select'])

const mapEl = ref(null)
let map = null
let markerLayer = null
const markersById = new Map()

const DEFAULT_CENTER = [36.5, 137.5]
const DEFAULT_ZOOM = 5

function tileUrl() {
  return props.theme === 'dark'
    ? 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
    : 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png'
}

function createPinIcon(place, isSelected) {
  const size = isSelected ? 36 : 28
  const color = isSelected ? '#c0342f' : '#a8262b'
  const ring = isSelected ? 'box-shadow:0 0 0 4px rgba(192,52,47,0.28);' : ''
  return L.divIcon({
    className: 'japan-map__pin-wrap',
    iconSize: [size, size + 10],
    iconAnchor: [size / 2, size + 8],
    popupAnchor: [0, -(size + 4)],
    html: `
      <div class="japan-map__pin" style="--pin-color:${color};width:${size}px;height:${size}px;${ring}">
        <span class="japan-map__pin-dot"></span>
      </div>
    `,
  })
}

function fitToPlaces() {
  if (!map || !props.places?.length) return
  if (props.places.length === 1) {
    const p = props.places[0]
    map.setView([p.lat, p.lng], 10, { animate: true })
    return
  }
  const bounds = L.latLngBounds(props.places.map((p) => [p.lat, p.lng]))
  map.fitBounds(bounds.pad(0.35), { animate: true, maxZoom: 8 })
}

function rebuildMarkers() {
  if (!map) return
  if (markerLayer) {
    markerLayer.clearLayers()
  } else {
    markerLayer = L.layerGroup().addTo(map)
  }
  markersById.clear()

  props.places.forEach((place, index) => {
    const selected = props.selected?.id === place.id
    const marker = L.marker([place.lat, place.lng], {
      icon: createPinIcon(place, selected),
      title: place.name,
      riseOnHover: true,
    })
    marker.bindPopup(
      `<strong>${place.name}</strong><br/><span style="opacity:.75;font-size:12px">${place.area}</span>`,
      { closeButton: false, offset: [0, -4] },
    )
    marker.on('click', () => emit('select', place))
    marker.addTo(markerLayer)
    markersById.set(place.id, { marker, place, index })
  })

  fitToPlaces()
}

function syncSelection() {
  if (!map || !props.selected) return
  markersById.forEach(({ marker, place }) => {
    marker.setIcon(createPinIcon(place, place.id === props.selected.id))
  })
  const entry = markersById.get(props.selected.id)
  if (entry) {
    map.panTo([props.selected.lat, props.selected.lng], { animate: true })
    entry.marker.openPopup()
  }
}

onMounted(async () => {
  await nextTick()
  if (!mapEl.value) return

  map = L.map(mapEl.value, {
    center: DEFAULT_CENTER,
    zoom: DEFAULT_ZOOM,
    scrollWheelZoom: false,
    zoomControl: true,
    attributionControl: true,
  })

  L.tileLayer(tileUrl(), {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright" rel="noopener noreferrer" target="_blank">OpenStreetMap</a> &copy; <a href="https://carto.com/" rel="noopener noreferrer" target="_blank">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 18,
  }).addTo(map)

  rebuildMarkers()
  syncSelection()

  // Leaflet needs a size recalc after layout
  requestAnimationFrame(() => map?.invalidateSize())
})

watch(
  () => props.places,
  () => {
    rebuildMarkers()
    syncSelection()
  },
  { deep: true },
)

watch(
  () => props.selected?.id,
  () => syncSelection(),
)

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
    markerLayer = null
    markersById.clear()
  }
})
</script>

<template>
  <div class="japan-map" :class="{ 'japan-map--dark': theme === 'dark' }" role="region" aria-label="ゆかりの地マップ">
    <div ref="mapEl" class="japan-map__canvas" />
    <div class="japan-map__label" aria-hidden="true">
      <p class="japan-map__label-title">ゆかりの地</p>
      <p class="japan-map__label-sub">PLACES · PILGRIMAGE</p>
      <p class="japan-map__label-meta">{{ places.length }} LOCATIONS</p>
    </div>
  </div>
</template>

<style scoped>
.japan-map {
  position: relative;
  width: 100%;
  aspect-ratio: 4 / 5;
  min-height: 420px;
  overflow: hidden;
  background: #e8eef4;
  border: 1px solid rgba(90, 60, 40, 0.15);
}
.japan-map--dark {
  background: #0d0806;
  border-color: #3a2a1a;
}
.japan-map__canvas {
  width: 100%;
  height: 100%;
  z-index: 0;
}
.japan-map__label {
  position: absolute;
  top: 14px;
  left: 14px;
  z-index: 500;
  padding: 12px 14px 10px;
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid #c9a961;
  box-shadow: 0 8px 24px rgba(40, 30, 25, 0.12);
  pointer-events: none;
}
.japan-map--dark .japan-map__label {
  background: rgba(13, 8, 6, 0.92);
}
.japan-map__label-title {
  margin: 0;
  font-family: var(--ff-mincho, 'Shippori Mincho', serif);
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.18em;
  color: #3a2b22;
}
.japan-map--dark .japan-map__label-title {
  color: #f4ede0;
}
.japan-map__label-sub {
  margin: 4px 0 0;
  font-family: var(--ff-latin, 'Playfair Display', serif);
  font-style: italic;
  font-size: 10px;
  letter-spacing: 0.14em;
  color: #a8873f;
}
.japan-map__label-meta {
  margin: 6px 0 0;
  font-family: var(--ff-mono, 'JetBrains Mono', monospace);
  font-size: 8px;
  letter-spacing: 0.16em;
  color: #8a7568;
}

@media (max-width: 640px) {
  .japan-map {
    aspect-ratio: 1 / 1.1;
    min-height: 360px;
  }
}
</style>

<style>
/* Leaflet pin (unscoped — rendered into map panes) */
.japan-map__pin-wrap {
  background: transparent !important;
  border: 0 !important;
}
.japan-map__pin {
  position: relative;
  border-radius: 50% 50% 50% 0;
  background: var(--pin-color, #a8262b);
  border: 2px solid #c9a961;
  transform: rotate(-45deg);
  box-sizing: border-box;
}
.japan-map__pin-dot {
  position: absolute;
  inset: 28%;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  transform: rotate(45deg);
}
.leaflet-container {
  font: inherit;
}
.leaflet-popup-content-wrapper {
  border-radius: 8px;
  border: 1px solid #c9a961;
  box-shadow: 0 10px 28px rgba(40, 30, 25, 0.16);
}
.leaflet-popup-content {
  margin: 10px 12px;
  font-family: 'Shippori Mincho', 'Noto Serif JP', serif;
  color: #3a2b22;
  line-height: 1.45;
}
.leaflet-popup-tip {
  border-top-color: #fff;
}
</style>
