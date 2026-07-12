<script setup>
/**
 * ページ: Music Memories SNSフィード
 * 役割: ストーリーズ・投稿種別タブ・投稿フィード・投稿作成の入口
 */
import { ref, onMounted, watch } from 'vue'
import UiButton from '../ui/UiButton.vue'
import UiIco from '../ui/UiIco.vue'
import TabBar from '../ui/TabBar.vue'
import SnsPostCard from './sns/SnsPostCard.vue'
import SnsCreatePostModal from './sns/SnsCreatePostModal.vue'
import SnsPostDetailModal from './sns/SnsPostDetailModal.vue'
import SnsStoryBar from './sns/SnsStoryBar.vue'
import SnsStoryViewer from './sns/SnsStoryViewer.vue'
import SnsShareModal from './sns/SnsShareModal.vue'
import SnsUsageLimitModal from '../modals/SnsUsageLimitModal.vue'
import SnsReportModal from '../modals/SnsReportModal.vue'
import { useAuth } from '../../composables/useAuth.js'
import { useSnsUsage } from '../../composables/useSnsUsage.js'
import { useSnsDmUnread } from '../../composables/useSnsDmUnread.js'
import { fetchSnsFeed, toggleSnsLike, toggleSnsSave, deleteSnsPost, fetchSnsStories, toggleSnsBlock } from '../../api/sns.js'

const props = defineProps({
  /** 外部（下部ナビの投稿ボタン等）からの投稿作成トリガー。値が変化すると作成モーダルを開く */
  createIntent: { type: Number, default: 0 },
})

const emit = defineEmits(['open-chat', 'need-auth', 'open-dm', 'open-profile'])

const { isLoggedIn, membership } = useAuth()
const { usageStatus, remainingMessage, nextResetLabel, refreshUsage } = useSnsUsage()
const { unreadCount: dmUnreadCount } = useSnsDmUnread()

const TABS = [
  { id: 'all', label: 'すべて' },
  { id: 'photo', label: '写真・動画' },
  { id: 'text', label: 'ひとこと' },
]

const activeTab = ref('all')
const posts = ref([])
const loading = ref(false)
const loadingMore = ref(false)
const errorMessage = ref('')
const nextBeforeId = ref(null)

const showCreateModal = ref(false)
const showLimitModal = ref(false)
const limitStatus = ref(null)
const detailPost = ref(null)
const sharePost = ref(null)
const reportTarget = ref(null) // { type, id }

function onShare(post) {
  if (!requireLogin()) return
  sharePost.value = post
}

function onReport(post) {
  if (!requireLogin()) return
  reportTarget.value = { type: 'post', id: post.post_id }
}

function onReportComment(comment) {
  if (!requireLogin()) return
  reportTarget.value = { type: 'comment', id: comment.comment_id }
}

async function onBlock(post) {
  if (!requireLogin()) return
  if (!window.confirm(`${post.author_name}さんをブロックしますか？`)) return
  try {
    await toggleSnsBlock(post.account_id)
    posts.value = posts.value.filter((p) => p.account_id !== post.account_id)
    if (detailPost.value?.account_id === post.account_id) detailPost.value = null
  } catch (err) {
    errorMessage.value = err?.message || 'ブロックに失敗しました'
  }
}

const storyGroups = ref([])
const storiesLoading = ref(false)
const viewerGroups = ref(null)
const viewerStartIndex = ref(0)

async function loadStories() {
  storiesLoading.value = true
  try {
    const data = await fetchSnsStories()
    storyGroups.value = data.groups
  } catch {
    storyGroups.value = []
  } finally {
    storiesLoading.value = false
  }
}

function openStoryViewer(group) {
  const index = storyGroups.value.findIndex((g) => g.account_id === group.account_id)
  viewerGroups.value = storyGroups.value
  viewerStartIndex.value = index >= 0 ? index : 0
}

function closeStoryViewer() {
  viewerGroups.value = null
  loadStories()
}

function onStoryDeleted() {
  loadStories()
}

async function loadFeed({ reset = true } = {}) {
  errorMessage.value = ''
  if (reset) {
    loading.value = true
    nextBeforeId.value = null
  }
  try {
    const data = await fetchSnsFeed({ type: activeTab.value })
    posts.value = data.posts
    nextBeforeId.value = data.next_before_id
  } catch (err) {
    errorMessage.value = err?.message || 'フィードの取得に失敗しました'
  } finally {
    loading.value = false
  }
}

