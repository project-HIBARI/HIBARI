<script setup>
/**
 * 部品名: アーティスト間の曲の繋がりボード
 * 役割: 美空ひばりの楽曲を起点に、同じ作詞家・作曲家が手がけた他アーティストの
 *       楽曲へ辿るハブ図を、起点曲タブ切り替え式で紹介する
 */
import { computed, ref, watch } from 'vue'
import UiButton from '../ui/UiButton.vue'
import SongYearBar from './SongYearBar.vue'
import { MUSIC_MEMORIES_ARTISTS } from '../../data/musicMemoriesData.js'

const props = defineProps({
  connections: { type: Array, required: true },
})

const emit = defineEmits(['enter-site'])

const activeConnectionId = ref(props.connections[0]?.id ?? '')
const showConnectionDetail = ref(false)

watch(
  () => props.connections,
  (list) => {
    if (!list.some((connection) => connection.id === activeConnectionId.value)) {
      activeConnectionId.value = list[0]?.id ?? ''
      showConnectionDetail.value = false
    }
  }
)

const activeConnection = computed(
  () =>
    props.connections.find((connection) => connection.id === activeConnectionId.value) ??
    props.connections[0]
)

function artistInfo(artistId) {
  return MUSIC_MEMORIES_ARTISTS.find((artist) => artist.id === artistId)
}

function selectConnection(id) {
  activeConnectionId.value = id
  showConnectionDetail.value = false
}

function onArtistNav(artistId) {
  emit('enter-site', artistId)
}
</script>

<template>
  <div v-if="activeConnection" class="mc-board">
    <div class="mc-board__tabs" role="tablist">
      <button
        v-for="connection in connections"
        :key="connection.id"
        type="button"
        role="tab"
        class="mc-board__tab"
        :class="{ 'mc-board__tab--active': connection.id === activeConnection.id }"
        :aria-selected="connection.id === activeConnection.id"
        @click="selectConnection(connection.id)"
      >
        <span class="mc-board__tab-song">{{ connection.originSong.title }}</span>
        <span class="mc-board__tab-creator">{{ connection.creator }}</span>
      </button>
    </div>

    <p class="mc-board__subtitle">
      音楽的なつながりを辿る：「{{ activeConnection.originSong.title }}」（{{ activeConnection.creatorRole }}：{{ activeConnection.creator }}）から
    </p>

    <div class="mc-board__diagram">
      <div class="mc-board__column">
        <p class="mc-board__column-head mc-board__column-head--origin">起点となる楽曲：美空ひばり</p>
        <ul class="mc-board__songs mc-board__songs--origin">
          <li class="mc-board__song mc-board__song--origin">
            <img
              v-if="artistInfo(activeConnection.originSong.artistId)?.image"
              :src="artistInfo(activeConnection.originSong.artistId).image"
              :alt="artistInfo(activeConnection.originSong.artistId).name"
              class="mc-board__song-image"
              loading="lazy"
              decoding="async"
            />
            <div class="mc-board__song-body">
              <p class="mc-board__song-title">
                {{ artistInfo(activeConnection.originSong.artistId)?.name }} - {{ activeConnection.originSong.title }} ({{ activeConnection.originSong.year }})
              </p>
              <p class="mc-board__song-credit">
                [作詞：{{ activeConnection.originSong.lyric }} ／ 作曲：{{ activeConnection.originSong.music }}]
              </p>
              <SongYearBar :year="activeConnection.originSong.year" class="mc-board__song-year" />
              <UiButton
                v-if="artistInfo(activeConnection.originSong.artistId)?.status === 'open'"
                variant="gold"
                size="sm"
                class="mc-board__song-cta"
                @click="onArtistNav(activeConnection.originSong.artistId)"
              >
                → このアーティストを見る
              </UiButton>
              <span v-else class="mc-board__song-badge">準備中</span>
            </div>
          </li>
        </ul>
      </div>

      <div class="mc-board__hub">
        <span class="mc-board__hub-mark" aria-hidden="true">縁</span>
        <p class="mc-board__hub-role">{{ activeConnection.creatorRole }}：{{ activeConnection.creator }}</p>
        <p class="mc-board__hub-desc">同じ{{ activeConnection.creatorRole }}が<br />手がけた楽曲たち</p>
      </div>

      <div class="mc-board__column">
        <p class="mc-board__column-head mc-board__column-head--target">
          同じ{{ activeConnection.creatorRole }}でつながる楽曲
        </p>
        <ul class="mc-board__songs mc-board__songs--target">
          <li
            v-for="song in activeConnection.targetSongs"
            :key="song.artistId + song.title"
            class="mc-board__song mc-board__song--target"
          >
            <img
              v-if="artistInfo(song.artistId)?.image"
              :src="artistInfo(song.artistId).image"
              :alt="artistInfo(song.artistId).name"
              class="mc-board__song-image"
              loading="lazy"
              decoding="async"
            />
            <div class="mc-board__song-body">
              <p class="mc-board__song-title">
                {{ artistInfo(song.artistId)?.name }} - {{ song.title }} ({{ song.year }})
              </p>
              <p class="mc-board__song-credit">
                [作詞：{{ song.lyric }} ／ 作曲：{{ song.music }}]
              </p>
              <SongYearBar :year="song.year" class="mc-board__song-year" />
              <UiButton
                v-if="artistInfo(song.artistId)?.status === 'open'"
                variant="gold"
                size="sm"
                class="mc-board__song-cta"
                @click="onArtistNav(song.artistId)"
              >
                → このアーティストを見る
              </UiButton>
              <span v-else class="mc-board__song-badge">準備中</span>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <div v-if="showConnectionDetail" class="mc-board__detail">
      <h3 class="mc-board__detail-title">
        {{ activeConnection.creator }} が繋いだ楽曲一覧
      </h3>
      <ul class="mc-board__detail-list">
        <li
          v-for="song in activeConnection.targetSongs"
          :key="'detail-' + song.artistId + song.title"
          class="mc-board__detail-item"
        >
          <span class="mc-board__detail-pair">
            {{ activeConnection.creator }} × {{ artistInfo(song.artistId)?.name }}
          </span>
          <span class="mc-board__detail-song">{{ song.title }}（{{ song.year }}）</span>
        </li>
      </ul>
      <p class="mc-board__note">
        {{ activeConnection.note }}
      </p>
    </div>

    <UiButton
      variant="gold"
      size="md"
      class="mc-board__cta"
      @click="showConnectionDetail = !showConnectionDetail"
    >
      {{ showConnectionDetail ? '閉じる' : 'つながりを詳しく見る' }}
    </UiButton>
  </div>
