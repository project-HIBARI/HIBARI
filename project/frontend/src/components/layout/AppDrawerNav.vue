<script setup>
/**
 * 部品名: スマホ用ドロワーナビ
 * 役割: モバイル時のページ切替・ログイン/新規登録・AI 等への導線
 */
import UiButton from '../ui/UiButton.vue'

defineProps({
  open: { type: Boolean, default: false },
  items: { type: Array, required: true },
  page: { type: String, required: true },
})

const emit = defineEmits(['close', 'navigate', 'open-modal', 'open-auth'])
</script>

<template>
  <div v-if="open" role="dialog" aria-modal="true" aria-label="ナビゲーション" class="drawer">
    <div class="drawer__overlay" @click="emit('close')" />
    <div class="drawer__panel">
      <div class="drawer__head">
        <span class="drawer__head-title">メニュー</span>
        <button type="button" class="drawer__close" aria-label="閉じる" @click="emit('close')">✕</button>
      </div>

      <button
        v-for="n in items"
        :key="n.id"
        type="button"
        class="drawer__link"
        :class="{ 'drawer__link--active': page === n.id }"
        :aria-current="page === n.id ? 'page' : undefined"
        @click="emit('navigate', n.id)"
      >
        {{ n.label }}
      </button>

      <div class="drawer__divider" />

      <div class="drawer__auth">
        <UiButton variant="outline" size="md" @click="emit('open-auth', 'login')">ログイン</UiButton>
        <UiButton variant="primary" size="md" @click="emit('open-auth', 'register')">新規登録</UiButton>
      </div>

      <div class="drawer__divider" />

      <button type="button" class="drawer__sub" @click="emit('open-modal', 'fanclub')">✦ ファンクラブ</button>
      <button type="button" class="drawer__sub" @click="emit('open-modal', 'ai')">✦ AI美空ひばり</button>
    </div>
  </div>
</template>

<style scoped>
.drawer {
  position: fixed;
  inset: 0;
  z-index: 200;
}
.drawer__overlay {
  position: absolute;
  inset: 0;
  background: rgba(40, 30, 25, 0.4);
}
.drawer__panel {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: min(300px, 88vw);
  background: var(--site-surface);
  border-left: 1px solid var(--site-border);
  display: flex;
  flex-direction: column;
  box-shadow: var(--site-shadow-md);
}
.drawer__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--site-border);
}
.drawer__head-title {
  font-family: var(--ff-mincho);
  font-size: 15px;
  letter-spacing: 0.1em;
  color: var(--site-text);
}
.drawer__close {
  background: transparent;
  border: 1px solid var(--site-border);
  color: var(--site-text-muted);
  width: 36px;
  height: 36px;
  border-radius: var(--site-radius-sm);
  cursor: pointer;
  font-size: 16px;
}
.drawer__link {
  border: 0;
  background: transparent;
  color: var(--site-text-muted);
  padding: 0 20px;
  min-height: 52px;
  text-align: left;
  cursor: pointer;
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  letter-spacing: 0.06em;
  border-bottom: 1px solid var(--site-border);
}
.drawer__link--active {
  background: var(--murasaki-100);
  color: var(--murasaki-700);
  font-weight: 700;
  border-left: 3px solid var(--murasaki-700);
}
.drawer__divider {
  border-top: 1px solid var(--site-border);
  margin: 8px 0;
}
.drawer__auth {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 12px 20px;
}
.drawer__sub {
  border: 0;
  background: transparent;
  color: var(--murasaki-700);
  padding: 0 20px;
  min-height: 48px;
  text-align: left;
  cursor: pointer;
  font-family: var(--ff-mincho);
  font-size: 14px;
  letter-spacing: 0.08em;
}
</style>
