<script setup>
/**
 * 部品名: ディスコグラフィ — 楽曲詳細ダイアログ
 */
import RecordChip from '../../ui/RecordChip.vue'

defineProps({
  detail: { type: Object, default: null },
})

const emit = defineEmits(['close'])
</script>

<template>
  <div
    v-if="detail"
    role="dialog"
    aria-modal="true"
    :aria-label="detail.title + 'の詳細'"
    style="position: fixed; inset: 0; z-index: 300; display: flex; align-items: center; justify-content: center; padding: 20px"
  >
    <div style="position: absolute; inset: 0; background: rgba(0,0,0,0.75)" @click="emit('close')" />
    <div style="position: relative; background: #0d0806; border: 1px solid var(--kin-500); padding: 40px; max-width: 520px; width: 100%; z-index: 1">
      <button
        type="button"
        style="position: absolute; top: 16px; right: 16px; background: transparent; border: 0; color: var(--paper-300); cursor: pointer; font-size: 20px"
        aria-label="閉じる"
        @click="emit('close')"
      >
        ✕
      </button>
      <div style="display: flex; gap: 24px; align-items: center; margin-bottom: 24px">
        <RecordChip :no="detail.no" color="var(--beni-700)" />
        <div>
          <div style="font-family: var(--ff-mono); font-size: 10px; color: var(--kin-500); letter-spacing: 0.2em">{{ detail.year }} · {{ detail.label }}</div>
          <div style="font-family: var(--ff-mincho); font-size: 28px; font-weight: 700; margin: 6px 0 2px">{{ detail.title }}</div>
          <div style="font-family: var(--ff-latin); font-style: italic; font-size: 13px; color: var(--paper-300)">{{ detail.romaji }}</div>
        </div>
      </div>
      <hr class="hr-gold" style="margin-bottom: 20px" />
      <dl style="display: grid; grid-template-columns: 80px 1fr; gap: 10px 16px; font-size: 14px">
        <dt style="color: var(--kin-500); font-family: var(--ff-mincho)">発売年</dt>
        <dd style="margin: 0">{{ detail.year }}年</dd>
        <dt style="color: var(--kin-500); font-family: var(--ff-mincho)">形態</dt>
        <dd style="margin: 0">{{ detail.type }}</dd>
        <dt style="color: var(--kin-500); font-family: var(--ff-mincho)">ジャンル</dt>
        <dd style="margin: 0">{{ detail.genre }}</dd>
        <dt style="color: var(--kin-500); font-family: var(--ff-mincho)">作詞</dt>
        <dd style="margin: 0">{{ detail.lyric }}</dd>
        <dt style="color: var(--kin-500); font-family: var(--ff-mincho)">作曲</dt>
        <dd style="margin: 0">{{ detail.music }}</dd>
        <dt style="color: var(--kin-500); font-family: var(--ff-mincho)">品番</dt>
        <dd style="margin: 0; font-family: var(--ff-mono); font-size: 12px">{{ detail.no }}</dd>
        <dt style="color: var(--kin-500); font-family: var(--ff-mincho)">レーベル</dt>
        <dd style="margin: 0">{{ detail.label }}</dd>
      </dl>
      <div
        v-if="detail.note"
        style="margin-top: 20px; padding: 14px; background: rgba(201,169,97,0.08); border: 1px solid rgba(201,169,97,0.25); font-size: 13px; color: var(--paper-200); line-height: 1.8"
      >
        {{ detail.note }}
      </div>
    </div>
  </div>
</template>
