<script setup>
/**
 * ページ: アーティスト間の曲の繋がり (Cross-Artist Connections)
 * 役割: 同じ作詞家・作曲家がロースター内の複数アーティストに楽曲提供している
 *       実例を、ホームより詳しく網羅的に紹介する専用ページ
 */
import MusicConnectionsBoard from '../common/MusicConnectionsBoard.vue'
import { CROSS_ARTIST_CONNECTIONS } from '../../data/crossArtistConnections.js'

const emit = defineEmits(['enter-site'])
</script>

<template>
  <div class="music-connections">
    <main class="music-connections__main">
      <section class="music-connections__hero" aria-labelledby="mc-hero-title">
        <p class="music-connections__eyebrow">Cross-Artist Connections</p>
        <h1 id="mc-hero-title" class="music-connections__title">
          アーティスト間の曲の繋がり
        </h1>
        <p class="music-connections__lead">
          同じ作詞家・作曲家が手がけた楽曲をたどることで、複数のアーティストへの関心が自然に広がります。
          Music Memories に登場するレジェンドたちを繋ぐ、音楽的な糸をここでは詳しくご紹介します。
        </p>
      </section>

      <section class="music-connections__board-section" aria-label="作家別のつながり一覧">
        <MusicConnectionsBoard
          :connections="CROSS_ARTIST_CONNECTIONS"
          @enter-site="(artistId) => emit('enter-site', artistId)"
        />
      </section>
    </main>
  </div>
</template>

<style scoped>
.music-connections {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background:
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(122, 80, 136, 0.14), transparent 55%),
    linear-gradient(180deg, #1a1418 0%, #231b22 42%, #2a2228 100%);
  color: #f8f4ef;
}

.music-connections__main {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: clamp(40px, 8vw, 80px) 24px 64px;
}

.music-connections__hero {
  text-align: center;
  margin-bottom: clamp(40px, 7vw, 64px);
}

.music-connections__eyebrow {
  margin: 0 0 16px;
  font-family: var(--ff-latin);
  font-size: var(--font-size-caption);
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: var(--kin-400);
}

.music-connections__title {
  margin: 0 0 20px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.75rem, 5vw, 2.5rem);
  font-weight: 600;
  line-height: 1.45;
  letter-spacing: 0.06em;
}

.music-connections__lead {
  margin: 0 auto;
  max-width: 640px;
  font-family: var(--ff-sans-jp);
  font-size: clamp(0.9rem, 2vw, 1rem);
  line-height: 1.9;
  color: rgba(248, 244, 239, 0.72);
}
</style>
