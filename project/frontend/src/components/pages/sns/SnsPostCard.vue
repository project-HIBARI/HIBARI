<script setup>
/**
 * 部品名: SNS投稿カード（写真・動画 / ひとこと 共通）
 */
import { ref, computed } from 'vue'
import UiIco from '../../ui/UiIco.vue'

const props = defineProps({
  post: { type: Object, required: true },
  /** true = 暗背景（プラットフォームのフィード）向け、false = 明背景（モーダル内）向け */
  dark: { type: Boolean, default: true },
})

const emit = defineEmits(['like', 'save', 'open', 'delete', 'open-profile', 'share', 'report', 'block'])

const menuOpen = ref(false)
const activeMediaIndex = ref(0)

const media = computed(() => props.post.media || [])
const isPhoto = computed(() => props.post.post_type === 'photo')

function formatDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleString('ja-JP', { month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

function onMenuAction(action) {
  menuOpen.value = false
  if (action === 'delete') emit('delete', props.post)
  if (action === 'report') emit('report', props.post)
  if (action === 'block') emit('block', props.post)
}
</script>

<template>
  <article class="sns-card" :class="{ 'sns-card--light': !dark }">
    <header class="sns-card__head">
      <button type="button" class="sns-card__author" @click="emit('open-profile', post.account_id)">
        <span class="sns-card__avatar" aria-hidden="true">
          <img v-if="post.author_avatar_path" :src="post.author_avatar_path" :alt="post.author_name" />
          <span v-else>{{ (post.author_name || '?').charAt(0) }}</span>
        </span>
        <span class="sns-card__author-meta">
          <span class="sns-card__name">{{ post.author_name }}</span>
          <span class="sns-card__time">{{ formatDate(post.created_at) }}</span>
        </span>
      </button>

      <div class="sns-card__menu-wrap">
        <button type="button" class="sns-card__menu-btn" aria-label="メニュー" @click="toggleMenu">
          <UiIco name="more" :size="18" />
        </button>
        <div v-if="menuOpen" class="sns-card__menu">
          <template v-if="post.is_owner">
            <button type="button" @click="onMenuAction('delete')">削除</button>
          </template>
          <template v-else>
            <button type="button" @click="onMenuAction('report')">通報</button>
            <button type="button" @click="onMenuAction('block')">ブロック</button>
          </template>
        </div>
      </div>
    </header>

    <button
      v-if="isPhoto && media.length"
      type="button"
      class="sns-card__media"
      @click="emit('open', post)"
    >
      <img
        v-if="media[activeMediaIndex].media_type === 'image'"
        :src="media[activeMediaIndex].file_path"
        :alt="post.body ? post.body.slice(0, 60) : `${post.author_name}の投稿画像`"
        loading="lazy"
      />
      <video v-else :src="media[activeMediaIndex].file_path" muted playsinline />
      <span v-if="media.length > 1" class="sns-card__media-count">{{ media.length }}枚</span>
    </button>

    <div class="sns-card__body">
      <p v-if="post.body" class="sns-card__text">{{ post.body }}</p>
      <p v-if="post.hashtags?.length" class="sns-card__hashtags">
        <span v-for="tag in post.hashtags" :key="tag">#{{ tag }}</span>
      </p>
      <img
        v-if="!isPhoto && media.length"
        class="sns-card__text-image"
        :src="media[0].file_path"
        :alt="post.body ? post.body.slice(0, 60) : `${post.author_name}の投稿画像`"
        loading="lazy"
      />
    </div>

    <footer class="sns-card__actions">
      <button
        type="button"
        class="sns-card__action"
        :class="{ 'sns-card__action--active': post.liked_by_viewer }"
        :aria-label="post.liked_by_viewer ? 'いいねを取り消す' : 'いいねする'"
        @click="emit('like', post)"
      >
        <UiIco name="heart" :size="18" />
        <span>{{ post.like_count }}</span>
      </button>
      <button
        type="button"
        class="sns-card__action"
        aria-label="コメントを見る"
        @click="emit('open', post)"
      >
        <UiIco name="chat" :size="18" />
        <span>{{ post.comment_count }}</span>
      </button>
      <button
        type="button"
        class="sns-card__action"
        :class="{ 'sns-card__action--active': post.saved_by_viewer }"
        :aria-label="post.saved_by_viewer ? '保存を解除する' : '保存する'"
        @click="emit('save', post)"
      >
        <UiIco name="bookmark" :size="18" />
      </button>
      <button type="button" class="sns-card__action sns-card__action--share" aria-label="共有する" @click="emit('share', post)">
        <UiIco name="share" :size="18" />
      </button>
    </footer>
  </article>
</template>

<style scoped>
.sns-card {
  border-radius: var(--site-radius-lg);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}
.sns-card__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
}
.sns-card__author {
  display: flex;
  align-items: center;
  gap: 10px;
  background: transparent;
  border: 0;
  padding: 0;
  cursor: pointer;
  text-align: left;
}
.sns-card__avatar {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--murasaki-700);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--ff-sans-jp);
  font-size: 14px;
}
.sns-card__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sns-card__author-meta {
  display: flex;
  flex-direction: column;
}
.sns-card__name {
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  color: #f8f4ef;
}
.sns-card__time {
  font-size: 11px;
  color: rgba(248, 244, 239, 0.5);
}
.sns-card__menu-wrap {
  position: relative;
}
.sns-card__menu-btn {
  background: transparent;
  border: 0;
  color: rgba(248, 244, 239, 0.6);
  cursor: pointer;
  padding: 6px;
}
.sns-card__menu {
  position: absolute;
  top: 100%;
  right: 0;
  z-index: 5;
  background: #231b22;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: var(--site-radius-sm);
  overflow: hidden;
  min-width: 100px;
}
.sns-card__menu button {
  display: block;
  width: 100%;
  padding: 10px 14px;
  background: transparent;
  border: 0;
  color: #f8f4ef;
  font-size: 12px;
  text-align: left;
  cursor: pointer;
}
.sns-card__menu button:hover {
  background: rgba(255, 255, 255, 0.08);
}
.sns-card__media {
  display: block;
  width: 100%;
  border: 0;
  padding: 0;
  cursor: pointer;
  position: relative;
  background: #100c0e;
}
.sns-card__media img,
.sns-card__media video {
  width: 100%;
  max-height: 520px;
  object-fit: cover;
  display: block;
}
.sns-card__media-count {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(0, 0, 0, 0.55);
  color: #fff;
  font-size: 11px;
}
.sns-card__body {
  padding: 12px 14px 4px;
}
.sns-card__text {
  margin: 0 0 8px;
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  line-height: 1.8;
  color: #f0ece6;
  white-space: pre-wrap;
  word-break: break-word;
}
.sns-card__hashtags {
  margin: 0 0 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 12px;
  color: var(--kin-400);
}
.sns-card__text-image {
  width: 100%;
  border-radius: var(--site-radius-md);
  margin-bottom: 8px;
}
.sns-card__actions {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 8px 14px 14px;
}
.sns-card__action {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: transparent;
  border: 0;
  color: rgba(248, 244, 239, 0.7);
  cursor: pointer;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  padding: 4px;
}
.sns-card__action--active {
  color: var(--beni-500);
}
.sns-card__action--share {
  margin-left: auto;
}

.sns-card--light {
  background: var(--site-surface);
  border-color: var(--site-border);
}
.sns-card--light .sns-card__name {
  color: var(--site-text);
}
.sns-card--light .sns-card__time {
  color: var(--site-text-light);
}
.sns-card--light .sns-card__menu-btn {
  color: var(--site-text-light);
}
.sns-card--light .sns-card__menu {
  background: var(--site-surface);
  border-color: var(--site-border);
}
.sns-card--light .sns-card__menu button {
  color: var(--site-text);
}
.sns-card--light .sns-card__menu button:hover {
  background: var(--site-surface-muted);
}
.sns-card--light .sns-card__text {
  color: var(--site-text);
}
.sns-card--light .sns-card__action {
  color: var(--site-text-muted);
}
</style>
