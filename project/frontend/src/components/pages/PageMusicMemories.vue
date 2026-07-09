<script setup>
/**
 * ページ: Music Memories プラットフォーム
 * 役割: 複数アーティストのファンクラブへの入口ハブ
 */
import UiButton from '../ui/UiButton.vue'
import { MUSIC_MEMORIES_ARTISTS } from '../../data/musicMemoriesData.js'

defineProps({
  /** PlatformShell 内ではヘッダーを非表示 */
  embedded: { type: Boolean, default: false },
})

const emit = defineEmits(['enter-site', 'open-chat'])

function onArtistClick(artist) {
  if (artist.status !== 'open') return
  emit('enter-site', artist.siteId)
}
</script>

<template>
  <div class="music-memories" :class="{ 'music-memories--embedded': embedded }">
    <header v-if="!embedded" class="music-memories__header" role="banner">
      <div class="music-memories__header-inner">
        <p class="music-memories__brand" aria-label="Music Memories">
          <span class="music-memories__brand-mark" aria-hidden="true">♪</span>
          Music Memories
        </p>
        <p class="music-memories__header-tag">音楽の記憶を、いつまでも</p>
      </div>
    </header>

    <main id="main-content" class="music-memories__main">
      <section class="music-memories__hero" aria-labelledby="mm-hero-title">
        <p class="music-memories__eyebrow">Artist Fan Club Platform</p>
        <h1 id="mm-hero-title" class="music-memories__title">
          あの時代の音楽を、<br class="music-memories__br-sp" />もう一度。
        </h1>
        <p class="music-memories__lead">
          レジェンドたちの歌声と歩みを、ファンクラブを通じて紡ぐプラットフォームです。
          お好きなアーティストを選んで、思い出の世界へお進みください。
        </p>
      </section>

      <section class="music-memories__chat-section" aria-labelledby="mm-chat-title">
        <div class="music-memories__chat-card">
          <div class="music-memories__chat-copy">
            <p class="music-memories__chat-eyebrow">Open Chat</p>
            <h2 id="mm-chat-title" class="music-memories__chat-title">ファン同士の交流広場</h2>
            <p class="music-memories__chat-desc">
              美空ひばりをはじめ、複数アーティストのファンが集まるオープンチャット。
              楽曲の話からイベントの感想まで、深い交流ができます。
            </p>
          </div>
          <UiButton variant="gold" size="md" @click="emit('open-chat')">
            オープンチャットへ
          </UiButton>
        </div>
      </section>

      <section class="music-memories__grid-section" aria-labelledby="mm-grid-title">
        <div class="music-memories__grid-head">
          <h2 id="mm-grid-title" class="music-memories__grid-title">ファンクラブ一覧</h2>
          <p class="music-memories__grid-desc">参加したいアーティストを選んでください</p>
        </div>

        <ul class="music-memories__grid">
          <li
            v-for="artist in MUSIC_MEMORIES_ARTISTS"
            :key="artist.id"
            class="music-memories__card-wrap"
          >
            <article
              class="music-memories__card"
              :class="{
                'music-memories__card--open': artist.status === 'open',
                'music-memories__card--soon': artist.status === 'soon',
              }"
            >
              <div class="music-memories__card-visual" aria-hidden="true">
                <img
                  v-if="artist.image"
                  :src="artist.image"
                  :alt="artist.name"
                  class="music-memories__card-image"
                  loading="lazy"
                  decoding="async"
                />
                <div v-else class="music-memories__card-placeholder">
                  <span>♪</span>
                </div>
              </div>

              <div class="music-memories__card-body">
                <p class="music-memories__card-en">{{ artist.nameEn }}</p>
                <h3 class="music-memories__card-name">{{ artist.name }}</h3>
                <p class="music-memories__card-tagline">{{ artist.tagline }}</p>

                <UiButton
                  v-if="artist.status === 'open'"
                  variant="gold"
                  size="md"
                  class="music-memories__card-cta"
                  @click="onArtistClick(artist)"
                >
                  ファンクラブへ
                </UiButton>
                <span v-else class="music-memories__card-badge">準備中</span>
              </div>
            </article>
          </li>
        </ul>
      </section>
    </main>

    <footer class="music-memories__footer" role="contentinfo">
      <p class="music-memories__copyright">© Music Memories Platform</p>
    </footer>
  </div>
</template>

<style scoped>
.music-memories--embedded {
  min-height: auto;
}

