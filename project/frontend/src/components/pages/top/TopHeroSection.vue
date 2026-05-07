<script setup>
/**
 * 部品名: トップ — ヒーロー（見出し＋導線＋ポートレート枠）
 */
import Photo from '../../ui/Photo.vue'
import UiIco from '../../ui/UiIco.vue'
import { btnBeni, btnGhost } from '../../../utils/hibaru.js'

const emit = defineEmits(['navigate'])
</script>

<template>
  <section style="display: grid; grid-template-columns: 1fr 440px; gap: 64px; align-items: center; min-height: 480px; margin-bottom: 8px" class="hero-grid">
    <div>
      <div
        style="font-family: var(--ff-latin); font-style: italic; font-size: 14px; letter-spacing: 0.4em; color: var(--kin-500); margin-bottom: 24px"
      >
        — THE SHŌWA SONGSTRESS —
      </div>
      <h1
        class="page-h1-scale"
        style="font-family: var(--ff-mincho); font-size: 88px; font-weight: 800; line-height: 1.05; margin: 0; letter-spacing: 0.08em"
      >
        <span style="color: var(--beni-500)">永遠</span>の<br />歌姫へ、
      </h1>
      <p style="font-size: 15px; line-height: 2.2; color: var(--paper-200); margin-top: 32px; max-width: 460px; letter-spacing: 0.05em">
        昭和十二年、横浜磯子に生を受け、八歳で初舞台。<br />
        生涯一千五百曲を超える録音を遺し、昭和という時代を歌い続けた不死鳥。<br />
        このサイトは、ひばりさんを愛し続けるファンの集いの場です。
      </p>
      <div style="display: flex; gap: 16px; margin-top: 36px; flex-wrap: wrap">
        <button type="button" :style="btnBeni" aria-label="ディスコグラフィへ" @click="emit('navigate', 'disco')">
          ディスコグラフィを巡る <UiIco name="arrow" :size="15" />
        </button>
        <button type="button" :style="btnGhost" aria-label="思い出掲示板へ" @click="emit('navigate', 'memories')">思い出を分かち合う</button>
      </div>
    </div>
    <div style="position: relative">
      <Photo :w="420" :h="540" caption="portrait · stage costume · c.1965" variant="dark" />
      <div
        style="position: absolute; bottom: -14px; right: -14px; background: var(--beni-700); padding: 10px 18px; font-family: var(--ff-mincho); font-size: 12px; letter-spacing: 0.2em; color: var(--paper-50); border: 1px solid var(--kin-500)"
      >
        昭和四十年頃
      </div>
    </div>
  </section>
</template>
