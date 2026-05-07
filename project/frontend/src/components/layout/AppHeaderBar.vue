<script setup>
/**
 * 部品名: サイトヘッダー（ロゴ行）
 * 役割: ロゴ・文字サイズ・映像再生・各種モーダル導線・SP はハンバーガー
 */
import Hanko from '../ui/Hanko.vue'
import TextSizeControl from '../ui/TextSizeControl.vue'
import { hdrBtn } from '../../utils/hibaru.js'

defineProps({
  /** モバイル表示か（767px 未満想定は親で付与） */
  isMobile: { type: Boolean, default: false },
})

const emit = defineEmits(['logo', 'replay-film', 'open-modal', 'open-drawer'])
</script>

<template>
  <div style="display: flex; align-items: center; justify-content: space-between; padding: 14px 32px">
    <button
      type="button"
      style="background: transparent; border: 0; cursor: pointer; display: flex; align-items: center; gap: 12px; padding: 0"
      aria-label="トップへ"
      @click="emit('logo')"
    >
      <Hanko text="雲雀" :size="38" />
      <div>
        <div style="font-family: var(--ff-mincho); font-weight: 800; font-size: 18px; letter-spacing: 0.12em">美空ひばり</div>
        <div style="font-family: var(--ff-latin); font-style: italic; font-size: 10px; opacity: 0.6; letter-spacing: 0.25em">
          MISORA HIBARI · 1937–1989
        </div>
      </div>
    </button>

    <div class="pc-only" style="display: flex; align-items: center; gap: 12px">
      <TextSizeControl tone="paper" />
      <button type="button" :style="hdrBtn" aria-label="オープニング映像を再生" @click="emit('replay-film')">▶ 映像</button>
      <button type="button" :style="hdrBtn" aria-label="ファンクラブ" @click="emit('open-modal', 'fanclub')">ファンクラブ</button>
      <button type="button" :style="hdrBtn" aria-label="グッズ" @click="emit('open-modal', 'goods')">グッズ</button>
      <button type="button" :style="hdrBtn" aria-label="AI美空ひばり" @click="emit('open-modal', 'ai')">AI美空ひばり</button>
    </div>

    <button
      type="button"
      class="sp-only"
      style="background: transparent; border: 0; cursor: pointer; color: var(--paper-100); display: flex; flex-direction: column; align-items: center; gap: 3px; padding: 8px"
      aria-label="メニューを開く"
      @click="emit('open-drawer')"
    >
      <span v-for="i in 3" :key="i" style="display: block; width: 22px; height: 2px; background: var(--paper-100)" />
      <span style="font-family: var(--ff-mincho); font-size: 9px; letter-spacing: 0.1em; margin-top: 2px">メニュー</span>
    </button>
  </div>
</template>
