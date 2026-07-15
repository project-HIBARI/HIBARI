<script setup>
/**
 * ページ: SNSプロフィール（自分 / 他ユーザー共通）
 */
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import UiButton from '../ui/UiButton.vue'
import UiIco from '../ui/UiIco.vue'
import TabBar from '../ui/TabBar.vue'
import SnsPostCard from './sns/SnsPostCard.vue'
import SnsPostDetailModal from './sns/SnsPostDetailModal.vue'
import SnsFollowListModal from './sns/SnsFollowListModal.vue'
import SnsProfileEditModal from './sns/SnsProfileEditModal.vue'
import SnsShareModal from './sns/SnsShareModal.vue'
import SnsReportModal from '../modals/SnsReportModal.vue'
import SnsCreatePostModal from './sns/SnsCreatePostModal.vue'
import SnsUsageLimitModal from '../modals/SnsUsageLimitModal.vue'
import SnsUsageCard from './sns/SnsUsageCard.vue'
import SnsEmptyState from './sns/SnsEmptyState.vue'
import SnsSkeletonCard from './sns/SnsSkeletonCard.vue'
import StoryAvatar from '../ui/StoryAvatar.vue'
import { useAuth } from '../../composables/useAuth.js'
import { useSnsUsage } from '../../composables/useSnsUsage.js'
import { useToast } from '../../composables/useToast.js'
import {
  fetchSnsProfile,
  fetchSnsProfilePosts,
  fetchSnsSavedPosts,
  fetchSnsStoryArchive,
  toggleSnsFollow,
  toggleSnsLike,
  toggleSnsSave,
  deleteSnsPost,
  toggleSnsBlock,
} from '../../api/sns.js'

const props = defineProps({
  accountId: { type: Number, required: true },
})

const emit = defineEmits(['need-auth', 'open-dm', 'open-profile'])

const { user, isLoggedIn } = useAuth()
const { remainingMessage, nextResetLabel, isUnlimited, refreshUsage } = useSnsUsage()
const { showToast } = useToast()

const isSelf = computed(() => isLoggedIn.value && user.value?.account_id === props.accountId)

const profile = ref(null)
const profileLoading = ref(true)
const profileError = ref('')
const followBusy = ref(false)

const activeTab = ref('photo')
const posts = ref([])
const postsLoading = ref(false)
const postsLoadingMore = ref(false)
const postsError = ref('')
const nextBeforeId = ref(null)

const storyArchive = ref([])
const archiveLoading = ref(false)
const archiveError = ref('')

let profileRequestId = 0
let tabRequestId = 0
let disposed = false

const detailPost = ref(null)
const showFollowModal = ref(null) // 'following' | 'followers' | null
const showEditModal = ref(false)
const sharePost = ref(null)
const reportTarget = ref(null)
const blockBusy = ref(false)
const showCreateModal = ref(false)
const createType = ref('photo')
const sharingProfile = ref(false)
const showLimitModal = ref(false)
const limitStatus = ref(null)

function openCreate(type) {
  if (!requireLogin()) return
  createType.value = type
  showCreateModal.value = true
}

function onPostCreated() {
  showCreateModal.value = false
  refreshUsage()
  loadProfile()
  loadTabContent()
}

async function onShareProfile() {
  if (sharingProfile.value || !profile.value) return
  sharingProfile.value = true
  try {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Music Memories',
          text: `${profile.value.name}さんのプロフィール`,
          url: window.location.href,
        })
        return
      } catch (err) {
        if (err?.name === 'AbortError') return
      }
    }
    await navigator.clipboard.writeText(window.location.href)
    showToast('リンクをコピーしました')
  } catch {
    showToast('通信に失敗しました', { tone: 'error' })
  } finally {
    sharingProfile.value = false
  }
}

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
      if (err?.name === 'AbortError') return
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

function onReportUser() {
  if (!requireLogin()) return
  reportTarget.value = { type: 'user', id: profile.value.account_id }
}

