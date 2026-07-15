<script setup>
/**
 * 部品名: Music Memories プラットフォームシェル
 * 役割: ハブ・ログイン・新規登録・アカウント設定を束ねる
 */
import { computed, ref, watch } from 'vue'
import PageMusicMemories from '../pages/PageMusicMemories.vue'
import PageMusicConnections from '../pages/PageMusicConnections.vue'
import PageArtistEncyclopedia from '../pages/PageArtistEncyclopedia.vue'
import PageArtistDiagnosis from '../pages/PageArtistDiagnosis.vue'
import PageLogin from '../pages/PageLogin.vue'
import PageRegister from '../pages/PageRegister.vue'
import PagePlatformOpenChat from '../pages/PagePlatformOpenChat.vue'
import PageSnsFeed from '../pages/PageSnsFeed.vue'
import PageSnsDiscover from '../pages/PageSnsDiscover.vue'
import PageSnsProfile from '../pages/PageSnsProfile.vue'
import PageSnsDm from '../pages/PageSnsDm.vue'
import HeaderAccountMenu from './HeaderAccountMenu.vue'
import PlatformDrawerNav from './PlatformDrawerNav.vue'
import AccountModal from '../modals/AccountModal.vue'
import MusicMemoriesLogo from '../brand/MusicMemoriesLogo.vue'
import UiIco from '../ui/UiIco.vue'
import ToastHost from '../ui/ToastHost.vue'
import { useAuth } from '../../composables/useAuth.js'
import { useBodyScrollLock } from '../../composables/useBodyScrollLock.js'
import { useSnsDmUnread } from '../../composables/useSnsDmUnread.js'
import { MEMBERSHIP } from '../../constants/membership.js'
import { SITE_NAME } from '../../constants/site.js'

const props = defineProps({
  view: { type: String, default: 'hub' },
  isLoggedIn: { type: Boolean, default: false },
  userName: { type: String, default: '' },
  membership: { type: String, default: null },
  registerPlan: { type: String, default: MEMBERSHIP.GENERAL },
  pendingDiscoverSong: { type: Object, default: null },
})

const emit = defineEmits([
  'update:view',
  'enter-site',
  'login-success',
  'register-complete',
  'logout',
  'open-auth',
  'user-updated',
  'discover-song-consumed',
])

const modal = ref(null)
const drawerOpen = ref(false)
const snsCreateIntent = ref(0)
const profileAccountId = ref(null)
const dmTargetAccountId = ref(null)

const navItems = [
  { id: 'hub', label: 'ホーム' },
  { id: 'sns', label: 'みんなの投稿' },
  { id: 'discover', label: '検索' },
  { id: 'open-chat', label: 'オープンチャット' },
  { id: 'connections', label: '曲の繋がり' },
  { id: 'artist-encyclopedia', label: 'アーティスト図鑑' },
  { id: 'artist-diagnosis', label: 'アーティスト診断' },
]

const drawerPage = computed(() => (props.view === 'profile' ? 'sns' : props.view))

const { user: authUser, isLoggedIn: authIsLoggedIn } = useAuth()
const { unreadCount: dmUnreadCount, startPolling: startDmPolling, stopPolling: stopDmPolling } = useSnsDmUnread()

useBodyScrollLock(drawerOpen)

watch(authIsLoggedIn, (loggedIn) => {
  if (loggedIn) startDmPolling()
  else stopDmPolling()
}, { immediate: true })

function setView(next) {
  drawerOpen.value = false
  emit('update:view', next)
}

function onDrawerNavigate(id) {
  setView(id)
}

function openProfile(accountId) {
  profileAccountId.value = accountId
  setView('profile')
}

function openDm(accountId = null) {
  if (!authUser.value) {
    onOpenAuth('login')
    return
  }
  dmTargetAccountId.value = accountId
  setView('dm')
}

function openMyProfile() {
  if (!authUser.value) {
    onOpenAuth('login')
    return
  }
  openProfile(authUser.value.account_id)
}

