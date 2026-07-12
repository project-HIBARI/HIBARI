<script setup>
/**
 * 部品名: Music Memories プラットフォームシェル
 * 役割: ハブ・ログイン・新規登録・アカウント設定を束ねる
 */
import { ref, watch } from 'vue'
import PageMusicMemories from '../pages/PageMusicMemories.vue'
import PageLogin from '../pages/PageLogin.vue'
import PageRegister from '../pages/PageRegister.vue'
import PagePlatformOpenChat from '../pages/PagePlatformOpenChat.vue'
import PageSnsFeed from '../pages/PageSnsFeed.vue'
import PageSnsProfile from '../pages/PageSnsProfile.vue'
import PageSnsDm from '../pages/PageSnsDm.vue'
import HeaderAccountMenu from './HeaderAccountMenu.vue'
import AccountModal from '../modals/AccountModal.vue'
import MusicMemoriesLogo from '../brand/MusicMemoriesLogo.vue'
import UiIco from '../ui/UiIco.vue'
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
  <div class="platform-shell">
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
          <button type="button" class="platform-shell__nav-btn" @click="setView('hub')">ホーム</button>
          <button
            type="button"
            class="platform-shell__nav-btn"
            :class="{ 'platform-shell__nav-btn--active': view === 'sns' }"
            @click="setView('sns')"
          >
            みんなの投稿
          </button>
          <button
            type="button"
            class="platform-shell__nav-btn"
            :class="{ 'platform-shell__nav-btn--active': view === 'open-chat' }"
            @click="setView('open-chat')"
          >
            オープンチャット
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
        :class="{ 'platform-shell__tab--active': view === 'open-chat' }"
        @click="setView('open-chat')"
      >
        <UiIco name="chat" :size="20" />
        <span>チャット</span>
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
  </div>
</template>

<style scoped>
.platform-shell {
  min-height: 100vh;
  background: #1a1418;
}

.platform-shell__header {
  position: sticky;
  top: 0;
  z-index: 40;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(26, 20, 24, 0.92);
  backdrop-filter: blur(10px);
}

.platform-shell__header-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 24px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 16px;
}

.platform-shell__nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.platform-shell__nav-btn {
  margin: 0;
  padding: 7px 14px;
  border: 1px solid transparent;
  border-radius: 999px;
  background: transparent;
  color: rgba(248, 244, 239, 0.72);
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  letter-spacing: 0.06em;
  cursor: pointer;
}

.platform-shell__nav-btn:hover,
.platform-shell__nav-btn--active {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.14);
  color: #f8f4ef;
}

.platform-shell__brand {
  display: inline-flex;
  align-items: center;
  margin: 0;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.platform-shell__brand :deep(.mm-logo--full) {
  max-height: 44px;
}

.platform-shell__account :deep(.header-account__btn--login) {
  background: transparent;
  color: #f8f4ef;
  border-color: rgba(255, 255, 255, 0.28);
}

.platform-shell__account :deep(.header-account__btn--register) {
  background: var(--murasaki-600);
  border-color: var(--murasaki-700);
}

.platform-shell__account :deep(.header-account__trigger) {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.14);
}

.platform-shell__account :deep(.header-account__name) {
  color: #f8f4ef;
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
  background: rgba(26, 20, 24, 0.96);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.platform-shell__tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  background: transparent;
  border: 0;
  color: rgba(248, 244, 239, 0.55);
  font-family: var(--ff-sans-jp);
  font-size: 10px;
  padding: 4px 6px;
  cursor: pointer;
  min-width: 56px;
}

.platform-shell__tab--active {
  color: var(--kin-400);
}

.platform-shell__tab--post {
  min-width: 48px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--murasaki-700);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
  transform: translateY(-8px);
  align-items: center;
  justify-content: center;
}
</style>
