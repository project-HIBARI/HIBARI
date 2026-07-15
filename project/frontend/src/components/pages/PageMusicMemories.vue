<script setup>
/**
 * ページ: Music Memories プラットフォーム
 * 役割: 複数アーティストのファンクラブへの入口ハブ
 */
import { computed } from 'vue'
import UiButton from '../ui/UiButton.vue'
import MusicMemoriesLogo from '../brand/MusicMemoriesLogo.vue'
import MusicMemoriesArtistCard from './music-memories/MusicMemoriesArtistCard.vue'
import MusicConnectionsBoard from '../common/MusicConnectionsBoard.vue'
import { MUSIC_MEMORIES_ARTISTS, PLATFORM_CHAT_ARTISTS, TODAYS_ARTIST } from '../../data/musicMemoriesData.js'
import { CROSS_ARTIST_CONNECTIONS } from '../../data/crossArtistConnections.js'
import { SITE_NAME, SITE_TAGLINE } from '../../constants/site.js'

defineProps({
  /** PlatformShell 内ではヘッダーを非表示 */
  embedded: { type: Boolean, default: false },
})

const emit = defineEmits(['enter-site', 'open-chat', 'open-connections'])

function onArtistClick(artist) {
  if (artist.status !== 'open') return
  emit('enter-site', artist.siteId)
}

const featuredConnections = computed(() =>
  CROSS_ARTIST_CONNECTIONS.filter((connection) => connection.featured)
)

function onEnterSite(siteId) {
  emit('enter-site', siteId)
}
</script>

<template>
  <div class="music-memories" :class="{ 'music-memories--embedded': embedded }">
    <header v-if="!embedded" class="music-memories__header" role="banner">
      <div class="music-memories__header-inner">
        <div class="music-memories__brand-wrap">
          <MusicMemoriesLogo variant="full" size="hero" />
        </div>
        <p class="music-memories__header-tag">{{ SITE_TAGLINE }}</p>
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

      <section class="music-memories__today-section" aria-labelledby="mm-today-title">
        <div class="music-memories__today">
          <div class="music-memories__today-visual" aria-hidden="true">
            <img
              v-if="TODAYS_ARTIST.image"
              :src="TODAYS_ARTIST.image"
              :alt="TODAYS_ARTIST.name"
              class="music-memories__today-image"
              loading="lazy"
              decoding="async"
            />
          </div>
          <div class="music-memories__today-body">
            <p class="music-memories__today-eyebrow">Today's Artist</p>
            <h2 id="mm-today-title" class="music-memories__today-title">今日のアーティスト</h2>
            <p class="music-memories__today-en">{{ TODAYS_ARTIST.nameEn }}</p>
            <h3 class="music-memories__today-name">{{ TODAYS_ARTIST.name }}</h3>
            <p class="music-memories__today-headline">{{ TODAYS_ARTIST.headline }}</p>
            <p class="music-memories__today-blurb">{{ TODAYS_ARTIST.blurb }}</p>
            <UiButton
              v-if="TODAYS_ARTIST.status === 'open'"
              variant="gold"
              size="md"
              class="music-memories__today-cta"
              @click="onArtistClick(TODAYS_ARTIST)"
            >
              ファンクラブをみる
            </UiButton>
          </div>
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
            <MusicMemoriesArtistCard :artist="artist" @enter-site="onEnterSite" />
          </li>
        </ul>
      </section>

      <section
        id="music-connections"
        class="music-memories__connections"
        aria-labelledby="mm-connections-title"
      >
        <p class="music-memories__connections-eyebrow">Cross-Artist Connections</p>
        <h2 id="mm-connections-title" class="music-memories__connections-title">
          アーティスト間の曲の繋がり
        </h2>
        <p class="music-memories__connections-lead">
          同じ作詞家・作曲家が手がけた楽曲をたどることで、複数のアーティストへの関心が自然に広がります。
          こちらは代表的な例です。
        </p>

        <MusicConnectionsBoard
          :connections="featuredConnections"
          @enter-site="(artistId) => emit('enter-site', artistId)"
        />

        <UiButton
          variant="gold"
          size="sm"
          class="music-memories__connections-more"
          @click="emit('open-connections')"
        >
          すべてのつながりを見る
        </UiButton>
      </section>
    </main>

    <footer class="music-memories__footer" role="contentinfo">
      <p class="music-memories__copyright">© {{ SITE_NAME }}</p>
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

.music-memories__brand-wrap {
  display: flex;
  align-items: center;
}

.music-memories__brand-wrap :deep(.mm-logo--full) {
  max-height: clamp(40px, 8vw, 56px);
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

.music-memories__connections {
  margin-bottom: clamp(40px, 7vw, 64px);
  text-align: center;
}

.music-memories__connections-eyebrow {
  margin: 0 0 12px;
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: var(--kin-400);
}

.music-memories__connections-title {
  margin: 0 0 12px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.3rem, 3.2vw, 1.75rem);
  letter-spacing: 0.08em;
}

.music-memories__connections-lead {
  margin: 0 auto 28px;
  max-width: 620px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.8;
  color: rgba(248, 244, 239, 0.68);
}

.music-memories__connections-more {
  display: flex;
  margin: 24px auto 0;
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

.music-memories__today-section {
  margin-bottom: clamp(40px, 7vw, 64px);
}

.music-memories__today {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
  gap: 0;
  overflow: hidden;
  border: 1px solid rgba(201, 169, 97, 0.28);
  border-radius: var(--site-radius-lg);
  background: linear-gradient(120deg, rgba(26, 20, 24, 0.55), rgba(122, 80, 136, 0.18));
}

.music-memories__today-visual {
  min-height: 220px;
  background: #1e161e;
  overflow: hidden;
}

.music-memories__today-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
  display: block;
  background: #1e161e;
}

.music-memories__today-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: clamp(24px, 4vw, 36px) clamp(22px, 4vw, 36px);
}

.music-memories__today-eyebrow {
  margin: 0 0 8px;
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: var(--kin-400);
}

.music-memories__today-title {
  margin: 0 0 18px;
  font-family: var(--ff-mincho);
  font-size: 1.35rem;
  letter-spacing: 0.08em;
}

.music-memories__today-en {
  margin: 0 0 4px;
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: rgba(201, 169, 97, 0.85);
}

.music-memories__today-name {
  margin: 0 0 10px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.5rem, 3vw, 1.85rem);
  letter-spacing: 0.06em;
}

.music-memories__today-headline {
  margin: 0 0 10px;
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  letter-spacing: 0.04em;
  color: rgba(248, 244, 239, 0.88);
}

.music-memories__today-blurb {
  margin: 0 0 20px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.85;
  color: rgba(248, 244, 239, 0.65);
}

.music-memories__today-cta {
  align-self: flex-start;
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

@media (max-width: 720px) {
  .music-memories__today {
    grid-template-columns: 1fr;
  }

  .music-memories__today-visual {
    aspect-ratio: 16 / 10;
    min-height: 0;
  }
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