function onOpenAuth(mode) {
  if (mode === 'login') {
    setView('login')
    return
  }
  if (mode === 'register' || mode === 'register-premium') {
    emit('open-auth', { mode })
    setView('register')
    return
  }
  if (mode === 'open-chat') {
    setView('open-chat')
    return
  }
  emit('open-auth', { mode })
}

function onSnsNeedAuth(payload) {
  onOpenAuth(payload?.mode || 'login')
}

function onLoginSuccess(user) {
  emit('login-success', user)
}

function onRegisterComplete(user) {
  emit('register-complete', user)
}

function onLogout() {
  drawerOpen.value = false
  modal.value = null
  emit('logout')
}

function onUserUpdated(account) {
  emit('user-updated', account)
}
</script>

<template>
  <div class="platform-shell mm-sns">
    <header
      class="platform-shell__header"
      :class="{ 'platform-shell__header--menu-open': drawerOpen }"
      role="banner"
    >
      <div class="platform-shell__header-inner">
        <button
          type="button"
          class="platform-shell__brand"
          aria-label="Music Memories ホーム"
          @click="setView('hub')"
        >
          <MusicMemoriesLogo variant="full" size="md" />
        </button>

        <nav class="platform-shell__nav" aria-label="プラットフォームナビ">
          <button
            type="button"
            class="platform-shell__nav-btn"
            :class="{ 'platform-shell__nav-btn--active': view === 'hub' }"
            @click="setView('hub')"
          >
            <UiIco name="home" :size="14" />
            ホーム
          </button>
          <button
            type="button"
            class="platform-shell__nav-btn"
            :class="{ 'platform-shell__nav-btn--active': view === 'sns' || view === 'profile' }"
            @click="setView('sns')"
          >
            <UiIco name="user" :size="14" />
            みんなの投稿
          </button>
          <button
            type="button"
            class="platform-shell__nav-btn"
            :class="{ 'platform-shell__nav-btn--active': view === 'discover' }"
            @click="setView('discover')"
          >
            <UiIco name="search" :size="14" />
            検索
          </button>
          <button
            type="button"
            class="platform-shell__nav-btn"
            :class="{ 'platform-shell__nav-btn--active': view === 'open-chat' }"
            @click="setView('open-chat')"
          >
            <UiIco name="chat" :size="14" />
            オープンチャット
          </button>
          <button
            type="button"
            class="platform-shell__nav-btn"
            :class="{ 'platform-shell__nav-btn--active': view === 'connections' }"
            @click="setView('connections')"
          >
            <UiIco name="disc" :size="14" />
            曲の繋がり
          </button>
          <button
            type="button"
            class="platform-shell__nav-btn"
            :class="{ 'platform-shell__nav-btn--active': view === 'artist-encyclopedia' }"
            @click="setView('artist-encyclopedia')"
          >
            <UiIco name="book" :size="14" />
            アーティスト図鑑
          </button>
          <button
            type="button"
            class="platform-shell__nav-btn"
            :class="{ 'platform-shell__nav-btn--active': view === 'artist-diagnosis' }"
            @click="setView('artist-diagnosis')"
          >
            <UiIco name="spark" :size="14" />
            アーティスト診断
          </button>
        </nav>

        <nav class="platform-shell__desktop-actions" aria-label="SNS quick menu">
          <button
            type="button"
            class="platform-shell__quick-btn"
            @click="setView('sns'); snsCreateIntent++"
          >
            <UiIco name="plus" :size="16" />
            <span>投稿</span>
          </button>
          <button
            type="button"
            class="platform-shell__quick-btn"
            :class="{ 'platform-shell__quick-btn--active': view === 'dm' }"
            @click="openDm()"
          >
            <span class="platform-shell__quick-icon">
              <UiIco name="mail" :size="16" />
              <span v-if="dmUnreadCount > 0" class="platform-shell__quick-badge">
                {{ dmUnreadCount > 9 ? '9+' : dmUnreadCount }}
              </span>
            </span>
            <span>DM</span>
          </button>
          <button
            type="button"
            class="platform-shell__quick-btn"
            :class="{ 'platform-shell__quick-btn--active': view === 'profile' }"
            @click="openMyProfile"
          >
            <UiIco name="user" :size="16" />
            <span>マイページ</span>
          </button>
        </nav>

        <HeaderAccountMenu
          class="platform-shell__account"
          :is-logged-in="isLoggedIn"
          :user-name="userName"
          :membership="membership || 'general'"
          @open-auth="onOpenAuth"
          @open-account="modal = 'account'"
          @logout="onLogout"
          @go-fanclub="emit('enter-site', 'hibari')"
        />

        <button
          type="button"
          class="platform-shell__menu sp-only"
          :class="{ 'platform-shell__menu--open': drawerOpen }"
          :aria-label="drawerOpen ? 'メニューを閉じる' : 'メニューを開く'"
          :aria-expanded="drawerOpen"
          @click="drawerOpen = !drawerOpen"
        >
          <span v-for="i in 3" :key="i" class="platform-shell__menu-line" />
        </button>
      </div>
    </header>

    <PlatformDrawerNav
      :open="drawerOpen"
      :items="navItems"
      :page="drawerPage"
      @close="drawerOpen = false"
      @navigate="onDrawerNavigate"
    />

    <PageMusicMemories
      v-if="view === 'hub'"
      embedded
      @enter-site="(siteId) => emit('enter-site', siteId)"
      @open-chat="setView('open-chat')"
      @open-connections="setView('connections')"
    />

    <PageMusicConnections
      v-else-if="view === 'connections'"
      @enter-site="(siteId) => emit('enter-site', siteId)"
    />

    <PageArtistEncyclopedia
      v-else-if="view === 'artist-encyclopedia'"
      @enter-site="(siteId) => emit('enter-site', siteId)"
    />

    <PageArtistDiagnosis
      v-else-if="view === 'artist-diagnosis'"
      @enter-site="(siteId) => emit('enter-site', siteId)"
      @open-encyclopedia="setView('artist-encyclopedia')"
    />

    <PagePlatformOpenChat
      v-else-if="view === 'open-chat'"
      @need-auth="(mode) => emit('open-auth', { mode, returnTo: { feature: 'open-chat' } })"
    />

    <PageSnsFeed
      v-else-if="view === 'sns'"
      :create-intent="snsCreateIntent"
      @need-auth="onSnsNeedAuth"
      @open-chat="setView('open-chat')"
      @open-dm="openDm()"
      @open-profile="openProfile"
    />

    <PageSnsDiscover
      v-else-if="view === 'discover'"
      :pending-song="pendingDiscoverSong"
      @need-auth="onSnsNeedAuth"
      @open-profile="openProfile"
      @song-consumed="emit('discover-song-consumed')"
    />

    <PageSnsProfile
      v-else-if="view === 'profile' && profileAccountId"
      :account-id="profileAccountId"
      @need-auth="onSnsNeedAuth"
      @open-dm="openDm"
      @open-profile="openProfile"
    />

    <PageSnsDm
      v-else-if="view === 'dm'"
      :target-account-id="dmTargetAccountId"
      @need-auth="onSnsNeedAuth"
      @open-chat="setView('open-chat')"
      @open-profile="openProfile"
    />

    <div v-else-if="view === 'login'" class="platform-shell__auth">
      <button type="button" class="platform-shell__back" @click="setView('hub')">
        ← {{ SITE_NAME }} へ戻る
      </button>
      <PageLogin
        variant="platform"
        @open-auth="onOpenAuth"
        @login-success="onLoginSuccess"
      />
    </div>

    <div v-else-if="view === 'register'" class="platform-shell__auth">
      <button type="button" class="platform-shell__back" @click="setView('hub')">
        ← {{ SITE_NAME }} へ戻る
      </button>
      <PageRegister
        variant="platform"
        :initial-plan="registerPlan"
        @navigate="setView('hub')"
        @open-auth="onOpenAuth"
        @complete="onRegisterComplete"
      />
    </div>

    <AccountModal
      v-if="modal === 'account'"
      @close="modal = null"
      @need-login="modal = null; setView('login')"
      @logout="onLogout"
      @user-updated="onUserUpdated"
    />

    <nav
      v-if="!['login', 'register'].includes(view)"
      class="platform-shell__tabbar sp-only"
      aria-label="モバイルナビゲーション"
    >
      <button
        type="button"
        class="platform-shell__tab"
        :class="{ 'platform-shell__tab--active': view === 'sns' }"
        @click="setView('sns')"
      >
        <UiIco name="home" :size="20" />
        <span>ホーム</span>
      </button>
      <button
        type="button"
        class="platform-shell__tab"
        :class="{ 'platform-shell__tab--active': view === 'discover' }"
        @click="setView('discover')"
      >
        <UiIco name="search" :size="20" />
        <span>検索</span>
      </button>
      <button
        type="button"
        class="platform-shell__tab platform-shell__tab--post"
        aria-label="投稿する"
        @click="setView('sns'); snsCreateIntent++"
      >
        <UiIco name="plus" :size="22" color="#fff" />
      </button>
      <button
        type="button"
        class="platform-shell__tab"
        :class="{ 'platform-shell__tab--active': view === 'dm' }"
        @click="openDm()"
      >
        <span class="platform-shell__tab-icon">
          <UiIco name="mail" :size="20" />
          <span v-if="dmUnreadCount > 0" class="platform-shell__tab-badge">
            {{ dmUnreadCount > 9 ? '9+' : dmUnreadCount }}
          </span>
        </span>
        <span>DM</span>
      </button>
      <button
        type="button"
        class="platform-shell__tab"
        :class="{ 'platform-shell__tab--active': view === 'profile' }"
        @click="openMyProfile"
      >
        <UiIco name="user" :size="20" />
        <span>マイページ</span>
      </button>
    </nav>

    <ToastHost />
  </div>
