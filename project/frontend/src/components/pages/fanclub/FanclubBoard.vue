<script setup>
/**
 * 部品名: ファンクラブ — 会員掲示板
 * 用途: ファンクラブサイト内の掲示板（一覧＋投稿・月10回制限）
 */
import { ref, computed, onMounted } from 'vue'
import MemoriesBoard from '../memories/MemoriesBoard.vue'
import BoardPostForm from '../../board/BoardPostForm.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'
import { fetchPosts, createPostWithMedia } from '../../../api/posts.js'
import { useBoardPost } from '../../../composables/useBoardPost.js'
import { revokeMediaPreview } from '../../../lib/boardMedia.js'

const emit = defineEmits(['need-auth'])

const { recordPost, canPostNow } = useBoardPost()

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
const apiPosts = ref([])
const loading = ref(true)
const extraLikes = ref({})

function mapApiPost(row) {
  return {
    id: `api-${row.post_id}`,
    song: row.song_id ? String(row.song_id) : '—',
    title: row.title,
    body: row.content,
    author: row.name || '匿名',
    age: row.age || '—',
    location: row.location || '—',
    likes: row.like_count || 0,
    comments: 0,
    date: row.created_at ? String(row.created_at).slice(0, 10) : '',
    imageUrl: row.image_path || null,
    videoUrl: row.video_path || null,
    displayLikes: (extraLikes.value[`api-${row.post_id}`] ?? 0) + (row.like_count || 0),
  }
}

const demoItems = computed(() =>
  HIBARU_DATA.memories.slice(0, 3).map((m) => ({
    ...m,
    displayLikes: (extraLikes.value[m.id] ?? 0) + m.likes,
  })),
)

const boardItems = computed(() => {
  const fromApi = apiPosts.value.map(mapApiPost)
  return [...fromApi, ...demoItems.value]
})

onMounted(async () => {
  try {
    const list = await fetchPosts()
    apiPosts.value = Array.isArray(list) ? list : []
  } catch {
    apiPosts.value = []
  } finally {
    loading.value = false
  }
})

function validate() {
  const e = {}
  if (!postData.value.title.trim()) e.title = 'タイトルを入力してください'
  if (!postData.value.body.trim()) e.body = '本文を入力してください'
  return e
}

async function handleSubmit() {
  if (!canPostNow.value) {
    emit('need-auth', 'login')
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
    const result = await createPostWithMedia(
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
    if (result?.post_id) {
      apiPosts.value = [
        {
          post_id: result.post_id,
          title: postData.value.title.trim(),
          content: postData.value.body.trim(),
          name: postData.value.name.trim() || '匿名',
          location: postData.value.pref.trim() || '',
          like_count: 0,
          created_at: new Date().toISOString(),
          image_path: result.image_path || null,
          video_path: result.video_path || null,
        },
        ...apiPosts.value,
      ]
    }
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
  <div class="fc-board">
    <div class="fc-board__layout">
      <div class="fc-board__list">
        <p v-if="loading" class="fc-board__loading">読み込み中…</p>
        <MemoriesBoard v-else :items="boardItems" @like="like" />
      </div>
      <aside class="fc-board__aside">
        <div class="fc-board__form-card">
          <BoardPostForm
            heading="掲示板に投稿"
            :post-data="postData"
            :errors="errors"
            :submitted="submitted"
            :submitting="submitting"
            :submit-error="submitError"
            @update:post-data="postData = $event"
            @submit="handleSubmit"
            @reset="resetForm"
            @need-auth="(m) => emit('need-auth', m)"
          />
        </div>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.fc-board__layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: var(--sp-6);
  align-items: start;
}
.fc-board__form-card {
  position: sticky;
  top: 120px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  padding: var(--sp-5);
  background: linear-gradient(135deg, var(--site-bg-pink) 0%, var(--site-surface) 100%);
  box-shadow: var(--site-shadow);
}
.fc-board__loading {
  margin: 0;
  padding: 24px;
  text-align: center;
  font-size: var(--font-size-button);
  color: var(--site-text-muted);
}

@media (max-width: 900px) {
  .fc-board__layout {
    grid-template-columns: 1fr;
  }
  .fc-board__form-card {
    position: static;
  }
}
</style>
