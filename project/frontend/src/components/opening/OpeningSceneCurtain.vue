<script setup>
/**
 * オープニング シーン1: 緞帳（カーテン）が開きタイトルが浮かぶ
 */
import { computed } from 'vue'

const props = defineProps({
  /** シーン内ローカル進行 0〜1 */
  lt: { type: Number, required: true },
})

const rise = computed(() => Math.min(props.lt / 0.45, 1))
const riseEase = computed(() => {
  const r = rise.value
  return r < 0.5 ? 2 * r * r : 1 - Math.pow(-2 * r + 2, 2) / 2
})
const curtainY = computed(() => riseEase.value * 110)
const spotOp = computed(() => Math.max(0, (curtainY.value - 25) / 75) * 0.8)
const mainTitleOp = computed(() => (props.lt > 0.44 ? Math.min((props.lt - 0.44) / 0.16, 1) : 0))
const subTitleOp = computed(() => (props.lt > 0.57 ? Math.min((props.lt - 0.57) / 0.14, 1) : 0))
const dividerOp = computed(() => (props.lt > 0.65 ? Math.min((props.lt - 0.65) / 0.12, 1) : 0))
const captionOp = computed(() => (props.lt > 0.73 ? Math.min((props.lt - 0.73) / 0.12, 1) : 0))

const folds = Array.from({ length: 9 }, (_, i) => i)
const fringe = Array.from({ length: 28 }, (_, i) => i)
const highlights = [1, 3, 5, 7]
</script>

