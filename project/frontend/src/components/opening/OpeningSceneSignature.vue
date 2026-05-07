<script setup>
/**
 * オープニング シーン3: レコード＋「歌は、我が命。」の締め
 */
import { ref, computed, onMounted, onUnmounted } from 'vue'
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

const spinEase = computed(() => {
  const lt = props.lt
  return lt < 0.28 ? 1440 + 200 * (1 - Math.pow(1 - lt / 0.28, 3)) : 1440 + 200
})

const recordOp = computed(() => (props.lt > 0.64 ? Math.max(0, 1 - (props.lt - 0.64) / 0.22) : 1))
const labelOp = computed(() => (props.lt > 0.33 ? Math.min((props.lt - 0.33) / 0.14, 1) : 0))
const textOp = computed(() => (props.lt > 0.48 ? Math.min((props.lt - 0.48) / 0.2, 1) : 0))
const subOp = computed(() => (props.lt > 0.7 ? Math.min((props.lt - 0.7) / 0.16, 1) : 0))

const sigArmAngle = computed(() => {
  const lt = props.lt
  const ARM_REST_SIG = -30
  const ARM_PLAY_SIG = 15
  const liftStart = 0.28
  const liftDur = 0.16
  const liftProgress = lt > liftStart ? Math.min((lt - liftStart) / liftDur, 1) : 0
  const liftEase = 1 - Math.pow(1 - liftProgress, 2)
  return ARM_PLAY_SIG + (ARM_REST_SIG - ARM_PLAY_SIG) * liftEase
})

const sigArmOp = computed(() =>
  props.lt > 0.64 ? Math.max(0, 1 - (props.lt - 0.64) / 0.22) : 1,
)
</script>

<template>
  <div
    style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; background: radial-gradient(ellipse at center, #1a0e0a 0%, #050302 75%)"
  >
    <div
      :style="{
        position: 'absolute',
        top: '50%',
        left: isSP ? '50%' : '46%',
        transform: `translate(-50%, -50%) rotate(${spinEase}deg)`,
        width: recordSize + 'px',
        height: recordSize + 'px',
        opacity: recordOp,
        filter: 'drop-shadow(0 20px 60px rgba(0,0,0,0.9))',
      }"
    >
      <div
        style="position: absolute; inset: 0; border-radius: 50%; background: radial-gradient(circle at center, #1a1410 0 22%, #8b1a1a 22% 27%, #1a1410 27% 44%, #2a1a12 44.5%, #1a1410 45% 100%)"
      />
      <div
        v-for="i in 32"
        :key="'sg' + i"
        :style="{
          position: 'absolute',
          inset: `${44 + (i - 1) * 1.2}%`,
          border: '0.4px solid rgba(255,255,255,0.04)',
          borderRadius: '50%',
        }"
      />
      <div
        :style="{
          position: 'absolute',
          inset: '34% 34% 34% 34%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          opacity: labelOp,
          transform: `rotate(${-spinEase}deg)`,
        }"
      >
        <div
          :style="{
            fontFamily: `'Shippori Mincho', serif`,
            fontWeight: 800,
            fontSize: recordSize * 0.07 + 'px',
            color: '#c9a961',
            letterSpacing: '0.08em',
            textAlign: 'center',
            lineHeight: 1.2,
          }"
        >
          美空<br />ひばり
        </div>
        <div
          :style="{
            fontFamily: `'JetBrains Mono', monospace`,
            fontSize: recordSize * 0.028 + 'px',
            color: 'rgba(201,169,97,0.6)',
            marginTop: '4px',
            letterSpacing: '0.12em',
          }"
        >
          1937–1989
        </div>
      </div>
      <div
        style="position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); border-radius: 50%; background: #050302"
        :style="{ width: recordSize * 0.022 + 'px', height: recordSize * 0.022 + 'px' }"
      />
    </div>

    <div
      v-if="!isSP"
      :style="{
        position: 'absolute',
        left: `calc(46% + ${recordSize * 0.51}px)`,
        top: `calc(50% - ${recordSize * 0.44}px)`,
        width: 0,
        height: 0,
        transformOrigin: '0 0',
        transform: `rotate(${sigArmAngle}deg)`,
        opacity: sigArmOp,
        pointerEvents: 'none',
        zIndex: 3,
      }"
    >
      <OpeningToneArmSvg :record-size="recordSize" />
    </div>

    <div
      :style="{
        position: 'absolute',
        right: 0,
        top: 0,
        bottom: 0,
        width: isSP ? '100%' : '55%',
        background: isSP
          ? 'radial-gradient(ellipse at 50% 50%, rgba(5,3,2,0.72) 0%, transparent 70%)'
          : 'linear-gradient(90deg, transparent 0%, rgba(5,3,2,0.55) 25%, rgba(5,3,2,0.75) 65%, rgba(5,3,2,0.80) 100%)',
        opacity: textOp,
        pointerEvents: 'none',
        zIndex: 15,
      }"
    />

    <div
      :style="{
        position: 'absolute',
        zIndex: 20,
        right: isSP ? 'auto' : '6%',
        left: isSP ? '50%' : 'auto',
        top: isSP ? '50%' : 'auto',
        transform: isSP ? 'translate(-50%, -50%)' : 'none',
        textAlign: isSP ? 'center' : 'right',
        opacity: textOp,
        paddingRight: isSP ? 0 : '2%',
      }"
    >
      <div
        :style="{
          width: '1px',
          height: `${textOp * 48}px`,
          background: 'linear-gradient(180deg, transparent, #c9a961)',
          margin: isSP ? '0 auto 16px' : '0 0 16px auto',
        }"
      />
      <div
        :style="{
          fontFamily: `'Shippori Mincho', serif`,
          fontWeight: 800,
          fontSize: 'clamp(24px, 4.5vw, 48px)',
          color: '#f4ede0',
          letterSpacing: '0.3em',
          lineHeight: 1.5,
          textShadow: '0 2px 20px rgba(201,169,97,0.25)',
          transform: `translateX(${(1 - textOp) * 24}px)`,
        }"
      >
        歌は、我が命。
      </div>
      <div
        :style="{
          width: `${textOp * 100}%`,
          maxWidth: '200px',
          height: '1px',
          background: 'linear-gradient(90deg, transparent, #c9a961)',
          margin: isSP ? '16px auto 12px' : '16px 0 12px auto',
        }"
      />
      <div
        :style="{
          fontFamily: `'Playfair Display', serif`,
          fontStyle: 'italic',
          fontSize: '11px',
          letterSpacing: '0.35em',
          color: 'rgba(201,169,97,0.7)',
          opacity: subOp,
          transform: `translateX(${(1 - subOp) * 16}px)`,
        }"
      >
        MISORA HIBARI OFFICIAL FAN SITE
      </div>
    </div>

    <div style="position: absolute; inset: 0; pointer-events: none; background: radial-gradient(ellipse at center, transparent 38%, rgba(0,0,0,0.75) 100%)" />
  </div>
</template>
