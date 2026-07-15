<script setup>
/**
 * 部品名: アーティスト間の曲の繋がりボード
 * 役割: 美空ひばりの楽曲を起点に、同じ作詞家・作曲家が手がけた他アーティストの
 *       楽曲へ辿るハブ図を、起点曲タブ切り替え式で紹介する
 */
import { computed, ref, watch } from 'vue'
import UiButton from '../ui/UiButton.vue'
import UiIco from '../ui/UiIco.vue'
import { MUSIC_MEMORIES_ARTISTS } from '../../data/musicMemoriesData.js'

const props = defineProps({
  connections: { type: Array, required: true },
})

const emit = defineEmits(['enter-site'])

const query = ref('')
const role = ref('all')
const sort = ref('featured')

const activeConnectionId = ref(null)

const SORT_LABELS = {
  'year-asc': '年代が古い順',
  'year-desc': '年代が新しい順',
  name: '作家名順',
}

function artistInfo(artistId) {
  return MUSIC_MEMORIES_ARTISTS.find((artist) => artist.id === artistId)
}

function connectionMatchesQuery(connection, q) {
  if (!q) return true
  const haystack = [
    connection.creator,
    connection.originSong.title,
    connection.originSong.lyric,
    connection.originSong.music,
    artistInfo(connection.originSong.artistId)?.name,
    ...connection.targetSongs.flatMap((song) => [
      song.title,
      song.lyric,
      song.music,
      artistInfo(song.artistId)?.name,
    ]),
  ]
  return haystack.some((value) => value && value.toLowerCase().includes(q))
}

const filteredConnections = computed(() => {
  const q = query.value.trim().toLowerCase()
  const list = props.connections.filter((connection) => {
    const matchQuery = connectionMatchesQuery(connection, q)
    const matchRole = role.value === 'all' || connection.creatorRole === role.value
    return matchQuery && matchRole
  })

  const sorted = [...list]
  if (sort.value === 'year-asc') {
    sorted.sort((a, b) => a.originSong.year - b.originSong.year)
  } else if (sort.value === 'year-desc') {
    sorted.sort((a, b) => b.originSong.year - a.originSong.year)
  } else if (sort.value === 'name') {
    sorted.sort((a, b) => a.creator.localeCompare(b.creator, 'ja'))
  } else {
    sorted.sort((a, b) => (b.featured ? 1 : 0) - (a.featured ? 1 : 0))
  }
  return sorted
})

const activeFilters = computed(() => {
  const tags = []
  if (role.value !== 'all') {
    tags.push({ key: 'role', label: role.value, clear: () => { role.value = 'all' } })
  }
  if (sort.value !== 'featured') {
    tags.push({ key: 'sort', label: SORT_LABELS[sort.value], clear: () => { sort.value = 'featured' } })
  }
  if (query.value.trim()) {
    tags.push({ key: 'query', label: `「${query.value.trim()}」`, clear: () => { query.value = '' } })
  }
  return tags
})

function resetFilters() {
  query.value = ''
  role.value = 'all'
  sort.value = 'featured'
}

watch(filteredConnections, (list) => {
  if (activeConnectionId.value && !list.some((connection) => connection.id === activeConnectionId.value)) {
    activeConnectionId.value = null
  }
})

const activeConnection = computed(
  () => filteredConnections.value.find((connection) => connection.id === activeConnectionId.value) ?? null
)

function selectConnection(id) {
  activeConnectionId.value = id
}

function onArtistNav(artistId) {
  emit('enter-site', artistId)
}
</script>

