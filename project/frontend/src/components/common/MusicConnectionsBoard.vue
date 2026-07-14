<script setup>
/**
 * 部品名: アーティスト間の曲の繋がりボード
 * 役割: 同じ作詞家・作曲家が手がけた楽曲を、作家タブ切り替え式のハブ図で紹介する
 */
import { computed, ref, watch } from 'vue'
import UiButton from '../ui/UiButton.vue'
import { MUSIC_MEMORIES_ARTISTS } from '../../data/musicMemoriesData.js'

const props = defineProps({
  connections: { type: Array, required: true },
})

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

const leftSongs = computed(() => activeConnection.value?.songs.filter((_, i) => i % 2 === 0) ?? [])
const rightSongs = computed(() => activeConnection.value?.songs.filter((_, i) => i % 2 === 1) ?? [])

function artistInfo(artistId) {
  return MUSIC_MEMORIES_ARTISTS.find((artist) => artist.id === artistId)
}

function selectConnection(id) {
  activeConnectionId.value = id
  showConnectionDetail.value = false
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
        {{ connection.creator }}
      </button>
    </div>

    <p class="mc-board__subtitle">
      音楽的なつながりを辿る：{{ activeConnection.creator }}の作品たち
    </p>

    <div class="mc-board__diagram">
      <ul class="mc-board__songs">
        <li
          v-for="song in leftSongs"
          :key="song.artistId + song.title"
          class="mc-board__song"
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
          </div>
        </li>
      </ul>

      <div class="mc-board__hub">
        <span class="mc-board__hub-mark" aria-hidden="true">縁</span>
        <p class="mc-board__hub-role">{{ activeConnection.role }}：{{ activeConnection.creator }}</p>
        <p class="mc-board__hub-desc">同じ{{ activeConnection.role }}が<br />手がけた楽曲たち</p>
      </div>

      <ul class="mc-board__songs">
        <li
          v-for="song in rightSongs"
          :key="song.artistId + song.title"
          class="mc-board__song"
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
          </div>
        </li>
      </ul>
    </div>

    <p v-if="showConnectionDetail" class="mc-board__note">
      {{ activeConnection.note }}
    </p>

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
  padding: 8px 18px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  background: transparent;
  color: rgba(248, 244, 239, 0.75);
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: border-color 0.25s, color 0.25s, background 0.25s;
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
  align-items: center;
}

.mc-board__songs {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.mc-board__song {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
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
}

.mc-board__song-title {
  margin: 0 0 4px;
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

.mc-board__note {
  margin: 20px 0 0;
  padding: 14px 18px;
  border-left: 2px solid var(--kin-400);
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
}
</style>
