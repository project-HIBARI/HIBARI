<script setup>

/**

 * 部品名: サイト全体シェル

 * 役割: ヘッダー／ナビ／ページ切替／モーダルを束ねる

 */

import { ref, onMounted } from 'vue'

import SiteHeader from './SiteHeader.vue'

import AppDrawerNav from './AppDrawerNav.vue'

import PremiumMemberBar from './PremiumMemberBar.vue'

import LoginCtaBanner from '../pages/login/LoginCtaBanner.vue'

import AppFooterBar from './AppFooterBar.vue'

import GoodsModal from '../modals/GoodsModal.vue'

import AiModal from '../modals/AiModal.vue'

import NewsListModal from '../modals/NewsListModal.vue'

import EventsListModal from '../modals/EventsListModal.vue'

import GalleryModal from '../modals/GalleryModal.vue'

import AuthNoticeModal from '../modals/AuthNoticeModal.vue'

import PageTop from '../pages/PageTop.vue'

import PageDisco from '../pages/PageDisco.vue'

import PageProfile from '../pages/PageProfile.vue'

import PagePlaces from '../pages/PagePlaces.vue'

import PageMemories from '../pages/PageMemories.vue'

import PageMessage from '../pages/PageMessage.vue'

import PageLogin from '../pages/PageLogin.vue'

import PageRegister from '../pages/PageRegister.vue'

import PageFanclub from '../pages/PageFanclub.vue'

import PageFanclubSite from '../pages/PageFanclubSite.vue'

import { useBodyScrollLock } from '../../composables/useBodyScrollLock.js'

import { useAuth } from '../../composables/useAuth.js'

import { MEMBERSHIP, PERMISSION } from '../../constants/membership.js'



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

const auth = useAuth()

const { membership, isLoggedIn, user, setUser, refreshUser } = auth



useBodyScrollLock(drawerOpen)



onMounted(() => {
  refreshUser()
})



function goTo(id) {

  page.value = id

  drawerOpen.value = false

  window.scrollTo({ top: 0, behavior: 'smooth' })

}



function handleNav(id) {

  if (id === 'news') {

    if (isLoggedIn.value && auth.can(PERMISSION.NEWSLETTER)) {

      openModal('news')

    } else {

      openAuth('news')

    }

    return

  }

  if (id === 'fanclub') {

    goTo(isLoggedIn.value ? 'fanclub-site' : 'fanclub')

    return

  }

  goTo(id)

}



/** モーダルを開く（fanclub はページ遷移に振り替え） */

function openModal(kind) {

  if (kind === 'fanclub') {

    goTo('fanclub')

    return

  }

  modal.value = kind

  drawerOpen.value = false

}



function openMemberFeature(mode) {

  const features = {

    news: { permission: PERMISSION.NEWSLETTER, modal: 'news' },

    events: { permission: PERMISSION.TICKET_PREORDER, modal: 'events' },

    gallery: { permission: PERMISSION.EXCLUSIVE_CONTENT, modal: 'gallery', premium: true },

    ai: { permission: PERMISSION.AI_CHAT, modal: 'ai' },

    memories: { permission: PERMISSION.BOARD_POST, page: 'memories' },

    fanclub: { memberPage: 'fanclub-site', guestPage: 'fanclub' },

    disco: { page: 'disco' },

    pv: { permission: PERMISSION.PREMIUM_VIDEO, page: 'disco', premium: true },

  }

  const feature = features[mode]

  if (!feature) {

    authMode.value = mode

    drawerOpen.value = false

    return

  }

  if (feature.memberPage) {

    goTo(isLoggedIn.value ? feature.memberPage : feature.guestPage)

    return

  }

  if (feature.page && !feature.permission) {

    goTo(feature.page)

    return

  }

  if (!isLoggedIn.value) {

    goTo('login')

    return

  }

  if (feature.permission && !auth.can(feature.permission)) {

    goRegister(feature.premium ? MEMBERSHIP.PREMIUM : MEMBERSHIP.GENERAL)

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



function closeAuth() {

  authMode.value = null

}



function handleLoginSuccess(user) {

  setUser(user)

  goTo('top')

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

</script>



<template>

  <div class="site-shell site-bg">

    <SiteHeader

      :items="navItems"

      :page="page"

      @logo="goTo('top')"

      @navigate="handleNav"

      @open-drawer="drawerOpen = true"

      @open-auth="openAuth"

      @open-search="openAuth('search')"

    />



    <AppDrawerNav

      :open="drawerOpen"

      :items="navItems"

      :page="page"

      @close="drawerOpen = false"

      @navigate="handleNav"

      @open-modal="openModal"

      @open-auth="openAuth"

    />



    <main

      id="main-content"

      :class="['main-pad', {
        'main-pad--flush': page === 'login' || page === 'register',
        'main-pad--top': page === 'top',
      }]"

      :style="page === 'login' || page === 'register'

        ? { minHeight: 'auto', color: 'var(--site-text)' }

        : { minHeight: '800px', maxWidth: '1400px', margin: '0 auto', color: 'var(--site-text)' }"

    >

      <PageTop

        v-if="page === 'top'"

        @navigate="goTo"

        @open-auth="openAuth"

        @open-modal="openModal"

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
        @open-auth="openAuth"
      />

      <PageMessage v-else-if="page === 'message'" />

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

      />

      <PageFanclubSite

        v-else-if="page === 'fanclub-site'"

        @navigate="goTo"

        @open-modal="openModal"

        @open-auth="openAuth"

      />

    </main>



    <LoginCtaBanner v-if="page !== 'top'" />

    <PremiumMemberBar
      v-if="page !== 'top' && page !== 'login' && page !== 'register'"
      @open-fanclub="openAuth('fanclub')"
    />

    <AppFooterBar />



    <GoodsModal v-if="modal === 'goods'" @close="modal = null" />

    <AiModal
      v-if="modal === 'ai'"
      :membership="membership"
      :is-logged-in="isLoggedIn"
      :account-id="user?.account_id"
      @close="modal = null"
      @open-auth="(mode) => { modal = null; openAuth(mode) }"
    />

    <NewsListModal v-if="modal === 'news'" @close="modal = null" />

    <EventsListModal v-if="modal === 'events'" @close="modal = null" />

    <GalleryModal v-if="modal === 'gallery'" @close="modal = null" />

    <AuthNoticeModal v-if="authMode" :mode="authMode" @close="closeAuth" />

  </div>

</template>



<style scoped>

.site-shell {

  min-height: 100vh;

  font-family: var(--ff-serif);

  font-size: 1rem;

  position: relative;

}

</style>
