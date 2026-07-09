<script setup>

/**

 * 部品名: サイト全体シェル

 * 役割: ヘッダー／ナビ／ページ切替／モーダルを束ねる

 */

import { ref, onMounted, onUnmounted, watch } from 'vue'

import SiteHeader from './SiteHeader.vue'

import SiteIntroVideo from './SiteIntroVideo.vue'

import AppDrawerNav from './AppDrawerNav.vue'

import AppFooterBar from './AppFooterBar.vue'

import GoodsModal from '../modals/GoodsModal.vue'

import AiModal from '../modals/AiModal.vue'

import NewsListModal from '../modals/NewsListModal.vue'

import EventsListModal from '../modals/EventsListModal.vue'

import GalleryModal from '../modals/GalleryModal.vue'
import PremiumVideoModal from '../modals/PremiumVideoModal.vue'

import AuthNoticeModal from '../modals/AuthNoticeModal.vue'
import AccountModal from '../modals/AccountModal.vue'

import PageTop from '../pages/PageTop.vue'

import PageNews from '../pages/PageNews.vue'

import PageDisco from '../pages/PageDisco.vue'

import PageProfile from '../pages/PageProfile.vue'

import PagePlaces from '../pages/PagePlaces.vue'

import PageMemories from '../pages/PageMemories.vue'

import PageMessage from '../pages/PageMessage.vue'

import PageFaq from '../pages/PageFaq.vue'

import PageContact from '../pages/PageContact.vue'

import PageTerms from '../pages/PageTerms.vue'

import PagePrivacyPolicy from '../pages/PagePrivacyPolicy.vue'

import PageLogin from '../pages/PageLogin.vue'

import PageRegister from '../pages/PageRegister.vue'

import PageFanclub from '../pages/PageFanclub.vue'

import PageFanclubSite from '../pages/PageFanclubSite.vue'

import { useBodyScrollLock } from '../../composables/useBodyScrollLock.js'

import { useSiteIntro } from '../../composables/useSiteIntro.js'

import { useAuth } from '../../composables/useAuth.js'

import { MEMBERSHIP, PERMISSION, hasPermission } from '../../constants/membership.js'
import { useOpenChatNotifications } from '../../composables/useOpenChatNotifications.js'



const navItems = [

  { id: 'top', label: 'ホーム' },

  { id: 'news', label: 'ニュース' },

  { id: 'profile', label: '美空ひばりについて' },

  { id: 'disco', label: 'ディスコグラフィ' },

  { id: 'map', label: 'ゆかりの地' },

  { id: 'memories', label: '思い出' },

  { id: 'message', label: '献花' },

  { id: 'fanclub', label: 'ファンクラブ' },

]



/** URL オープン時は常にホームから開始 */

const page = ref('top')

const drawerOpen = ref(false)

const modal = ref(null)

const authMode = ref(null)

const registerPlan = ref(MEMBERSHIP.GENERAL)

/** ログイン後に戻るページ／開く特典 */
const postLoginRedirect = ref(null)

/** ファンクラブ会員サイト内の表示セクション */
const fanclubSection = ref('overview')

/** ページ切替時のアニメーション用 */
const pageEnterKey = ref(0)

/** イントロビデオ表示 */
const { introVisible, introLeaving, completeIntro } = useSiteIntro()
const siteReady = ref(false)

const auth = useAuth()

const { membership, isLoggedIn, user, setUser, refreshUser, logout } = auth

const { startPolling: startOpenChatNotify, stopPolling: stopOpenChatNotify, setActiveRoomId } =
  useOpenChatNotifications()



useBodyScrollLock(drawerOpen)

function syncOpenChatNotifications() {
  if (isLoggedIn.value && hasPermission(membership.value, PERMISSION.OPEN_CHAT)) {
    startOpenChatNotify()
    return
  }
  stopOpenChatNotify()
  setActiveRoomId(null)
}

watch([isLoggedIn, membership], syncOpenChatNotifications, { immediate: true })