async function onBlockPost(post) {
  await onBlockUser(post.account_id, post.author_name)
}

async function onBlockUser(targetId = profile.value?.account_id, targetName = profile.value?.name) {
  if (!requireLogin() || blockBusy.value || !targetId) return
  if (!window.confirm(`${targetName}さんをブロックしますか？`)) return
  blockBusy.value = true
  try {
    await toggleSnsBlock(targetId)
    posts.value = posts.value.filter((p) => p.account_id !== targetId)
    if (targetId === profile.value.account_id) {
      await loadProfile()
    }
  } catch (err) {
    postsError.value = err?.message || 'ブロックに失敗しました'
  } finally {
    blockBusy.value = false
  }
}

const tabs = computed(() => {
  const base = [
    { id: 'photo', label: '写真・動画' },
    { id: 'text', label: 'ひとこと' },
  ]
  if (isSelf.value) {
    base.push({ id: 'saved', label: '保存済み' })
    base.push({ id: 'archive', label: 'ストーリーズ' })
  }
  return base
})

async function loadProfile() {
  const requestId = ++profileRequestId
  profileLoading.value = true
  profileError.value = ''
  try {
    const data = await fetchSnsProfile(props.accountId)
    if (disposed || requestId !== profileRequestId) return
    profile.value = data
  } catch (err) {
    if (disposed || requestId !== profileRequestId) return
    profileError.value = err?.message || 'プロフィールの取得に失敗しました'
  } finally {
    if (requestId === profileRequestId) profileLoading.value = false
  }
}

async function loadTabContent({ reset = true } = {}) {
  const requestId = ++tabRequestId
  const tab = activeTab.value
  postsError.value = ''
  archiveError.value = ''
  if (reset) {
    postsLoading.value = true
    nextBeforeId.value = null
    if (tab !== 'archive') posts.value = []
  }
  try {
    if (tab === 'archive') {
      archiveLoading.value = true
      const data = await fetchSnsStoryArchive()
      if (disposed || requestId !== tabRequestId || activeTab.value !== 'archive') return
      storyArchive.value = data.stories || []
      return
    }
    if (tab === 'saved') {
      const data = await fetchSnsSavedPosts()
      if (disposed || requestId !== tabRequestId || activeTab.value !== 'saved') return
      posts.value = data.posts || []
      nextBeforeId.value = data.next_before_id
      return
    }
    const data = await fetchSnsProfilePosts(props.accountId, { type: tab })
    if (disposed || requestId !== tabRequestId || activeTab.value !== tab) return
    posts.value = data.posts || []
    nextBeforeId.value = data.next_before_id
  } catch (err) {
    if (disposed || requestId !== tabRequestId) return
    if (tab === 'archive') {
      archiveError.value = err?.message || 'アーカイブの取得に失敗しました'
    } else {
      postsError.value = err?.message || '投稿の取得に失敗しました'
    }
  } finally {
    if (requestId === tabRequestId) {
      postsLoading.value = false
      archiveLoading.value = false
    }
  }
}

async function loadMorePosts() {
  if (!nextBeforeId.value || postsLoadingMore.value || postsLoading.value) return
  if (activeTab.value === 'archive') return
  postsLoadingMore.value = true
  const tab = activeTab.value
  const beforeId = nextBeforeId.value
  try {
    const data = tab === 'saved'
      ? await fetchSnsSavedPosts({ beforeId })
      : await fetchSnsProfilePosts(props.accountId, { type: tab, beforeId })
    if (disposed || activeTab.value !== tab) return
    posts.value = [...posts.value, ...(data.posts || [])]
    nextBeforeId.value = data.next_before_id
  } catch (err) {
    if (!disposed) postsError.value = err?.message || '追加の読み込みに失敗しました'
  } finally {
    postsLoadingMore.value = false
  }
}

function onTabChange(tabId) {
  activeTab.value = tabId
  loadTabContent()
}

