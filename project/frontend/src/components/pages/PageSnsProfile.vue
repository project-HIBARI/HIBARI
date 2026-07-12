<script setup>
/**
 * ページ: SNSプロフィール（自分 / 他ユーザー共通）
 */
import { ref, computed, watch, onMounted } from 'vue'
import UiButton from '../ui/UiButton.vue'
import UiIco from '../ui/UiIco.vue'
import TabBar from '../ui/TabBar.vue'
import SnsPostCard from './sns/SnsPostCard.vue'
import SnsPostDetailModal from './sns/SnsPostDetailModal.vue'
import SnsFollowListModal from './sns/SnsFollowListModal.vue'
import SnsProfileEditModal from './sns/SnsProfileEditModal.vue'
import SnsShareModal from './sns/SnsShareModal.vue'
import SnsReportModal from '../modals/SnsReportModal.vue'
import { useAuth } from '../../composables/useAuth.js'
import { useSnsUsage } from '../../composables/useSnsUsage.js'
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
const { remainingMessage, nextResetLabel, refreshUsage } = useSnsUsage()

const isSelf = computed(() => isLoggedIn.value && user.value?.account_id === props.accountId)

const profile = ref(null)
const profileLoading = ref(true)
const profileError = ref('')
const followBusy = ref(false)

const activeTab = ref('photo')
const posts = ref([])
const postsLoading = ref(false)
const postsError = ref('')
const nextBeforeId = ref(null)

const storyArchive = ref([])
const archiveLoading = ref(false)

const detailPost = ref(null)
const showFollowModal = ref(null) // 'following' | 'followers' | null
const showEditModal = ref(false)
const sharePost = ref(null)
const reportTarget = ref(null)
const blockBusy = ref(false)

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
  profileLoading.value = true
  profileError.value = ''
  try {
    profile.value = await fetchSnsProfile(props.accountId)
  } catch (err) {
    profileError.value = err?.message || 'プロフィールの取得に失敗しました'
  } finally {
    profileLoading.value = false
  }
}

async function loadTabContent({ reset = true } = {}) {
  postsError.value = ''
  if (reset) {
    postsLoading.value = true
    nextBeforeId.value = null
  }
  try {
    if (activeTab.value === 'archive') {
      archiveLoading.value = true
      const data = await fetchSnsStoryArchive()
      storyArchive.value = data.stories
      archiveLoading.value = false
      return
    }
    if (activeTab.value === 'saved') {
      const data = await fetchSnsSavedPosts()
      posts.value = data.posts
      nextBeforeId.value = data.next_before_id
      return
    }
    const data = await fetchSnsProfilePosts(props.accountId, { type: activeTab.value })
    posts.value = data.posts
    nextBeforeId.value = data.next_before_id
  } catch (err) {
    postsError.value = err?.message || '投稿の取得に失敗しました'
  } finally {
    postsLoading.value = false
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
    if (activeTab.value === 'saved' && !result.saved) {
      posts.value = posts.value.filter((p) => p.post_id !== post.post_id)
    }
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
    if (profile.value) profile.value.post_count = Math.max(0, profile.value.post_count - 1)
  } catch (err) {
    postsError.value = err?.message || '削除に失敗しました'
  }
}

function onProfileUpdated({ bio, avatarPath }) {
  profile.value.bio = bio
  if (avatarPath) profile.value.avatar_path = avatarPath
  showEditModal.value = false
}

watch(() => props.accountId, () => {
  activeTab.value = 'photo'
  loadProfile()
  loadTabContent()
})

onMounted(() => {
  loadProfile()
  loadTabContent()
  if (isSelf.value) refreshUsage()
})
</script>

