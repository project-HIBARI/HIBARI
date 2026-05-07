<script setup>
/**
 * ページ: トップ（序）
 * 構成: ヒーロー / ティッカー / 装飾 / ショートカット / 今日の一曲 / 思い出
 */
import { computed } from 'vue'
import Ornament from '../ui/Ornament.vue'
import TopHeroSection from './top/TopHeroSection.vue'
import TopNewsTicker from './top/TopNewsTicker.vue'
import TopShortcutCards from './top/TopShortcutCards.vue'
import TopSongAnniversary from './top/TopSongAnniversary.vue'
import TopLatestMemories from './top/TopLatestMemories.vue'
import { todaysSong } from '../../utils/hibaru.js'

const emit = defineEmits(['navigate'])

const song = computed(() => todaysSong())
</script>

<template>
  <div>
    <TopHeroSection @navigate="emit('navigate', $event)" />
    <TopNewsTicker />
    <Ornament tone="gold" style="margin-bottom: 64px" />
    <TopShortcutCards @navigate="emit('navigate', $event)" />
    <TopSongAnniversary :song="song" @navigate="emit('navigate', $event)" />
    <TopLatestMemories @navigate="emit('navigate', $event)" />
  </div>
</template>
