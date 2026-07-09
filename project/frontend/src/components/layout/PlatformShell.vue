<script setup>
/**
 * 部品名: Music Memories プラットフォームシェル
 * 役割: ハブ・ログイン・新規登録・アカウント設定を束ねる
 */
import { ref } from 'vue'
import PageMusicMemories from '../pages/PageMusicMemories.vue'
import PageLogin from '../pages/PageLogin.vue'
import PageRegister from '../pages/PageRegister.vue'
import PagePlatformOpenChat from '../pages/PagePlatformOpenChat.vue'
import HeaderAccountMenu from './HeaderAccountMenu.vue'
import AccountModal from '../modals/AccountModal.vue'
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

function setView(next) {
  emit('update:view', next)
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
          <span class="platform-shell__brand-mark" aria-hidden="true">♪</span>
          {{ SITE_NAME }}
        </button>

        <nav class="platform-shell__nav" aria-label="プラットフォームナビ">
          <button type="button" class="platform-shell__nav-btn" @click="setView('hub')">ホーム</button>
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

    <div v-else-if="view === 'login'" class="platform-shell__auth">
      <button type="button" class="platform-shell__back" @click="setView('hub')">
        ← {{ SITE_NAME }} へ戻る
      </button>
      <PageLogin
        @open-auth="onOpenAuth"
        @login-success="onLoginSuccess"
      />
    </div>

    <div v-else-if="view === 'register'" class="platform-shell__auth">
      <button type="button" class="platform-shell__back" @click="setView('hub')">
        ← {{ SITE_NAME }} へ戻る
      </button>
      <PageRegister
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
  gap: 10px;
  margin: 0;
  padding: 0;
  border: 0;
  background: transparent;
  color: #f8f4ef;
  font-family: var(--ff-latin);
  font-size: clamp(1.1rem, 2.5vw, 1.4rem);
  font-weight: 600;
  letter-spacing: 0.14em;
  cursor: pointer;
}

.platform-shell__brand-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--murasaki-600), var(--murasaki-800));
  font-size: 13px;
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
  background: var(--site-bg);
  min-height: calc(100vh - 65px);
}

.platform-shell__back {
  position: absolute;
  top: 20px;
  left: 24px;
  z-index: 20;
  margin: 0;
  padding: 8px 14px;
  border: 1px solid var(--site-border);
  border-radius: 999px;
  background: #fff;
  color: var(--murasaki-700);
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  letter-spacing: 0.06em;
  cursor: pointer;
}
</style>
