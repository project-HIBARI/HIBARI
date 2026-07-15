<script setup>
/**
 * 部品名: モーダル共通シェル
 * 役割: オーバーレイ＋枠＋閉じるボタン。ESC で閉じる
 * 備考: body へ Teleport し、親の transform/overflow に影響されず常に画面中央へ表示する
 */
import { onMounted, onUnmounted } from 'vue'

defineProps({
  title: { type: String, required: true },
  wide: { type: Boolean, default: false },
})

const emit = defineEmits(['close'])

function onKey(e) {
  if (e.key === 'Escape') emit('close')
}

onMounted(() => {
  window.addEventListener('keydown', onKey)
  document.body.style.overflow = 'hidden'
})
onUnmounted(() => {
  window.removeEventListener('keydown', onKey)
  document.body.style.overflow = ''
})
</script>

<template>
  <Teleport to="body">
    <div
      role="dialog"
      aria-modal="true"
      :aria-label="title"
      class="modal-shell"
    >
      <div class="modal-shell__overlay" @click="emit('close')" />
      <div class="modal-shell__panel" :class="{ 'modal-shell__panel--wide': wide }">
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
  </Teleport>
</template>

<style scoped>
.modal-shell {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100vw;
  height: 100dvh;
  max-height: 100vh;
  z-index: 400;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  box-sizing: border-box;
  pointer-events: auto;
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
  max-height: 85dvh;
  overflow-y: auto;
  z-index: 1;
  box-shadow: var(--site-shadow-md);
  color: var(--site-text);
  animation: modalShellIn 0.42s cubic-bezier(0.22, 1, 0.36, 1) both;
  box-sizing: border-box;
  min-width: 0;
}
.modal-shell__overlay {
  position: absolute;
  inset: 0;
  background: rgba(40, 30, 25, 0.45);
  animation: modalOverlayIn 0.32s ease both;
}
.modal-shell__panel--wide {
  max-width: 760px;
}
.modal-shell__close {
  position: absolute;
  top: 12px;
  right: 12px;
  background: transparent;
  border: 0;
  color: var(--site-text-muted);
  cursor: pointer;
  font-size: var(--font-size-subtitle);
  line-height: 1;
  min-width: 44px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.modal-shell__close:hover {
  color: var(--murasaki-700);
}
.modal-shell__title {
  font-family: var(--ff-mincho);
  font-size: var(--font-size-subtitle);
  font-weight: 700;
  margin-bottom: 24px;
  letter-spacing: 0.1em;
  color: var(--site-text);
  padding-right: 40px;
  overflow-wrap: anywhere;
  white-space: normal;
}
.modal-shell__rule {
  margin-bottom: 24px;
}

@media (max-width: 767px) {
  .modal-shell {
    padding: 12px;
    padding-top: max(12px, env(safe-area-inset-top, 0px));
    padding-bottom: max(12px, env(safe-area-inset-bottom, 0px));
    align-items: center;
  }
  .modal-shell__panel {
    padding: 24px 20px;
    max-height: 90vh;
    max-height: 90dvh;
  }
  .modal-shell__title {
    font-size: var(--font-size-emphasis);
    margin-bottom: 16px;
    overflow-wrap: anywhere;
  }
  .modal-shell__close {
    min-width: 44px;
    min-height: 44px;
  }
}

@keyframes modalOverlayIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes modalShellIn {
  from {
    opacity: 0;
    transform: scale(0.96) translateY(12px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
</style>