watch([page, fanclubSection], ([currentPage, currentSection]) => {
  if (currentPage !== 'fanclub-site' || currentSection !== 'open-chat') {
    setActiveRoomId(null)
  }
})

onUnmounted(() => {
  stopOpenChatNotify()
  setActiveRoomId(null)
})



onMounted(() => {
  refreshUser()
  if (!introVisible.value) {
    siteReady.value = true
  }
})

function onIntroComplete() {
  completeIntro()
  siteReady.value = true
}



function goTo(id) {

  if (id !== 'fanclub-site') {

    fanclubSection.value = 'overview'

  }

  page.value = id

  drawerOpen.value = false

  pageEnterKey.value += 1

  window.scrollTo({ top: 0, behavior: 'smooth' })

}



function handleNav(id) {

  if (id === 'fanclub') {

    fanclubSection.value = 'overview'

    goTo(isLoggedIn.value ? 'fanclub-site' : 'fanclub')

    return

  }

  goTo(id)

}



/** モーダルを開く（fanclub はページ遷移に振り替え） */

const GATED_MODALS = {
  gallery: { permission: PERMISSION.EXCLUSIVE_CONTENT, premium: true, feature: 'gallery' },
  'premium-video': { permission: PERMISSION.PREMIUM_VIDEO, premium: true, feature: 'pv' },
  events: { permission: PERMISSION.TICKET_PREORDER, premium: false, feature: 'events' },
}

function openModal(kind) {

  if (kind === 'fanclub') {

    goTo('fanclub')

    return

  }

  const gate = GATED_MODALS[kind]
  if (gate) {
    if (!isLoggedIn.value) {
      postLoginRedirect.value = { feature: gate.feature }
      goTo('login')
      return
    }
    if (gate.premium && !auth.isPremium.value) {
      goRegister(MEMBERSHIP.PREMIUM)
      return
    }
    if (!auth.can(gate.permission)) {
      goRegister(gate.premium ? MEMBERSHIP.PREMIUM : MEMBERSHIP.GENERAL)
      return
    }
  }

  modal.value = kind

  drawerOpen.value = false

}



function openMemberFeature(mode) {

  if (mode === 'ai') {
    openModal('ai')
    return
  }

  const features = {

    news: { permission: PERMISSION.NEWSLETTER, memberPage: 'fanclub-site', section: 'newsletter', guestPage: 'fanclub' },

    events: { permission: PERMISSION.TICKET_PREORDER, memberPage: 'fanclub-site', section: 'events', guestPage: 'fanclub' },

    'priority-events': { permission: PERMISSION.PRIORITY_DISCOUNT, memberPage: 'fanclub-site', section: 'priority-events', premium: true, guestPage: 'fanclub' },

    gallery: { permission: PERMISSION.EXCLUSIVE_CONTENT, memberPage: 'fanclub-site', section: 'exclusive-content', premium: true, guestPage: 'fanclub' },

    ai: { permission: PERMISSION.AI_CHAT, modal: 'ai' },

    board: { permission: PERMISSION.BOARD_POST, memberPage: 'fanclub-site', section: 'board', guestPage: 'fanclub' },

    'open-chat': { permission: PERMISSION.OPEN_CHAT, memberPage: 'fanclub-site', section: 'open-chat', guestPage: 'fanclub' },

    fanclub: { memberPage: 'fanclub-site', guestPage: 'fanclub' },

    disco: { permission: PERMISSION.PREMIUM_VIDEO, memberPage: 'fanclub-site', section: 'premium-video', premium: true, guestPage: 'fanclub' },

    pv: { permission: PERMISSION.PREMIUM_VIDEO, memberPage: 'fanclub-site', section: 'premium-video', premium: true, guestPage: 'fanclub' },

  }

  const feature = features[mode]

  if (!feature) {

    authMode.value = mode

    drawerOpen.value = false

    return

  }

  if (feature.memberPage && !feature.permission) {

    fanclubSection.value = feature.section || 'overview'

    goTo(isLoggedIn.value ? feature.memberPage : feature.guestPage)

    return

  }

  if (feature.page && !feature.permission) {

    goTo(feature.page)

    return

  }

  if (!isLoggedIn.value) {

    postLoginRedirect.value = { feature: mode }

    goTo('login')

    return

  }

  if (feature.permission && !auth.can(feature.permission)) {

    goRegister(feature.premium ? MEMBERSHIP.PREMIUM : MEMBERSHIP.GENERAL)

    return

  }

  if (feature.memberPage && feature.section) {

    fanclubSection.value = feature.section

    goTo(isLoggedIn.value ? feature.memberPage : (feature.guestPage || 'fanclub'))

    return

  }

  if (feature.modal) {

    openModal(feature.modal)

    return

  }

  if (feature.page) {

    goTo(feature.page)

  }

}



