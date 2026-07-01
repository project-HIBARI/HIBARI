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
    class="modal-shell"
  >
    <div class="modal-shell__overlay" @click="emit('close')" />
    <div class="modal-shell__panel">
      <button
        type="button"
        class="modal-shell__close"
        aria-label="閉じる"
        @click="emit('close')"
      >
        ✕
      </button>
      <div class="modal-shell__title">{{ title }}</div>
      <hr class="hr-gold modal-shell__rule" />
      <slot />
    </div>
  </div>
</template>

<style scoped>
.modal-shell {
  position: fixed;
  inset: 0;
  z-index: 400;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.modal-shell__overlay {
  position: absolute;
  inset: 0;
  background: rgba(40, 30, 25, 0.45);
}
.modal-shell__panel {
  position: relative;
  background: var(--site-surface);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  padding: 40px;
  width: 100%;
  max-width: 600px;
  max-height: 85vh;
  overflow-y: auto;
  z-index: 1;
  box-shadow: var(--site-shadow-md);
  color: var(--site-text);
}
.modal-shell__close {
  position: absolute;
  top: 16px;
  right: 16px;
  background: transparent;
  border: 0;
  color: var(--site-text-muted);
  cursor: pointer;
  font-size: 22px;
  line-height: 1;
}
.modal-shell__close:hover {
  color: var(--murasaki-700);
}
.modal-shell__title {
  font-family: var(--ff-mincho);
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 24px;
  letter-spacing: 0.1em;
  color: var(--site-text);
  padding-right: 32px;
}
.modal-shell__rule {
  margin-bottom: 24px;
}
</style>
