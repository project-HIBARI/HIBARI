<script setup>
/**
 * ページ: Music Memories SNS 検索・発見
 * 役割: ユーザー・投稿・ハッシュタグの横断検索、未検索時は写真・動画のグリッド発見
 */
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import UiButton from '../ui/UiButton.vue'
import UiIco from '../ui/UiIco.vue'
import TabBar from '../ui/TabBar.vue'
import SnsPostDetailModal from './sns/SnsPostDetailModal.vue'
import SnsShareModal from './sns/SnsShareModal.vue'
import SnsReportModal from '../modals/SnsReportModal.vue'
import SnsEmptyState from './sns/SnsEmptyState.vue'
import { useAuth } from '../../composables/useAuth.js'
import { useToast } from '../../composables/useToast.js'
import {
  fetchSnsSearchTop,
  fetchSnsSearchUsers,
  fetchSnsSearchPosts,
  fetchSnsSearchHashtags,
  fetchSnsDiscoverPosts,
  toggleSnsFollow,
  toggleSnsLike,
  toggleSnsSave,
  deleteSnsPost,
  toggleSnsBlock,
} from '../../api/sns.js'
import { fetchSongMemories } from '../../api/songMemories.js'
import { memoryTypeMeta } from '../../constants/songMemory.js'
import { HIBARU_DATA } from '../../data/hibaruData.js'

const props = defineProps({
  pendingSong: { type: Object, default: null },
})

const emit = defineEmits(['need-auth', 'open-profile', 'song-consumed'])

const { isLoggedIn } = useAuth()
const { showToast } = useToast()

const CATEGORY_TABS = [
  { id: 'top', label: 'トップ' },
  { id: 'users', label: 'ユーザー' },
  { id: 'posts', label: '投稿' },
  { id: 'hashtags', label: 'ハッシュタグ' },
  { id: 'songs', label: '曲', icon: 'disc' },
]

const TOP_SONG_LIMIT = 5

const query = ref('')
const activeCategory = ref('top')
const searching = ref(false)
const loadingMore = ref(false)
const searchError = ref('')

const topUsers = ref([])
const topPosts = ref([])
const topHashtags = ref([])

const userResults = ref([])
const userOffset = ref(null)

const postResults = ref([])
const postOffset = ref(null)

const hashtagResults = ref([])
const hashtagOffset = ref(null)

const discoverPosts = ref([])
const discoverOffset = ref(0)
const discoverLoading = ref(false)
const discoverLoadingMore = ref(false)
const discoverError = ref('')
let discoverSeenIds = new Set()

const detailPost = ref(null)
const sharePost = ref(null)
const reportTarget = ref(null)

const selectedSong = ref(null)
const songFans = ref([])
const songFansLoading = ref(false)
const songFansError = ref('')

const trimmedQuery = computed(() => query.value.trim())
const isSearchMode = computed(() => trimmedQuery.value.length > 0)

const songSearchResults = computed(() => {
  const q = trimmedQuery.value
  if (!q) return []
  const qLower = q.toLowerCase()
  return HIBARU_DATA.discography
    .filter((d) => d.title.includes(q) || d.romaji.toLowerCase().includes(qLower))
    .slice(0, 30)
})

const topSongs = computed(() => songSearchResults.value.slice(0, TOP_SONG_LIMIT))

const hasAnyTopResult = computed(
  () =>
    topUsers.value.length ||
    topPosts.value.length ||
    topHashtags.value.length ||
    songSearchResults.value.length
)

let searchEpoch = 0
let debounceTimer = null

function requireLogin() {
  if (isLoggedIn.value) return true
  emit('need-auth', { mode: 'login' })
  return false
}

async function loadTop(q, epoch) {
  searching.value = true
  searchError.value = ''
  try {
    const data = await fetchSnsSearchTop(q)
    if (epoch !== searchEpoch) return
    topUsers.value = data.users
    topPosts.value = data.posts
    topHashtags.value = data.hashtags
  } catch (err) {
    if (epoch !== searchEpoch) return
    searchError.value = err?.message || '検索に失敗しました'
  } finally {
    if (epoch === searchEpoch) searching.value = false
  }
}

async function loadUsers(q, epoch, { reset = true } = {}) {
  if (reset) {
    searching.value = true
    userResults.value = []
    userOffset.value = null
  } else {
    loadingMore.value = true
  }
  searchError.value = ''
  try {
    const data = await fetchSnsSearchUsers(q, { offset: reset ? 0 : userOffset.value || 0 })
    if (epoch !== searchEpoch) return
    userResults.value = reset ? data.users : [...userResults.value, ...data.users]
    userOffset.value = data.next_offset
  } catch (err) {
    if (epoch !== searchEpoch) return
    searchError.value = err?.message || 'ユーザー検索に失敗しました'
  } finally {
    if (epoch === searchEpoch) {
      searching.value = false
      loadingMore.value = false
    }
  }
}

