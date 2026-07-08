<script setup>
/**
 * ページ: 思い出（掲示板＋イベント）
 * 用途: ファンの思い出投稿と交流イベントを表示する（ライトテーマ）
 */
import { ref, computed } from 'vue'
import PageHead from '../ui/PageHead.vue'
import TabBar from '../ui/TabBar.vue'
import MemoriesBoard from './memories/MemoriesBoard.vue'
import MemoriesPostAside from './memories/MemoriesPostAside.vue'
import MemoriesEventsGrid from './memories/MemoriesEventsGrid.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'
import { createPost } from '../../api/posts.js'
import { useBoardPost } from '../../composables/useBoardPost.js'

const emit = defineEmits(['open-auth'])

const { recordPost, canPostNow } = useBoardPost()

const memTab = ref('memories')
const tagFilter = ref('all')
const postData = ref({ name: '', pref: '', title: '', body: '', song: '' })
const errors = ref({})
const submitted = ref(false)
const submitting = ref(false)
const submitError = ref('')
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

async function handleSubmit() {
  if (!canPostNow.value) {
    emit('open-auth', 'login')
    return
  }

  const e = validate()
  if (Object.keys(e).length) {
    errors.value = e
    return
  }

  submitting.value = true
  submitError.value = ''
  try {
    await createPost({
      title: postData.value.title.trim(),
      content: postData.value.body.trim(),
      name: postData.value.name.trim() || null,
      location: postData.value.pref.trim() || null,
      song_id: null,
    })
    recordPost()
    submitted.value = true
  } catch (err) {
    if (err.message?.includes('Failed to fetch') || err.message?.includes('NetworkError')) {
      submitError.value = 'サーバーに接続できません。バックエンド（Flask）が起動しているか確認してください。'
    } else {
      submitError.value = err.message || '投稿に失敗しました。'
    }
  } finally {
    submitting.value = false
  }
}

function resetForm() {
  submitted.value = false
  submitError.value = ''
  postData.value = { name: '', pref: '', title: '', body: '', song: '' }
  errors.value = {}
}

function like(id) {
  extraLikes.value = { ...extraLikes.value, [id]: (extraLikes.value[id] ?? 0) + 1 }
}
</script>

<template>
  <div class="page-memories">
    <PageHead kanji="憶" title="思い出" sub="Memories · 証言と愛唱 · ファンの集い" />

    <TabBar
      :dark="false"
      :tabs="[
        { id: 'memories', label: '思い出投稿', icon: 'chat' },
        { id: 'events', label: '交流イベント', icon: 'calendar' },
      ]"
      :active="memTab"
      @update:active="(v) => (memTab = v)"
    />

    <div v-if="memTab === 'memories'" class="page-memories__layout mem-grid">
      <div>
        <div class="page-memories__tags">
          <button
            type="button"
            class="page-memories__tag"
            :class="{ 'page-memories__tag--active': tagFilter === 'all' }"
            @click="tagFilter = 'all'"
          >
            全て
          </button>
          <button
            v-for="s in songs.slice(0, 6)"
            :key="s"
            type="button"
            class="page-memories__tag"
            :class="{ 'page-memories__tag--active': tagFilter === s }"
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
        :submitting="submitting"
        :submit-error="submitError"
        :errors="errors"
        @update:post-data="postData = $event"
        @submit="handleSubmit"
        @reset="resetForm"
        @need-auth="(m) => emit('open-auth', m)"
      />
    </div>

    <MemoriesEventsGrid v-else @need-auth="(m) => emit('open-auth', m)" />
  </div>
</template>

<style scoped>
.page-memories {
  color: var(--site-text);
}
.page-memories__layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: var(--sp-7);
  margin-top: var(--sp-5);
}
.page-memories__tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: var(--sp-5);
}
.page-memories__tag {
  background: var(--site-surface);
  color: var(--site-text-muted);
  border: 1px solid var(--site-border);
  padding: 6px 14px;
  cursor: pointer;
  font-family: var(--ff-mincho);
  font-size: 11px;
  letter-spacing: 0.06em;
  border-radius: var(--site-radius-sm);
  transition: background 0.2s, border-color 0.2s, color 0.2s;
}
.page-memories__tag:hover {
  border-color: var(--murasaki-400);
  color: var(--murasaki-700);
}
.page-memories__tag--active {
  background: var(--murasaki-700);
  color: #fff;
  border-color: var(--murasaki-800);
}

@media (max-width: 767px) {
  .page-memories__layout {
    grid-template-columns: 1fr;
  }
}
</style>
