<script setup>
/**
 * ページ: 献花・メッセージ（花）
 * 用途: 誕生日・不死鳥忌の献花とメッセージ壁を表示する（ライトテーマ）
 */
import { ref } from 'vue'
import MessageHero from './message/MessageHero.vue'
import MessageAnniversaryCards from './message/MessageAnniversaryCards.vue'
import MessageOfferingBlock from './message/MessageOfferingBlock.vue'
import MessageWallGrid from './message/MessageWallGrid.vue'
import { useScrollReveal } from '../../composables/useScrollReveal.js'

const pageRoot = ref(null)
useScrollReveal(pageRoot)
</script>

<template>
  <div ref="pageRoot" class="page-message">
    <MessageHero class="site-reveal is-visible site-reveal--slow" />
    <MessageAnniversaryCards class="site-reveal site-reveal--slow site-reveal--delay-1" />
    <MessageOfferingBlock class="site-reveal site-reveal--slow site-reveal--delay-2" />
    <MessageWallGrid class="site-reveal site-reveal--slow site-reveal--delay-3" />
  </div>
</template>

<style scoped>
.page-message {
  color: var(--site-text);
}
</style>