<template>
  <div class="mc-board">
    <section class="mc-board__filters" aria-label="つながりを検索・絞り込み">
      <div class="mc-board__filter-grid">
        <label class="mc-board__field mc-board__field--search">
          <span class="mc-board__label">名前検索</span>
          <span class="mc-board__search-wrap">
            <UiIco name="search" :size="15" color="rgba(201, 169, 97, 0.85)" class="mc-board__search-ico" />
            <input
              v-model="query"
              type="search"
              class="mc-board__input"
              placeholder="曲名・作詞家・作曲家・アーティスト名"
              autocomplete="off"
              aria-label="曲名・作詞家・作曲家・アーティスト名で検索"
            />
          </span>
        </label>

        <label class="mc-board__field">
          <span class="mc-board__label">役割</span>
          <select v-model="role" class="mc-board__select" aria-label="役割">
            <option value="all">すべて</option>
            <option value="作詞家">作詞家</option>
            <option value="作曲家">作曲家</option>
          </select>
        </label>

        <label class="mc-board__field">
          <span class="mc-board__label">並び順</span>
          <select v-model="sort" class="mc-board__select" aria-label="並び順">
            <option value="featured">おすすめ順</option>
            <option value="year-asc">年代が古い順</option>
            <option value="year-desc">年代が新しい順</option>
            <option value="name">作家名順</option>
          </select>
        </label>
      </div>

      <div class="mc-board__filter-actions">
        <UiButton variant="outline" size="sm" @click="resetFilters">
          条件をリセット
        </UiButton>
      </div>
    </section>

    <div class="mc-board__summary" aria-live="polite">
      <p class="mc-board__counts">
        <span>全{{ connections.length }}件のつながり</span>
        <span class="mc-board__counts-sep" aria-hidden="true">·</span>
        <span>検索結果 {{ filteredConnections.length }}件</span>
      </p>
      <ul v-if="activeFilters.length" class="mc-board__tags" aria-label="適用中の条件">
        <li v-for="tag in activeFilters" :key="tag.key">
          <button
            type="button"
            class="mc-board__tag"
            :aria-label="tag.label + 'の条件を解除'"
            @click="tag.clear()"
          >
            <span>{{ tag.label }}</span>
            <span class="mc-board__tag-x" aria-hidden="true">×</span>
          </button>
        </li>
      </ul>
    </div>

    <div v-if="!filteredConnections.length" class="mc-board__empty" role="status">
      <p class="mc-board__empty-title">該当するつながりが見つかりませんでした</p>
      <p class="mc-board__empty-desc">
        検索条件を変更するか、条件をリセットしてもう一度お試しください。
      </p>
      <UiButton variant="gold" size="sm" @click="resetFilters">条件をリセット</UiButton>
    </div>

    <template v-else>
      <ul class="mc-board__list">
        <li v-for="connection in filteredConnections" :key="connection.id">
          <button
            type="button"
            class="mc-board__list-item"
            :class="{ 'mc-board__list-item--active': connection.id === activeConnection?.id }"
            @click="selectConnection(connection.id)"
          >
            <span class="mc-board__list-song">{{ connection.originSong.title }}</span>
            <span class="mc-board__list-meta">
              {{ connection.creatorRole }}：{{ connection.creator }} · 他{{ connection.targetSongs.length }}曲
            </span>
          </button>
        </li>
      </ul>

      <p v-if="!activeConnection" class="mc-board__hint">
        曲を選択すると、つながりの詳細が表示されます
      </p>

      <template v-else>
      <div class="mc-board__panel">
        <aside class="mc-board__creator">
          <div class="mc-board__creator-photo">
            <img
              v-if="activeConnection.creatorImage"
              :src="activeConnection.creatorImage"
              :alt="activeConnection.creator"
              loading="lazy"
              decoding="async"
            />
            <span v-else class="mc-board__creator-photo-fallback" aria-hidden="true">
              {{ activeConnection.creator.charAt(0) }}
            </span>
          </div>
          <p class="mc-board__creator-role">{{ activeConnection.creatorRole }}</p>
          <h3 class="mc-board__creator-name">{{ activeConnection.creator }}</h3>
          <p v-if="activeConnection.creatorYears" class="mc-board__creator-years">{{ activeConnection.creatorYears }}</p>
          <p v-if="activeConnection.creatorBio" class="mc-board__creator-bio">{{ activeConnection.creatorBio }}</p>
        </aside>

        <div class="mc-board__songs-panel">
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
      </div>

      <p v-if="activeConnection.note" class="mc-board__note">
        {{ activeConnection.note }}
      </p>
      </template>
    </template>
  </div>
</template>

<style scoped>
.mc-board {
  padding: clamp(20px, 4vw, 32px);
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.mc-board__filters {
  padding: 22px 22px 18px;
  border: 1px solid rgba(201, 169, 97, 0.28);
  border-radius: var(--site-radius-lg);
  background: linear-gradient(135deg, rgba(122, 80, 136, 0.16), rgba(26, 20, 24, 0.45));
}

.mc-board__filter-grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr 1fr;
  gap: 14px 16px;
}

.mc-board__field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
}

.mc-board__label {
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  letter-spacing: 0.1em;
  color: rgba(248, 244, 239, 0.6);
}

.mc-board__search-wrap {
  position: relative;
  display: block;
}

.mc-board__search-ico {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
}

.mc-board__input,
.mc-board__select {
  width: 100%;
  box-sizing: border-box;
  min-height: 42px;
  padding: 10px 12px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: var(--site-radius-md);
  background: rgba(255, 255, 255, 0.06);
  color: #f8f4ef;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
}

.mc-board__input {
  padding-left: 36px;
}

.mc-board__input::placeholder {
  color: rgba(248, 244, 239, 0.4);
}

.mc-board__input:focus,
.mc-board__select:focus {
  outline: 2px solid rgba(201, 169, 97, 0.55);
  outline-offset: 1px;
  border-color: rgba(201, 169, 97, 0.45);
}

.mc-board__select option {
  color: #231b22;
  background: #f8f4ef;
}

.mc-board__filter-actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.mc-board__filter-actions :deep(.ui-btn) {
  border-color: rgba(201, 169, 97, 0.4);
  color: rgba(248, 244, 239, 0.85);
  background: transparent;
}

