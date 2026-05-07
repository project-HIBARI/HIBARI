<script setup>
/**
 * 部品名: モーダル共通シェル
 * 役割: オーバーレイ＋枠＋閉じるボタン。ESC で閉じる
 */
import { onMounted, onUnmounted } from 'vue'

defineProps({
  title: { type: String, required: true },
})

const emit = defineEmits(['close'])

function onKey(e) {
  if (e.key === 'Escape') emit('close')
}

onMounted(() => window.addEventListener('keydown', onKey))
onUnmounted(() => window.removeEventListener('keydown', onKey))
</script>

<template>
  <div
    role="dialog"
    aria-modal="true"
    :aria-label="title"
    style="position: fixed; inset: 0; z-index: 400; display: flex; align-items: center; justify-content: center; padding: 20px"
  >
    <div style="position: absolute; inset: 0; background: rgba(0,0,0,0.8)" @click="emit('close')" />
    <div
      style="position: relative; background: #0d0806; border: 1px solid var(--kin-500); padding: 40px; width: 100%; max-width: 600px; max-height: 85vh; overflow-y: auto; z-index: 1"
    >
      <button
        type="button"
        style="position: absolute; top: 16px; right: 16px; background: transparent; border: 0; color: var(--paper-300); cursor: pointer; font-size: 22px"
        aria-label="閉じる"
        @click="emit('close')"
      >
        ✕
      </button>
      <div
        style="font-family: var(--ff-mincho); font-size: 22px; font-weight: 700; margin-bottom: 24px; letter-spacing: 0.1em; color: var(--paper-50)"
      >
        {{ title }}
      </div>
      <hr class="hr-gold" style="margin-bottom: 24px" />
      <slot />
    </div>
  </div>
</template>