function requireLogin() {
  if (isLoggedIn.value) return true
  emit('need-auth', { mode: 'login' })
  return false
}

async function onToggleFollow() {
  if (!requireLogin() || followBusy.value) return
  followBusy.value = true
  const prev = profile.value.is_following
  profile.value.is_following = !prev
  profile.value.follower_count += prev ? -1 : 1
  try {
    const result = await toggleSnsFollow(props.accountId)
    profile.value.is_following = result.following
    profile.value.follower_count = result.follower_count
  } catch {
    profile.value.is_following = prev
    profile.value.follower_count += prev ? 1 : -1
  } finally {
    followBusy.value = false
  }
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
    if (activeTab.value === 'saved' && !result.saved) {
      posts.value = posts.value.filter((p) => p.post_id !== post.post_id)
    }
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
    if (profile.value) profile.value.post_count = Math.max(0, profile.value.post_count - 1)
  } catch (err) {
    postsError.value = err?.message || '削除に失敗しました'
  }
}

function onProfileUpdated({ bio, avatarPath }) {
  profile.value.bio = bio
  if (avatarPath) profile.value.avatar_path = avatarPath
  showEditModal.value = false
  showToast('プロフィールを更新しました')
}

watch(() => props.accountId, () => {
  activeTab.value = 'photo'
  loadProfile()
  loadTabContent()
})

onMounted(() => {
  disposed = false
  loadProfile()
  loadTabContent()
  if (isSelf.value) refreshUsage()
})

onUnmounted(() => {
  disposed = true
  profileRequestId += 1
  tabRequestId += 1
})
</script>

