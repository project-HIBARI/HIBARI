<script setup>
/**
 * ページ: Music Memory Book（プラットフォーム）
 * 役割: 複数アーティスト対応の思い出帳機能を紹介し、ファンクラブへ誘導
 */
import MusicMemoriesMemoryBookBand from './music-memories/MusicMemoriesMemoryBookBand.vue'

const emit = defineEmits(['enter-memory-book'])
</script>

<template>
  <main id="main-content" class="platform-mbook">
    <header class="platform-mbook__head">
      <p class="platform-mbook__eyebrow">Artist Fan Club Platform</p>
      <h1 class="platform-mbook__title">Music Memory Book</h1>
      <p class="platform-mbook__lead">
        献花・思い出・お気に入り楽曲・AIとの会話——あなたの音楽体験を、年ごとのアルバムに残す共通機能です。
      </p>
    </header>

    <MusicMemoriesMemoryBookBand @open-memory-book="emit('enter-memory-book')" />
  </main>
</template>

<style scoped>
.platform-mbook {
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
  padding: clamp(40px, 8vw, 72px) clamp(20px, 4vw, 40px) 64px;
  color: #f8f4ef;
}

.platform-mbook__head {
  text-align: center;
  margin-bottom: clamp(32px, 6vw, 48px);
}

.platform-mbook__eyebrow {
  margin: 0 0 12px;
  font-family: var(--ff-latin);
  font-size: var(--font-size-caption);
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: var(--kin-400);
}

.platform-mbook__title {
  margin: 0 0 14px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.6rem, 4vw, 2.2rem);
  font-weight: 600;
  letter-spacing: 0.08em;
}

.platform-mbook__lead {
  margin: 0 auto;
  max-width: 680px;
  font-family: var(--ff-sans-jp);
  font-size: clamp(0.9rem, 2vw, 1rem);
  line-height: 1.9;
  color: rgba(248, 244, 239, 0.72);
}
</style>