</template>

<style scoped>
.platform-shell {
  min-height: 100vh;
  background: var(--sns-bg);
  --bottom-nav-height: 66px;
}

.platform-shell__header {
  position: sticky;
  top: 0;
  z-index: 40;
  width: 100%;
  border-bottom: 1px solid var(--sns-border-soft);
  background: rgba(22, 15, 24, 0.92);
  backdrop-filter: blur(10px);
}

.platform-shell__header-inner {
  width: 100%;
  max-width: none;
  margin: 0;
  padding: 14px 20px;
  display: grid;
  grid-template-columns: minmax(0, auto) minmax(0, 1fr) minmax(0, auto) minmax(0, auto);
  align-items: center;
  gap: 16px;
  min-width: 0;
}

.platform-shell__nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  flex-wrap: nowrap;
  min-width: 0;
  overflow-x: auto;
  scrollbar-width: none;
}

.platform-shell__nav::-webkit-scrollbar {
  display: none;
}

.platform-shell__nav-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin: 0;
  padding: 7px 14px;
  border: 1px solid transparent;
  border-bottom: 2px solid transparent;
  border-radius: 999px;
  background: transparent;
  color: var(--sns-text-muted);
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  letter-spacing: 0;
  cursor: pointer;
  min-width: 0;
  white-space: nowrap;
}

