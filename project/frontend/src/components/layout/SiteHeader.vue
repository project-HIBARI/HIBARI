<script setup>
/**
 * 部品名: 共通サイトヘッダー
 * 用途: ロゴ・ナビ・検索・ログイン/ファンクラブ加入・文字サイズ（1段構成）
 */
import UiIco from '../ui/UiIco.vue'
import TextSizeControl from '../ui/TextSizeControl.vue'

defineProps({
  items: { type: Array, required: true },
  page: { type: String, required: true },
})

const emit = defineEmits(['logo', 'navigate', 'open-drawer', 'open-auth', 'open-search'])

const logoSrc = '/images/misorahibari-logo-cropped.png'
</script>

<template>
  <header role="banner" class="site-header">
    <div class="site-header__inner">
      <button
        type="button"
        class="site-header__logo"
        aria-label="ホームへ"
        @click="emit('logo')"
      >
        <img
          :src="logoSrc"
          alt="美空ひばり 公式ファンサイト"
          class="site-header__logo-img"
          width="948"
          height="337"
          decoding="async"
        />
      </button>

      <nav
        class="site-header__nav"
        role="navigation"
        aria-label="メインナビゲーション"
      >
        <button
          v-for="n in items"
          :key="n.id"
          type="button"
          class="site-header__nav-link"
          :class="{ 'site-header__nav-link--active': page === n.id }"
          :aria-current="page === n.id ? 'page' : undefined"
          @click="emit('navigate', n.id)"
        >
          {{ n.label }}
        </button>
      </nav>

      <div class="site-header__actions-bar">
        <div class="site-header__actions-primary">
          <button
            type="button"
            class="site-header__search"
            aria-label="検索（準備中）"
            @click="emit('open-search')"
          >
            <UiIco name="search" :size="20" color="var(--site-text)" />
          </button>

          <div class="site-header__auth">
            <button
              type="button"
              class="site-header__btn site-header__btn--login"
              @click="emit('open-auth', 'login')"
            >
              ログイン
            </button>
            <button
              type="button"
              class="site-header__btn site-header__btn--register"
              @click="emit('open-auth', 'register')"
            >
              ファンクラブ加入
            </button>
          </div>
        </div>

        <TextSizeControl tone="ink" variant="header" class="site-header__text-size" />
      </div>

      <button
        type="button"
        class="site-header__menu"
        aria-label="メニューを開く"
        @click="emit('open-drawer')"
      >
        <span v-for="i in 3" :key="i" class="site-header__menu-line" />
      </button>
    </div>
  </header>
</template>

<style scoped>
.site-header {
  position: sticky;
  top: 0;
  z-index: 50;
  width: 100%;
  max-width: 100%;
  overflow-x: clip;
  background: linear-gradient(180deg, #fffefb 0%, #fdf9f5 100%);
  border-bottom: 1px solid var(--site-border);
  box-shadow: 0 2px 12px rgba(60, 40, 30, 0.04);
}

.site-header__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  width: 100%;
  max-width: 1520px;
  margin: 0 auto;
  padding: 16px 24px;
  min-width: 0;
}

.site-header__logo {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  padding: 4px 0;
  margin: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.site-header__logo-img {
  display: block;
  width: min(180px, 52vw);
  height: auto;
  object-fit: contain;
  object-position: left center;
}

.site-header__nav,
.site-header__actions-bar {
  display: none;
}

.site-header__menu {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  flex-shrink: 0;
  padding: 8px;
  margin: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.site-header__menu-line {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--site-text);
  border-radius: 1px;
}

.site-header__actions-bar {
  align-items: center;
  gap: 14px;
  flex-shrink: 0;
}

.site-header__actions-primary {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-shrink: 0;
}

.site-header__auth {
  display: flex;
  align-items: center;
  gap: 10px;
}

.site-header__search {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  margin: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
  color: var(--site-text);
  transition: opacity 0.2s;
  flex-shrink: 0;
}

.site-header__search:hover {
  opacity: 0.65;
}

.site-header__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 7px 16px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.06em;
  white-space: nowrap;
  border-radius: 999px;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s, color 0.2s, box-shadow 0.2s;
}

.site-header__btn--login {
  background: #fff;
  color: var(--site-text);
  border: 1px solid var(--kin-500);
}

.site-header__btn--login:hover {
  background: #fffefb;
  border-color: var(--kin-600);
  box-shadow: 0 2px 8px rgba(201, 169, 97, 0.15);
}

.site-header__btn--register {
  background: var(--murasaki-700);
  color: #fff;
  border: 1px solid var(--murasaki-800);
  box-shadow: 0 2px 8px rgba(93, 58, 107, 0.18);
}

.site-header__btn--register:hover {
  background: var(--murasaki-800);
}

