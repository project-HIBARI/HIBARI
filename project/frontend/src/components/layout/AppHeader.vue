<script setup>
/**
 * 部品名: 共通サイトヘッダー
 * 用途: ロゴ・グローバルナビ・検索・ログイン/新規登録（全ページ共通）
 */
import TextSizeControl from '../ui/TextSizeControl.vue'
import UiButton from '../ui/UiButton.vue'
import UiIco from '../ui/UiIco.vue'

defineProps({
  items: { type: Array, required: true },
  page: { type: String, required: true },
})

const emit = defineEmits(['logo', 'navigate', 'open-drawer', 'open-auth', 'open-search'])

const logoSrc = '/images/misorahibari-logo.png'
</script>

<template>
  <header role="banner" class="app-header">
    <div class="header-bar">
      <button
        type="button"
        class="header-bar__logo"
        aria-label="ホームへ"
        @click="emit('logo')"
      >
        <img
          :src="logoSrc"
          alt=""
          class="header-bar__logo-img"
          width="220"
          height="48"
          decoding="async"
        />
      </button>

      <nav
        class="app-main-nav header-bar__nav"
        role="navigation"
        aria-label="メインナビゲーション"
      >
        <button
          v-for="n in items"
          :key="n.id"
          type="button"
          class="app-main-nav__link"
          :class="{ 'app-main-nav__link--active': page === n.id }"
          :aria-current="page === n.id ? 'page' : undefined"
          @click="emit('navigate', n.id)"
        >
          {{ n.label }}
        </button>
      </nav>

      <div class="header-bar__actions">
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
        <UiButton variant="primary" size="sm" @click="emit('open-auth', 'register')">ファンクラブ加入</UiButton>
      </div>

      <button
        type="button"
        class="header-bar__menu"
        aria-label="メニューを開く"
        @click="emit('open-drawer')"
      >
        <span v-for="i in 3" :key="i" class="header-bar__menu-line" />
        <span class="header-bar__menu-label">メニュー</span>
      </button>
    </div>
  </header>
</template>

<style scoped>
.header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 0 14px;
  gap: 12px;
  width: 100%;
  min-width: 0;
}
.header-bar__logo {
  background: transparent;
  border: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 0;
  flex-shrink: 0;
  min-width: 0;
}
.header-bar__logo-img {
  height: 44px;
  width: auto;
  max-width: min(220px, 52vw);
  object-fit: contain;
  object-position: left center;
  display: block;
}
.header-bar__nav,
.header-bar__actions {
  display: none;
}
.header-bar__actions {
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}
.header-bar__search {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  background: var(--site-surface);
  border: 1px solid var(--site-border);
  border-radius: 50%;
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.header-bar__search:hover {
  border-color: var(--murasaki-400);
  box-shadow: var(--site-shadow);
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
  flex-shrink: 0;
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

@media (min-width: 1024px) {
  .header-bar {
    display: grid;
    grid-template-columns: minmax(0, auto) minmax(0, 1fr) minmax(0, auto);
    align-items: center;
    column-gap: 16px;
    padding-bottom: 0;
  }
  .header-bar__logo {
    grid-column: 1;
    justify-self: start;
  }
  .header-bar__nav {
    display: flex;
    grid-column: 2;
    justify-self: center;
    justify-content: center;
    min-width: 0;
    max-width: 100%;
    border-top: 0;
    background: transparent;
    overflow: hidden;
    gap: 2px;
  }
  .header-bar__actions {
    display: flex;
    grid-column: 3;
    justify-self: end;
  }
  .header-bar__menu {
    display: none;
  }
  .header-bar__logo-img {
    height: 48px;
    max-width: 220px;
  }
}

@media (max-width: 767px) {
  .header-bar {
    padding: 0;
  }
  .header-bar__logo-img {
    height: 36px;
    max-width: min(180px, 48vw);
  }
}
</style>

<style scoped>
@media (min-width: 1024px) {
  .header-bar__nav :deep(.app-main-nav__link) {
    flex: 0 1 auto;
    min-width: 0;
    padding: 8px 6px;
    font-size: 12px;
    letter-spacing: 0.04em;
  }
}
@media (min-width: 1280px) {
  .header-bar__nav :deep(.app-main-nav__link) {
    padding: 8px 10px;
    font-size: 13px;
    letter-spacing: 0.06em;
  }
}
</style>
