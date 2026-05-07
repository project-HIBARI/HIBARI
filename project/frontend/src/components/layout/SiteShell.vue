<script setup>
/**
 * 部品名: サイト全体シェル
 * 役割: ヘッダー／ナビ／ページ切替／モーダル／オープニングを束ねる
 */
import { ref } from 'vue'
import AppHeaderBar from './AppHeaderBar.vue'
import AppMainNav from './AppMainNav.vue'
import AppDrawerNav from './AppDrawerNav.vue'
import PremiumMemberBar from './PremiumMemberBar.vue'
import AppFooterBar from './AppFooterBar.vue'
import OpeningFilm from '../opening/OpeningFilm.vue'
import FanclubModal from '../modals/FanclubModal.vue'
import GoodsModal from '../modals/GoodsModal.vue'
import AiModal from '../modals/AiModal.vue'
import PageTop from '../pages/PageTop.vue'
import PageDisco from '../pages/PageDisco.vue'
import PageProfile from '../pages/PageProfile.vue'
import PagePlaces from '../pages/PagePlaces.vue'
import PageMemories from '../pages/PageMemories.vue'
import PageMessage from '../pages/PageMessage.vue'
import { useBodyScrollLock } from '../../composables/useBodyScrollLock.js'

const navItems = [
  { id: 'top', kanji: '序', label: 'トップ' },
  { id: 'disco', kanji: '曲', label: 'ディスコグラフィ' },
  { id: 'profile', kanji: '歴', label: '歩み' },
  { id: 'map', kanji: '縁', label: 'ゆかりの地' },
  { id: 'memories', kanji: '憶', label: '思い出' },
  { id: 'message', kanji: '花', label: '献花' },
]

const page = ref('top')
const drawerOpen = ref(false)
const modal = ref(null)
const filmKey = ref(0)

const filmDone = ref(false)
try {
  filmDone.value = sessionStorage.getItem('hbr-film') === '1'
} catch {
  filmDone.value = false
}

useBodyScrollLock(drawerOpen)

function goTo(id) {
  page.value = id
  drawerOpen.value = false
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function finishFilm() {
  filmDone.value = true
  try {
    sessionStorage.setItem('hbr-film', '1')
  } catch {
    /* ignore */
  }
}

function replayFilm() {
  try {
    sessionStorage.removeItem('hbr-film')
  } catch {
    /* ignore */
  }
  filmDone.value = false
  filmKey.value += 1
}

</script>

<template>
  <div
    style="min-height: 100vh; background: var(--sumi); color: var(--paper-100); font-family: var(--ff-serif); font-size: var(--size-base); position: relative"
  >
    <OpeningFilm v-if="!filmDone" :key="filmKey" @done="finishFilm" />

    <header role="banner" style="background: #0d0806; border-bottom: 1px solid rgba(201,169,97,0.3); position: sticky; top: 0; z-index: 50">
      <AppHeaderBar
        @logo="goTo('top')"
        @replay-film="replayFilm"
        @open-modal="(k) => (modal = k)"
        @open-drawer="drawerOpen = true"
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
      @replay-film="replayFilm"
    />

    <main id="main-content" class="main-pad" style="padding: 48px 64px; min-height: 800px; max-width: 1400px; margin: 0 auto">
      <PageTop v-if="page === 'top'" @navigate="goTo" />
      <PageDisco v-else-if="page === 'disco'" />
      <PageProfile v-else-if="page === 'profile'" />
      <PagePlaces v-else-if="page === 'map'" />
      <PageMemories v-else-if="page === 'memories'" />
      <PageMessage v-else-if="page === 'message'" />
    </main>

    <AppFooterBar />

    <FanclubModal v-if="modal === 'fanclub'" @close="modal = null" />
    <GoodsModal v-if="modal === 'goods'" @close="modal = null" />
    <AiModal v-if="modal === 'ai'" @close="modal = null" />
  </div>
</template>