</template>

<style scoped>
.mc-board {
  padding: clamp(20px, 4vw, 32px);
  border: 1px solid rgba(201, 169, 97, 0.35);
  border-radius: var(--site-radius-lg);
  background: linear-gradient(180deg, rgba(122, 80, 136, 0.1), rgba(26, 20, 24, 0.4));
  text-align: left;
}

.mc-board__tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin-bottom: 20px;
}

.mc-board__tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 8px 18px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  background: transparent;
  color: rgba(248, 244, 239, 0.75);
  font-family: var(--ff-sans-jp);
  cursor: pointer;
  transition: border-color 0.25s, color 0.25s, background 0.25s;
}

.mc-board__tab-song {
  font-size: 13px;
  letter-spacing: 0.05em;
}

.mc-board__tab-creator {
  font-size: 10px;
  letter-spacing: 0.05em;
  color: rgba(248, 244, 239, 0.5);
}

.mc-board__tab:hover {
  border-color: rgba(201, 169, 97, 0.5);
  color: #f8f4ef;
}

.mc-board__tab--active {
  border-color: var(--kin-400);
  background: rgba(201, 169, 97, 0.18);
  color: var(--kin-400);
}

.mc-board__tab--active .mc-board__tab-creator {
  color: rgba(217, 189, 125, 0.75);
}

.mc-board__subtitle {
  margin: 0 0 24px;
  text-align: center;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  letter-spacing: 0.06em;
  color: rgba(248, 244, 239, 0.6);
}

.mc-board__diagram {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 20px;
  align-items: start;
}

.mc-board__column {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 0;
}

.mc-board__column-head {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  letter-spacing: 0.08em;
  font-weight: 600;
}

.mc-board__column-head--origin {
  color: var(--kin-400);
}

.mc-board__column-head--target {
  color: var(--murasaki-400);
}

.mc-board__songs {
  list-style: none;
  margin: 0;
  padding: 0 4px 0 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
  max-height: 360px;
  overflow-y: auto;
}

.mc-board__song {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 14px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-left-width: 3px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
}

.mc-board__song--origin {
  border-left-color: var(--kin-400);
}

.mc-board__song--target {
  border-left-color: var(--murasaki-400);
}

.mc-board__song-image {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
  object-position: center top;
  flex-shrink: 0;
}

.mc-board__song-body {
  min-width: 0;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.mc-board__song-title {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  color: #f8f4ef;
}

.mc-board__song-credit {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  color: rgba(248, 244, 239, 0.55);
}

.mc-board__song-year {
  margin: 2px 0;
}

.mc-board__song-cta {
  align-self: flex-start;
}

.mc-board__song-badge {
  align-self: flex-start;
  display: inline-flex;
  padding: 4px 12px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  font-family: var(--ff-sans-jp);
  font-size: 10px;
  letter-spacing: 0.1em;
  color: rgba(248, 244, 239, 0.5);
}

.mc-board__hub {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 20px;
  min-width: 140px;
  border: 1px solid rgba(201, 169, 97, 0.45);
  border-radius: var(--site-radius-lg);
  background: rgba(201, 169, 97, 0.08);
  text-align: center;
}

.mc-board__hub-mark {
  font-family: var(--ff-mincho);
  font-size: 1.5rem;
  color: var(--kin-400);
}

.mc-board__hub-role {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 0.95rem;
  color: #f8f4ef;
}

.mc-board__hub-desc {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  line-height: 1.6;
  color: rgba(248, 244, 239, 0.6);
}

.mc-board__detail {
  margin-top: 20px;
  padding: 16px 18px;
  border-left: 2px solid var(--kin-400);
}

.mc-board__detail-title {
  margin: 0 0 12px;
  font-family: var(--ff-mincho);
  font-size: 0.9rem;
  color: #f8f4ef;
}

.mc-board__detail-list {
  list-style: none;
  margin: 0 0 14px;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.mc-board__detail-item {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 8px;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
}

.mc-board__detail-pair {
  color: var(--kin-400);
  font-weight: 600;
}

.mc-board__detail-song {
  color: rgba(248, 244, 239, 0.75);
}

.mc-board__note {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  line-height: 1.8;
  color: rgba(248, 244, 239, 0.7);
}

.mc-board__cta {
  display: flex;
  margin: 24px auto 0;
}

@media (max-width: 720px) {
  .mc-board__diagram {
    grid-template-columns: 1fr;
  }

  .mc-board__hub {
    order: -1;
  }

  .mc-board__songs {
    max-height: none;
    overflow-y: visible;
  }
}
</style>