async function loadMore() {
  if (!nextBeforeId.value || loadingMore.value) return
  loadingMore.value = true
  try {
    const data = await fetchSnsFeed({ type: activeTab.value, beforeId: nextBeforeId.value })
    posts.value = [...posts.value, ...data.posts]
    nextBeforeId.value = data.next_before_id
  } catch {
    // 追加読み込み失敗時は現状を維持し、再度ボタン押下で再試行できるようにする
  } finally {
    loadingMore.value = false
  }
}

function onTabChange(tabId) {
  activeTab.value = tabId
  loadFeed()
}

function requireLogin(action) {
  if (isLoggedIn.value) return true
  emit('need-auth', { mode: 'login' })
  return false
}

function openCreateModal() {
  if (!requireLogin()) return
  if (usageStatus.value && !usageStatus.value.can_post) {
    limitStatus.value = usageStatus.value
    showLimitModal.value = true
    return
  }
  showCreateModal.value = true
}

function onPostCreated() {
  showCreateModal.value = false
  refreshUsage()
  loadFeed()
  loadStories()
}

function onLimitReached(status) {
  showCreateModal.value = false
  limitStatus.value = status
  showLimitModal.value = true
}

function onViewPlans() {
  showLimitModal.value = false
  emit('need-auth', { mode: 'register' })
}

async function onLike(post) {
  if (!requireLogin()) return
  const prevLiked = post.liked_by_viewer
  const prevCount = post.like_count
  post.liked_by_viewer = !prevLiked
  post.like_count += prevLiked ? -1 : 1
  try {
    const result = await toggleSnsLike(post.post_id)
    post.liked_by_viewer = result.liked
    post.like_count = result.like_count
  } catch {
    post.liked_by_viewer = prevLiked
    post.like_count = prevCount
  }
}

async function onSave(post) {
  if (!requireLogin()) return
  const prev = post.saved_by_viewer
  post.saved_by_viewer = !prev
  try {
    const result = await toggleSnsSave(post.post_id)
    post.saved_by_viewer = result.saved
  } catch {
    post.saved_by_viewer = prev
  }
}

async function onDelete(post) {
  if (!window.confirm('この投稿を削除しますか？')) return
  try {
    await deleteSnsPost(post.post_id)
    posts.value = posts.value.filter((p) => p.post_id !== post.post_id)
    if (detailPost.value?.post_id === post.post_id) detailPost.value = null
  } catch (err) {
    errorMessage.value = err?.message || '削除に失敗しました'
  }
}

function openDetail(post) {
  detailPost.value = post
}

onMounted(() => {
  loadFeed()
  loadStories()
  if (isLoggedIn.value) refreshUsage()
})

watch(() => props.createIntent, (value, oldValue) => {
  if (value !== oldValue && value > 0) openCreateModal()
})
</script>