.platform-shell__nav-btn:hover {
  background: rgba(255, 255, 255, 0.06);
  color: var(--sns-ivory);
}

.platform-shell__nav-btn--active {
  background: rgba(228, 190, 99, 0.1);
  border-color: rgba(228, 190, 99, 0.35);
  color: var(--sns-gold);
  font-weight: 600;
}

.platform-shell__desktop-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  min-width: 0;
}

.platform-shell__quick-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 34px;
  margin: 0;
  padding: 7px 12px;
  border: 1px solid var(--sns-border);
  border-radius: 999px;
  background: var(--sns-card);
  color: var(--sns-ivory);
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  letter-spacing: 0;
  white-space: nowrap;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s, color 0.2s;
}

.platform-shell__quick-btn:hover,
.platform-shell__quick-btn--active {
  background: rgba(228, 190, 99, 0.1);
  border-color: rgba(228, 190, 99, 0.4);
  color: var(--sns-gold);
}

.platform-shell__quick-icon {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  overflow: visible;
}

.platform-shell__quick-badge {
  position: absolute;
  top: -10px;
  right: -11px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: 999px;
  background: var(--beni-600);
  color: #fff;
  font-size: 9px;
  line-height: 16px;
  text-align: center;
  border: 2px solid rgba(22, 15, 24, 0.96);
}