function openAuth(mode) {

  if (mode === 'login') {

    if (page.value !== 'login' && page.value !== 'register' && !postLoginRedirect.value) {

      postLoginRedirect.value = { page: page.value }

    }

    goTo('login')

    return

  }

  if (mode === 'register') {

    goRegister(MEMBERSHIP.GENERAL)

    return

  }

  if (mode === 'register-premium') {

    goRegister(MEMBERSHIP.PREMIUM)

    return

  }

  openMemberFeature(mode)

  drawerOpen.value = false

}



async function handleLogout() {

  await logout()

  modal.value = null

  if (page.value === 'fanclub-site') {

    goTo('fanclub')

  }

}



function openAccountModal() {

  if (!isLoggedIn.value) {

    openAuth('login')

    return

  }

  modal.value = 'account'

  drawerOpen.value = false

}



function handleAccountUserUpdated(account) {

  if (account) setUser(account)

}



function closeAuth() {

  authMode.value = null

}



function handleLoginSuccess(user) {

  setUser(user)

  const redirect = postLoginRedirect.value

  postLoginRedirect.value = null

  if (redirect?.feature) {

    openMemberFeature(redirect.feature)

    return

  }

  const returnPage = redirect?.page

  if (returnPage && !['login', 'register', 'top'].includes(returnPage)) {

    goTo(returnPage)

    if (redirect?.modal) openModal(redirect.modal)

    return

  }

  goTo('fanclub-site')

}



function goRegister(plan = MEMBERSHIP.GENERAL) {

  registerPlan.value = plan

  goTo('register')

}



/** 新規会員登録の完了後: ファンクラブ会員サイトへ誘導 */

function handleRegisterComplete(user) {

  if (user) setUser(user)

  goTo('fanclub-site')

}



function handleAiModalAuth(mode) {

  if (mode === 'login' && modal.value === 'ai') {

    postLoginRedirect.value = { feature: 'ai' }

  }

  modal.value = null

  openAuth(mode)

}

</script>