async function loadPosts(q, epoch, { reset = true } = {}) {
  if (reset) {
    searching.value = true
    postResults.value = []
    postOffset.value = null
  } else {
    loadingMore.value = true
  }
  searchError.value = ''
  try {
    const data = await fetchSnsSearchPosts(q, { offset: reset ? 0 : postOffset.value || 0 })
    if (epoch !== searchEpoch) return
    postResults.value = reset ? data.posts : [...postResults.value, ...data.posts]
    postOffset.value = data.next_offset
  } catch (err) {
    if (epoch !== searchEpoch) return
    searchError.value = err?.message || '投稿検索に失敗しました'
  } finally {
    if (epoch === searchEpoch) {
      searching.value = false
      loadingMore.value = false
    }
  }
}

async function loadHashtags(q, epoch, { reset = true } = {}) {
  if (reset) {
    searching.value = true
    hashtagResults.value = []
    hashtagOffset.value = null
  } else {
    loadingMore.value = true
  }
  searchError.value = ''
  try {
    const data = await fetchSnsSearchHashtags(q, { offset: reset ? 0 : hashtagOffset.value || 0 })
    if (epoch !== searchEpoch) return
    hashtagResults.value = reset ? data.hashtags : [...hashtagResults.value, ...data.hashtags]
    hashtagOffset.value = data.next_offset
  } catch (err) {
    if (epoch !== searchEpoch) return
    searchError.value = err?.message || 'ハッシュタグ検索に失敗しました'
  } finally {
    if (epoch === searchEpoch) {
      searching.value = false
      loadingMore.value = false
    }
  }
}

function dispatchLoad(q, epoch, opts = {}) {
  if (activeCategory.value === 'top') return loadTop(q, epoch)
  if (activeCategory.value === 'users') return loadUsers(q, epoch, opts)
  if (activeCategory.value === 'posts') return loadPosts(q, epoch, opts)
  if (activeCategory.value === 'hashtags') return loadHashtags(q, epoch, opts)
  // 'songs' はクライアント側フィルタ（songSearchResults）で完結するためネットワーク不要
}

function bumpEpoch() {
  searchEpoch += 1
  return searchEpoch
}

function onSearchInput() {
  clearTimeout(debounceTimer)
  selectedSong.value = null
  const q = trimmedQuery.value
  if (!q) {
    bumpEpoch()
    searching.value = false
    searchError.value = ''
    return
  }
  debounceTimer = setTimeout(() => {
    const epoch = bumpEpoch()
    dispatchLoad(q, epoch, { reset: true })
  }, 300)
}

function onCategoryChange(id) {
  activeCategory.value = id
  selectedSong.value = null
  const q = trimmedQuery.value
  if (!q) return
  const epoch = bumpEpoch()
  dispatchLoad(q, epoch, { reset: true })
}

function clearQuery() {
  clearTimeout(debounceTimer)
  query.value = ''
  selectedSong.value = null
  bumpEpoch()
  searching.value = false
  searchError.value = ''
}

function onHashtagSelect(tag) {
  clearTimeout(debounceTimer)
  query.value = tag
  activeCategory.value = 'posts'
  selectedSong.value = null
  const epoch = bumpEpoch()
  dispatchLoad(tag, epoch, { reset: true })
}

async function loadDiscover({ reset = false } = {}) {
  if (reset) {
    discoverLoading.value = true
    discoverPosts.value = []
    discoverOffset.value = 0
    discoverSeenIds = new Set()
    discoverError.value = ''
  } else {
    if (discoverOffset.value == null || discoverLoadingMore.value) return
    discoverLoadingMore.value = true
  }
  try {
    const data = await fetchSnsDiscoverPosts({ offset: reset ? 0 : discoverOffset.value })
    const fresh = data.posts.filter((p) => !discoverSeenIds.has(p.post_id))
    fresh.forEach((p) => discoverSeenIds.add(p.post_id))
    discoverPosts.value = reset ? fresh : [...discoverPosts.value, ...fresh]
    discoverOffset.value = data.next_offset
  } catch (err) {
    discoverError.value = err?.message || '発見コンテンツの取得に失敗しました'
  } finally {
    discoverLoading.value = false
    discoverLoadingMore.value = false
  }
}

function loadMoreActive() {
  const q = trimmedQuery.value
  if (q) {
    if (loadingMore.value) return
    if (activeCategory.value === 'users' && userOffset.value != null) {
      dispatchLoad(q, searchEpoch, { reset: false })
    } else if (activeCategory.value === 'posts' && postOffset.value != null) {
      dispatchLoad(q, searchEpoch, { reset: false })
    } else if (activeCategory.value === 'hashtags' && hashtagOffset.value != null) {
      dispatchLoad(q, searchEpoch, { reset: false })
    }
  } else {
    loadDiscover({ reset: false })
  }
}

