<script setup>
/**
 * 部品名: オープニング映像（全画面）
 * 役割: 初回訪問時の演出。24秒で自動終了／スキップ可
 */
import { ref, onMounted, onUnmounted } from 'vue'
import { SCENES, sceneOpacity, localT } from './openingMath.js'
import OpeningSceneCurtain from './OpeningSceneCurtain.vue'
import OpeningSceneRecord from './OpeningSceneRecord.vue'
import OpeningSceneSignature from './OpeningSceneSignature.vue'

const emit = defineEmits(['done'])

const DUR = 24000
const t = ref(0)
const paused = ref(false)
let startMs = null
let pausedAt = 0
let raf = 0

function step(now) {
  if (paused.value) {
    raf = requestAnimationFrame(step)
    return
  }
  if (startMs == null) startMs = now - pausedAt
  const nt = Math.min((now - startMs) / DUR, 1)
  t.value = nt
  if (nt >= 1) {
    setTimeout(() => emit('done'), 300)
    return
  }
  raf = requestAnimationFrame(step)
}

function togglePause() {
  if (!paused.value) pausedAt = t.value * DUR
  else startMs = null
  paused.value = !paused.value
}

function onKey(e) {
  if (e.key === 'Escape' || e.key === 'Enter') emit('done')
  if (e.key === ' ') {
    e.preventDefault()
    togglePause()
  }
}

onMounted(() => {
  raf = requestAnimationFrame(step)
  window.addEventListener('keydown', onKey)
})

onUnmounted(() => {
  cancelAnimationFrame(raf)
  window.removeEventListener('keydown', onKey)
})

function skip() {
  emit('done')
}

const grainUrl = `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>")`
</script>

<template>
  <div
    class="opening-film-root"
    style="position: fixed; inset: 0; z-index: 100; background: #050302; color: #f4ede0; overflow: hidden; font-family: 'Noto Serif JP', serif"
  >
    <template v-for="s in SCENES" :key="s.id">
      <div
        v-if="sceneOpacity(t, s) > 0"
        style="position: absolute; inset: 0; transition: none"
        :style="{ opacity: sceneOpacity(t, s) }"
      >
        <OpeningSceneCurtain v-if="s.id === 'curtain'" :lt="localT(t, s)" />
        <OpeningSceneRecord v-if="s.id === 'record'" :lt="localT(t, s)" />
        <OpeningSceneSignature v-if="s.id === 'signature'" :lt="localT(t, s)" />
      </div>
    </template>

    <div
      style="position: absolute; inset: 0; pointer-events: none; opacity: 0.16; mix-blend-mode: overlay; animation: grain 0.6s steps(3) infinite"
      :style="{ backgroundImage: grainUrl }"
    />

    <div
      style="position: absolute; top: 0; left: 0; right: 0; padding: 18px 28px; display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: 0.2em; color: #c9a961; opacity: 0.85; pointer-events: none"
    >
      <span>◉ REC · 8mm · HIBARI PRODUCTION</span>
      <span>{{ String(Math.floor(t * 24)).padStart(2, '0') }}s / 24s</span>
    </div>

    <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 18px 28px; display: flex; align-items: center; gap: 12px">
      <button
        type="button"
        class="of-ctrl-btn"
        style="background: transparent; border: 1px solid rgba(244,237,224,0.4); color: #f4ede0; padding: 8px 16px; cursor: pointer; font-family: 'Noto Serif JP', serif; font-size: 11px; letter-spacing: 0.15em; min-height: 44px; min-width: 88px; flex-shrink: 0"
        :aria-label="paused ? '再生' : '一時停止'"
        @click="togglePause"
      >
        {{ paused ? '▶ 再生' : '❚❚ 停止' }}
      </button>
      <div style="flex: 1; height: 2px; background: rgba(255,255,255,0.15); position: relative; margin: 0 4px">
        <div style="position: absolute; inset: 0 auto 0 0; background: #c9a961" :style="{ width: `${t * 100}%` }" />
      </div>
      <button
        type="button"
        class="of-ctrl-btn"
        style="background: transparent; border: 1px solid #f4ede0; color: #f4ede0; padding: 8px 20px; cursor: pointer; font-family: 'Noto Serif JP', serif; font-size: 12px; letter-spacing: 0.2em; min-height: 44px; min-width: 88px; flex-shrink: 0"
        aria-label="スキップ"
        @click="skip"
      >
        スキップ ›
      </button>
    </div>
  </div>
</template>
