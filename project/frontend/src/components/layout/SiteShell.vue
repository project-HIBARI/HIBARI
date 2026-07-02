<script setup>

/**

 * 部品名: サイト全体シェル

 * 役割: ヘッダー／ナビ／ページ切替／モーダルを束ねる

 */

import { ref } from 'vue'

import AppHeaderBar from './AppHeaderBar.vue'

import AppMainNav from './AppMainNav.vue'

import AppDrawerNav from './AppDrawerNav.vue'

import PremiumMemberBar from './PremiumMemberBar.vue'

import AppFooterBar from './AppFooterBar.vue'

import FanclubModal from '../modals/FanclubModal.vue'

import GoodsModal from '../modals/GoodsModal.vue'

import AiModal from '../modals/AiModal.vue'

import AuthNoticeModal from '../modals/AuthNoticeModal.vue'

import PageTop from '../pages/PageTop.vue'

import PageDisco from '../pages/PageDisco.vue'

import PageProfile from '../pages/PageProfile.vue'

import PagePlaces from '../pages/PagePlaces.vue'

import PageMemories from '../pages/PageMemories.vue'

import PageMessage from '../pages/PageMessage.vue'

import { useBodyScrollLock } from '../../composables/useBodyScrollLock.js'



const navItems = [

  { id: 'top', label: 'ホーム' },

  { id: 'disco', label: 'ディスコグラフィー' },

  { id: 'profile', label: '歩み' },

  { id: 'map', label: 'ゆかりの地' },

  { id: 'memories', label: '思い出' },

  { id: 'message', label: '献花' },

]



/** URL オープン時は常にホームから開始 */

const page = ref('top')

const drawerOpen = ref(false)

const modal = ref(null)

const authMode = ref(null)



useBodyScrollLock(drawerOpen)



function goTo(id) {

  page.value = id

  drawerOpen.value = false

  window.scrollTo({ top: 0, behavior: 'smooth' })

}



function openAuth(mode) {

  authMode.value = mode

  drawerOpen.value = false

}



function closeAuth() {

  authMode.value = null

}

</script>



<template>

  <div class="site-shell site-bg">

    <header role="banner" class="app-header">

      <AppHeaderBar

        @logo="goTo('top')"

        @open-drawer="drawerOpen = true"

        @open-auth="openAuth"

        @open-search="openAuth('search')"

      />

      <AppMainNav :items="navItems" :page="page" @navigate="goTo" />

    </header>



    <PremiumMemberBar @open-fanclub="modal = 'fanclub'" />



    <AppDrawerNav

      :open="drawerOpen"

      :items="navItems"

      :page="page"

      @close="drawerOpen = false"

      @navigate="goTo"

      @open-modal="(k) => { modal = k; drawerOpen = false }"

      @open-auth="openAuth"

    />



    <main

      id="main-content"

      class="main-pad"

      style="min-height: 800px; max-width: 1400px; margin: 0 auto; color: var(--site-text)"

    >

      <PageTop

        v-if="page === 'top'"

        @navigate="goTo"

        @open-auth="openAuth"

        @open-modal="(k) => (modal = k)"

      />

      <PageDisco

        v-else-if="page === 'disco'"

        @navigate="goTo"

        @open-auth="openAuth"

        @open-modal="(k) => (modal = k)"

      />

      <PageProfile

        v-else-if="page === 'profile'"

        @open-auth="openAuth"

        @open-modal="(k) => (modal = k)"

        @navigate="goTo"

      />

      <PagePlaces

        v-else-if="page === 'map'"

        @navigate="goTo"

        @open-auth="openAuth"

        @open-modal="(k) => (modal = k)"

      />

      <PageMemories v-else-if="page === 'memories'" />

      <PageMessage v-else-if="page === 'message'" />

    </main>



    <AppFooterBar />



    <FanclubModal v-if="modal === 'fanclub'" @close="modal = null" />

    <GoodsModal v-if="modal === 'goods'" @close="modal = null" />

    <AiModal v-if="modal === 'ai'" @close="modal = null" />

    <AuthNoticeModal v-if="authMode" :mode="authMode" @close="closeAuth" />

  </div>

</template>



<style scoped>

.site-shell {

  min-height: 100vh;

  font-family: var(--ff-serif);

  font-size: var(--size-base);

  position: relative;

}

</style>

