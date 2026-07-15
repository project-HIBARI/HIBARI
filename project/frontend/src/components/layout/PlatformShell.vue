<script setup>
/**
 * 部品名: Music Memories プラットフォームシェル
 * 役割: ハブ・ログイン・新規登録・アカウント設定を束ねる
 */
import { ref, watch } from 'vue'
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
import AccountModal from '../modals/AccountModal.vue'
import MusicMemoriesLogo from '../brand/MusicMemoriesLogo.vue'
import UiIco from '../ui/UiIco.vue'
import ToastHost from '../ui/ToastHost.vue'
import { useAuth } from '../../composables/useAuth.js'
import { useSnsDmUnread } from '../../composables/useSnsDmUnread.js'
import { MEMBERSHIP } from '../../constants/membership.js'
import { SITE_NAME } from '../../constants/site.js'

defineProps({
  view: { type: String, default: 'hub' },
  isLoggedIn: { type: Boolean, default: false },
  userName: { type: String, default: '' },
  membership: { type: String, default: null },
  registerPlan: { type: String, default: MEMBERSHIP.GENERAL },
})

const emit = defineEmits([
  'update:view',
  'enter-site',
  'login-success',
  'register-complete',
  'logout',
  'open-auth',
  'user-updated',
])

const modal = ref(null)
const snsCreateIntent = ref(0)
const profileAccountId = ref(null)
const dmTargetAccountId = ref(null)

const { user: authUser, isLoggedIn: authIsLoggedIn } = useAuth()
const { unreadCount: dmUnreadCount, startPolling: startDmPolling, stopPolling: stopDmPolling } = useSnsDmUnread()

watch(authIsLoggedIn, (loggedIn) => {
  if (loggedIn) startDmPolling()
  else stopDmPolling()
}, { immediate: true })

function setView(next) {
  emit('update:view', next)
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
  modal.value = null
  emit('logout')
}

function onUserUpdated(account) {
  emit('user-updated', account)
}
</script>

<template>
  <div class="platform-shell mm-sns">
    <header class="platform-shell__header" role="banner">
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
      </div>
    </header>

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
      @need-auth="onSnsNeedAuth"
      @open-profile="openProfile"
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
        class="platform-shell__tab"
        :class="{ 'platform-shell__tab--active': view === 'hub' }"
        @click="setView('hub')"
      >
        <UiIco name="disc" :size="20" />
        <span>Music Memories</span>
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
  border-bottom: 1px solid var(--sns-border-soft);
  background: rgba(22, 15, 24, 0.92);
  backdrop-filter: blur(10px);
}

.platform-shell__header-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 24px;
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
  flex-wrap: wrap;
  min-width: 0;
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
  min-width: 0;
  margin: 0;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.platform-shell__brand :deep(.mm-logo--full) {
  max-height: 44px;
  max-width: 125px;
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
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 50;
  align-items: center;
  justify-content: space-around;
  padding: 6px 8px calc(6px + env(safe-area-inset-bottom, 0px));
  min-height: calc(var(--bottom-nav-height) + env(safe-area-inset-bottom, 0px));
  background: rgba(22, 15, 24, 0.96);
  backdrop-filter: blur(10px);
  border-top: 1px solid var(--sns-border-soft);
}

.platform-shell__tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  background: transparent;
  border: 0;
  color: var(--sns-text-muted);
  font-family: var(--ff-sans-jp);
  font-size: 10px;
  padding: 4px 4px;
  min-height: 44px;
  min-width: 46px;
  cursor: pointer;
  overflow: hidden;
  white-space: nowrap;
}

.platform-shell__tab span {
  max-width: 54px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.platform-shell__tab-icon {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
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

.platform-shell__tab--post {
  min-width: 48px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--sns-purple);
  border: 1px solid rgba(228, 190, 99, 0.4);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
  transform: translateY(-8px);
  align-items: center;
  justify-content: center;
}

@media (max-width: 767px) {
  .platform-shell__header-inner {
    grid-template-columns: minmax(0, 1fr) minmax(96px, auto);
    grid-template-areas:
      "brand account"
      "nav nav";
    gap: 8px 12px;
    padding: 10px 12px 8px;
  }

  .platform-shell__brand {
    grid-area: brand;
  }

  .platform-shell__brand :deep(.mm-logo--full) {
    max-height: 40px;
    max-width: 125px;
  }

  .platform-shell__account {
    grid-area: account;
    justify-self: end;
    min-width: 0;
    max-width: 120px;
  }

  .platform-shell__account :deep(.header-account__trigger),
  .platform-shell__account :deep(.header-account__btn) {
    max-width: 120px;
    min-width: 0;
  }

  .platform-shell__account :deep(.header-account__name) {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .platform-shell__nav {
    grid-area: nav;
    justify-content: flex-start;
    gap: 6px;
    flex-wrap: wrap;
    width: 100%;
  }

  .platform-shell__nav-btn {
    flex: 1 1 calc(50% - 6px);
    justify-content: center;
    padding: 7px 4px;
    min-height: 44px;
    font-size: 12px;
    overflow: hidden;
  }

  .platform-shell__nav-btn svg {
    flex: 0 0 auto;
  }

  .platform-shell__desktop-actions {
    display: none;
  }

  .platform-shell__auth {
    min-height: calc(100vh - 112px);
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

  .platform-shell__tab {
    min-width: 40px;
    padding-inline: 2px;
  }

  .platform-shell__tab span {
    max-width: 44px;
    font-size: 8.5px;
  }
}
</style>