<template>
  <div class="sns-feed">
    <header class="sns-feed__head">
      <h1 class="sns-feed__title">みんなの投稿</h1>
      <button type="button" class="sns-feed__dm-btn" aria-label="ダイレクトメッセージ" @click="emit('open-dm')">
        <UiIco name="mail" :size="20" />
        <span v-if="dmUnreadCount > 0" class="sns-feed__dm-badge">{{ dmUnreadCount > 9 ? '9+' : dmUnreadCount }}</span>
      </button>
    </header>

    <SnsStoryBar
      :groups="storyGroups"
      :loading="storiesLoading"
      @open="openStoryViewer"
      @create="openCreateModal"
    />

    <TabBar :tabs="TABS" :active="activeTab" @update:active="onTabChange" />

    <p v-if="isLoggedIn" class="sns-feed__usage">{{ remainingMessage }}</p>

    <section class="sns-feed__list" aria-label="投稿一覧">
      <p v-if="loading" class="sns-feed__state">読み込み中…</p>

      <template v-else-if="errorMessage">
        <p class="sns-feed__state sns-feed__state--error">{{ errorMessage }}</p>
        <UiButton variant="outline" size="sm" @click="loadFeed()">再試行</UiButton>
      </template>

      <template v-else-if="!posts.length">
        <p class="sns-feed__state">
          まだ投稿がありません。最初の思い出を投稿するか、オープンチャットでみんなと語り合いましょう。
        </p>
        <div class="sns-feed__empty-actions">
          <UiButton variant="gold" size="sm" @click="openCreateModal">投稿する</UiButton>
          <UiButton variant="outline" size="sm" @click="emit('open-chat')">オープンチャットに参加する</UiButton>
        </div>
      </template>

      <template v-else>
        <SnsPostCard
          v-for="post in posts"
          :key="post.post_id"
          :post="post"
          @like="onLike"
          @save="onSave"
          @open="openDetail"
          @delete="onDelete"
          @open-profile="(id) => emit('open-profile', id)"
          @share="onShare"
          @report="onReport"
          @block="onBlock"
        />
        <UiButton v-if="nextBeforeId" variant="outline" size="sm" :disabled="loadingMore" @click="loadMore">
          {{ loadingMore ? '読み込み中…' : 'もっと見る' }}
        </UiButton>
      </template>
    </section>

    <section class="sns-feed__chat-cta">
      <p class="sns-feed__chat-text">みんなで美空ひばりさんの思い出を語りませんか？</p>
      <UiButton variant="gold" size="sm" @click="emit('open-chat')">オープンチャットに参加する</UiButton>
    </section>

    <button type="button" class="sns-feed__fab" aria-label="投稿する" @click="openCreateModal">
      <UiIco name="plus" :size="24" color="#fff" />
    </button>

    <SnsCreatePostModal
      v-if="showCreateModal"
      @close="showCreateModal = false"
      @created="onPostCreated"
      @limit-reached="onLimitReached"
    />

    <SnsPostDetailModal
      v-if="detailPost"
      :post="detailPost"
      @close="detailPost = null"
      @like="onLike"
      @save="onSave"
      @delete="onDelete"
      @open-profile="(id) => emit('open-profile', id)"
      @share="onShare"
      @report="onReport"
      @block="onBlock"
      @report-comment="onReportComment"
    />

    <SnsShareModal v-if="sharePost" :post="sharePost" @close="sharePost = null" />

    <SnsReportModal
      v-if="reportTarget"
      :target-type="reportTarget.type"
      :target-id="reportTarget.id"
      @close="reportTarget = null"
    />

    <SnsUsageLimitModal
      v-if="showLimitModal"
      :membership="membership"
      :next-reset-label="limitStatus?.next_reset_label || nextResetLabel"
      @close="showLimitModal = false"
      @view-plans="onViewPlans"
    />

    <SnsStoryViewer
      v-if="viewerGroups"
      :groups="viewerGroups"
      :initial-group-index="viewerStartIndex"
      @close="closeStoryViewer"
      @open-profile="(id) => emit('open-profile', id)"
      @deleted="onStoryDeleted"
      @need-auth="(payload) => emit('need-auth', payload)"
    />
  </div>
</template>

<style scoped>
.sns-feed {
  position: relative;
  max-width: 640px;
  margin: 0 auto;
  padding: 24px 16px 96px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.sns-feed__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sns-feed__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: clamp(1.35rem, 4vw, 1.75rem);
  color: #f8f4ef;
  letter-spacing: 0.06em;
}

.sns-feed__dm-btn {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.16);
  background: rgba(255, 255, 255, 0.06);
  color: #f8f4ef;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sns-feed__dm-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: 999px;
  background: var(--beni-600);
  color: #fff;
  font-size: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #1a1418;
}

.sns-feed__usage {
  margin: -4px 0 0;
  font-size: 12px;
  color: var(--kin-400);
}

.sns-feed__list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.sns-feed__state {
  margin: 0;
  padding: 24px 12px;
  text-align: center;
  font-size: 13px;
  color: rgba(248, 244, 239, 0.6);
}

.sns-feed__state--error {
  color: #e08a8a;
}

.sns-feed__empty-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.sns-feed__chat-cta {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: flex-start;
  padding: 20px;
  border-radius: var(--site-radius-lg);
  border: 1px solid rgba(201, 169, 97, 0.35);
  background: linear-gradient(135deg, rgba(122, 80, 136, 0.22), rgba(26, 20, 24, 0.5));
}

.sns-feed__chat-text {
  margin: 0;
  font-size: 13px;
  color: rgba(248, 244, 239, 0.8);
}

.sns-feed__fab {
  position: fixed;
  right: 20px;
  bottom: calc(20px + env(safe-area-inset-bottom, 0px));
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: 0;
  background: var(--murasaki-700);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 30;
}

@media (max-width: 767px) {
  .sns-feed__fab {
    bottom: calc(76px + env(safe-area-inset-bottom, 0px));
  }
}
</style>
