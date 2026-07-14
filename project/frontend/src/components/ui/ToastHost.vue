<script setup>
/**
 * 部品名: トースト表示ホスト
 * 用途: useToast() で積まれた通知を画面下部に順番表示する
 */
import { useToast } from '../../composables/useToast.js'

const { toasts, dismissToast } = useToast()
</script>

<template>
  <div class="toast-host" aria-live="polite" role="status">
    <TransitionGroup name="toast-fade">
      <div
        v-for="t in toasts"
        :key="t.id"
        class="toast-host__item"
        :class="`toast-host__item--${t.tone}`"
        @click="dismissToast(t.id)"
      >
        {{ t.message }}
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-host {
  position: fixed;
  left: 50%;
  bottom: calc(84px + env(safe-area-inset-bottom, 0px));
  transform: translateX(-50%);
  z-index: 500;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  pointer-events: none;
  width: 100%;
  padding: 0 16px;
}
.toast-host__item {
  pointer-events: auto;
  max-width: 360px;
  padding: 10px 18px;
  border-radius: 999px;
  background: var(--sns-card-strong, #2b1b31);
  border: 1px solid var(--sns-border, rgba(255, 255, 255, 0.12));
  color: var(--sns-ivory, #f6f0ea);
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  text-align: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  cursor: pointer;
}
.toast-host__item--error {
  border-color: rgba(224, 138, 138, 0.5);
  color: #f2c6c6;
}
.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@media (min-width: 768px) {
  .toast-host {
    bottom: 24px;
  }
}
</style>
