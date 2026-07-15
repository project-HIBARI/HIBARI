<script setup>

/**

 * 部品名: サイト全体シェル

 * 役割: ヘッダー／ナビ／ページ切替／モーダルを束ねる

 */

import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'

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

import PageTop from '../pages/PageTop.vue'

import PageNews from '../pages/PageNews.vue'

import PageDisco from '../pages/PageDisco.vue'

import PageProfile from '../pages/PageProfile.vue'

import PagePlaces from '../pages/PagePlaces.vue'

import PageMemories from '../pages/PageMemories.vue'

import PageMessage from '../pages/PageMessage.vue'

import PageMemoryBook from '../pages/PageMemoryBook.vue'

import PageFaq from '../pages/PageFaq.vue'

import PageContact from '../pages/PageContact.vue'

import PageTerms from '../pages/PageTerms.vue'

import PagePrivacyPolicy from '../pages/PagePrivacyPolicy.vue'

import PageFanclub from '../pages/PageFanclub.vue'

import PageFanclubSite from '../pages/PageFanclubSite.vue'

import { useBodyScrollLock } from '../../composables/useBodyScrollLock.js'

import { useSiteIntro } from '../../composables/useSiteIntro.js'

import { useAuth } from '../../composables/useAuth.js'

import { MEMBERSHIP, PERMISSION, hasPermission } from '../../constants/membership.js'
import { useOpenChatNotifications } from '../../composables/useOpenChatNotifications.js'
import { initAos, scheduleAosRefresh, destroyAosScheduling } from '../../lib/aos.js'

const props = defineProps({
  pendingFeature: { type: String, default: null },
})

const emit = defineEmits(['exit-platform', 'need-platform-auth', 'clear-pending-feature', 'search-song-fans'])



const navItems = [

  { id: 'top', label: 'ホーム' },

  { id: 'news', label: 'ニュース' },

  { id: 'profile', label: '美空ひばりについて', shortLabel: '美空ひばり' },

  { id: 'disco', label: 'ディスコグラフィ', shortLabel: 'ディスコ' },

  { id: 'map', label: 'ゆかりの地' },

  { id: 'memories', label: '思い出' },

  { id: 'message', label: '献花' },

  { id: 'memory-book', label: 'Music Memory Book', shortLabel: '思い出帳' },

  { id: 'fanclub', label: 'ファンクラブ' },

]



/** URL オープン時は常にホームから開始 */

const page = ref('top')

const drawerOpen = ref(false)

const modal = ref(null)

const authMode = ref(null)

/** プラットフォーム認証後に開く特典 */
const postLoginRedirect = ref(null)

/** 楽曲チャットへのディープリンク先ルームID */
const pendingChatRoomId = ref(null)

/** ファンクラブ会員サイト内の表示セクション */
const fanclubSection = ref('overview')

/** ページ切替時のアニメーション用 */
const pageEnterKey = ref(0)

/** イントロビデオ表示 */
const { introVisible, introLeaving, completeIntro } = useSiteIntro()
const siteReady = ref(false)

const auth = useAuth()

const { membership, isLoggedIn, isFanclubMember, user, setUser, refreshUser } = auth

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
    pendingChatRoomId.value = null
  }
})

onUnmounted(() => {
  stopOpenChatNotify()
  setActiveRoomId(null)
  destroyAosScheduling()
})



onMounted(() => {
  refreshUser()
  if (!introVisible.value) {
    siteReady.value = true
    nextTick(() => {
      initAos()
      scheduleAosRefresh()
    })
  }
})

watch(
  () => props.pendingFeature,
  (feature) => {
    if (!feature) return
    window.setTimeout(() => {
      openMemberFeature(feature)
      emit('clear-pending-feature')
    }, introVisible.value ? 900 : 0)
  },
  { immediate: true },
)

function onIntroComplete() {
  completeIntro()
  siteReady.value = true
  nextTick(() => {
    initAos()
    scheduleAosRefresh()
  })
}

watch(siteReady, (ready) => {
  if (!ready || introVisible.value) return
  nextTick(() => {
    initAos()
    scheduleAosRefresh()
  })
})

watch([page, pageEnterKey], () => {
  nextTick(() => {
    scheduleAosRefresh()
  })
}, { flush: 'post' })



