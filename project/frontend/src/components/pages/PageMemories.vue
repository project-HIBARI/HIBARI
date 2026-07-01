<script setup>
/**
 * ページ: 思い出（掲示板＋イベント）
 */
import { ref, computed } from 'vue'
import PageHead from '../ui/PageHead.vue'
import TabBar from '../ui/TabBar.vue'
import MemoriesBoard from './memories/MemoriesBoard.vue'
import MemoriesPostAside from './memories/MemoriesPostAside.vue'
import MemoriesEventsGrid from './memories/MemoriesEventsGrid.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'

const memTab = ref('memories')
const tagFilter = ref('all')
const postData = ref({ name: '', pref: '', title: '', body: '', song: '' })
const errors = ref({})
const submitted = ref(false)
const extraLikes = ref({})

const songs = HIBARU_DATA.discography.map((d) => d.title)

const filtered = computed(() =>
  tagFilter.value === 'all' ? HIBARU_DATA.memories : HIBARU_DATA.memories.filter((m) => m.song === tagFilter.value),
)

const boardItems = computed(() =>
  filtered.value.map((m) => ({
    ...m,
    displayLikes: (extraLikes.value[m.id] ?? 0) + m.likes,
  })),
)

function validate() {
  const e = {}
  if (!postData.value.title.trim()) e.title = 'タイトルを入力してください'
  if (!postData.value.body.trim()) e.body = '本文を入力してください'
  return e
}

function handleSubmit() {
  const e = validate()
  if (Object.keys(e).length) {
    errors.value = e
    return
  }
  submitted.value = true
}

function resetForm() {
  submitted.value = false
  postData.value = { name: '', pref: '', title: '', body: '', song: '' }
  errors.value = {}
}

function like(id) {
  extraLikes.value = { ...extraLikes.value, [id]: (extraLikes.value[id] ?? 0) + 1 }
}
</script>

<template>
  <div>
    <PageHead kanji="憶" title="思い出" sub="Memories · 証言と愛唱 · ファンの集い" tone="legacy" />
    <TabBar
      :tabs="[
        { id: 'memories', label: '思い出投稿', icon: 'chat' },
        { id: 'events', label: '交流イベント', icon: 'calendar' },
      ]"
      :active="memTab"
      @update:active="(v) => (memTab = v)"
    />

    <div v-if="memTab === 'memories'" style="display: grid; grid-template-columns: 1fr 300px; gap: 48px; margin-top: 24px" class="mem-grid">
      <div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px">
          <button
            type="button"
            :style="{
              background: tagFilter === 'all' ? 'var(--beni-700)' : 'transparent',
              color: tagFilter === 'all' ? 'var(--paper-50)' : 'var(--paper-200)',
              border: '1px solid rgba(201,169,97,0.4)',
              padding: '5px 14px',
              cursor: 'pointer',
              fontFamily: 'var(--ff-mincho)',
              fontSize: '11px',
            }"
            @click="tagFilter = 'all'"
          >
            全て
          </button>
          <button
            v-for="s in songs.slice(0, 6)"
            :key="s"
            type="button"
            :style="{
              background: tagFilter === s ? 'var(--beni-700)' : 'transparent',
              color: tagFilter === s ? 'var(--paper-50)' : 'var(--paper-200)',
              border: '1px solid rgba(201,169,97,0.4)',
              padding: '5px 12px',
              cursor: 'pointer',
              fontFamily: 'var(--ff-mincho)',
              fontSize: '11px',
            }"
            @click="tagFilter = s"
          >
            {{ s }}
          </button>
        </div>
        <MemoriesBoard :items="boardItems" @like="like" />
      </div>
      <MemoriesPostAside
        :post-data="postData"
        :submitted="submitted"
        :errors="errors"
        @update:post-data="postData = $event"
        @submit="handleSubmit"
        @reset="resetForm"
      />
    </div>

    <MemoriesEventsGrid v-else />
  </div>
</template>
