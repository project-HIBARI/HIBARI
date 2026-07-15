<script setup>
/**
 * ルート: Music Memories プラットフォーム → 各ファンクラブサイト
 */
import { ref, onMounted } from 'vue'
import PlatformShell from './components/layout/PlatformShell.vue'
import SiteShell from './components/layout/SiteShell.vue'
import { useAuth } from './composables/useAuth.js'
import { MEMBERSHIP } from './constants/membership.js'
import { SITE_DOCUMENT_TITLE } from './constants/site.js'

const appView = ref('platform')
const platformView = ref('hub')
const registerPlan = ref(MEMBERSHIP.GENERAL)
const pendingReturn = ref(null)
const sitePendingFeature = ref(null)
const pendingDiscoverSong = ref(null)

const auth = useAuth()
const { refreshUser, setUser, logout, isLoggedIn, user, membership } = auth

onMounted(() => {
  document.title = SITE_DOCUMENT_TITLE
  refreshUser()
})

function enterHibariSite(_siteId = 'hibari', options = {}) {
  appView.value = 'hibari'
  if (options?.page) {
    sitePendingFeature.value = options.page
  }
  window.scrollTo({ top: 0 })
}

function exitToPlatform() {
  appView.value = 'platform'
  platformView.value = 'hub'
  window.scrollTo({ top: 0 })
}

function goToSongSearch(song) {
  pendingDiscoverSong.value = song
  appView.value = 'platform'
  platformView.value = 'discover'
  window.scrollTo({ top: 0 })
}

function openPlatformAuth(payload = {}) {
  const mode = payload.mode || 'login'
  if (mode === 'register' || mode === 'register-premium') {
    registerPlan.value = payload.plan || (mode === 'register-premium' ? MEMBERSHIP.PREMIUM : MEMBERSHIP.GENERAL)
    platformView.value = 'register'
  } else if (mode === 'login') {
    platformView.value = 'login'
  }
  if (payload.returnTo) {
    pendingReturn.value = payload.returnTo
  }
  appView.value = 'platform'
  window.scrollTo({ top: 0 })
}

function applyPendingReturn() {
  const ret = pendingReturn.value
  pendingReturn.value = null
  if (!ret) return

  if (ret.feature === 'open-chat') {
    platformView.value = 'open-chat'
    return
  }

  if (ret.feature) {
    sitePendingFeature.value = ret.feature
    appView.value = 'hibari'
    return
  }

  if (ret.action === 'enter-hibari' || ret.site === 'hibari') {
    appView.value = 'hibari'
  }
}

function handleLoginSuccess(user) {
  setUser(user)
  platformView.value = 'hub'
  applyPendingReturn()
}

function handleRegisterComplete(user) {
  setUser(user)
  platformView.value = 'hub'
  applyPendingReturn()
}

function onSiteNeedPlatformAuth(payload) {
  openPlatformAuth({
    mode: payload.mode || 'login',
    plan: payload.plan,
    returnTo: {
      feature: payload.feature,
      page: payload.page,
      site: payload.feature === 'open-chat' ? 'platform' : 'hibari',
    },
  })
}

async function handleLogout() {
  await logout()
  platformView.value = 'hub'
}

function handleUserUpdated(account) {
  if (account) setUser(account)
}
</script>

<template>
  <PlatformShell
    v-if="appView === 'platform'"
    :view="platformView"
    :is-logged-in="isLoggedIn"
    :user-name="user?.name || ''"
    :membership="membership"
    :register-plan="registerPlan"
    :pending-discover-song="pendingDiscoverSong"
    @update:view="platformView = $event"
    @enter-site="enterHibariSite"
    @login-success="handleLoginSuccess"
    @register-complete="handleRegisterComplete"
    @logout="handleLogout"
    @open-auth="openPlatformAuth"
    @user-updated="handleUserUpdated"
    @discover-song-consumed="pendingDiscoverSong = null"
  />
  <SiteShell
    v-else
    :pending-feature="sitePendingFeature"
    @exit-platform="exitToPlatform"
    @need-platform-auth="onSiteNeedPlatformAuth"
    @clear-pending-feature="sitePendingFeature = null"
    @search-song-fans="goToSongSearch"
  />
</template>