<template>
  <div class="sns-profile">
    <SnsSkeletonCard v-if="profileLoading" variant="profile" />

    <template v-else-if="profileError">
      <div class="sns-profile__error-card">
        <p class="sns-profile__state sns-profile__state--error">読み込みに失敗しました</p>
        <UiButton variant="outline" size="sm" @click="loadProfile">もう一度試す</UiButton>
      </div>
    </template>

    <template v-else-if="profile">
      <header class="sns-profile__head">
        <span class="sns-profile__avatar">
          <StoryAvatar
            :account-id="profile.account_id"
            :name="profile.name"
            :avatar-path="profile.avatar_path"
            :size="90"
          />
          <button
            v-if="isSelf"
            type="button"
            class="sns-profile__avatar-camera"
            aria-label="プロフィール画像を変更"
            @click="showEditModal = true"
          >
            <UiIco name="camera" :size="16" color="var(--sns-bg)" />
          </button>
        </span>
        <div class="sns-profile__info">
          <h1 class="sns-profile__name">{{ profile.name }}</h1>
          <p class="sns-profile__bio" :class="{ 'sns-profile__bio--empty': !profile.bio }">
            {{ profile.bio || (isSelf ? '自己紹介はまだ入力されていません' : '') }}
          </p>
          <div class="sns-profile__stats">
            <span>{{ profile.post_count }} 投稿</span>
            <button type="button" @click="showFollowModal = 'followers'">{{ profile.follower_count }} フォロワー</button>
            <button type="button" @click="showFollowModal = 'following'">{{ profile.following_count }} フォロー中</button>
          </div>
        </div>
      </header>

      <div class="sns-profile__actions">
        <template v-if="isSelf">
          <UiButton variant="gold" size="sm" @click="showEditModal = true">プロフィール編集</UiButton>
          <UiButton variant="outline" size="sm" :disabled="sharingProfile" @click="onShareProfile">
            <UiIco name="share" :size="14" /> シェア
          </UiButton>
        </template>
        <template v-else>
          <UiButton
            :variant="profile.is_following ? 'ghost' : 'primary'"
            size="sm"
            :disabled="followBusy"
            @click="onToggleFollow"
          >
            {{ profile.is_following ? 'フォロー中' : 'フォローする' }}
          </UiButton>
          <UiButton variant="outline" size="sm" @click="emit('open-dm', profile.account_id)">
            <UiIco name="mail" :size="14" /> DM
          </UiButton>
          <UiButton variant="ghost" size="sm" @click="onReportUser">通報</UiButton>
          <UiButton variant="ghost" size="sm" :disabled="blockBusy" @click="onBlockUser()">ブロック</UiButton>
        </template>
      </div>

      <SnsUsageCard
        v-if="isSelf"
        :message="remainingMessage"
        :next-reset-label="nextResetLabel"
        :unlimited="isUnlimited"
      />

      <div v-if="isSelf" class="sns-profile__shortcuts">
        <button type="button" class="sns-profile__shortcut" @click="openCreate('story')">
          <UiIco name="story-ring" :size="18" color="var(--sns-gold)" />
          <span class="sns-profile__shortcut-title">ストーリーズを追加</span>
          <span class="sns-profile__shortcut-sub">日常のひとコマをシェアしよう</span>
        </button>
        <button type="button" class="sns-profile__shortcut" @click="openCreate('text')">
          <UiIco name="chat" :size="18" color="var(--sns-gold)" />
          <span class="sns-profile__shortcut-title">ひとことを投稿</span>
          <span class="sns-profile__shortcut-sub">気持ちや想いをつぶやいてみよう</span>
        </button>
        <button type="button" class="sns-profile__shortcut" @click="activeTab = 'saved'; loadTabContent()">
          <UiIco name="bookmark" :size="18" color="var(--sns-gold)" />
          <span class="sns-profile__shortcut-title">保存済みを見る</span>
          <span class="sns-profile__shortcut-sub">お気に入りの投稿をチェック</span>
        </button>
      </div>

      <TabBar :tabs="tabs" :active="activeTab" pill @update:active="onTabChange" />

      <section v-if="activeTab === 'archive'" class="sns-profile__archive" aria-label="ストーリーズのアーカイブ">
        <SnsSkeletonCard v-if="archiveLoading" variant="story" :count="4" />
        <div v-else-if="archiveError" class="sns-profile__error-card">
          <p class="sns-profile__state sns-profile__state--error">{{ archiveError }}</p>
          <UiButton variant="outline" size="sm" @click="loadTabContent">もう一度試す</UiButton>
        </div>
        <SnsEmptyState
          v-else-if="!storyArchive.length"
          icon="story-ring"
          title="まだストーリーズがありません"
          :message="isSelf ? '日常のひとコマをストーリーズでシェアしてみましょう' : ''"
          :action-label="isSelf ? 'ストーリーズを追加' : ''"
          @action="openCreate('story')"
        />
        <div v-else class="sns-profile__archive-grid">
          <div v-for="s in storyArchive" :key="s.story_id" class="sns-profile__archive-item">
            <img
              v-if="s.media_type === 'image'"
              :src="s.file_path"
              :alt="s.caption || 'ストーリーズ'"
              loading="lazy"
            />
            <video v-else :src="s.file_path" muted playsinline preload="none" />
            <span v-if="!s.is_active" class="sns-profile__archive-expired">期限切れ</span>
          </div>
        </div>
      </section>

      <section v-else-if="activeTab === 'photo'" class="sns-profile__grid" aria-label="写真・動画投稿">
        <SnsSkeletonCard v-if="postsLoading" variant="post" :count="2" />
        <div v-else-if="postsError && !posts.length" class="sns-profile__error-card">
          <p class="sns-profile__state sns-profile__state--error">読み込みに失敗しました</p>
          <UiButton variant="outline" size="sm" @click="loadTabContent">もう一度試す</UiButton>
        </div>
        <SnsEmptyState
          v-else-if="!posts.length"
          icon="image"
          title="まだ投稿がありません"
          :message="isSelf ? '写真や動画を投稿して、あなたの思い出をみんなとシェアしましょう' : ''"
          :action-label="isSelf ? '最初の投稿を作成する' : ''"
          @action="openCreate('photo')"
        />
        <template v-else>
          <div class="sns-profile__grid-inner">
            <button
              v-for="post in posts"
              :key="post.post_id"
              type="button"
              class="sns-profile__grid-cell"
              @click="detailPost = post"
            >
              <img
                v-if="post.media[0]?.media_type === 'image'"
                :src="post.media[0].file_path"
                :alt="post.body ? post.body.slice(0, 40) : '投稿画像'"
                loading="lazy"
              />
              <video
                v-else-if="post.media[0]"
                :src="post.media[0].file_path"
                muted
                playsinline
                preload="none"
              />
            </button>
          </div>
          <div v-if="nextBeforeId" class="sns-profile__more">
            <UiButton variant="outline" size="sm" :disabled="postsLoadingMore" @click="loadMorePosts">
              {{ postsLoadingMore ? '読み込み中…' : 'さらに読み込む' }}
            </UiButton>
          </div>
        </template>
      </section>

      <section v-else class="sns-profile__list" aria-label="ひとこと投稿">
        <SnsSkeletonCard v-if="postsLoading" variant="post" :count="2" />
        <div v-else-if="postsError && !posts.length" class="sns-profile__error-card">
          <p class="sns-profile__state sns-profile__state--error">読み込みに失敗しました</p>
          <UiButton variant="outline" size="sm" @click="loadTabContent">もう一度試す</UiButton>
        </div>
        <SnsEmptyState
          v-else-if="!posts.length"
          :icon="activeTab === 'saved' ? 'bookmark' : 'chat'"
          :title="activeTab === 'saved' ? '保存した投稿はありません' : 'まだ投稿がありません'"
          :message="activeTab === 'saved' ? '気になる投稿を保存すると、ここに表示されます' : (isSelf ? '今の気持ちをひとことでシェアしてみましょう' : '')"
          :action-label="activeTab === 'text' && isSelf ? 'ひとことを投稿する' : ''"
          @action="openCreate('text')"
        />
        <template v-else>
          <SnsPostCard
            v-for="post in posts"
            :key="post.post_id"
            :post="post"
            @like="onLike"
            @save="onSave"
            @open="(p) => (detailPost = p)"
            @delete="onDelete"
            @open-profile="(id) => emit('open-profile', id)"
            @share="onShare"
            @report="onReport"
            @block="onBlockPost"
          />
          <div v-if="nextBeforeId" class="sns-profile__more">
            <UiButton variant="outline" size="sm" :disabled="postsLoadingMore" @click="loadMorePosts">
              {{ postsLoadingMore ? '読み込み中…' : 'さらに読み込む' }}
            </UiButton>
          </div>
        </template>
      </section>

      <section v-if="isSelf" class="sns-profile__activity" aria-label="最近のアクティビティ">
        <h2 class="sns-profile__section-title">最近のアクティビティ</h2>
        <p class="sns-profile__state">最近のアクティビティはありません</p>
      </section>
    </template>

    <SnsCreatePostModal
      v-if="showCreateModal"
      :initial-type="createType"
      @close="showCreateModal = false"
      @created="onPostCreated"
      @limit-reached="(status) => { showCreateModal = false; limitStatus = status; showLimitModal = true }"
    />

    <SnsUsageLimitModal
      v-if="showLimitModal"
      :membership="profile?.membership"
      :next-reset-label="limitStatus?.next_reset_label || nextResetLabel"
      @close="showLimitModal = false"
      @view-plans="showLimitModal = false; emit('need-auth', { mode: 'register' })"
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
      @block="onBlockPost"
      @report-comment="onReportComment"
    />

    <SnsShareModal v-if="sharePost" :post="sharePost" @close="sharePost = null" />

    <SnsReportModal
      v-if="reportTarget"
      :target-type="reportTarget.type"
      :target-id="reportTarget.id"
      @close="reportTarget = null"
    />

    <SnsFollowListModal
      v-if="showFollowModal"
      :account-id="profile.account_id"
      :mode="showFollowModal"
      @close="showFollowModal = null"
      @open-profile="(id) => emit('open-profile', id)"
    />

    <SnsProfileEditModal
      v-if="showEditModal"
      :bio="profile.bio"
      :avatar-path="profile.avatar_path"
      @close="showEditModal = false"
      @updated="onProfileUpdated"
    />
  </div>
