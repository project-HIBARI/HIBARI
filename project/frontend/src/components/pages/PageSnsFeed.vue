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
import SnsShareModal from './sns/SnsShareModal.vue'
import SnsUsageLimitModal from '../modals/SnsUsageLimitModal.vue'
import SnsReportModal from '../modals/SnsReportModal.vue'
import SnsUsageCard from './sns/SnsUsageCard.vue'
import SnsEmptyState from './sns/SnsEmptyState.vue'
import SnsSkeletonCard from './sns/SnsSkeletonCard.vue'
import { useAuth } from '../../composables/useAuth.js'
import { useSnsUsage } from '../../composables/useSnsUsage.js'
import { useSnsDmUnread } from '../../composables/useSnsDmUnread.js'
import { useSnsStoryPresence } from '../../composables/useSnsStoryPresence.js'
import { useToast } from '../../composables/useToast.js'
import { fetchSnsFeed, toggleSnsLike, toggleSnsSave, deleteSnsPost, fetchSnsPost, toggleSnsBlock } from '../../api/sns.js'

const props = defineProps({
  /** 外部（下部ナビの投稿ボタン等）からの投稿作成トリガー。値が変化すると作成モーダルを開く */
  createIntent: { type: Number, default: 0 },
  /** 通知等、外部から特定の投稿詳細を開くためのトリガー */
  openPostId: { type: Number, default: null },
})

const emit = defineEmits(['open-chat', 'need-auth', 'open-dm', 'open-profile', 'post-opened'])

const { isLoggedIn, membership } = useAuth()
const { usageStatus, remainingMessage, nextResetLabel, isUnlimited, refreshUsage } = useSnsUsage()
const { unreadCount: dmUnreadCount } = useSnsDmUnread()
const storyPresence = useSnsStoryPresence()
const { showToast } = useToast()

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

async function onShare(post) {
  if (!requireLogin()) return
  if (navigator.share) {
    try {
      await navigator.share({
        title: 'Music Memories',
        text: post.body ? post.body.slice(0, 80) : `${post.author_name}さんの投稿`,
        url: window.location.href,
      })
      return
    } catch (err) {
      if (err?.name === 'AbortError') return // ユーザーによるキャンセル
      sharePost.value = post
      return
    }
  }
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

const { groups: storyGroups, loading: storiesLoading, ensureLoaded: loadStories, openGroup: openStoryViewer } =
  storyPresence

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
  loadStories({ force: true })
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
    showToast(result.saved ? '投稿を保存しました' : '保存を解除しました')
  } catch {
    post.saved_by_viewer = prev
    showToast('通信に失敗しました', { tone: 'error' })
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

async function openPostById(postId) {
  try {
    const data = await fetchSnsPost(postId)
    detailPost.value = data.post
  } catch {
    showToast('投稿の取得に失敗しました', { tone: 'error' })
  } finally {
    emit('post-opened')
  }
}

onMounted(() => {
  loadFeed()
  loadStories()
  if (isLoggedIn.value) refreshUsage()
  if (props.openPostId) openPostById(props.openPostId)
})

watch(() => props.createIntent, (value, oldValue) => {
  if (value !== oldValue && value > 0) openCreateModal()
})

watch(() => props.openPostId, (value) => {
  if (value) openPostById(value)
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

    <TabBar :tabs="TABS" :active="activeTab" pill @update:active="onTabChange" />

    <SnsUsageCard
      v-if="isLoggedIn"
      :message="remainingMessage"
      :next-reset-label="nextResetLabel"
      :unlimited="isUnlimited"
    />

    <section class="sns-feed__list" aria-label="投稿一覧">
      <SnsSkeletonCard v-if="loading" variant="post" :count="3" />

      <template v-else-if="errorMessage">
        <div class="sns-feed__error-card">
          <p class="sns-feed__state sns-feed__state--error">読み込みに失敗しました</p>
          <UiButton variant="outline" size="sm" @click="loadFeed()">もう一度試す</UiButton>
        </div>
      </template>

      <SnsEmptyState
        v-else-if="!posts.length"
        icon="image"
        title="まだ投稿がありません"
        message="最初の思い出を投稿するか、オープンチャットでみんなと語り合いましょう"
        action-label="投稿する"
        @action="openCreateModal"
      />

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
      <span class="sns-feed__chat-deco" aria-hidden="true">♪</span>
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
  </div>
</template>

<style scoped>
.sns-feed {
  position: relative;
  max-width: 640px;
  margin: 0 auto;
  padding: 24px 16px calc(var(--bottom-nav-height, 66px) + env(safe-area-inset-bottom, 0px) + 32px);
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
  color: var(--sns-ivory);
  letter-spacing: 0.06em;
}

.sns-feed__dm-btn {
  position: relative;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 1px solid rgba(228, 190, 99, 0.4);
  background: rgba(228, 190, 99, 0.08);
  color: var(--sns-gold);
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
  border: 2px solid var(--sns-bg);
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
  color: var(--sns-text-muted);
}

.sns-feed__state--error {
  color: #e08a8a;
}

.sns-feed__chat-cta {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: flex-start;
  padding: 20px;
  border-radius: var(--site-radius-lg);
  border: 1px solid rgba(228, 190, 99, 0.35);
  background: linear-gradient(135deg, rgba(109, 61, 130, 0.3), var(--sns-bg) 80%);
  overflow: hidden;
}

.sns-feed__chat-text {
  margin: 0;
  max-width: 80%;
  font-family: var(--ff-mincho);
  font-size: 14px;
  line-height: 1.7;
  color: var(--sns-ivory);
}

.sns-feed__chat-deco {
  position: absolute;
  right: 12px;
  bottom: -10px;
  font-size: 56px;
  color: rgba(228, 190, 99, 0.16);
  pointer-events: none;
}

.sns-feed__fab {
  position: fixed;
  right: 20px;
  bottom: calc(20px + env(safe-area-inset-bottom, 0px));
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: 1px solid rgba(228, 190, 99, 0.4);
  background: var(--sns-purple);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 30;
}

@media (max-width: 767px) {
  /* モバイルでは下部ナビ中央の投稿ボタンのみを使い、FABは重複表示しない */
  .sns-feed__fab {
    display: none;
  }

  .sns-feed {
    padding-top: 18px;
  }
}

.sns-feed__error-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 32px 16px;
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--sns-border);
  background: var(--sns-card);
}
</style>