<template>

  <SiteIntroVideo
    v-if="introVisible"
    :leaving="introLeaving"
    @complete="onIntroComplete"
  />

  <div
    class="site-shell site-bg"
    :class="{
      'site-shell--during-intro': introVisible && !introLeaving,
      'site-shell--ready': siteReady && !introVisible,
    }"
  >

    <SiteHeader

      :items="navItems"

      :page="page"

      :is-logged-in="isLoggedIn"

      :user-name="user?.name || ''"

      :membership="membership"

      @logo="goTo('top')"

      @navigate="handleNav"

      @open-drawer="drawerOpen = true"

      @open-auth="openAuth"

      @open-account="openAccountModal"

      @logout="handleLogout"

      @go-fanclub="goTo(isLoggedIn ? 'fanclub-site' : 'fanclub')"

    />



    <AppDrawerNav

      :open="drawerOpen"

      :items="navItems"

      :page="page"

      :is-logged-in="isLoggedIn"

      :user-name="user?.name || ''"

      @close="drawerOpen = false"

      @navigate="handleNav"

      @open-modal="openModal"

      @open-auth="openAuth"

      @open-account="openAccountModal"

      @logout="handleLogout"

    />



    <main
      id="main-content"
      :key="pageEnterKey"
      :class="[
        'main-pad',
        'site-main',
        'motion-page-enter',
        'site-page-enter',
        {
          'main-pad--flush': page === 'login' || page === 'register',
          'main-pad--top': page === 'top',
          'site-main--flush': page === 'login' || page === 'register',
        },
      ]"
    >

      <PageTop

        v-if="page === 'top'"

        @navigate="goTo"

        @open-auth="openAuth"

        @open-modal="openModal"

        @use-feature="openMemberFeature"

      />

      <PageNews

        v-else-if="page === 'news'"

        @open-auth="openAuth"

      />

      <PageDisco

        v-else-if="page === 'disco'"

        @navigate="goTo"

        @open-auth="openAuth"

        @open-modal="openModal"

      />

      <PageProfile

        v-else-if="page === 'profile'"

        @open-auth="openAuth"

        @open-modal="openModal"

        @navigate="goTo"

      />

      <PagePlaces

        v-else-if="page === 'map'"

        @navigate="goTo"

        @open-auth="openAuth"

        @open-modal="openModal"

      />

      <PageMemories
        v-else-if="page === 'memories'"
        @navigate="goTo"
        @open-auth="openAuth"
      />

      <PageMessage
        v-else-if="page === 'message'"
        @navigate="goTo"
        @open-auth="openAuth"
      />

      <PageFaq v-else-if="page === 'faq'" />

      <PageContact v-else-if="page === 'contact'" />

      <PageTerms v-else-if="page === 'terms'" />

      <PagePrivacyPolicy v-else-if="page === 'privacy-policy'" />

      <PageLogin

        v-else-if="page === 'login'"

        @open-auth="openAuth"

        @login-success="handleLoginSuccess"

      />

      <PageRegister

        v-else-if="page === 'register'"

        :initial-plan="registerPlan"

        @navigate="goTo"

        @open-auth="openAuth"

        @complete="handleRegisterComplete"

      />

      <PageFanclub

        v-else-if="page === 'fanclub'"

        @navigate="goTo"

        @register="goRegister"

        @use-feature="openMemberFeature"

      />

      <PageFanclubSite

        v-else-if="page === 'fanclub-site'"

        :active-section="fanclubSection"

        @navigate="goTo"

        @open-modal="openModal"

        @open-auth="openAuth"

        @section-change="fanclubSection = $event"

      />

    </main>

    <AppFooterBar @navigate="goTo" />



    <GoodsModal v-if="modal === 'goods'" @close="modal = null" />

    <AiModal
      v-if="modal === 'ai'"
      :membership="membership"
      :is-logged-in="isLoggedIn"
      :account-id="user?.account_id"
      @close="modal = null"
      @open-auth="handleAiModalAuth"
    />

    <NewsListModal v-if="modal === 'news'" @close="modal = null" />

    <EventsListModal v-if="modal === 'events'" @close="modal = null" @navigate="goTo" />

    <GalleryModal
      v-if="modal === 'gallery'"
      @close="modal = null"
      @need-auth="(m) => { modal = null; openAuth(m) }"
    />

    <PremiumVideoModal
      v-if="modal === 'premium-video'"
      @close="modal = null"
      @need-auth="(m) => { modal = null; openAuth(m) }"
    />

    <AuthNoticeModal v-if="authMode" :mode="authMode" @close="closeAuth" />

    <AccountModal
      v-if="modal === 'account'"
      @close="modal = null"
      @need-login="modal = null; openAuth('login')"
      @logout="handleLogout"
      @user-updated="handleAccountUserUpdated"
    />

  </div>

</template>



<style scoped>

.site-shell {
  min-height: 100vh;
  font-family: var(--ff-serif);
  font-size: var(--size-base);
  position: relative;
  overflow-x: clip;
}

</style>
