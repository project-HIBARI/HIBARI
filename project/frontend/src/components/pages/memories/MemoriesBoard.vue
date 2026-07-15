<script setup>
/**
 * 部品名: 思い出掲示板 — 投稿リスト
 * 用途: 思い出ページでファン投稿をカード形式で表示する
 */
import { aosAttrs } from '../../../lib/aos.js'

defineProps({
  items: { type: Array, required: true },
})

const emit = defineEmits(['like', 'edit', 'delete'])

function onImageError(event) {
  const img = event?.target
  if (!img) return
  img.style.display = 'none'
  const wrap = img.closest('.mem-board__media')
  if (!wrap) return
  const hasVisibleImage = [...wrap.querySelectorAll('img')].some((el) => el.style.display !== 'none')
  const hasVideo = wrap.querySelector('video')
  if (!hasVisibleImage && !hasVideo) {
    wrap.style.display = 'none'
  }
}

function authorLine(m) {
  const parts = []
  if (m.age != null && m.age !== '' && m.age !== '—') parts.push(`${m.age}歳`)
  if (m.location) parts.push(m.location)
  return parts.length ? `${m.author}（${parts.join('・')}）` : m.author
}
</script>

<template>
  <div class="mem-board">
    <article v-for="(m, i) in items" :key="m.id" class="mem-board__item" v-bind="aosAttrs(i * 80)">
      <div class="mem-board__song">♪ {{ m.song }}</div>
      <h3 class="mem-board__title">{{ m.title }}</h3>
      <p class="mem-board__body">{{ m.body }}</p>
      <div v-if="m.imageUrl || m.videoUrl" class="mem-board__media">
        <img
          v-if="m.imageUrl"
          :src="m.imageUrl"
          :alt="`${m.title}の添付画像`"
          class="mem-board__image"
          loading="lazy"
          @error="onImageError"
        />
        <video
          v-if="m.videoUrl"
          :src="m.videoUrl"
          class="mem-board__video"
          controls
          playsinline
          preload="metadata"
        />
      </div>
      <footer class="mem-board__foot">
        <span class="mem-board__author">{{ authorLine(m) }}</span>
        <div class="mem-board__actions">
          <template v-if="m.isOwn">
            <button type="button" class="mem-board__manage" @click="emit('edit', m)">編集</button>
            <button type="button" class="mem-board__manage mem-board__manage--danger" @click="emit('delete', m)">
              削除
            </button>
          </template>
          <button type="button" class="mem-board__like" aria-label="いいね" @click="emit('like', m.id)">
            ♡ {{ m.displayLikes }}
          </button>
          <span class="mem-board__meta">💬 {{ m.comments }}</span>
          <span class="mem-board__meta">{{ m.date }}</span>
        </div>
      </footer>
    </article>
  </div>
</template>

<style scoped>
.mem-board {
  display: flex;
  flex-direction: column;
  gap: var(--sp-5);
}
.mem-board__item {
  position: relative;
  border: 1px solid var(--site-border);
  border-left: 4px solid var(--murasaki-500);
  border-radius: var(--site-radius-md);
  padding: var(--sp-5);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
}
.mem-board__song {
  position: absolute;
  top: -11px;
  right: 20px;
  background: var(--murasaki-700);
  color: var(--kin-400);
  padding: 3px 12px;
  font-family: var(--ff-mono);
  font-size: var(--font-size-badge);
  letter-spacing: 0.15em;
  border: 1px solid var(--kin-500);
  border-radius: var(--site-radius-sm);
}
.mem-board__title {
  font-family: var(--ff-mincho);
  font-size: var(--font-size-emphasis);
  margin: 0 0 12px;
  letter-spacing: 0.06em;
  color: var(--site-text);
}
.mem-board__body {
  font-size: var(--font-size-small);
  line-height: 2;
  color: var(--site-text-muted);
  margin: 0;
}
.mem-board__media {
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.mem-board__image,
.mem-board__video {
  width: 100%;
  max-height: 360px;
  object-fit: contain;
  border-radius: var(--site-radius-sm);
  border: 1px solid var(--site-border);
  background: #111;
}
.mem-board__foot {
  margin-top: var(--sp-4);
  padding-top: 12px;
  border-top: 1px solid var(--site-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}
.mem-board__author {
  font-size: var(--font-size-caption);
  color: var(--site-text-light);
}
.mem-board__actions {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}
.mem-board__manage {
  padding: 4px 10px;
  border: 1px solid var(--site-border-strong, var(--site-border));
  border-radius: var(--site-radius-sm);
  background: #fff;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  color: var(--murasaki-700);
  cursor: pointer;
}
.mem-board__manage:hover {
  border-color: var(--murasaki-400);
  background: var(--murasaki-100, #f7f0fa);
}
.mem-board__manage--danger {
  color: var(--beni-600, #9b2c2c);
}
.mem-board__manage--danger:hover {
  border-color: rgba(155, 44, 44, 0.45);
  background: #fff5f5;
}
.mem-board__like {
  background: transparent;
  border: 0;
  cursor: pointer;
  color: var(--murasaki-600);
  display: flex;
  align-items: center;
  gap: 5px;
  font-family: var(--ff-mono);
  font-size: var(--font-size-caption);
}
.mem-board__meta {
  color: var(--site-text-light);
  font-family: var(--ff-mono);
  font-size: var(--font-size-caption);
}

@media (max-width: 480px) {
  .mem-board__item {
    padding: var(--sp-4);
  }
  .mem-board__song {
    position: static;
    display: inline-block;
    margin-bottom: 10px;
  }
  .mem-board__foot {
    flex-direction: column;
    align-items: flex-start;
  }
  .mem-board__actions {
    width: 100%;
    flex-wrap: wrap;
    gap: 10px;
  }
}
</style>
