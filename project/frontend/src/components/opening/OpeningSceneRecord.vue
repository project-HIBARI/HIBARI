<script setup>
/**
 * オープニング シーン2: 回転レコード・フォトフレーム・見出しカード
 */
import { ref, computed, onMounted, onUnmounted } from 'vue'
import {
  ASSETS,
  itemOpacity,
  PHOTO_OFFSETS_PC,
  PHOTO_OFFSETS_SP,
  HEADLINE_OFFSETS_PC,
  HEADLINE_OFFSETS_SP,
  TOUCH_LT,
} from './openingMath.js'
import OpeningToneArmSvg from './OpeningToneArmSvg.vue'

const props = defineProps({
  lt: { type: Number, required: true },
})

const ww = ref(typeof window !== 'undefined' ? window.innerWidth : 1280)
function onResize() {
  ww.value = window.innerWidth
}
onMounted(() => window.addEventListener('resize', onResize))
onUnmounted(() => window.removeEventListener('resize', onResize))

const isSP = computed(() => ww.value < 768)
const recordSize = computed(() => Math.min(ww.value * 0.55, 480))

const spin = computed(() => {
  const lt = props.lt
  const spinProgress = lt > TOUCH_LT ? (lt - TOUCH_LT) / (1 - TOUCH_LT) : 0
  return spinProgress * 1440
})

function photoStyle(off, op, landscape, frameW) {
  const base = {
    position: 'absolute',
    opacity: op,
    width: frameW,
    background: 'rgba(20,12,8,0.88)',
    border: '1px solid #c9a961',
    padding: '10px',
    boxShadow: '0 12px 32px rgba(0,0,0,0.7)',
    zIndex: 5,
  }
  const tr = `translateX(${off.entryX * (1 - op)}px) translateY(${off.entryY * (1 - op)}px) rotate(${off.rotate}deg) scale(${off.scale * (0.92 + op * 0.08)})`
  if (isSP.value) {
    return { ...base, bottom: off.bottom, left: off.left, transform: tr }
  }
  return { ...base, ...(off.left ? { left: off.left } : {}), ...(off.right ? { right: off.right } : {}), top: off.top, transform: tr }
}

function headlineStyle(off, op) {
  const tr = `translateX(${off.entryX * (1 - op)}px) translateY(${off.entryY * (1 - op)}px) rotate(${off.rotate}deg)`
  const w = isSP.value ? 'min(250px, 82vw)' : 'min(250px, 34vw)'
  if (isSP.value) {
    return {
      position: 'absolute',
      top: off.top,
      left: off.left,
      zIndex: 5,
      width: w,
      opacity: op,
      transform: tr,
      background: 'rgba(239,226,198,0.92)',
      color: '#1a1410',
      border: '1px solid #8a6a3a',
      padding: '14px 16px',
      fontFamily: `'Noto Serif JP', serif`,
      boxShadow: '0 8px 24px rgba(0,0,0,0.5)',
    }
  }
  return {
    position: 'absolute',
    ...(off.left ? { left: off.left } : {}),
    ...(off.right ? { right: off.right } : {}),
    top: off.top,
    zIndex: 5,
    width: w,
    opacity: op,
    transform: tr,
    background: 'rgba(239,226,198,0.92)',
    color: '#1a1410',
    border: '1px solid #8a6a3a',
    padding: '14px 16px',
    fontFamily: `'Noto Serif JP', serif`,
    boxShadow: '0 8px 24px rgba(0,0,0,0.5)',
  }
}

function photoOpacity(i, off) {
  const ltAdj = off?.overlap
    ? props.lt < TOUCH_LT
      ? 0
      : (props.lt - TOUCH_LT) / (1 - TOUCH_LT)
    : props.lt
  return itemOpacity(ltAdj, i, ASSETS.photoFrames.length, { stagger: 0.18, window: 0.42, fadeDur: 0.07 })
}

function headlineOp(i, off) {
  const ltAdj = off?.overlap
    ? props.lt < TOUCH_LT
      ? 0
      : (props.lt - TOUCH_LT) / (1 - TOUCH_LT)
    : props.lt
  return itemOpacity(ltAdj, i, ASSETS.headlines.length, { stagger: 0.22, window: 0.46, fadeDur: 0.07 })
}

const armAngle = computed(() => {
  const lt = props.lt
  const ARM_REST = -30
  const ARM_PLAY = 15
  const dropProgress = Math.min(lt / 0.14, 1)
  const dropEase = dropProgress < 0.5 ? 2 * dropProgress * dropProgress : 1 - Math.pow(-2 * dropProgress + 2, 2) / 2
  return ARM_REST + (ARM_PLAY - ARM_REST) * dropEase
})
</script>