.platform-shell__brand {
  display: inline-flex;
  align-items: center;
  justify-self: start;
  min-width: 0;
  margin: 0;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.platform-shell__brand :deep(.mm-logo--full) {
  max-height: 44px;
  max-width: 140px;
  width: auto;
  object-position: left center;
}

.platform-shell__menu {
  display: none;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  padding: 8px;
  margin: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
  position: relative;
  z-index: 220;
}

.platform-shell__menu-line {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--sns-ivory);
  border-radius: 1px;
  transform-origin: center;
  transition:
    transform 0.48s cubic-bezier(0.22, 1, 0.36, 1),
    opacity 0.32s ease,
    background 0.25s ease;
}

.platform-shell__menu--open .platform-shell__menu-line:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.platform-shell__menu--open .platform-shell__menu-line:nth-child(2) {
  opacity: 0;
  transform: scaleX(0);
}

.platform-shell__menu--open .platform-shell__menu-line:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

.platform-shell__header--menu-open {
  z-index: 250;
  background: transparent;
  border-color: transparent;
  backdrop-filter: none;
}

.platform-shell__header--menu-open .platform-shell__brand,
.platform-shell__header--menu-open .platform-shell__nav,
.platform-shell__header--menu-open .platform-shell__desktop-actions,
.platform-shell__header--menu-open .platform-shell__account {
  visibility: hidden;
  pointer-events: none;
}

.platform-shell__header--menu-open .platform-shell__menu {
  position: fixed;
  top: 12px;
  right: 12px;
  padding: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.12);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.28);
}

@media (prefers-reduced-motion: reduce) {
  .platform-shell__menu-line {
    transition: none !important;
  }

  .platform-shell__menu--open .platform-shell__menu-line:nth-child(1),
  .platform-shell__menu--open .platform-shell__menu-line:nth-child(2),
  .platform-shell__menu--open .platform-shell__menu-line:nth-child(3) {
    transform: none;
    opacity: 1;
  }
}

.platform-shell__account :deep(.header-account__btn--login) {
  background: transparent;
  color: var(--sns-ivory);
  border-color: rgba(255, 255, 255, 0.28);
}

.platform-shell__account :deep(.header-account__btn--register) {
  background: var(--sns-purple);
  border-color: var(--murasaki-700);
}

.platform-shell__account :deep(.header-account__trigger) {
  background: var(--sns-card);
  border-color: var(--sns-border);
}

.platform-shell__account :deep(.header-account__trigger):hover {
  border-color: rgba(228, 190, 99, 0.4);
}

.platform-shell__account :deep(.header-account__avatar) {
  background: var(--sns-purple);
}

.platform-shell__account :deep(.header-account__name) {
  color: var(--sns-ivory);
}

.platform-shell__account :deep(.header-account__chevron) {
  color: var(--sns-text-muted);
}

.platform-shell__account :deep(.header-account__menu) {
  background: var(--sns-card-strong);
  border-color: var(--sns-border);
}

.platform-shell__account :deep(.header-account__plan) {
  color: var(--sns-gold-pale);
  border-bottom-color: var(--sns-border);
}

.platform-shell__account :deep(.header-account__item) {
  color: var(--sns-ivory);
}

.platform-shell__account :deep(.header-account__item:hover) {
  background: rgba(255, 255, 255, 0.06);
}

.platform-shell__account :deep(.header-account__item--logout) {
  border-top-color: var(--sns-border);
}

.platform-shell__auth {
  position: relative;
  min-height: calc(100vh - 65px);
  overflow: hidden;
}

.platform-shell__back {
  position: absolute;
  top: 20px;
  left: 24px;
  z-index: 20;
  margin: 0;
  padding: 8px 14px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  color: #f8f4ef;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  letter-spacing: 0.06em;
  cursor: pointer;
  backdrop-filter: blur(8px);
  transition: background 0.2s, border-color 0.2s;
}

.platform-shell__back:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(201, 169, 97, 0.45);
}