<template>
  <div style="position: absolute; inset: 0">
    <div style="position: absolute; inset: 0; background: #050302" />

    <template v-if="spotOp > 0">
      <div
        :style="{
          position: 'absolute',
          top: 0,
          left: '50%',
          transform: 'translateX(-50%)',
          width: 0,
          height: 0,
          borderLeft: '380px solid transparent',
          borderRight: '380px solid transparent',
          borderTop: '120vh solid rgba(255,220,140,0.05)',
          filter: 'blur(20px)',
          opacity: spotOp,
          pointerEvents: 'none',
        }"
      />
      <div
        :style="{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: '18%',
          background: 'linear-gradient(0deg, rgba(139,80,30,0.10), transparent)',
          opacity: spotOp,
          pointerEvents: 'none',
        }"
      />
    </template>

    <!-- 左パネル -->
    <div
      :style="{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '51%',
        height: '100%',
        transform: `translateY(-${curtainY}%)`,
      }"
    >
      <div
        style="position: absolute; inset: 0; background: linear-gradient(90deg, #1a0404 0%, #5e1111 15%, #8b1a1a 50%, #6a1414 80%, #4a0e0e 100%)"
      />
      <div
        style="position: absolute; inset: 0; background: radial-gradient(ellipse 80% 60% at 70% 30%, rgba(255,200,180,0.06), transparent)"
      />
      <div
        v-for="i in folds"
        :key="'fl' + i"
        :style="{
          position: 'absolute',
          top: 0,
          bottom: 0,
          left: `${(i / 9) * 100}%`,
          width: '13%',
          background:
            i % 2 === 0
              ? 'linear-gradient(90deg, transparent 0%, rgba(255,160,120,0.04) 20%, rgba(255,180,140,0.08) 50%, rgba(255,160,120,0.04) 80%, transparent 100%)'
              : 'linear-gradient(90deg, transparent 0%, rgba(0,0,0,0.18) 30%, rgba(0,0,0,0.28) 55%, rgba(0,0,0,0.14) 80%, transparent 100%)',
        }"
      />
      <div
        v-for="i in highlights"
        :key="'hl' + i"
        :style="{
          position: 'absolute',
          top: 0,
          bottom: 0,
          left: `${(i / 9) * 100 + 1}%`,
          width: '1px',
          background: 'linear-gradient(180deg, transparent 0%, rgba(255,200,160,0.12) 20%, rgba(255,220,180,0.18) 50%, rgba(255,200,160,0.1) 80%, transparent 100%)',
        }"
      />
      <div
        style="position: absolute; top: 0; bottom: 0; right: 0; width: 12%; background: linear-gradient(90deg, transparent, rgba(0,0,0,0.45))"
      />
      <div
        style="position: absolute; bottom: 0; left: 0; right: 0; height: 20px; background: linear-gradient(180deg, #6a4a1a 0%, #c9a961 30%, #e8d090 55%, #c9a961 75%, #8a6a3a 100%); box-shadow: 0 -2px 6px rgba(0,0,0,0.6), 0 2px 12px rgba(201,169,97,0.3)"
      />
      <div style="position: absolute; bottom: -22px; left: 0; right: 0; height: 26px">
        <div
          v-for="i in fringe"
          :key="'fr' + i"
          :style="{
            position: 'absolute',
            left: `${(i / 28) * 100 + 1}%`,
            top: 0,
            width: '1.5px',
            height: `${16 + Math.sin(i * 1.3) * 5 + (i % 3) * 3}px`,
            background: 'linear-gradient(180deg, #c9a961 0%, #8a6a3a 70%, rgba(138,106,58,0) 100%)',
            opacity: 0.85,
          }"
        />
      </div>
    </div>

    <!-- 右パネル（左右対称のグラデーション反転） -->
    <div
      :style="{
        position: 'absolute',
        top: 0,
        right: 0,
        width: '51%',
        height: '100%',
        transform: `translateY(-${curtainY}%)`,
      }"
    >
      <div
        style="position: absolute; inset: 0; background: linear-gradient(90deg, #4a0e0e 0%, #6a1414 20%, #8b1a1a 50%, #5e1111 85%, #1a0404 100%)"
      />
      <div
        style="position: absolute; inset: 0; background: radial-gradient(ellipse 80% 60% at 30% 30%, rgba(255,200,180,0.06), transparent)"
      />
      <div
        v-for="i in folds"
        :key="'fr2' + i"
        :style="{
          position: 'absolute',
          top: 0,
          bottom: 0,
          left: `${(i / 9) * 100}%`,
          width: '13%',
          background:
            i % 2 === 0
              ? 'linear-gradient(90deg, transparent 0%, rgba(255,160,120,0.04) 20%, rgba(255,180,140,0.08) 50%, rgba(255,160,120,0.04) 80%, transparent 100%)'
              : 'linear-gradient(90deg, transparent 0%, rgba(0,0,0,0.18) 30%, rgba(0,0,0,0.28) 55%, rgba(0,0,0,0.14) 80%, transparent 100%)',
        }"
      />
      <div
        v-for="i in highlights"
        :key="'hl2' + i"
        :style="{
          position: 'absolute',
          top: 0,
          bottom: 0,
          left: `${(i / 9) * 100 + 1}%`,
          width: '1px',
          background: 'linear-gradient(180deg, transparent 0%, rgba(255,200,160,0.12) 20%, rgba(255,220,180,0.18) 50%, rgba(255,200,160,0.1) 80%, transparent 100%)',
        }"
      />
      <div
        style="position: absolute; top: 0; bottom: 0; left: 0; width: 12%; background: linear-gradient(90deg, rgba(0,0,0,0.45), transparent)"
      />
      <div
        style="position: absolute; bottom: 0; left: 0; right: 0; height: 20px; background: linear-gradient(180deg, #6a4a1a 0%, #c9a961 30%, #e8d090 55%, #c9a961 75%, #8a6a3a 100%); box-shadow: 0 -2px 6px rgba(0,0,0,0.6), 0 2px 12px rgba(201,169,97,0.3)"
      />
      <div style="position: absolute; bottom: -22px; left: 0; right: 0; height: 26px">
        <div
          v-for="i in fringe"
          :key="'frb' + i"
          :style="{
            position: 'absolute',
            left: `${(i / 28) * 100 + 1}%`,
            top: 0,
            width: '1.5px',
            height: `${16 + Math.sin(i * 1.3) * 5 + (i % 3) * 3}px`,
            background: 'linear-gradient(180deg, #c9a961 0%, #8a6a3a 70%, rgba(138,106,58,0) 100%)',
            opacity: 0.85,
          }"
        />
      </div>
    </div>

    <div
      style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center"
    >
      <h1
        class="of-title-main"
        :style="{
          fontFamily: `'Shippori Mincho', serif`,
          fontWeight: 800,
          fontSize: 'clamp(56px, 12vw, 120px)',
          color: '#f4ede0',
          letterSpacing: '0.15em',
          margin: 0,
          lineHeight: 1.1,
          opacity: mainTitleOp,
          transform: `translateY(${(1 - mainTitleOp) * 24}px)`,
        }"
      >
        美空ひばり
      </h1>
      <div
        class="of-title-sub"
        :style="{
          fontFamily: `'Shippori Mincho', serif`,
          fontStyle: 'italic',
          fontSize: 'clamp(16px, 3vw, 28px)',
          color: '#c9a961',
          letterSpacing: '0.4em',
          marginTop: '16px',
          opacity: subTitleOp,
          transform: `translateY(${(1 - subTitleOp) * 12}px)`,
        }"
      >
        不死鳥は、今も歌う。
      </div>
      <div
        :style="{
          width: '200px',
          height: '1px',
          background: 'linear-gradient(90deg, transparent, #c9a961, transparent)',
          margin: '24px auto',
          opacity: dividerOp,
          transform: `scaleX(${dividerOp})`,
          transformOrigin: 'center',
        }"
      />
      <div
        :style="{
          fontFamily: `'Playfair Display', serif`,
          fontStyle: 'italic',
          fontSize: '12px',
          color: 'rgba(244,237,224,0.6)',
          letterSpacing: '0.4em',
          opacity: captionOp,
        }"
      >
        1937–1989 · MISORA HIBARI
      </div>
    </div>
  </div>
</template>
