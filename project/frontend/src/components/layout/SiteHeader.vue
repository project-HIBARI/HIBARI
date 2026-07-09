<script setup>
/**
 * 部品名: 共通サイトヘッダー
 * 用途: ロゴ・ナビ・検索・ログイン/ファンクラブ加入・文字サイズ（レスポンシブ・1段構成）
 */
import { ref, onMounted, onUnmounted } from 'vue'
import TextSizeControl from '../ui/TextSizeControl.vue'
import HeaderSearch from './HeaderSearch.vue'
import FanclubMembershipBadge from './FanclubMembershipBadge.vue'

defineProps({
  items: { type: Array, required: true },
  page: { type: String, required: true },
  isLoggedIn: { type: Boolean, default: false },
  userName: { type: String, default: '' },
  membership: { type: String, default: 'general' },
  isFanclubMember: { type: Boolean, default: false },
  menuOpen: { type: Boolean, default: false },
  showPlatformBack: { type: Boolean, default: false },
  authOnPlatformOnly: { type: Boolean, default: false },
})

const emit = defineEmits(['logo', 'navigate', 'toggle-drawer', 'open-auth', 'exit-platform'])

const logoSrc = '/images/misorahibari-logo-cropped.png'
const scrolled = ref(false)

function onScroll() {
  scrolled.value = window.scrollY > 20
}

onMounted(() => {
  onScroll()
  window.addEventListener('scroll', onScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<template>
  <header
    role="banner"
    class="site-header"
    :class="{ 'site-header--scrolled': scrolled, 'site-header--menu-open': menuOpen }"
  >
    <div class="site-header__inner">
      <button
        v-if="showPlatformBack"
        type="button"
        class="site-header__platform-back"
        @click="emit('exit-platform')"
      >
        <span class="site-header__platform-back-icon" aria-hidden="true">←</span>
        Music Memories
      </button>

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
        <HeaderSearch class="site-header__search-inline" @navigate="(page) => emit('navigate', page)" />

        <TextSizeControl tone="ink" variant="header" class="site-header__text-size" />

        <FanclubMembershipBadge
          v-if="authOnPlatformOnly && isLoggedIn"
          :user-name="userName"
          :membership="membership"
          :is-fanclub-member="isFanclubMember"
        />
      </div>

      <button
        type="button"
        class="site-header__menu"
        :class="{ 'site-header__menu--open': menuOpen }"
        :aria-label="menuOpen ? 'メニューを閉じる' : 'メニューを開く'"
        :aria-expanded="menuOpen"
        @click="emit('toggle-drawer')"
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
  background: linear-gradient(180deg, #fffefb 0%, #fdf9f5 100%);
  border-bottom: 1px solid var(--site-border);
  box-shadow: 0 2px 12px rgba(60, 40, 30, 0.04);
  transition:
    background 0.55s ease,
    box-shadow 0.55s ease,
    border-color 0.55s ease,
    backdrop-filter 0.55s ease;
}

.site-header__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  width: 100%;
  max-width: 1520px;
  margin: 0 auto;
  padding: 14px 16px;
  min-width: 0;
}

.site-header__platform-back {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin: 0;
  padding: 6px 10px;
  border: 1px solid var(--site-border);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.7);
  color: var(--murasaki-700);
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.06em;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s, color 0.2s;
}

.site-header__platform-back:hover {
  background: #fff;
  border-color: var(--murasaki-400);
  color: var(--murasaki-800);
}

.site-header__platform-back-icon {
  font-size: 12px;
  line-height: 1;
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
  width: min(168px, 48vw);
  height: auto;
  object-fit: contain;
  object-position: left center;
}

/* 1099px以下: ナビ非表示・ハンバーガー */
.site-header__nav {
  display: none;
}

.site-header__actions-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
  margin-left: auto;
}

.site-header__search-inline {
  flex-shrink: 1;
  min-width: 0;
}

.site-header__auth {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  margin-left: auto;
}

.site-header__text-size {
  display: none;
  flex-shrink: 0;
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
  position: relative;
  z-index: 220;
}

.site-header__menu-line {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--site-text);
  border-radius: 1px;
  transform-origin: center;
  transition:
    transform 0.48s cubic-bezier(0.22, 1, 0.36, 1),
    opacity 0.32s ease,
    background 0.25s ease;
}

.site-header__menu--open .site-header__menu-line:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.site-header__menu--open .site-header__menu-line:nth-child(2) {
  opacity: 0;
  transform: scaleX(0);
}

.site-header__menu--open .site-header__menu-line:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

.site-header--menu-open {
  z-index: 250;
  background: transparent;
  border-color: transparent;
  box-shadow: none;
}