.platform-shell__tabbar {
  /* .sp-only の display:flex !important を上書きし、画面幅に対する均等5列にする */
  display: grid !important;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  align-items: center;
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 50;
  width: 100%;
  max-width: 100vw;
  box-sizing: border-box;
  padding: 6px 4px calc(6px + env(safe-area-inset-bottom, 0px));
  min-height: calc(var(--bottom-nav-height) + env(safe-area-inset-bottom, 0px));
  background: rgba(22, 15, 24, 0.96);
  backdrop-filter: blur(10px);
  border-top: 1px solid var(--sns-border-soft);
  overflow: visible;
}

.platform-shell__tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  width: 100%;
  min-width: 0;
  min-height: 44px;
  height: 100%;
  margin: 0;
  padding: 4px 2px;
  background: transparent;
  border: 0;
  color: var(--sns-text-muted);
  font-family: var(--ff-sans-jp);
  font-size: 10px;
  line-height: 1.2;
  cursor: pointer;
  overflow: hidden;
  white-space: nowrap;
  box-sizing: border-box;
}

.platform-shell__tab > span:not(.platform-shell__tab-icon) {
  display: block;
  width: 100%;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: center;
  line-height: 1.2;
}

.platform-shell__tab-icon {
  position: relative;
  display: inline-flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  overflow: visible;
}

.platform-shell__tab-badge {
  position: absolute;
  top: -7px;
  right: -10px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: 999px;
  background: var(--beni-600);
  color: #fff;
  font-size: 9px;
  line-height: 16px;
  text-align: center;
  border: 2px solid var(--sns-bg);
}

.platform-shell__tab--active {
  color: var(--sns-gold);
}

.platform-shell__tab :deep(svg) {
  display: block;
  flex-shrink: 0;
}

.platform-shell__tab--post {
  width: 48px;
  height: 48px;
  min-width: 48px;
  min-height: 48px;
  margin: 0;
  padding: 0;
  gap: 0;
  justify-self: center;
  border-radius: 50%;
  background: var(--sns-purple);
  border: 1px solid rgba(228, 190, 99, 0.4);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
  /* 水平は Grid 3列目の中央。浮きは縦方向のみ */
  transform: translateY(-8px);
  align-items: center;
  justify-content: center;
  line-height: 0;
  overflow: visible;
}

@media (max-width: 767px) {
  .platform-shell__header-inner {
    grid-template-columns: minmax(0, 1fr) minmax(0, auto) auto;
    gap: 8px 10px;
    padding: 10px 12px;
  }

  .platform-shell__brand {
    justify-self: start;
  }

  .platform-shell__brand :deep(.mm-logo--full) {
    max-height: 40px;
    max-width: 125px;
  }

  .platform-shell__nav {
    display: none;
  }

  .platform-shell__account {
    justify-self: end;
    min-width: 0;
  }

  .platform-shell__account :deep(.header-account__trigger) {
    max-width: 112px;
    min-width: 0;
  }

  .platform-shell__account :deep(.header-account__name) {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .platform-shell__account :deep(.header-account__btn) {
    padding: 6px 10px;
    font-size: 11px;
  }

  .platform-shell__account :deep(.header-account__btn--register) {
    display: none;
  }

  .platform-shell__desktop-actions {
    display: none;
  }

  .platform-shell__auth {
    min-height: calc(100vh - 65px);
  }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .platform-shell__header-inner {
    padding: 14px 18px;
    gap: 12px;
  }

  .platform-shell__nav-btn {
    padding-inline: 10px;
  }

  .platform-shell__desktop-actions {
    gap: 6px;
  }

  .platform-shell__quick-btn {
    padding-inline: 10px;
  }
}

@media (max-width: 374px) {
  .platform-shell__header-inner {
    padding-inline: 10px;
  }

  .platform-shell__nav-btn {
    font-size: 11px;
    gap: 4px;
  }

  .platform-shell__tabbar {
    padding-inline: 2px;
  }

  .platform-shell__tab {
    padding-inline: 1px;
    font-size: 8.5px;
  }

  .platform-shell__tab--post {
    width: 44px;
    height: 44px;
    min-width: 44px;
    min-height: 44px;
  }
}
</style>
