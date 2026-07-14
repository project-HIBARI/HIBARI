<script setup>
/**
 * ページ: 思い出（掲示板＋イベント）
 * 用途: ファンの思い出投稿と交流イベントを表示する（ライトテーマ）
 */
import { ref, computed } from 'vue'
import MemoriesHeroSection from './memories/MemoriesHeroSection.vue'
import MemoriesTabSection from './memories/MemoriesTabSection.vue'
import MemoriesMemoriesPanel from './memories/MemoriesMemoriesPanel.vue'
import MemoriesPostAside from './memories/MemoriesPostAside.vue'
import MemoriesEventsGrid from './memories/MemoriesEventsGrid.vue'
import MemoriesAiCard from './memories/MemoriesAiCard.vue'
import MemoriesRelatedCards from './memories/MemoriesRelatedCards.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'
import { createPostWithMedia } from '../../api/posts.js'
import { useBoardPost } from '../../composables/useBoardPost.js'
import { revokeMediaPreview } from '../../lib/boardMedia.js'

const emit = defineEmits(['navigate', 'open-auth', 'open-modal'])

const { recordPost, canPostNow } = useBoardPost()

const memTab = ref('memories')
const tagFilter = ref('all')
const postData = ref({
  name: '',
  pref: '',
  title: '',
  body: '',
  song: '',
  mediaFile: null,
  mediaPreviewUrl: '',
  mediaKind: null,
})
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
  if (!canPostNow.value) return

  const e = validate()
  if (Object.keys(e).length) {
    errors.value = e
    return
  }

  submitting.value = true
  submitError.value = ''
  try {
    await createPostWithMedia(
      {
        title: postData.value.title.trim(),
        content: postData.value.body.trim(),
        name: postData.value.name.trim() || null,
        location: postData.value.pref.trim() || null,
        song_id: null,
      },
      postData.value.mediaFile,
    )
    recordPost()
    submitted.value = true
  } catch (err) {
    if (err.status === 429) {
      submitError.value = err.message || '投稿上限に達しています。'
      await recordPost()
    } else if (err.message?.includes('Failed to fetch') || err.message?.includes('NetworkError')) {
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
  revokeMediaPreview(postData.value.mediaPreviewUrl)
  postData.value = {
    name: '',
    pref: '',
    title: '',
    body: '',
    song: '',
    mediaFile: null,
    mediaPreviewUrl: '',
    mediaKind: null,
  }
  errors.value = {}
}

function like(id) {
  extraLikes.value = { ...extraLikes.value, [id]: (extraLikes.value[id] ?? 0) + 1 }
}
</script>

<template>
  <div class="page-memories">
    <MemoriesHeroSection @open-ai="emit('open-modal', 'ai')" />

    <MemoriesTabSection v-model:active="memTab">
      <div v-if="memTab === 'memories'" class="page-memories__layout mem-grid">
        <MemoriesMemoriesPanel
          :items="boardItems"
          :songs="songs"
          :tag-filter="tagFilter"
          @update:tag-filter="tagFilter = $event"
          @like="like"
        />
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

      <MemoriesEventsGrid
        v-else
        @need-auth="(m) => emit('open-auth', m)"
        @navigate="(p) => emit('navigate', p)"
      />
    </MemoriesTabSection>

    <MemoriesAiCard @open-ai="emit('open-modal', 'ai')" />

    <MemoriesRelatedCards
      @navigate="(id) => emit('navigate', id)"
      @coming-soon="(mode) => emit('open-auth', mode)"
    />
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

@media (max-width: 767px) {
  .page-memories__layout {
    grid-template-columns: 1fr;
  }
}
</style>