async function onToggleFollow(userItem) {
  if (!requireLogin() || userItem._followBusy) return
  userItem._followBusy = true
  const prev = userItem.is_following
  userItem.is_following = !prev
  try {
    const result = await toggleSnsFollow(userItem.account_id)
    userItem.is_following = result.following
  } catch {
    userItem.is_following = prev
    showToast('通信に失敗しました', { tone: 'error' })
  } finally {
    userItem._followBusy = false
  }
}

function openProfile(accountId) {
  emit('open-profile', accountId)
}

async function selectSong(song) {
  selectedSong.value = song
  songFans.value = []
  songFansError.value = ''
  songFansLoading.value = true
  try {
    const data = await fetchSongMemories(song.songId)
    songFans.value = data?.memories || []
  } catch (err) {
    songFansError.value = err?.message || '取得に失敗しました'
  } finally {
    songFansLoading.value = false
  }
}

function openDetail(post) {
  detailPost.value = post
}

function findAndPatchPost(postId, patch) {
  for (const list of [topPosts.value, postResults.value, discoverPosts.value]) {
    const found = list.find((p) => p.post_id === postId)
    if (found) Object.assign(found, patch)
  }
  if (detailPost.value?.post_id === postId) Object.assign(detailPost.value, patch)
}

async function onLike(post) {
  if (!requireLogin()) return
  const prevLiked = post.liked_by_viewer
  const prevCount = post.like_count
  findAndPatchPost(post.post_id, { liked_by_viewer: !prevLiked, like_count: prevCount + (prevLiked ? -1 : 1) })
  try {
    const result = await toggleSnsLike(post.post_id)
    findAndPatchPost(post.post_id, { liked_by_viewer: result.liked, like_count: result.like_count })
  } catch {
    findAndPatchPost(post.post_id, { liked_by_viewer: prevLiked, like_count: prevCount })
  }
}

async function onSave(post) {
  if (!requireLogin()) return
  const prev = post.saved_by_viewer
  findAndPatchPost(post.post_id, { saved_by_viewer: !prev })
  try {
    const result = await toggleSnsSave(post.post_id)
    findAndPatchPost(post.post_id, { saved_by_viewer: result.saved })
    showToast(result.saved ? '投稿を保存しました' : '保存を解除しました')
  } catch {
    findAndPatchPost(post.post_id, { saved_by_viewer: prev })
    showToast('通信に失敗しました', { tone: 'error' })
  }
}

async function onDelete(post) {
  if (!window.confirm('この投稿を削除しますか？')) return
  try {
    await deleteSnsPost(post.post_id)
    topPosts.value = topPosts.value.filter((p) => p.post_id !== post.post_id)
    postResults.value = postResults.value.filter((p) => p.post_id !== post.post_id)
    discoverPosts.value = discoverPosts.value.filter((p) => p.post_id !== post.post_id)
    if (detailPost.value?.post_id === post.post_id) detailPost.value = null
  } catch (err) {
    showToast(err?.message || '削除に失敗しました', { tone: 'error' })
  }
}

async function onBlock(post) {
  if (!requireLogin()) return
  if (!window.confirm(`${post.author_name}さんをブロックしますか？`)) return
  try {
    await toggleSnsBlock(post.account_id)
    topPosts.value = topPosts.value.filter((p) => p.account_id !== post.account_id)
    postResults.value = postResults.value.filter((p) => p.account_id !== post.account_id)
    discoverPosts.value = discoverPosts.value.filter((p) => p.account_id !== post.account_id)
    if (detailPost.value?.account_id === post.account_id) detailPost.value = null
  } catch (err) {
    showToast(err?.message || 'ブロックに失敗しました', { tone: 'error' })
  }
}