.music-memories--embedded .music-memories__main {
  padding-top: clamp(32px, 6vw, 56px);
}

.music-memories {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background:
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(122, 80, 136, 0.14), transparent 55%),
    linear-gradient(180deg, #1a1418 0%, #231b22 42%, #2a2228 100%);
  color: #f8f4ef;
}

.music-memories__header {
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.music-memories__header-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.music-memories__brand {
  margin: 0;
  font-family: var(--ff-latin);
  font-size: clamp(1.25rem, 2.5vw, 1.6rem);
  font-weight: 600;
  letter-spacing: 0.14em;
  display: flex;
  align-items: center;
  gap: 10px;
}

.music-memories__brand-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--murasaki-600), var(--murasaki-800));
  font-size: 14px;
  color: #fff;
}

.music-memories__header-tag {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  letter-spacing: 0.16em;
  color: rgba(248, 244, 239, 0.55);
}

.music-memories__main {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: clamp(40px, 8vw, 80px) 24px 64px;
}

.music-memories__hero {
  text-align: center;
  margin-bottom: clamp(48px, 8vw, 72px);
}

.music-memories__eyebrow {
  margin: 0 0 16px;
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: var(--kin-400);
}

.music-memories__title {
  margin: 0 0 20px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.75rem, 5vw, 2.75rem);
  font-weight: 600;
  line-height: 1.45;
  letter-spacing: 0.06em;
}

.music-memories__lead {
  margin: 0 auto;
  max-width: 640px;
  font-family: var(--ff-sans-jp);
  font-size: clamp(0.9rem, 2vw, 1rem);
  line-height: 1.9;
  color: rgba(248, 244, 239, 0.72);
}

.music-memories__grid-head {
  margin-bottom: 28px;
}

.music-memories__chat-section {
  margin-bottom: clamp(40px, 7vw, 64px);
}

.music-memories__chat-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
  padding: 28px 30px;
  border: 1px solid rgba(201, 169, 97, 0.35);
  border-radius: var(--site-radius-lg);
  background: linear-gradient(135deg, rgba(122, 80, 136, 0.22), rgba(26, 20, 24, 0.5));
}

.music-memories__chat-eyebrow {
  margin: 0 0 8px;
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: var(--kin-400);
}

.music-memories__chat-title {
  margin: 0 0 10px;
  font-family: var(--ff-mincho);
  font-size: 1.35rem;
  letter-spacing: 0.08em;
}

.music-memories__chat-desc {
  margin: 0;
  max-width: 640px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.8;
  color: rgba(248, 244, 239, 0.68);
}

.music-memories__grid-title {
  margin: 0 0 8px;
  font-family: var(--ff-mincho);
  font-size: 1.25rem;
  letter-spacing: 0.1em;
}

.music-memories__grid-desc {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  color: rgba(248, 244, 239, 0.55);
}

.music-memories__grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.music-memories__card {
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: var(--site-radius-lg);
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.04);
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.35s, border-color 0.35s;
}

.music-memories__card--open:hover {
  transform: translateY(-4px);
  border-color: rgba(201, 169, 97, 0.45);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35);
}

.music-memories__card--soon {
  opacity: 0.65;
}

.music-memories__card-visual {
  aspect-ratio: 16 / 10;
  background: linear-gradient(145deg, rgba(90, 58, 107, 0.35), rgba(26, 20, 24, 0.6));
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.music-memories__card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
}

.music-memories__card-placeholder {
  font-size: 2.5rem;
  color: rgba(255, 255, 255, 0.2);
}

.music-memories__card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px 22px 24px;
  gap: 6px;
}

.music-memories__card-en {
  margin: 0;
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--kin-400);
}

.music-memories__card-name {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 1.35rem;
  letter-spacing: 0.06em;
}

.music-memories__card-tagline {
  margin: 0 0 12px;
  flex: 1;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.7;
  color: rgba(248, 244, 239, 0.65);
}

.music-memories__card-cta {
  align-self: flex-start;
}

.music-memories__card-badge {
  align-self: flex-start;
  display: inline-flex;
  padding: 6px 14px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  letter-spacing: 0.12em;
  color: rgba(248, 244, 239, 0.5);
}

.music-memories__footer {
  padding: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  text-align: center;
}

.music-memories__copyright {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  color: rgba(248, 244, 239, 0.4);
  letter-spacing: 0.08em;
}

@media (max-width: 640px) {
  .music-memories__br-sp {
    display: none;
  }

  .music-memories__header-inner {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
  }
}
</style>