function goTo(id) {

  if (id !== 'fanclub-site') {

    fanclubSection.value = 'overview'

  }

  page.value = id

  drawerOpen.value = false

  pageEnterKey.value += 1

  window.scrollTo({ top: 0, left: 0, behavior: 'auto' })

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

function requestPlatformAuth(mode, extra = {}) {
  const payload = { mode }
  if (mode === 'register-premium') {
    payload.plan = MEMBERSHIP.PREMIUM
  } else if (mode === 'register') {
    payload.plan = MEMBERSHIP.GENERAL
  }
  const feature = extra.feature || postLoginRedirect.value?.feature
  const returnPage = extra.page || postLoginRedirect.value?.page
  if (feature) {
    payload.returnTo = { feature }
  } else if (returnPage) {
    payload.returnTo = { page: returnPage }
  }
  postLoginRedirect.value = null
  emit('need-platform-auth', payload)
}

function openModal(kind) {

  if (kind === 'fanclub') {

    goTo('fanclub')

    return

  }

  const gate = GATED_MODALS[kind]
  if (gate) {
    if (!isLoggedIn.value) {
      requestPlatformAuth('login', { feature: gate.feature })
      return
    }
    if (gate.premium && !auth.isPremium.value) {
      requestPlatformAuth('register-premium', { feature: gate.feature })
      return
    }
    if (!auth.can(gate.permission)) {
      requestPlatformAuth(gate.premium ? 'register-premium' : 'register', { feature: gate.feature })
      return
    }
  }

  modal.value = kind

  drawerOpen.value = false

}



function openSongChat(roomId) {
  pendingChatRoomId.value = roomId
  fanclubSection.value = 'open-chat'
  goTo('fanclub-site')
}

function openMemberFeature(mode) {

  if (mode === 'ai') {
    openModal('ai')
    return
  }

  if (mode === 'memory-book') {
    goTo('memory-book')
    return
  }

  if (mode === 'board' && !auth.isFanclubMember.value) {
    requestPlatformAuth(isLoggedIn.value ? 'register' : 'login', { feature: mode })
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
    requestPlatformAuth('login', { feature: mode })
    return
  }

  if (feature.permission && !auth.can(feature.permission)) {
    if (!auth.isFanclubMember.value) {
      requestPlatformAuth('register', { feature: mode })
    } else {
      requestPlatformAuth(feature.premium ? 'register-premium' : 'register', { feature: mode })
    }
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

    if (!postLoginRedirect.value) {

      postLoginRedirect.value = { page: page.value }

    }

    requestPlatformAuth('login')

    return

  }

  if (mode === 'register') {

    requestPlatformAuth('register')

    return

  }

  if (mode === 'register-premium') {

    requestPlatformAuth('register-premium')

    return

  }

  if (['forgot-password', 'terms', 'privacy', 'search'].includes(mode)) {

    authMode.value = mode

    drawerOpen.value = false

    return

  }

  openMemberFeature(mode)

  drawerOpen.value = false

}



function closeAuth() {
  authMode.value = null
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

      :menu-open="drawerOpen"

      show-platform-back
      auth-on-platform-only
      :is-fanclub-member="isFanclubMember"

      @logo="goTo('top')"

      @navigate="handleNav"

      @toggle-drawer="drawerOpen = !drawerOpen"

      @open-auth="openAuth"

      @go-fanclub="goTo(isLoggedIn ? 'fanclub-site' : 'fanclub')"

      @exit-platform="emit('exit-platform')"

    />



    <AppDrawerNav

      :open="drawerOpen"

      :items="navItems"

      :page="page"

      :is-logged-in="isLoggedIn"

      :user-name="user?.name || ''"

      show-platform-back
      auth-on-platform-only

      @close="drawerOpen = false"

      @navigate="handleNav"

      @open-modal="openModal"

      @open-auth="openAuth"

      @exit-platform="emit('exit-platform')"

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
          'main-pad--flush': false,
          'main-pad--top': page === 'top',
          'site-main--flush': false,
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

        @open-song-chat="openSongChat"

        @search-song-fans="(song) => emit('search-song-fans', song)"

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
        @open-modal="openModal"
      />

      <PageMessage
        v-else-if="page === 'message'"
        @navigate="goTo"
        @open-auth="openAuth"
        @open-modal="openModal"
      />

      <PageMemoryBook
        v-else-if="page === 'memory-book'"
        @navigate="goTo"
        @open-auth="openAuth"
        @open-modal="openModal"
      />

      <PageFaq v-else-if="page === 'faq'" />

      <PageContact v-else-if="page === 'contact'" />

      <PageTerms v-else-if="page === 'terms'" />

      <PagePrivacyPolicy v-else-if="page === 'privacy-policy'" />

      <PageFanclub

        v-else-if="page === 'fanclub'"

        @navigate="goTo"

        @register="() => openAuth('register')"

        @use-feature="openMemberFeature"

      />

      <PageFanclubSite

        v-else-if="page === 'fanclub-site'"

        :active-section="fanclubSection"

        :initial-chat-room-id="pendingChatRoomId"

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