<template>
  <div style="position: absolute; inset: 0">
    <div style="position: absolute; inset: 0; background: radial-gradient(ellipse at center, #2a1410 0%, #050302 70%)" />

    <div
      :style="{
        position: 'absolute',
        top: '50%',
        left: isSP ? '50%' : '46%',
        transform: `translate(-50%, -50%) rotate(${spin}deg)`,
        width: recordSize + 'px',
        height: recordSize + 'px',
        filter: 'drop-shadow(0 20px 50px rgba(0,0,0,0.8))',
      }"
    >
      <div
        style="position: absolute; inset: 0; border-radius: 50%; background: radial-gradient(circle at center, #1a1410 0 22%, #8b1a1a 22% 27%, #1a1410 27% 44%, #2a1a12 44.5%, #1a1410 45% 100%)"
      />
      <div
        v-for="i in 32"
        :key="'groove' + i"
        :style="{
          position: 'absolute',
          inset: `${44 + (i - 1) * 1.2}%`,
          border: '0.4px solid rgba(255,255,255,0.04)',
          borderRadius: '50%',
        }"
      />
      <template v-for="(hl, i) in ASSETS.headlines" :key="'lbl' + i">
        <div
          v-if="itemOpacity(lt, i, ASSETS.headlines.length, { stagger: 0.22, window: 0.46, fadeDur: 0.07 }) > 0"
          :style="{
            position: 'absolute',
            inset: '34% 34% 34% 34%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#c9a961',
            fontFamily: `'Shippori Mincho', serif`,
            fontSize: recordSize * 0.044 + 'px',
            textAlign: 'center',
            lineHeight: 1.4,
            padding: '0 4px',
            opacity: itemOpacity(lt, i, ASSETS.headlines.length, { stagger: 0.22, window: 0.46, fadeDur: 0.07 }),
          }"
        >
          <div style="font-weight: 700; letter-spacing: 0.02em; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 90%">
            {{ hl.song }}
          </div>
          <div :style="{ fontFamily: `'JetBrains Mono', monospace`, fontSize: recordSize * 0.03 + 'px', opacity: 0.7, marginTop: '2px' }">
            {{ hl.year }}
          </div>
          <div :style="{ fontSize: recordSize * 0.028 + 'px', opacity: 0.6, marginTop: '1px', letterSpacing: '0.1em' }">日本コロムビア</div>
        </div>
      </template>
      <div
        style="position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); border-radius: 50%; background: #050302"
        :style="{ width: recordSize * 0.022 + 'px', height: recordSize * 0.022 + 'px' }"
      />
    </div>

    <template v-for="(photo, i) in ASSETS.photoFrames" :key="'ph' + i">
      <div
        v-if="photoOpacity(i, (isSP ? PHOTO_OFFSETS_SP : PHOTO_OFFSETS_PC)[i]) > 0"
        v-bind:style="
          photoStyle(
            (isSP ? PHOTO_OFFSETS_SP : PHOTO_OFFSETS_PC)[i],
            photoOpacity(i, (isSP ? PHOTO_OFFSETS_SP : PHOTO_OFFSETS_PC)[i]),
            (isSP ? PHOTO_OFFSETS_SP : PHOTO_OFFSETS_PC)[i].landscape,
            (isSP ? PHOTO_OFFSETS_SP : PHOTO_OFFSETS_PC)[i].landscape
              ? isSP
                ? 'min(240px, 55vw)'
                : 'min(260px, 36vw)'
              : isSP
                ? 'min(180px, 40vw)'
                : 'min(200px, 28vw)',
          )
        "
      >
        <svg viewBox="0 0 200 250" style="width: 100%; display: block" :style="{ aspectRatio: (isSP ? PHOTO_OFFSETS_SP : PHOTO_OFFSETS_PC)[i].landscape ? '5/3' : '4/5' }">
          <defs>
            <linearGradient :id="'silg' + i" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0" stop-color="#4a2820" />
              <stop offset="1" stop-color="#1a0a06" />
            </linearGradient>
          </defs>
          <rect width="200" height="250" :fill="`url(#silg${i})`" />
          <path
            d="M 100 240 C 80 240 60 228 58 202 C 54 178 70 168 76 155 C 68 148 62 138 60 122 C 57 104 63 86 74 74 C 85 62 98 57 112 60 C 126 63 137 75 140 92 C 143 110 140 128 132 140 C 138 148 142 158 139 170 C 152 178 164 192 166 212 C 167 234 142 240 122 240 Z"
            fill="#000"
            opacity="0.8"
          />
        </svg>
        <div :style="{ fontFamily: `'JetBrains Mono', monospace`, fontSize: '9px', color: '#c9a961', letterSpacing: '0.1em', marginTop: '6px', textAlign: 'center' }">
          ▣ {{ photo.caption }}
        </div>
      </div>
    </template>

    <template v-for="(hl, i) in ASSETS.headlines" :key="'hc' + i">
      <div
        v-if="headlineOp(i, (isSP ? HEADLINE_OFFSETS_SP : HEADLINE_OFFSETS_PC)[i]) > 0"
        :style="headlineStyle((isSP ? HEADLINE_OFFSETS_SP : HEADLINE_OFFSETS_PC)[i], headlineOp(i, (isSP ? HEADLINE_OFFSETS_SP : HEADLINE_OFFSETS_PC)[i]))"
      >
        <div :style="{ fontFamily: `'JetBrains Mono', monospace`, fontSize: '10px', color: '#8b1a1a', letterSpacing: '0.2em' }">{{ hl.year }}</div>
        <div style="font-weight: 700; font-size: 17px; color: #1a1410; margin-top: 6px; line-height: 1.4">{{ hl.title }}</div>
        <div style="font-size: 11px; color: #5a3a1a; margin-top: 6px; line-height: 1.6">{{ hl.sub }}</div>
      </div>
    </template>

    <div
      v-if="!isSP"
      :style="{
        position: 'absolute',
        left: `calc(46% + ${recordSize * 0.51}px)`,
        top: `calc(50% - ${recordSize * 0.44}px)`,
        width: 0,
        height: 0,
        transformOrigin: '0 0',
        transform: `rotate(${armAngle}deg)`,
        pointerEvents: 'none',
        zIndex: 3,
      }"
    >
      <OpeningToneArmSvg :record-size="recordSize" />
    </div>

    <div style="position: absolute; inset: 0; background: radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.7) 100%); pointer-events: none" />
  </div>
</template>
