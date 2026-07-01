<script setup>
/**
 * 部品名: サイトヘッダー（ロゴ行）
 * 役割: ロゴ・検索・ログイン/新規登録・SP はハンバーガー
 */
import Hanko from '../ui/Hanko.vue'
import TextSizeControl from '../ui/TextSizeControl.vue'
import UiButton from '../ui/UiButton.vue'
import UiIco from '../ui/UiIco.vue'

defineProps({
  isMobile: { type: Boolean, default: false },
})

const emit = defineEmits(['logo', 'open-drawer', 'open-auth', 'open-search'])
</script>

<template>
  <div class="header-bar">
    <button
      type="button"
      class="header-bar__logo"
      aria-label="ホームへ"
      @click="emit('logo')"
    >
      <Hanko text="雲雀" :size="40" />
      <div class="header-bar__brand">
        <div class="header-bar__title">美空ひばり</div>
        <div class="header-bar__subtitle">公式ファンサイト</div>
      </div>
    </button>

    <div class="pc-only header-bar__actions">
      <TextSizeControl tone="ink" />
      <button
        type="button"
        class="header-bar__search"
        aria-label="検索（準備中）"
        @click="emit('open-search')"
      >
        <UiIco name="search" :size="18" color="var(--site-text-muted)" />
      </button>
      <UiButton variant="outline" size="sm" @click="emit('open-auth', 'login')">ログイン</UiButton>
      <UiButton variant="primary" size="sm" @click="emit('open-auth', 'register')">新規登録</UiButton>
    </div>

    <button
      type="button"
      class="sp-only header-bar__menu"
      aria-label="メニューを開く"
      @click="emit('open-drawer')"
    >
      <span v-for="i in 3" :key="i" class="header-bar__menu-line" />
      <span class="header-bar__menu-label">メニュー</span>
    </button>
  </div>
</template>

<style scoped>
.header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 32px;
  gap: 16px;
}
.header-bar__logo {
  background: transparent;
  border: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 0;
  text-align: left;
}
.header-bar__brand {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.header-bar__title {
  font-family: var(--ff-mincho);
  font-weight: 800;
  font-size: 18px;
  letter-spacing: 0.14em;
  color: var(--site-text);
}
.header-bar__subtitle {
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  letter-spacing: 0.08em;
  color: var(--site-text-muted);
}
.header-bar__actions {
  display: flex;
  align-items: center;
  gap: 10px;
}
.header-bar__search {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: var(--site-surface-muted);
  border: 1px solid var(--site-border);
  border-radius: 50%;
  cursor: pointer;
  transition: border-color 0.2s;
}
.header-bar__search:hover {
  border-color: var(--murasaki-400);
}
.header-bar__menu {
  background: transparent;
  border: 0;
  cursor: pointer;
  color: var(--site-text);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  padding: 8px;
}
.header-bar__menu-line {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--site-text);
}
.header-bar__menu-label {
  font-family: var(--ff-mincho);
  font-size: 9px;
  letter-spacing: 0.1em;
  margin-top: 2px;
}
@media (max-width: 767px) {
  .header-bar {
    padding: 12px 16px;
  }
}
</style>
