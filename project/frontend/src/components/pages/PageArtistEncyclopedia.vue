<script setup>
/**
 * ページ: Music Memories アーティスト図鑑
 * 役割: 参加中・準備中アーティストを検索・絞り込みで探す図鑑
 */
import { computed, ref } from 'vue'
import UiButton from '../ui/UiButton.vue'
import UiIco from '../ui/UiIco.vue'
import MusicMemoriesArtistCard from './music-memories/MusicMemoriesArtistCard.vue'
import {
  MUSIC_MEMORIES_ARTISTS,
  ARTIST_ENCYCLOPEDIA_DECADES,
  ARTIST_ENCYCLOPEDIA_GENDERS,
  ARTIST_ENCYCLOPEDIA_STATUSES,
  ARTIST_ENCYCLOPEDIA_SORTS,
  decadeLabel,
  genderLabel,
  statusLabel,
} from '../../data/musicMemoriesData.js'
import { SITE_NAME } from '../../constants/site.js'

const emit = defineEmits(['enter-site'])

const query = ref('')
const decade = ref('all')
const gender = ref('all')
const status = ref('all')
const sort = ref('featured')

const totalCount = MUSIC_MEMORIES_ARTISTS.length

const filteredArtists = computed(() => {
  const q = query.value.trim().toLowerCase()
  let list = MUSIC_MEMORIES_ARTISTS.filter((artist) => {
    const matchName =
      !q ||
      artist.name.toLowerCase().includes(q) ||
      artist.nameEn.toLowerCase().includes(q)

    const matchDecade =
      decade.value === 'all' ||
      (artist.activeDecades || []).includes(Number(decade.value))

    const matchGender = gender.value === 'all' || artist.gender === gender.value
    const matchStatus = status.value === 'all' || artist.status === status.value

    return matchName && matchDecade && matchGender && matchStatus
  })

  const sorted = [...list]
  if (sort.value === 'name') {
    sorted.sort((a, b) => a.name.localeCompare(b.name, 'ja'))
  } else if (sort.value === 'year-asc') {
    sorted.sort((a, b) => (a.activeStartYear || 0) - (b.activeStartYear || 0))
  } else if (sort.value === 'year-desc') {
    sorted.sort((a, b) => (b.activeStartYear || 0) - (a.activeStartYear || 0))
  } else {
    sorted.sort((a, b) => (a.featuredOrder || 99) - (b.featuredOrder || 99))
  }
  return sorted
})

const activeFilters = computed(() => {
  const tags = []
  if (decade.value !== 'all') {
    tags.push({
      key: 'decade',
      label: decadeLabel(Number(decade.value)),
      clear: () => { decade.value = 'all' },
    })
  }
  if (gender.value !== 'all') {
    tags.push({
      key: 'gender',
      label: genderLabel(gender.value),
      clear: () => { gender.value = 'all' },
    })
  }
  if (status.value !== 'all') {
    tags.push({
      key: 'status',
      label: statusLabel(status.value),
      clear: () => { status.value = 'all' },
    })
  }
  if (sort.value !== 'featured') {
    const sortOpt = ARTIST_ENCYCLOPEDIA_SORTS.find((s) => s.value === sort.value)
    if (sortOpt) {
      tags.push({
        key: 'sort',
        label: sortOpt.label,
        clear: () => { sort.value = 'featured' },
      })
    }
  }
  if (query.value.trim()) {
    tags.push({
      key: 'query',
      label: `「${query.value.trim()}」`,
      clear: () => { query.value = '' },
    })
  }
  return tags
})

function resetFilters() {
  query.value = ''
  decade.value = 'all'
  gender.value = 'all'
  status.value = 'all'
  sort.value = 'featured'
}
</script>

