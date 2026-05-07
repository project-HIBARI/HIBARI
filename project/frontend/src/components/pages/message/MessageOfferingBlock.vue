<script setup>
/**
 * 部品名: 献花 — 花の選択とフォーム
 */
import { ref } from 'vue'
import UiIco from '../../ui/UiIco.vue'
import { btnBeni, inputDark } from '../../../utils/hibaru.js'

const flowers = ['白百合', '紅薔薇', '白菊', 'かすみ草', '桔梗', '小手毬']
const flowerEmoji = ['🌸', '🌹', '🌼', '🌿', '🔔', '🍃']

const selFlower = ref(0)
const particles = ref([])
const formData = ref({ name: '', location: '', body: '' })

function pickFlower(i) {
  selFlower.value = i
  particles.value = Array.from({ length: 12 }, (_, k) => ({
    id: Date.now() + k,
    x: Math.random() * 100,
    y: Math.random() * 100,
    emoji: flowerEmoji[i],
    size: 14 + Math.random() * 20,
  }))
  window.setTimeout(() => {
    particles.value = []
  }, 1600)
}
</script>

<template>
  <section style="background: rgba(201,169,97,0.04); border: 1px solid var(--kin-500); padding: 40px; margin-bottom: 48px; position: relative; overflow: hidden">
    <div
      v-for="p in particles"
      :key="p.id"
      style="position: absolute; pointer-events: none; animation: particleFade 1.5s ease-out forwards"
      :style="{ left: p.x + '%', top: p.y + '%', fontSize: p.size + 'px' }"
    >
      {{ p.emoji }}
    </div>
    <h3 style="font-family: var(--ff-mincho); font-size: 22px; margin: 0 0 8px">献花する</h3>
    <p style="font-size: 13px; color: var(--paper-200); margin-bottom: 24px">お花を選び、短いメッセージをお書きください。</p>
    <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px; margin-bottom: 24px">
      <button
        v-for="(f, i) in flowers"
        :key="f"
        type="button"
        :style="{
          background: selFlower === i ? 'var(--beni-700)' : 'transparent',
          border: `1px solid ${selFlower === i ? 'var(--kin-500)' : 'rgba(201,169,97,0.4)'}`,
          color: 'var(--paper-100)',
          padding: '14px 6px',
          cursor: 'pointer',
          fontFamily: 'var(--ff-mincho)',
          fontSize: '12px',
          letterSpacing: '0.08em',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '6px',
        }"
        :aria-pressed="selFlower === i"
        :aria-label="f + 'を選択'"
        @click="pickFlower(i)"
      >
        <span style="font-size: 20px">{{ flowerEmoji[i] }}</span>
        {{ f }}
      </button>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px">
      <input v-model="formData.name" placeholder="お名前（匿名可）" :style="inputDark" aria-label="お名前" />
      <input v-model="formData.location" placeholder="お住まい" :style="inputDark" aria-label="お住まい" />
    </div>
    <textarea v-model="formData.body" rows="4" placeholder="ひばりさんへ、一言——" :style="{ ...inputDark, resize: 'vertical', marginBottom: '16px' }" aria-label="メッセージ" />
    <button type="button" :style="btnBeni" aria-label="献花する">献花する <UiIco name="flower" :size="14" /></button>
  </section>
</template>
