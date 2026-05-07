<script setup>
/**
 * ページ: ディスコグラフィ（曲）
 */
import { ref, computed } from 'vue'
import PageHead from '../ui/PageHead.vue'
import RecordChip from '../ui/RecordChip.vue'
import UiIco from '../ui/UiIco.vue'
import DiscoDetailDialog from './disco/DiscoDetailDialog.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'
import { inputDark } from '../../utils/hibaru.js'

const query = ref('')
const filter = ref('all')
const genre = ref('all')
const year = ref([1949, 1989])
const detail = ref(null)

function setYearStart(v) {
  const next = [...year.value]
  next[0] = v
  if (next[0] > next[1]) next[1] = next[0]
  year.value = next
}
function setYearEnd(v) {
  const next = [...year.value]
  next[1] = v
  if (next[1] < next[0]) next[0] = next[1]
  year.value = next
}

const items = computed(() =>
  HIBARU_DATA.discography.filter((d) => {
    const q = query.value.toLowerCase()
    const matchQ =
      !q || d.title.includes(query.value) || d.romaji.toLowerCase().includes(q) || d.lyric.includes(query.value) || d.music.includes(query.value)
    const matchT = filter.value === 'all' || d.type === filter.value
    const matchG = genre.value === 'all' || d.genre === genre.value
    const matchY = d.year >= year.value[0] && d.year <= year.value[1]
    return matchQ && matchT && matchG && matchY
  }),
)
</script>

<template>
  <div>
    <PageHead kanji="曲" title="ディスコグラフィ" sub="Discography · MISORA HIBARI · 1949—1989" />

    <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 32px">
      <div style="position: relative">
        <input
          v-model="query"
          placeholder="曲名・作詞・作曲で検索"
          aria-label="楽曲を検索"
          :style="{ ...inputDark, paddingLeft: '36px', background: 'rgba(10,6,4,0.8)' }"
        />
        <div style="position: absolute; top: 50%; left: 12px; transform: translateY(-50%); pointer-events: none">
          <UiIco name="search" :size="15" color="var(--kin-500)" />
        </div>
      </div>
      <div style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center">
        <button
          v-for="[k, l] in [
            ['all', '全作品'],
            ['シングル', 'シングル'],
            ['アルバム', 'アルバム'],
          ]"
          :key="k"
          type="button"
          :style="{
            background: filter === k ? 'var(--beni-700)' : 'transparent',
            color: filter === k ? 'var(--paper-50)' : 'var(--paper-200)',
            border: '1px solid rgba(201,169,97,0.4)',
            padding: '7px 18px',
            cursor: 'pointer',
            fontFamily: 'var(--ff-mincho)',
            fontSize: '12px',
            letterSpacing: '0.1em',
          }"
          @click="filter = k"
        >
          {{ l }}
        </button>
        <select v-model="genre" :style="{ ...inputDark, width: 'auto', background: 'rgba(10,6,4,0.8)' }" aria-label="ジャンル">
          <option value="all">全ジャンル</option>
          <option v-for="g in ['演歌', '歌謡曲', '民謡', 'ポップス']" :key="g" :value="g">{{ g }}</option>
        </select>
        <div style="display: flex; align-items: center; gap: 8px; font-family: var(--ff-mono); font-size: 11px; color: var(--paper-300)">
          <span>{{ year[0] }}年</span>
          <input
            type="range"
            min="1949"
            max="1989"
            :value="year[0]"
            aria-label="開始年"
            style="accent-color: var(--beni-700)"
            @input="setYearStart(+$event.target.value)"
          />
          <span>〜</span>
          <input
            type="range"
            min="1949"
            max="1989"
            :value="year[1]"
            aria-label="終了年"
            style="accent-color: var(--beni-700)"
            @input="setYearEnd(+$event.target.value)"
          />
          <span>{{ year[1] }}年</span>
        </div>
      </div>
    </div>

    <div v-if="items.length === 0" style="text-align: center; padding: 80px 0; color: var(--paper-300); font-family: var(--ff-mincho); font-size: 16px">
      該当する楽曲が見つかりませんでした
    </div>
    <div v-else style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px">
      <button
        v-for="(d, i) in items"
        :key="i"
        type="button"
        style="display: grid; grid-template-columns: 96px 1fr auto; gap: 18px; background: rgba(201,169,97,0.04); border: 1px solid rgba(201,169,97,0.22); padding: 18px; align-items: center; cursor: pointer; text-align: left; color: var(--paper-100)"
        :aria-label="d.title + 'の詳細を見る'"
        @click="detail = d"
        @mouseenter="(e) => (e.currentTarget.style.background = 'rgba(201,169,97,0.1)')"
        @mouseleave="(e) => (e.currentTarget.style.background = 'rgba(201,169,97,0.04)')"
      >
        <RecordChip :no="d.no" :color="i % 3 === 0 ? 'var(--beni-700)' : i % 3 === 1 ? '#3a2a1a' : '#2a2040'" />
        <div>
          <div style="font-family: var(--ff-mono); font-size: 10px; color: var(--kin-500); letter-spacing: 0.2em; margin-bottom: 4px">
            {{ d.year }} · {{ d.no }} · {{ d.genre }}
          </div>
          <div style="font-family: var(--ff-mincho); font-size: 20px; font-weight: 700; letter-spacing: 0.05em">{{ d.title }}</div>
          <div style="font-family: var(--ff-latin); font-style: italic; font-size: 12px; color: var(--paper-300); margin-top: 2px">{{ d.romaji }}</div>
          <div style="font-size: 11px; color: var(--paper-300); margin-top: 5px">作詞：{{ d.lyric }} / 作曲：{{ d.music }}</div>
          <div v-if="d.note" style="font-size: 11px; color: var(--paper-200); margin-top: 4px">{{ d.note }}</div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px; align-items: center">
          <span
            style="background: transparent; border: 1px solid var(--kin-500); color: var(--kin-500); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center"
            aria-hidden="true"
          >
            <UiIco name="play" :size="13" color="var(--kin-500)" />
          </span>
          <span
            v-if="d.note && d.note.includes('賞')"
            style="font-size: 9px; color: var(--kin-500); border: 1px solid var(--kin-500); padding: 2px 6px; letter-spacing: 0.1em; font-family: var(--ff-mincho); text-align: center"
            >受賞</span
          >
        </div>
      </button>
    </div>

    <DiscoDetailDialog :detail="detail" @close="detail = null" />
  </div>
</template>