<template>
  <div class="artist-encyc">
    <main id="main-content" class="artist-encyc__main">
      <header class="artist-encyc__hero">
        <p class="artist-encyc__eyebrow">ARTIST ENCYCLOPEDIA</p>
        <h1 class="artist-encyc__title">アーティスト図鑑</h1>
        <p class="artist-encyc__lead">
          時代を彩ったレジェンドたち。<br />
          名前や年代から、あなたの記憶に残るアーティストを探してみましょう。
        </p>
      </header>

      <section class="artist-encyc__filters" aria-label="検索・絞り込み">
        <div class="artist-encyc__filter-grid">
          <label class="artist-encyc__field artist-encyc__field--search">
            <span class="artist-encyc__label">名前検索</span>
            <span class="artist-encyc__search-wrap">
              <UiIco name="search" :size="15" color="rgba(201, 169, 97, 0.85)" class="artist-encyc__search-ico" />
              <input
                v-model="query"
                type="search"
                class="artist-encyc__input"
                placeholder="アーティスト名を入力"
                autocomplete="off"
                aria-label="アーティスト名を入力"
              />
            </span>
          </label>

          <label class="artist-encyc__field">
            <span class="artist-encyc__label">活動年代</span>
            <select v-model="decade" class="artist-encyc__select" aria-label="活動年代">
              <option
                v-for="opt in ARTIST_ENCYCLOPEDIA_DECADES"
                :key="String(opt.value)"
                :value="opt.value"
              >
                {{ opt.label }}
              </option>
            </select>
          </label>

          <label class="artist-encyc__field">
            <span class="artist-encyc__label">性別</span>
            <select v-model="gender" class="artist-encyc__select" aria-label="性別">
              <option
                v-for="opt in ARTIST_ENCYCLOPEDIA_GENDERS"
                :key="opt.value"
                :value="opt.value"
              >
                {{ opt.label }}
              </option>
            </select>
          </label>

          <label class="artist-encyc__field">
            <span class="artist-encyc__label">公開状態</span>
            <select v-model="status" class="artist-encyc__select" aria-label="公開状態">
              <option
                v-for="opt in ARTIST_ENCYCLOPEDIA_STATUSES"
                :key="opt.value"
                :value="opt.value"
              >
                {{ opt.label }}
              </option>
            </select>
          </label>

          <label class="artist-encyc__field">
            <span class="artist-encyc__label">並び順</span>
            <select v-model="sort" class="artist-encyc__select" aria-label="並び順">
              <option
                v-for="opt in ARTIST_ENCYCLOPEDIA_SORTS"
                :key="opt.value"
                :value="opt.value"
              >
                {{ opt.label }}
              </option>
            </select>
          </label>
        </div>

        <div class="artist-encyc__filter-actions">
          <UiButton variant="outline" size="sm" @click="resetFilters">
            条件をリセット
          </UiButton>
        </div>
      </section>

      <div class="artist-encyc__summary" aria-live="polite">
        <p class="artist-encyc__counts">
          <span>掲載アーティスト {{ totalCount }}名</span>
          <span class="artist-encyc__counts-sep" aria-hidden="true">·</span>
          <span>検索結果 {{ filteredArtists.length }}名</span>
        </p>
        <ul v-if="activeFilters.length" class="artist-encyc__tags" aria-label="適用中の条件">
          <li v-for="tag in activeFilters" :key="tag.key">
            <button
              type="button"
              class="artist-encyc__tag"
              :aria-label="tag.label + 'の条件を解除'"
              @click="tag.clear()"
            >
              <span>{{ tag.label }}</span>
              <span class="artist-encyc__tag-x" aria-hidden="true">×</span>
            </button>
          </li>
        </ul>
      </div>

      <section class="artist-encyc__grid-section" aria-label="アーティスト一覧">
        <div v-if="filteredArtists.length === 0" class="artist-encyc__empty" role="status">
          <h2 class="artist-encyc__empty-title">該当するアーティストが見つかりませんでした</h2>
          <p class="artist-encyc__empty-desc">
            検索条件を変更するか、条件をリセットしてもう一度お試しください。
          </p>
          <UiButton variant="gold" size="md" @click="resetFilters">
            条件をリセット
          </UiButton>
        </div>

        <ul v-else class="artist-encyc__grid">
          <li
            v-for="artist in filteredArtists"
            :key="artist.id"
            class="artist-encyc__card-wrap"
          >
            <MusicMemoriesArtistCard
              :artist="artist"
              show-meta
              @enter-site="(siteId) => emit('enter-site', siteId)"
            />
          </li>
        </ul>
      </section>
    </main>

    <footer class="artist-encyc__footer" role="contentinfo">
      <p class="artist-encyc__copyright">© {{ SITE_NAME }}</p>
    </footer>
  </div>
</template>

<style scoped>
.artist-encyc {
  min-height: calc(100vh - 72px);
  display: flex;
  flex-direction: column;
  background:
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(122, 80, 136, 0.14), transparent 55%),
    linear-gradient(180deg, #1a1418 0%, #231b22 42%, #2a2228 100%);
  color: #f8f4ef;
}

.artist-encyc__main {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: clamp(32px, 6vw, 56px) 24px 64px;
  box-sizing: border-box;
}

