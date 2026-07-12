<script setup>
/**
 * 部品名: SNS投稿詳細モーダル（コメント一覧・投稿）
 */
import { ref, onMounted, computed } from 'vue'
import ModalShell from '../../modals/ModalShell.vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'
import SnsPostCard from './SnsPostCard.vue'
import { fetchSnsComments, createSnsComment, deleteSnsComment } from '../../../api/sns.js'
import { useAuth } from '../../../composables/useAuth.js'

const props = defineProps({
  post: { type: Object, required: true },
})

const emit = defineEmits(['close', 'like', 'save', 'delete', 'open-profile', 'share', 'report', 'block', 'report-comment'])

const { user, isLoggedIn } = useAuth()

const comments = ref([])
const loading = ref(false)
const errorMessage = ref('')
const commentBody = ref('')
const submitting = ref(false)
const nextBeforeId = ref(null)

const MAX_COMMENT = 500
const remaining = computed(() => MAX_COMMENT - commentBody.value.length)

async function loadComments() {
  loading.value = true
  errorMessage.value = ''
  try {
    const data = await fetchSnsComments(props.post.post_id)
    comments.value = data.comments
    nextBeforeId.value = data.next_before_id
  } catch (err) {
    errorMessage.value = err?.message || 'コメントの取得に失敗しました'
  } finally {
    loading.value = false
  }
}

async function loadMore() {
  if (!nextBeforeId.value) return
  try {
    const data = await fetchSnsComments(props.post.post_id, { beforeId: nextBeforeId.value })
    comments.value = [...data.comments, ...comments.value]
    nextBeforeId.value = data.next_before_id
  } catch {
    // 追加読み込み失敗時は現状維持
  }
}

async function submitComment() {
  if (submitting.value || !commentBody.value.trim()) return
  submitting.value = true
  errorMessage.value = ''
  try {
    await createSnsComment(props.post.post_id, commentBody.value.trim())
    commentBody.value = ''
    await loadComments()
  } catch (err) {
    errorMessage.value = err?.message || 'コメントの投稿に失敗しました'
  } finally {
    submitting.value = false
  }
}

async function removeComment(commentId) {
  try {
    await deleteSnsComment(commentId)
    comments.value = comments.value.filter((c) => c.comment_id !== commentId)
  } catch (err) {
    errorMessage.value = err?.message || 'コメントの削除に失敗しました'
  }
}

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleString('ja-JP', { month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

onMounted(loadComments)
</script>

<template>
  <ModalShell title="投稿" wide @close="emit('close')">
    <div class="sns-detail">
      <SnsPostCard
        :post="post"
        :dark="false"
        @like="emit('like', post)"
        @save="emit('save', post)"
        @delete="emit('delete', post)"
        @open-profile="(id) => emit('open-profile', id)"
        @share="emit('share', post)"
        @report="emit('report', post)"
        @block="emit('block', post)"
      />

      <section class="sns-detail__comments" aria-label="コメント">
        <button v-if="nextBeforeId" type="button" class="sns-detail__more" @click="loadMore">
          過去のコメントをもっと見る
        </button>

        <p v-if="loading" class="sns-detail__state">読み込み中…</p>
        <p v-else-if="!comments.length" class="sns-detail__state">
          まだコメントがありません。最初のコメントを送ってみましょう。
        </p>

        <ul v-else class="sns-detail__list">
          <li v-for="c in comments" :key="c.comment_id" class="sns-detail__comment">
            <span class="sns-detail__avatar" aria-hidden="true">
              <img v-if="c.author_avatar_path" :src="c.author_avatar_path" :alt="c.author_name" />
              <span v-else>{{ (c.author_name || '?').charAt(0) }}</span>
            </span>
            <div class="sns-detail__comment-body">
              <p class="sns-detail__comment-meta">
                <span class="sns-detail__comment-name">{{ c.author_name }}</span>
                <span class="sns-detail__comment-time">{{ formatDate(c.created_at) }}</span>
              </p>
              <p class="sns-detail__comment-text">{{ c.body }}</p>
            </div>
            <button
              v-if="user && c.account_id === user.account_id"
              type="button"
              class="sns-detail__comment-delete"
              aria-label="コメントを削除"
              @click="removeComment(c.comment_id)"
            >
              <UiIco name="close" :size="12" />
            </button>
            <button
              v-else-if="isLoggedIn"
              type="button"
              class="sns-detail__comment-delete"
              aria-label="コメントを通報"
              @click="emit('report-comment', c)"
            >
              通報
            </button>
          </li>
        </ul>
      </section>

      <form v-if="isLoggedIn && post.comments_enabled" class="sns-detail__form" @submit.prevent="submitComment">
        <input
          v-model="commentBody"
          type="text"
          class="sns-detail__input"
          :maxlength="MAX_COMMENT"
          placeholder="コメントを入力"
        />
        <UiButton type="submit" variant="primary" size="sm" :disabled="submitting || !commentBody.trim()">
          送信
        </UiButton>
      </form>
      <p v-else-if="!post.comments_enabled" class="sns-detail__state">この投稿はコメントが許可されていません。</p>
      <p v-else class="sns-detail__state">コメントするにはログインしてください。</p>

      <p v-if="errorMessage" class="sns-detail__error">{{ errorMessage }}</p>
    </div>
  </ModalShell>
</template>

<style scoped>
.sns-detail {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.sns-detail__comments {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.sns-detail__more {
  align-self: center;
  background: transparent;
  border: 0;
  color: var(--murasaki-700);
  font-size: 12px;
  cursor: pointer;
}
.sns-detail__state {
  margin: 0;
  font-size: 13px;
  color: var(--site-text-muted);
  text-align: center;
  padding: 8px 0;
}
.sns-detail__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 320px;
  overflow-y: auto;
}
.sns-detail__comment {
  display: flex;
  gap: 10px;
  align-items: flex-start;
}
.sns-detail__avatar {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--murasaki-600);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
}
.sns-detail__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sns-detail__comment-body {
  flex: 1;
}
.sns-detail__comment-meta {
  margin: 0 0 2px;
  display: flex;
  gap: 8px;
  align-items: baseline;
}
.sns-detail__comment-name {
  font-size: 12px;
  font-weight: 600;
  color: var(--site-text);
}
.sns-detail__comment-time {
  font-size: 11px;
  color: var(--site-text-light);
}
.sns-detail__comment-text {
  margin: 0;
  font-size: 13px;
  line-height: 1.7;
  color: var(--site-text);
  white-space: pre-wrap;
  word-break: break-word;
}
.sns-detail__comment-delete {
  background: transparent;
  border: 0;
  color: var(--site-text-light);
  cursor: pointer;
  padding: 4px;
}
.sns-detail__form {
  display: flex;
  gap: 8px;
}
.sns-detail__input {
  flex: 1;
  border: 1px solid var(--site-border);
  border-radius: 999px;
  padding: 8px 16px;
  font-size: 13px;
  color: var(--site-text);
}
.sns-detail__error {
  margin: 0;
  color: var(--beni-600);
  font-size: 12px;
}
</style>