<template>
  <div class="sns-profile">
    <p v-if="profileLoading" class="sns-profile__state">読み込み中…</p>

    <template v-else-if="profileError">
      <p class="sns-profile__state sns-profile__state--error">{{ profileError }}</p>
      <UiButton variant="outline" size="sm" @click="loadProfile">再試行</UiButton>
    </template>

    <template v-else-if="profile">
      <header class="sns-profile__head">
        <span class="sns-profile__avatar">
          <img v-if="profile.avatar_path" :src="profile.avatar_path" :alt="profile.name" />
          <span v-else>{{ (profile.name || '?').charAt(0) }}</span>
        </span>
        <div class="sns-profile__info">
          <h1 class="sns-profile__name">{{ profile.name }}</h1>
          <p v-if="profile.bio" class="sns-profile__bio">{{ profile.bio }}</p>
          <div class="sns-profile__stats">
            <span>{{ profile.post_count }} 投稿</span>
            <button type="button" @click="showFollowModal = 'followers'">{{ profile.follower_count }} フォロワー</button>
            <button type="button" @click="showFollowModal = 'following'">{{ profile.following_count }} フォロー中</button>
          </div>
        </div>
      </header>

      <div class="sns-profile__actions">
        <UiButton v-if="isSelf" variant="outline" size="sm" @click="showEditModal = true">プロフィール編集</UiButton>
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

      <p v-if="isSelf" class="sns-profile__usage">
        {{ remainingMessage }}<template v-if="nextResetLabel"> ／ 次回リセット：{{ nextResetLabel }}</template>
      </p>

      <TabBar :tabs="tabs" :active="activeTab" @update:active="onTabChange" />

      <section v-if="activeTab === 'archive'" class="sns-profile__archive" aria-label="ストーリーズのアーカイブ">
        <p v-if="archiveLoading" class="sns-profile__state">読み込み中…</p>
        <p v-else-if="!storyArchive.length" class="sns-profile__state">まだストーリーズがありません</p>
        <div v-else class="sns-profile__archive-grid">
          <div v-for="s in storyArchive" :key="s.story_id" class="sns-profile__archive-item">
            <img v-if="s.media_type === 'image'" :src="s.file_path" :alt="s.caption || 'ストーリーズ'" />
            <video v-else :src="s.file_path" muted playsinline />
            <span v-if="!s.is_active" class="sns-profile__archive-expired">期限切れ</span>
          </div>
        </div>
      </section>

      <section v-else-if="activeTab === 'photo'" class="sns-profile__grid" aria-label="写真・動画投稿">
        <p v-if="postsLoading" class="sns-profile__state">読み込み中…</p>
        <template v-else-if="postsError">
          <p class="sns-profile__state sns-profile__state--error">{{ postsError }}</p>
          <UiButton variant="outline" size="sm" @click="loadTabContent">再試行</UiButton>
        </template>
        <p v-else-if="!posts.length" class="sns-profile__state">まだ投稿がありません</p>
        <div v-else class="sns-profile__grid-inner">
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
            />
            <video v-else-if="post.media[0]" :src="post.media[0].file_path" muted />
          </button>
        </div>
      </section>

      <section v-else class="sns-profile__list" aria-label="ひとこと投稿">
        <p v-if="postsLoading" class="sns-profile__state">読み込み中…</p>
        <template v-else-if="postsError">
          <p class="sns-profile__state sns-profile__state--error">{{ postsError }}</p>
          <UiButton variant="outline" size="sm" @click="loadTabContent">再試行</UiButton>
        </template>
        <p v-else-if="!posts.length" class="sns-profile__state">
          {{ activeTab === 'saved' ? '保存した投稿はありません' : 'まだ投稿がありません' }}
        </p>
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
        </template>
      </section>
    </template>

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
  color: rgba(248, 244, 239, 0.6);
}
.sns-profile__state--error {
  color: #e08a8a;
}
.sns-profile__head {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}
.sns-profile__avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--murasaki-700);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  flex-shrink: 0;
}
.sns-profile__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sns-profile__info {
  flex: 1;
  min-width: 0;
}
.sns-profile__name {
  margin: 0 0 4px;
  font-family: var(--ff-mincho);
  font-size: 1.2rem;
  color: #f8f4ef;
}
.sns-profile__bio {
  margin: 0 0 8px;
  font-size: 12px;
  line-height: 1.7;
  color: rgba(248, 244, 239, 0.75);
  white-space: pre-wrap;
}
.sns-profile__stats {
  display: flex;
  gap: 14px;
  font-size: 12px;
  color: rgba(248, 244, 239, 0.75);
}
.sns-profile__stats button {
  background: transparent;
  border: 0;
  color: inherit;
  cursor: pointer;
  padding: 0;
  font: inherit;
}
.sns-profile__actions {
  display: flex;
  gap: 10px;
}
.sns-profile__usage {
  margin: -6px 0 0;
  font-size: 12px;
  color: var(--kin-400);
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
  background: rgba(255, 255, 255, 0.06);
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
.sns-profile__archive-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 3px;
}
.sns-profile__archive-item {
  position: relative;
  aspect-ratio: 9 / 16;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.06);
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
</style>