.mc-board__summary {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.mc-board__counts {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  letter-spacing: 0.04em;
  color: rgba(248, 244, 239, 0.7);
}

.mc-board__counts-sep {
  margin: 0 8px;
  opacity: 0.45;
}

.mc-board__tags {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.mc-board__tag {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 5px 10px;
  border-radius: 999px;
  border: 1px solid rgba(201, 169, 97, 0.35);
  background: rgba(201, 169, 97, 0.1);
  color: #f8f4ef;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  letter-spacing: 0.06em;
  cursor: pointer;
}

.mc-board__tag:hover {
  border-color: rgba(201, 169, 97, 0.55);
  background: rgba(201, 169, 97, 0.18);
}

.mc-board__tag-x {
  font-size: 13px;
  line-height: 1;
  opacity: 0.75;
}

.mc-board__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 14px;
  padding: clamp(40px, 8vw, 64px) 20px;
  border: 1px dashed rgba(255, 255, 255, 0.16);
  border-radius: var(--site-radius-lg);
  background: rgba(255, 255, 255, 0.03);
}

.mc-board__empty-title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 1.05rem;
  letter-spacing: 0.06em;
}

.mc-board__empty-desc {
  margin: 0 0 8px;
  max-width: 420px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.8;
  color: rgba(248, 244, 239, 0.65);
}

.mc-board__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  justify-content: center;
  gap: 8px;
}

.mc-board__list > li {
  min-width: 0;
}

.mc-board__list-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
  padding: 10px 16px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(255, 255, 255, 0.03);
  color: rgba(248, 244, 239, 0.8);
  font-family: var(--ff-sans-jp);
  cursor: pointer;
  text-align: left;
  transition: border-color 0.2s, color 0.2s, background 0.2s;
}

.mc-board__list-item:hover {
  border-color: rgba(201, 169, 97, 0.5);
  color: #f8f4ef;
}

.mc-board__list-item--active {
  border-color: var(--kin-400);
  background: rgba(201, 169, 97, 0.16);
  color: var(--kin-400);
}

.mc-board__list-song {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.03em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.mc-board__list-meta {
  font-size: 10.5px;
  letter-spacing: 0.03em;
  color: rgba(248, 244, 239, 0.5);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.mc-board__list-item--active .mc-board__list-meta {
  color: rgba(217, 189, 125, 0.75);
}

.mc-board__hint {
  margin: 0;
  padding: clamp(32px, 6vw, 48px) 20px;
  text-align: center;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  color: rgba(248, 244, 239, 0.5);
  border: 1px dashed rgba(255, 255, 255, 0.16);
  border-radius: var(--site-radius-lg);
}

.mc-board__panel {
  display: grid;
  grid-template-columns: minmax(200px, 260px) 1fr;
  gap: clamp(20px, 3vw, 32px);
  padding: clamp(20px, 3vw, 28px);
  border: 1px solid rgba(201, 169, 97, 0.28);
  border-radius: var(--site-radius-lg);
  background: linear-gradient(160deg, rgba(122, 80, 136, 0.12), rgba(26, 20, 24, 0.5));
}

.mc-board__creator {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 6px;
  padding-right: clamp(16px, 3vw, 24px);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.mc-board__creator-photo {
  width: 112px;
  height: 112px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid rgba(201, 169, 97, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(201, 169, 97, 0.12);
  margin-bottom: 8px;
  flex-shrink: 0;
}

.mc-board__creator-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
}

.mc-board__creator-photo-fallback {
  font-family: var(--ff-mincho);
  font-size: 2.25rem;
  color: var(--kin-400);
}

.mc-board__creator-role {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  letter-spacing: 0.1em;
  color: var(--kin-400);
}

.mc-board__creator-name {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 1.35rem;
  letter-spacing: 0.06em;
  color: #f8f4ef;
}

.mc-board__creator-years {
  margin: 0;
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.04em;
  color: rgba(248, 244, 239, 0.5);
}

.mc-board__creator-bio {
  margin: 10px 0 0;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  line-height: 1.8;
  color: rgba(248, 244, 239, 0.72);
  text-align: left;
}

.mc-board__songs-panel {
  display: flex;
  flex-direction: column;
  gap: 22px;
  min-width: 0;
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

.mc-board__note {
  margin: 0;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  line-height: 1.8;
  color: rgba(248, 244, 239, 0.7);
}

@media (max-width: 720px) {
  .mc-board__filter-grid {
    grid-template-columns: 1fr;
  }

  .mc-board__filter-actions :deep(.ui-btn) {
    width: 100%;
  }

  .mc-board__panel {
    grid-template-columns: 1fr;
  }

  .mc-board__creator {
    padding-right: 0;
    padding-bottom: 20px;
    border-right: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .mc-board__songs {
    max-height: none;
    overflow-y: visible;
  }
}
</style>
