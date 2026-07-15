<script setup>
/**
 * ページ: 思い出（掲示板＋イベント）
 * 用途: ファンの思い出投稿と交流イベントを表示する（ライトテーマ）
 */
import { ref, computed, onMounted, watch } from 'vue'
import MemoriesHeroSection from './memories/MemoriesHeroSection.vue'
import MemoriesTabSection from './memories/MemoriesTabSection.vue'
import MemoriesMemoriesPanel from './memories/MemoriesMemoriesPanel.vue'
import MemoriesPostAside from './memories/MemoriesPostAside.vue'
import MemoriesPostEditModal from './memories/MemoriesPostEditModal.vue'
import MemoriesEventsGrid from './memories/MemoriesEventsGrid.vue'
import MemoriesAiCard from './memories/MemoriesAiCard.vue'
import MemoriesRelatedCards from './memories/MemoriesRelatedCards.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'
import { createPostWithMedia, fetchPosts, updatePost, deletePost } from '../../api/posts.js'
import { mapApiPostToBoardItem } from '../../lib/boardPosts.js'
import { useBoardPost } from '../../composables/useBoardPost.js'
import { useAuth } from '../../composables/useAuth.js'
import { revokeMediaPreview } from '../../lib/boardMedia.js'

const emit = defineEmits(['navigate', 'open-auth', 'open-modal'])

const { recordPost, canPostNow } = useBoardPost()
const { user, isLoggedIn } = useAuth()

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
const apiPosts = ref([])
const loading = ref(true)
const loadError = ref('')

const editOpen = ref(false)
const editingPost = ref(null)
const editSubmitting = ref(false)
const editError = ref('')
const actionError = ref('')

const songs = HIBARU_DATA.discography.map((d) => d.title)
const currentAccountId = computed(() => user.value?.account_id ?? null)

const boardItems = computed(() => {
  let rows = apiPosts.value
  if (tagFilter.value === 'mine') {
    if (currentAccountId.value == null) return []
    rows = rows.filter((r) => Number(r.account_id) === Number(currentAccountId.value))
  }
  const mapped = rows.map((row) =>
    mapApiPostToBoardItem(row, extraLikes.value, currentAccountId.value),
  )
  if (tagFilter.value === 'all' || tagFilter.value === 'mine') return mapped
  return mapped.filter((m) => m.song === tagFilter.value)
})

const emptyMessage = computed(() => {
  if (tagFilter.value === 'mine') {
    if (!isLoggedIn.value) return '自分の投稿を見るにはログインしてください。'
    return '自分の投稿はまだありません。'
  }
  if (apiPosts.value.length) return '該当する投稿がありません。'
  return 'まだ思い出の投稿がありません。最初の投稿をしてみましょう。'
})

async function loadPosts() {
  loading.value = true
  loadError.value = ''
  actionError.value = ''
  try {
    const list = await fetchPosts()
    apiPosts.value = Array.isArray(list) ? list : []
  } catch (err) {
    apiPosts.value = []
    loadError.value = err?.message || '投稿の取得に失敗しました。'
  } finally {
    loading.value = false
  }
}

function onTagFilter(next) {
  if (next === 'mine' && !isLoggedIn.value) {
    emit('open-auth', 'login')
    return
  }
  tagFilter.value = next
}

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
    await loadPosts()
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

function openEdit(post) {
  if (!post?.isOwn) return
  editingPost.value = post
  editError.value = ''
  editOpen.value = true
}

function closeEdit() {
  editOpen.value = false
  editingPost.value = null
  editError.value = ''
  editSubmitting.value = false
}

async function saveEdit(payload) {
  editSubmitting.value = true
  editError.value = ''
  try {
    await updatePost(payload.postId, {
      title: payload.title,
      content: payload.content,
      name: payload.name,
      location: payload.location,
    })
    apiPosts.value = apiPosts.value.map((row) => {
      if (Number(row.post_id) !== Number(payload.postId)) return row
      return {
        ...row,
        title: payload.title,
        content: payload.content,
        name: payload.name,
        location: payload.location,
      }
    })
    closeEdit()
  } catch (err) {
    editError.value = err?.message || '投稿の更新に失敗しました。'
  } finally {
    editSubmitting.value = false
  }
}

async function handleDelete(post) {
  if (!post?.isOwn || !post.postId) return
  const ok = window.confirm(`「${post.title}」を削除しますか？`)
  if (!ok) return
  actionError.value = ''
  try {
    await deletePost(post.postId)
    apiPosts.value = apiPosts.value.filter((row) => Number(row.post_id) !== Number(post.postId))
  } catch (err) {
    actionError.value = err?.message || '投稿の削除に失敗しました。'
  }
}

watch(isLoggedIn, (loggedIn) => {
  if (!loggedIn && tagFilter.value === 'mine') {
    tagFilter.value = 'all'
  }
})

onMounted(() => {
  loadPosts()
})
</script>

<template>
  <div class="page-memories">
    <MemoriesHeroSection @open-ai="emit('open-modal', 'ai')" />

    <MemoriesTabSection v-model:active="memTab">
      <div v-if="memTab === 'memories'" class="page-memories__layout mem-grid">
        <div class="page-memories__list">
          <p v-if="loading" class="page-memories__state">読み込み中…</p>
          <div v-else-if="loadError" class="page-memories__state page-memories__state--error">
            <p>{{ loadError }}</p>
            <button type="button" class="page-memories__retry" @click="loadPosts">もう一度試す</button>
          </div>
          <template v-else>
            <MemoriesMemoriesPanel
              :items="boardItems"
              :songs="songs"
              :tag-filter="tagFilter"
              @update:tag-filter="onTagFilter"
              @like="like"
              @edit="openEdit"
              @delete="handleDelete"
            />
            <p v-if="actionError" class="page-memories__state page-memories__state--error">{{ actionError }}</p>
            <p v-if="!boardItems.length" class="page-memories__state">{{ emptyMessage }}</p>
          </template>
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

    <MemoriesPostEditModal
      :open="editOpen"
      :post="editingPost"
      :submitting="editSubmitting"
      :error="editError"
      @close="closeEdit"
      @save="saveEdit"
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
.page-memories__list {
  min-width: 0;
}
.page-memories__state {
  margin: var(--sp-5) 0 0;
  padding: 24px 20px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  background: var(--site-surface);
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  line-height: 1.8;
  color: var(--site-text-muted);
  text-align: center;
}
.page-memories__state--error {
  color: var(--beni-600, #9b2c2c);
}
.page-memories__retry {
  margin-top: 12px;
  padding: 8px 16px;
  border: 1px solid var(--site-border-strong, var(--site-border));
  border-radius: var(--site-radius-sm);
  background: #fff;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  color: var(--site-text);
  cursor: pointer;
}
.page-memories__retry:hover {
  border-color: var(--murasaki-400);
  color: var(--murasaki-700);
}

@media (max-width: 767px) {
  .page-memories__layout {
    grid-template-columns: 1fr;
  }
}
</style>