</template>

<style scoped>
.sns-profile {
  max-width: 640px;
  margin: 0 auto;
  padding: 24px 16px 96px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.sns-profile__state {
  margin: 0;
  padding: 24px 12px;
  text-align: center;
  font-size: 13px;
  color: var(--sns-text-muted);
}
.sns-profile__state--error {
  color: #e08a8a;
}
.sns-profile__error-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 32px 16px;
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--sns-border);
  background: var(--sns-card);
}
.sns-profile__head {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}
.sns-profile__avatar {
  position: relative;
  width: 96px;
  height: 96px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.sns-profile__avatar-camera {
  position: absolute;
  right: -2px;
  bottom: -2px;
  width: 32px;
  height: 32px;
  min-width: 32px;
  min-height: 32px;
  border-radius: 50%;
  background: var(--sns-gold);
  border: 2px solid var(--sns-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.sns-profile__info {
  flex: 1;
  min-width: 0;
  padding-top: 4px;
}
.sns-profile__name {
  margin: 0 0 4px;
  font-family: var(--ff-mincho);
  font-size: 1.2rem;
  color: var(--sns-ivory);
}
.sns-profile__bio {
  margin: 0 0 8px;
  font-size: 12px;
  line-height: 1.7;
  color: rgba(246, 240, 234, 0.8);
  white-space: pre-wrap;
}
.sns-profile__bio--empty {
  color: var(--sns-text-muted);
  font-style: italic;
}
.sns-profile__stats {
  display: flex;
  gap: 14px;
  font-size: 12px;
  color: rgba(246, 240, 234, 0.8);
}
.sns-profile__stats button {
  background: transparent;
  border: 0;
  color: inherit;
  cursor: pointer;
  padding: 6px 0;
  font: inherit;
  min-height: 44px;
}
.sns-profile__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.sns-profile__shortcuts {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}
.sns-profile__shortcut {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  padding: 14px;
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--sns-border);
  background: var(--sns-card);
  color: var(--sns-ivory);
  text-align: left;
  cursor: pointer;
  min-height: 44px;
}
.sns-profile__shortcut:hover {
  border-color: rgba(228, 190, 99, 0.4);
  background: var(--sns-card-strong);
}
.sns-profile__shortcut-title {
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  font-weight: 600;
}
.sns-profile__shortcut-sub {
  font-size: 10px;
  color: var(--sns-text-muted);
  line-height: 1.5;
}
.sns-profile__section-title {
  margin: 0 0 -6px;
  font-family: var(--ff-mincho);
  font-size: 14px;
  color: var(--sns-ivory);
}
.sns-profile__activity {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.sns-profile__grid-inner {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 3px;
}
.sns-profile__grid-cell {
  aspect-ratio: 1 / 1;
  border: 0;
  padding: 0;
  background: var(--sns-card);
  cursor: pointer;
  overflow: hidden;
}
.sns-profile__grid-cell img,
.sns-profile__grid-cell video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sns-profile__list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.sns-profile__more {
  display: flex;
  justify-content: center;
  padding: 12px 0 4px;
}
.sns-profile__archive-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 3px;
}
.sns-profile__archive-item {
  position: relative;
  aspect-ratio: 9 / 16;
  overflow: hidden;
  background: var(--sns-card);
}
.sns-profile__archive-item img,
.sns-profile__archive-item video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sns-profile__archive-expired {
  position: absolute;
  top: 4px;
  right: 4px;
  background: rgba(0, 0, 0, 0.6);
  color: #fff;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 999px;
}

@media (max-width: 420px) {
  .sns-profile__shortcuts {
    grid-template-columns: 1fr;
  }
}
</style>