/* 文字サイズUIコンパクト化 */
.site-header__text-size :deep(.text-size-control) {
  gap: 6px;
}

.site-header__text-size :deep(.text-size-control__group) {
  gap: 2px;
  padding: 1px;
}

.site-header__text-size :deep(.text-size-control__btn) {
  min-width: 26px;
  height: 26px;
  padding: 0 4px;
  font-size: 11px;
}

@media (min-width: 1024px) {
  .site-header__inner {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr) auto;
    grid-template-rows: auto;
    align-items: center;
    column-gap: 28px;
    padding: 16px 28px;
    min-height: 88px;
  }

  .site-header__logo {
    grid-column: 1;
    grid-row: 1;
    justify-self: start;
    padding-right: 24px;
  }

  .site-header__logo-img {
    width: 170px;
  }

  .site-header__nav {
    display: flex;
    grid-column: 2;
    grid-row: 1;
    justify-self: center;
    align-items: center;
    flex-wrap: nowrap;
    gap: 16px;
    flex-shrink: 0;
  }

  .site-header__nav-link {
    flex: 0 0 auto;
    padding: 6px 0;
    margin: 0;
    border: 0;
    border-bottom: 2px solid transparent;
    background: transparent;
    cursor: pointer;
    font-family: var(--ff-sans-jp);
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.06em;
    color: var(--site-text);
    white-space: nowrap;
    transition: color 0.2s, border-color 0.2s;
  }

  .site-header__nav-link:hover {
    color: var(--ink-700);
    border-bottom-color: var(--kin-400);
  }

  .site-header__nav-link--active {
    color: var(--site-text);
    font-weight: 700;
    border-bottom-color: var(--kin-500);
  }

  .site-header__actions-bar {
    display: flex;
    grid-column: 3;
    grid-row: 1;
    justify-self: end;
    gap: 14px;
  }

  .site-header__menu {
    display: none;
  }

  /* 1360px未満: ラベル非表示 */
  .site-header__text-size :deep(.text-size-control__label) {
    display: none;
  }
}

@media (min-width: 1200px) {
  .site-header__inner {
    column-gap: 32px;
    padding: 18px 32px;
  }

  .site-header__logo {
    padding-right: 28px;
  }

  .site-header__logo-img {
    width: 188px;
  }

  .site-header__nav {
    gap: 20px;
  }

  .site-header__nav-link {
    font-size: 13px;
    letter-spacing: 0.08em;
  }

  .site-header__actions-bar {
    gap: 16px;
  }

  .site-header__text-size :deep(.text-size-control__btn) {
    min-width: 28px;
    height: 28px;
    font-size: 12px;
  }

  /* 1200〜1359px: ラベルを「文字」に短縮 */
  .site-header__text-size :deep(.text-size-control__label) {
    display: inline;
    font-size: 0;
    letter-spacing: 0;
  }

  .site-header__text-size :deep(.text-size-control__label)::after {
    content: '文字';
    font-size: 12px;
    letter-spacing: 0.04em;
  }
}

@media (min-width: 1360px) {
  .site-header__inner {
    column-gap: 36px;
    padding: 18px 36px;
  }

  .site-header__logo {
    padding-right: 32px;
  }

  .site-header__logo-img {
    width: 205px;
  }

  .site-header__nav {
    gap: 22px;
  }

  .site-header__nav-link {
    font-size: 14px;
    letter-spacing: 0.1em;
  }

  .site-header__actions-bar {
    gap: 18px;
  }

  .site-header__text-size :deep(.text-size-control__label) {
    display: inline;
    font-size: 12px;
  }

  .site-header__text-size :deep(.text-size-control__label)::after {
    content: none;
  }
}

/* 1024〜1099px: 横幅不足時のみ文字サイズを2段目へ */
@media (max-width: 1099px) and (min-width: 1024px) {
  .site-header__inner {
    grid-template-rows: auto auto;
    row-gap: 8px;
    column-gap: 24px;
    padding: 14px 24px 10px;
  }

  .site-header__logo-img {
    width: 165px;
  }

  .site-header__nav {
    gap: 14px;
  }

  .site-header__actions-bar {
    display: contents;
  }

  .site-header__actions-primary {
    grid-column: 3;
    grid-row: 1;
    justify-self: end;
    gap: 12px;
  }

  .site-header__text-size {
    grid-column: 1 / -1;
    grid-row: 2;
    justify-self: end;
  }

  .site-header__btn {
    padding: 6px 12px;
    font-size: 12px;
  }
}

@media (max-width: 767px) {
  .site-header__inner {
    padding: 14px 16px;
  }

  .site-header__logo-img {
    width: min(170px, 54vw);
  }
}
</style>