@media (max-width: 1099px) {
  .site-header--menu-open .site-header__logo,
  .site-header--menu-open .site-header__actions-bar {
    visibility: hidden;
    pointer-events: none;
  }

  .site-header--menu-open .site-header__inner {
    justify-content: flex-end;
  }

  .site-header--menu-open .site-header__menu {
    position: fixed;
    top: 14px;
    right: 14px;
    padding: 10px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.75);
    box-shadow: 0 2px 12px rgba(40, 30, 25, 0.12);
  }
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
  padding: 6px 12px;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
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

@media (prefers-reduced-motion: reduce) {
  .site-header__menu-line {
    transition: none !important;
  }

  .site-header__menu--open .site-header__menu-line:nth-child(1),
  .site-header__menu--open .site-header__menu-line:nth-child(2),
  .site-header__menu--open .site-header__menu-line:nth-child(3) {
    transform: none;
    opacity: 1;
  }
}

/* 768px以上1099px以下: ヘッダーに検索・認証を表示 */
@media (min-width: 768px) and (max-width: 1099px) {
  .site-header__inner {
    padding: 14px 20px;
    gap: 12px;
  }

  .site-header__logo-img {
    width: min(180px, 36vw);
  }

  .site-header__actions-primary {
    gap: 10px;
  }

  .site-header__auth {
    gap: 8px;
  }

  .site-header__btn {
    padding: 7px 14px;
    font-size: 13px;
  }
}

/* 767px以下: 認証ボタンはドロワー内、ヘッダーは検索+メニュー */
@media (max-width: 767px) {
  .site-header__inner {
    padding: 12px 14px;
    gap: 8px;
  }

  .site-header__logo-img {
    width: min(156px, 52vw);
  }

  .site-header__auth {
    display: none;
  }
}

/* 1100px以上: 横並びナビ（コンパクト） */
@media (min-width: 1100px) {
  .site-header__inner {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr) auto;
    align-items: center;
    column-gap: 20px;
    padding: 14px 24px;
    min-height: 80px;
  }

  .site-header__logo {
    grid-column: 1;
    justify-self: start;
    padding-right: 12px;
  }

  .site-header__logo-img {
    width: 150px;
  }

  .site-header__nav {
    display: flex;
    grid-column: 2;
    justify-self: center;
    align-items: center;
    justify-content: center;
    flex-wrap: nowrap;
    gap: 10px;
    min-width: 0;
  }

  .site-header__nav-link {
    flex: 0 0 auto;
    padding: 6px 0;
    margin: 0;
    border: 0;
    border-bottom: none;
    background: transparent;
    cursor: pointer;
    font-family: var(--ff-sans-jp);
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.05em;
    color: var(--site-text);
    white-space: nowrap;
    transition: color 0.2s, border-color 0.2s;
  }

  .site-header__nav-link:hover {
    color: var(--ink-700);
  }

  .site-header__nav-link--active {
    color: var(--murasaki-700);
    font-weight: 700;
  }

  .site-header__actions-bar {
    grid-column: 3;
    justify-self: end;
    margin-left: 0;
    gap: 12px;
    flex-wrap: nowrap;
  }

  .site-header__auth {
    order: 3;
    margin-left: 0;
  }

  .site-header__text-size {
    display: block;
    order: 2;
  }

  .site-header__search-inline {
    order: 1;
  }

  .site-header__text-size :deep(.text-size-control__label) {
    display: none;
  }

  .site-header__menu {
    display: none;
  }

  .site-header__btn {
    padding: 6px 12px;
    font-size: 12px;
  }
}

/* 1280px以上: フルPC表示 */
@media (min-width: 1280px) {
  .site-header__inner {
    column-gap: 28px;
    padding: 16px 32px;
    min-height: 88px;
  }

  .site-header__logo {
    padding-right: 20px;
  }

  .site-header__logo-img {
    width: 180px;
  }

  .site-header__nav {
    gap: 16px;
  }

  .site-header__nav-link {
    font-size: 13px;
    letter-spacing: 0.08em;
  }

  .site-header__actions-bar {
    gap: 14px;
  }

  .site-header__actions-primary {
    gap: 12px;
  }

  .site-header__auth {
    gap: 10px;
  }

  .site-header__btn {
    padding: 7px 16px;
    font-size: 13px;
  }

  .site-header__text-size :deep(.text-size-control__btn) {
    min-width: 28px;
    height: 28px;
    font-size: 12px;
  }

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

/* 1360px以上: ゆとりあるフル表示 */
@media (min-width: 1360px) {
  .site-header__inner {
    column-gap: 32px;
    padding: 18px 36px;
  }

  .site-header__logo {
    padding-right: 24px;
  }

  .site-header__logo-img {
    width: 198px;
  }

  .site-header__nav {
    gap: 18px;
  }

  .site-header__nav-link {
    font-size: 14px;
    letter-spacing: 0.08em;
  }

  .site-header__actions-bar {
    gap: 16px;
  }

  .site-header__text-size :deep(.text-size-control__label) {
    display: inline;
    font-size: 12px;
  }

  .site-header__text-size :deep(.text-size-control__label)::after {
    content: none;
  }
}
</style>
