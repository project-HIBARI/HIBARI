<script setup>
/**
 * ページ: ゆかりの地（地図）
 */
import { ref } from 'vue'
import PageHead from '../ui/PageHead.vue'
import TabBar from '../ui/TabBar.vue'
import JapanMap from '../map/JapanMap.vue'
import PlacesListAndDetail from './places/PlacesListAndDetail.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'

const sel = ref(HIBARU_DATA.places[0])
const tab = ref('map')
</script>

<template>
  <div>
    <PageHead kanji="縁" title="ゆかりの地" sub="Places · Pilgrimage · ひばりさんの足跡を訪ねて" />
    <TabBar
      :tabs="[
        { id: 'map', label: '地図', icon: 'map' },
        { id: 'list', label: '一覧', icon: 'pin' },
      ]"
      :active="tab"
      @update:active="(v) => (tab = v)"
    />
    <div style="display: grid; grid-template-columns: 1.3fr 1fr; gap: 32px; margin-top: 24px" class="map-grid">
      <div :class="tab === 'list' ? 'sp-hide' : ''">
        <JapanMap :places="HIBARU_DATA.places" :selected="sel" @select="sel = $event" />
      </div>
      <PlacesListAndDetail :selected="sel" @select="sel = $event" />
    </div>
  </div>
</template>