function onImgError(post) {
  post._mediaError = true
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

watch(
  () => props.pendingSong,
  (song) => {
    if (!song) return
    query.value = song.title
    activeCategory.value = 'songs'
    selectSong(song)
    emit('song-consumed')
  },
  { immediate: true },
)

const sentinel = ref(null)
let observer = null

onMounted(() => {
  loadDiscover({ reset: true })
  nextTick(() => {
    observer = new IntersectionObserver(
      (entries) => {
        if (entries[0]?.isIntersecting) loadMoreActive()
      },
      { rootMargin: '400px 0px' }
    )
    if (sentinel.value) observer.observe(sentinel.value)
  })
})

onBeforeUnmount(() => {
  clearTimeout(debounceTimer)
  if (observer) observer.disconnect()
})
</script>

<template>
  <div class="sns-discover">
    <div class="sns-discover__searchbar-wrap">
      <label class="sns-discover__searchbar">
        <UiIco name="search" :size="18" color="var(--sns-text-muted)" />
        <input
          v-model="query"
          type="search"
          inputmode="search"
          placeholder="検索"
          autocomplete="off"
          aria-label="ユーザー・投稿・曲を検索"
          @input="onSearchInput"
        />
        <button
          v-if="query"
          type="button"
          class="sns-discover__clear"
          aria-label="検索文字をクリア"
          @click="clearQuery"
        >
          <UiIco name="close" :size="14" />
        </button>
      </label>
    </div>

    <template v-if="isSearchMode">
      <div class="sns-discover__inner">
        <template v-if="selectedSong">
          <button type="button" class="sns-discover__song-back" @click="selectedSong = null">
            <UiIco name="arrow" :size="14" color="var(--sns-text-muted)" class="sns-discover__song-back-icon" />
            検索結果に戻る
          </button>

          <div class="sns-discover__song-selected">
            <span class="sns-discover__song-selected-title">{{ selectedSong.title }}</span>
            <span class="sns-discover__song-selected-year">{{ selectedSong.year }}年</span>
          </div>

          <div v-if="songFansLoading" class="sns-discover__loading">
            <span class="sns-discover__spinner" aria-hidden="true" />
            <span>読み込み中…</span>
          </div>

          <div v-else-if="songFansError" class="sns-discover__error-card">
            <p class="sns-discover__state sns-discover__state--error">読み込みに失敗しました</p>
            <UiButton variant="outline" size="sm" @click="selectSong(selectedSong)">もう一度試す</UiButton>
          </div>

          <SnsEmptyState v-else-if="!songFans.length" icon="search" title="まだ思い出が登録されていません" />

          <ul v-else class="sns-discover__user-list">
            <li v-for="fan in songFans" :key="fan.account_id" class="sns-discover__user-row">
              <button type="button" class="sns-discover__user-main" @click="openProfile(fan.account_id)">
                <span class="sns-discover__avatar" aria-hidden="true">
                  <img v-if="fan.avatar_path" :src="fan.avatar_path" :alt="fan.name" loading="lazy" />
                  <span v-else>{{ (fan.name || '?').charAt(0) }}</span>
                </span>
                <span class="sns-discover__user-meta">
                  <span class="sns-discover__user-name">
                    <UiIco
                      v-if="memoryTypeMeta(fan.memory_type)"
                      :name="memoryTypeMeta(fan.memory_type).icon"
                      :size="13"
                      color="var(--sns-gold, var(--kin-500))"
                    />
                    {{ fan.name }}
                  </span>
                  <span v-if="fan.comment" class="sns-discover__user-bio">「{{ fan.comment }}」</span>
                </span>
              </button>
              <UiButton
                :variant="fan.is_following ? 'ghost' : 'primary'"
                size="sm"
                :disabled="fan._followBusy"
                @click="onToggleFollow(fan)"
              >
                {{ fan.is_following ? 'フォロー中' : 'フォローする' }}
              </UiButton>
            </li>
          </ul>
        </template>

        <template v-else>
          <TabBar :tabs="CATEGORY_TABS" :active="activeCategory" @update:active="onCategoryChange" />

          <div class="sns-discover__results">
            <template v-if="activeCategory === 'songs'">
              <SnsEmptyState v-if="!songSearchResults.length" icon="search" title="曲が見つかりませんでした" />
              <ul v-else class="sns-discover__song-list">
                <li v-for="song in songSearchResults" :key="song.songId">
                  <button type="button" class="sns-discover__song-row" @click="selectSong(song)">
                    <span class="sns-discover__song-icon" aria-hidden="true">
                      <UiIco name="disc" :size="18" color="var(--sns-gold, var(--kin-500))" />
                    </span>
                    <span class="sns-discover__user-meta">
                      <span class="sns-discover__song-name">{{ song.title }}</span>
                      <span class="sns-discover__song-year">{{ song.year }}年</span>
                    </span>
                  </button>
                </li>
              </ul>
            </template>

            <template v-else>
              <div v-if="searching" class="sns-discover__loading">
                <span class="sns-discover__spinner" aria-hidden="true" />
                <span>検索中…</span>
              </div>

              <div v-else-if="searchError" class="sns-discover__error-card">
                <p class="sns-discover__state sns-discover__state--error">読み込みに失敗しました</p>
                <UiButton variant="outline" size="sm" @click="onCategoryChange(activeCategory)">もう一度試す</UiButton>
              </div>

              <template v-else-if="activeCategory === 'top'">
                <SnsEmptyState v-if="!hasAnyTopResult" icon="search" title="検索結果が見つかりませんでした" />
                <template v-else>
                  <section v-if="topUsers.length" class="sns-discover__section">
                    <div class="sns-discover__section-head">
                      <h2>ユーザー</h2>
                      <button type="button" @click="onCategoryChange('users')">すべて見る</button>
                    </div>
                    <ul class="sns-discover__user-list">
                      <li v-for="u in topUsers" :key="u.account_id" class="sns-discover__user-row">
                        <button type="button" class="sns-discover__user-main" @click="openProfile(u.account_id)">
                          <span class="sns-discover__avatar" aria-hidden="true">
                            <img v-if="u.avatar_path" :src="u.avatar_path" :alt="u.name" loading="lazy" />
                            <span v-else>{{ (u.name || '?').charAt(0) }}</span>
                          </span>
                          <span class="sns-discover__user-meta">
                            <span class="sns-discover__user-name">{{ u.name }}</span>
                            <span class="sns-discover__user-id">@{{ u.account_id }}</span>
                            <span v-if="u.bio" class="sns-discover__user-bio">{{ u.bio }}</span>
                          </span>
                        </button>
                        <UiButton
                          :variant="u.is_following ? 'ghost' : 'primary'"
                          size="sm"
                          :disabled="u._followBusy"
                          @click="onToggleFollow(u)"
                        >
                          {{ u.is_following ? 'フォロー中' : 'フォローする' }}
                        </UiButton>
                      </li>
                    </ul>
                  </section>

                  <section v-if="topSongs.length" class="sns-discover__section">
                    <div class="sns-discover__section-head">
                      <h2>曲</h2>
                      <button type="button" @click="onCategoryChange('songs')">すべて見る</button>
                    </div>
                    <ul class="sns-discover__song-list">
                      <li v-for="song in topSongs" :key="song.songId">
                        <button type="button" class="sns-discover__song-row" @click="selectSong(song)">
                          <span class="sns-discover__song-icon" aria-hidden="true">
                            <UiIco name="disc" :size="18" color="var(--sns-gold, var(--kin-500))" />
                          </span>
                          <span class="sns-discover__user-meta">
                            <span class="sns-discover__song-name">{{ song.title }}</span>
                            <span class="sns-discover__song-year">{{ song.year }}年</span>
                          </span>
                        </button>
                      </li>
                    </ul>
                  </section>

                  <section v-if="topHashtags.length" class="sns-discover__section">
                    <div class="sns-discover__section-head">
                      <h2>ハッシュタグ</h2>
                      <button type="button" @click="onCategoryChange('hashtags')">すべて見る</button>
                    </div>
                    <ul class="sns-discover__hashtag-list">
                      <li v-for="h in topHashtags" :key="h.tag">
                        <button type="button" class="sns-discover__hashtag-row" @click="onHashtagSelect(h.tag)">
                          <span class="sns-discover__hashtag-icon" aria-hidden="true">#</span>
                          <span class="sns-discover__user-meta">
                            <span class="sns-discover__hashtag-tag">#{{ h.tag }}</span>
                            <span class="sns-discover__hashtag-count">{{ h.post_count }}件の投稿</span>
                          </span>
                        </button>
                      </li>
                    </ul>
                  </section>

                  <section v-if="topPosts.length" class="sns-discover__section">
                    <div class="sns-discover__section-head">
                      <h2>投稿</h2>
                      <button type="button" @click="onCategoryChange('posts')">すべて見る</button>
                    </div>
                    <ul class="sns-discover__post-list">
                      <li v-for="p in topPosts" :key="p.post_id">
                        <button type="button" class="sns-discover__post-row" @click="openDetail(p)">
                          <span class="sns-discover__post-thumb">
                            <img
                              v-if="p.media[0]?.media_type === 'image' && !p._mediaError"
                              :src="p.media[0].file_path"
                              :alt="p.body ? p.body.slice(0, 40) : '投稿画像'"
                              loading="lazy"
                              @error="onImgError(p)"
                            />
                            <video
                              v-else-if="p.media[0]?.media_type === 'video' && !p._mediaError"
                              :src="p.media[0].file_path"
                              preload="metadata"
                              muted
                              playsinline
                              @error="onImgError(p)"
                            />
                            <span v-else class="sns-discover__post-thumb-fallback">
                              <UiIco name="chat" :size="18" color="var(--sns-text-muted)" />
                            </span>
                            <UiIco
                              v-if="p.media[0]?.media_type === 'video'"
                              name="play"
                              :size="12"
                              color="#fff"
                              class="sns-discover__post-thumb-play"
                            />
                          </span>
                          <span class="sns-discover__post-body">
                            <span class="sns-discover__post-author">{{ p.author_name }}</span>
                            <span class="sns-discover__post-text">{{ p.body }}</span>
                          </span>
                        </button>
                      </li>
                    </ul>
                  </section>
                </template>
              </template>

              <template v-else-if="activeCategory === 'users'">
                <SnsEmptyState v-if="!userResults.length" icon="search" title="検索結果が見つかりませんでした" />
                <ul v-else class="sns-discover__user-list">
                  <li v-for="u in userResults" :key="u.account_id" class="sns-discover__user-row">
                    <button type="button" class="sns-discover__user-main" @click="openProfile(u.account_id)">
                      <span class="sns-discover__avatar" aria-hidden="true">
                        <img v-if="u.avatar_path" :src="u.avatar_path" :alt="u.name" loading="lazy" />
                        <span v-else>{{ (u.name || '?').charAt(0) }}</span>
                      </span>
                      <span class="sns-discover__user-meta">
                        <span class="sns-discover__user-name">{{ u.name }}</span>
                        <span class="sns-discover__user-id">@{{ u.account_id }}</span>
                        <span v-if="u.bio" class="sns-discover__user-bio">{{ u.bio }}</span>
                      </span>
                    </button>
                    <UiButton
                      :variant="u.is_following ? 'ghost' : 'primary'"
                      size="sm"
                      :disabled="u._followBusy"
                      @click="onToggleFollow(u)"
                    >
                      {{ u.is_following ? 'フォロー中' : 'フォローする' }}
                    </UiButton>
                  </li>
                </ul>
              </template>

              <template v-else-if="activeCategory === 'posts'">
                <SnsEmptyState v-if="!postResults.length" icon="search" title="検索結果が見つかりませんでした" />
                <ul v-else class="sns-discover__post-list">
                  <li v-for="p in postResults" :key="p.post_id">
                    <button type="button" class="sns-discover__post-row" @click="openDetail(p)">
                      <span class="sns-discover__post-thumb">
                        <img
                          v-if="p.media[0]?.media_type === 'image' && !p._mediaError"
                          :src="p.media[0].file_path"
                          :alt="p.body ? p.body.slice(0, 40) : '投稿画像'"
                          loading="lazy"
                          @error="onImgError(p)"
                        />
                        <video
                          v-else-if="p.media[0]?.media_type === 'video' && !p._mediaError"
                          :src="p.media[0].file_path"
                          preload="metadata"
                          muted
                          playsinline
                          @error="onImgError(p)"
                        />
                        <span v-else class="sns-discover__post-thumb-fallback">
                          <UiIco name="chat" :size="18" color="var(--sns-text-muted)" />
                        </span>
                        <UiIco
                          v-if="p.media[0]?.media_type === 'video'"
                          name="play"
                          :size="12"
                          color="#fff"
                          class="sns-discover__post-thumb-play"
                        />
                      </span>
                      <span class="sns-discover__post-body">
                        <span class="sns-discover__post-author">{{ p.author_name }}</span>
                        <span class="sns-discover__post-text">{{ p.body }}</span>
                        <span class="sns-discover__post-stats">
                          <UiIco name="heart" :size="12" /> {{ p.like_count }}
                          <UiIco name="chat" :size="12" /> {{ p.comment_count }}
                        </span>
                      </span>
                    </button>
                  </li>
                </ul>
              </template>

              <template v-else-if="activeCategory === 'hashtags'">
                <SnsEmptyState v-if="!hashtagResults.length" icon="search" title="検索結果が見つかりませんでした" />
                <ul v-else class="sns-discover__hashtag-list">
                  <li v-for="h in hashtagResults" :key="h.tag">
                    <button type="button" class="sns-discover__hashtag-row" @click="onHashtagSelect(h.tag)">
                      <span class="sns-discover__hashtag-icon" aria-hidden="true">#</span>
                      <span class="sns-discover__user-meta">
                        <span class="sns-discover__hashtag-tag">#{{ h.tag }}</span>
                        <span class="sns-discover__hashtag-count">{{ h.post_count }}件の投稿</span>
                      </span>
                    </button>
                  </li>
                </ul>
              </template>
            </template>

            <div v-if="loadingMore" class="sns-discover__loading sns-discover__loading--inline">
              <span class="sns-discover__spinner" aria-hidden="true" />
            </div>
          </div>
        </template>
      </div>
    </template>

    <template v-else>
      <div v-if="discoverLoading" class="sns-discover__loading">
        <span class="sns-discover__spinner" aria-hidden="true" />
        <span>読み込み中…</span>
      </div>

      <div v-else-if="discoverError && !discoverPosts.length" class="sns-discover__error-card">
        <p class="sns-discover__state sns-discover__state--error">読み込みに失敗しました</p>
        <UiButton variant="outline" size="sm" @click="loadDiscover({ reset: true })">もう一度試す</UiButton>
      </div>

      <SnsEmptyState
        v-else-if="!discoverPosts.length"
        icon="image"
        title="まだ発見できる投稿がありません"
        message="写真や動画が投稿されると、ここに表示されます"
      />

      <div v-else class="sns-discover__grid">
        <button
          v-for="post in discoverPosts"
          :key="post.post_id"
          type="button"
          class="sns-discover__cell"
          @click="openDetail(post)"
        >
          <img
            v-if="post.media[0]?.media_type === 'image' && !post._mediaError"
            :src="post.media[0].file_path"
            :alt="post.body ? post.body.slice(0, 40) : '投稿画像'"
            loading="lazy"
            @error="onImgError(post)"
          />
          <video
            v-else-if="post.media[0]?.media_type === 'video' && !post._mediaError"
            :src="post.media[0].file_path"
            preload="metadata"
            muted
            playsinline
            @error="onImgError(post)"
          />
          <span v-else class="sns-discover__cell-fallback">
            <UiIco name="video" :size="22" color="var(--sns-text-muted)" />
          </span>
          <span v-if="post.media[0]?.media_type === 'video'" class="sns-discover__cell-badge sns-discover__cell-badge--play">
            <UiIco name="play" :size="12" color="#fff" />
          </span>
          <span v-else-if="post.media.length > 1" class="sns-discover__cell-badge">
            <UiIco name="copy" :size="12" color="#fff" />
          </span>
        </button>
      </div>

      <div v-if="discoverLoadingMore" class="sns-discover__loading sns-discover__loading--inline">
        <span class="sns-discover__spinner" aria-hidden="true" />
      </div>
    </template>

    <div ref="sentinel" class="sns-discover__sentinel" aria-hidden="true" />

    <SnsPostDetailModal
      v-if="detailPost"
      :post="detailPost"
      @close="detailPost = null"
      @like="onLike"
      @save="onSave"
      @delete="onDelete"
      @open-profile="(id) => openProfile(id)"
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
  </div>
</template>

<style scoped>
.sns-discover {
  max-width: 1080px;
  margin: 0 auto;
  padding: 16px 0 calc(var(--bottom-nav-height, 66px) + env(safe-area-inset-bottom, 0px) + 32px);
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.sns-discover__searchbar-wrap {
  padding: 0 16px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.sns-discover__searchbar {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  height: 44px;
  padding: 0 14px;
  border-radius: 999px;
  background: var(--sns-card, rgba(255, 255, 255, 0.06));
  border: 1px solid var(--sns-border, rgba(255, 255, 255, 0.1));
}

.sns-discover__song-back {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 4px;
  background: transparent;
  border: 0;
  color: var(--sns-text-muted);
  font-size: 12px;
  cursor: pointer;
  padding: 6px 0;
}

.sns-discover__song-back-icon {
  transform: rotate(180deg);
}

.sns-discover__song-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.sns-discover__song-row {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  background: transparent;
  border: 0;
  padding: 10px 4px;
  cursor: pointer;
  text-align: left;
}

.sns-discover__song-year {
  flex-shrink: 0;
  font-family: var(--ff-mono);
  font-size: 11px;
  color: var(--sns-text-muted);
}

.sns-discover__song-name {
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  color: var(--sns-ivory, #f8f4ef);
}

.sns-discover__song-selected {
  display: flex;
  align-items: baseline;
  gap: 8px;
  padding: 4px 4px 4px;
}

.sns-discover__song-selected-title {
  font-family: var(--ff-mincho);
  font-size: 15px;
  font-weight: 700;
  color: var(--sns-ivory, #f8f4ef);
}

.sns-discover__song-selected-year {
  font-size: 11px;
  color: var(--sns-text-muted);
}

.sns-discover__searchbar input {
  flex: 1;
  min-width: 0;
  border: 0;
  background: transparent;
  outline: none;
  color: var(--sns-ivory, #f8f4ef);
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  height: 100%;
}

.sns-discover__searchbar input::placeholder {
  color: var(--sns-text-muted, rgba(248, 244, 239, 0.5));
}

.sns-discover__searchbar input::-webkit-search-cancel-button {
  display: none;
}

.sns-discover__clear {
  flex-shrink: 0;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  border: 0;
  background: rgba(255, 255, 255, 0.12);
  color: var(--sns-ivory, #f8f4ef);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.sns-discover__inner {
  padding: 0 16px;
  max-width: 640px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.sns-discover__inner :deep(.tab-bar) {
  gap: 24px;
  border-bottom: 1px solid var(--sns-border, rgba(255, 255, 255, 0.1));
}

.sns-discover__inner :deep(.tab-bar__btn) {
  padding: 12px 0;
  gap: 4px;
  color: var(--sns-text-muted, rgba(248, 244, 239, 0.55));
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  font-weight: 500;
}

.sns-discover__inner :deep(.tab-bar__btn--active) {
  color: var(--sns-ivory, #f8f4ef);
  border-bottom-color: var(--sns-gold, var(--kin-500));
  font-weight: 700;
}

.sns-discover__results {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.sns-discover__section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.sns-discover__section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sns-discover__section-head h2 {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 14px;
  color: var(--sns-ivory);
}

.sns-discover__section-head button {
  background: transparent;
  border: 0;
  color: var(--sns-gold-pale, var(--kin-400));
  font-size: 12px;
  cursor: pointer;
  padding: 6px 0;
  min-height: 32px;
}

.sns-discover__user-list,
.sns-discover__post-list,
.sns-discover__hashtag-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.sns-discover__user-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 4px;
}

.sns-discover__user-main {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 10px;
  background: transparent;
  border: 0;
  padding: 0;
  cursor: pointer;
  text-align: left;
}

.sns-discover__avatar {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--sns-purple, var(--murasaki-700));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--ff-sans-jp);
  font-size: 16px;
}

.sns-discover__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.sns-discover__user-meta {
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.sns-discover__user-name {
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  font-weight: 600;
  color: var(--sns-ivory, #f8f4ef);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.sns-discover__user-id {
  font-size: 11px;
  color: var(--sns-text-muted, rgba(248, 244, 239, 0.55));
}

.sns-discover__user-bio {
  font-size: 11px;
  color: var(--sns-text-muted, rgba(248, 244, 239, 0.7));
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 240px;
}

.sns-discover__hashtag-row {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  background: transparent;
  border: 0;
  padding: 10px 4px;
  cursor: pointer;
  text-align: left;
}

.sns-discover__hashtag-icon,
.sns-discover__song-icon {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--sns-border, rgba(255, 255, 255, 0.1));
  color: var(--sns-gold, var(--kin-500));
  font-family: var(--ff-sans-jp);
  font-size: 18px;
  font-weight: 600;
}

.sns-discover__hashtag-tag {
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  font-weight: 600;
  color: var(--sns-gold, var(--kin-500));
}

.sns-discover__hashtag-count {
  font-size: 11px;
  color: var(--sns-text-muted, rgba(248, 244, 239, 0.6));
}

.sns-discover__post-row {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  background: transparent;
  border: 0;
  padding: 8px 4px;
  cursor: pointer;
  text-align: left;
}

.sns-discover__post-thumb {
  position: relative;
  flex-shrink: 0;
  width: 56px;
  height: 56px;
  border-radius: var(--site-radius-sm);
  overflow: hidden;
  background: var(--sns-card, rgba(255, 255, 255, 0.06));
}

.sns-discover__post-thumb img,
.sns-discover__post-thumb video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.sns-discover__post-thumb-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sns-discover__post-thumb-play {
  position: absolute;
  top: 4px;
  right: 4px;
}

.sns-discover__post-body {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.sns-discover__post-author {
  font-size: 12px;
  font-weight: 600;
  color: var(--sns-ivory, #f8f4ef);
}

.sns-discover__post-text {
  font-size: 12px;
  color: var(--sns-text-muted, rgba(248, 244, 239, 0.75));
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
}

.sns-discover__post-stats {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: var(--sns-text-muted, rgba(248, 244, 239, 0.6));
}

.sns-discover__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2px;
  padding: 0 2px;
}

.sns-discover__cell {
  position: relative;
  aspect-ratio: 1 / 1;
  border: 0;
  padding: 0;
  background: var(--sns-card, rgba(255, 255, 255, 0.06));
  cursor: pointer;
  overflow: hidden;
}

.sns-discover__cell img,
.sns-discover__cell video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.sns-discover__cell-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sns-discover__cell-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
}

.sns-discover__state {
  margin: 0;
  padding: 24px 12px;
  text-align: center;
  font-size: 13px;
  color: var(--sns-text-muted);
}

.sns-discover__state--error {
  color: #e08a8a;
}

.sns-discover__error-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 32px 16px;
  margin: 0 16px;
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--sns-border);
  background: var(--sns-card);
}

.sns-discover__loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 32px 12px;
  color: var(--sns-text-muted);
  font-size: 12px;
}

.sns-discover__loading--inline {
  padding: 16px 12px;
}

.sns-discover__spinner {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 2px solid rgba(228, 190, 99, 0.25);
  border-top-color: var(--sns-gold, var(--kin-500));
  animation: sns-discover-spin 0.8s linear infinite;
}

.sns-discover__sentinel {
  height: 1px;
}

@keyframes sns-discover-spin {
  to {
    transform: rotate(360deg);
  }
}

@media (min-width: 768px) {
  .sns-discover__grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 4px;
  }
}

@media (min-width: 1024px) {
  .sns-discover__grid {
    grid-template-columns: repeat(5, 1fr);
  }
}

@media (min-width: 1440px) {
  .sns-discover__grid {
    grid-template-columns: repeat(6, 1fr);
  }
}
</style>