.artist-encyc__hero {
  text-align: center;
  margin-bottom: clamp(28px, 5vw, 40px);
}

.artist-encyc__eyebrow {
  margin: 0 0 16px;
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: var(--kin-400);
}

.artist-encyc__title {
  margin: 0 0 16px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.75rem, 5vw, 2.5rem);
  font-weight: 600;
  line-height: 1.4;
  letter-spacing: 0.08em;
}

.artist-encyc__lead {
  margin: 0 auto;
  max-width: 560px;
  font-family: var(--ff-sans-jp);
  font-size: clamp(0.9rem, 2vw, 1rem);
  line-height: 1.9;
  color: rgba(248, 244, 239, 0.72);
}

.artist-encyc__filters {
  margin-bottom: 24px;
  padding: 22px 22px 18px;
  border: 1px solid rgba(201, 169, 97, 0.28);
  border-radius: var(--site-radius-lg);
  background: linear-gradient(135deg, rgba(122, 80, 136, 0.16), rgba(26, 20, 24, 0.45));
}

.artist-encyc__filter-grid {
  display: grid;
  grid-template-columns: 1.4fr repeat(4, minmax(0, 1fr));
  gap: 14px 16px;
}

.artist-encyc__field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
}

.artist-encyc__label {
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  letter-spacing: 0.1em;
  color: rgba(248, 244, 239, 0.6);
}

.artist-encyc__search-wrap {
  position: relative;
  display: block;
}

.artist-encyc__search-ico {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
}

.artist-encyc__input,
.artist-encyc__select {
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

.artist-encyc__input {
  padding-left: 36px;
}

.artist-encyc__input::placeholder {
  color: rgba(248, 244, 239, 0.4);
}

.artist-encyc__input:focus,
.artist-encyc__select:focus {
  outline: 2px solid rgba(201, 169, 97, 0.55);
  outline-offset: 1px;
  border-color: rgba(201, 169, 97, 0.45);
}

.artist-encyc__select option {
  color: #231b22;
  background: #f8f4ef;
}

.artist-encyc__filter-actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.artist-encyc__filter-actions :deep(.ui-btn) {
  border-color: rgba(201, 169, 97, 0.4);
  color: rgba(248, 244, 239, 0.85);
  background: transparent;
}

.artist-encyc__summary {
  margin-bottom: 22px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.artist-encyc__counts {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  letter-spacing: 0.04em;
  color: rgba(248, 244, 239, 0.7);
}

.artist-encyc__counts-sep {
  margin: 0 8px;
  opacity: 0.45;
}

.artist-encyc__tags {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.artist-encyc__tag {
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

.artist-encyc__tag:hover {
  border-color: rgba(201, 169, 97, 0.55);
  background: rgba(201, 169, 97, 0.18);
}

.artist-encyc__tag-x {
  font-size: 13px;
  line-height: 1;
  opacity: 0.75;
}

.artist-encyc__grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.artist-encyc__card-wrap {
  min-width: 0;
}

.artist-encyc__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 14px;
  padding: clamp(48px, 10vw, 80px) 20px;
  border: 1px dashed rgba(255, 255, 255, 0.16);
  border-radius: var(--site-radius-lg);
  background: rgba(255, 255, 255, 0.03);
}

.artist-encyc__empty-title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 1.2rem;
  letter-spacing: 0.06em;
}

.artist-encyc__empty-desc {
  margin: 0 0 8px;
  max-width: 420px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.8;
  color: rgba(248, 244, 239, 0.65);
}

.artist-encyc__footer {
  padding: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  text-align: center;
}

.artist-encyc__copyright {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  color: rgba(248, 244, 239, 0.4);
  letter-spacing: 0.08em;
}

@media (max-width: 1024px) {
  .artist-encyc__filter-grid {
    grid-template-columns: 1fr 1fr;
  }

  .artist-encyc__field--search {
    grid-column: 1 / -1;
  }

  .artist-encyc__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .artist-encyc__main {
    padding: 28px 16px 48px;
  }

  .artist-encyc__filter-grid {
    grid-template-columns: 1fr;
  }

  .artist-encyc__field--search {
    grid-column: auto;
  }

  .artist-encyc__filter-actions {
    justify-content: stretch;
  }

  .artist-encyc__filter-actions :deep(.ui-btn) {
    width: 100%;
  }

  .artist-encyc__grid {
    grid-template-columns: 1fr;
  }
}
</style>
