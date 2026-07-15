<script setup>
/**
 * 部品名: ディスコグラフィ — 公式 PV 風カードエリア
 * 用途: YouTube 公式 PV のサムネイル表示と、クリック時の埋め込み再生（プレミアム PV は権限制御）
 */
import { ref } from 'vue'
import SectionTitle from '../../ui/SectionTitle.vue'
import UiIco from '../../ui/UiIco.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'
import { useMemberAccess } from '../../../composables/useMemberAccess.js'
import { aosAttrs } from '../../../lib/aos.js'

const items = HIBARU_DATA.featuredPv

const emit = defineEmits(['play', 'coming-soon', 'need-auth'])

const { canUse, isLoggedIn, PERMISSION } = useMemberAccess()

const PREMIUM_PV_IDS = new Set(['pv-002', 'pv-003'])
const playingId = ref(null)

function isPremiumPv(pv) {
  return PREMIUM_PV_IDS.has(pv.id)
}

function thumbUrl(youtubeId) {
  return `https://img.youtube.com/vi/${youtubeId}/hqdefault.jpg`
}

function embedUrl(youtubeId) {
  return `https://www.youtube-nocookie.com/embed/${youtubeId}?autoplay=1&rel=0`
}

function onClick(pv) {
  if (isPremiumPv(pv) && !canUse(PERMISSION.PREMIUM_VIDEO)) {
    emit('need-auth', isLoggedIn.value ? 'register-premium' : 'login')
    return
  }
  if (!pv.youtubeId) {
    emit('coming-soon')
    return
  }
  playingId.value = playingId.value === pv.id ? null : pv.id
  emit('play', pv)
}
</script>

<template>
  <section class="disco-pv" aria-label="公式 PV">
    <SectionTitle title="公式 PV" sub="Featured Music Videos" size="md" />

    <div class="disco-pv__grid">
      <article
        v-for="(pv, i) in items"
        :key="pv.id"
        class="disco-pv__card"
        :class="{ 'disco-pv__card--premium': isPremiumPv(pv) && !canUse(PERMISSION.PREMIUM_VIDEO) }"
        v-bind="aosAttrs(i * 80)"
      >
        <div class="disco-pv__media">
          <div v-if="playingId === pv.id && pv.youtubeId" class="disco-pv__embed">
            <iframe
              :src="embedUrl(pv.youtubeId)"
              :title="pv.title + ' の公式 PV'"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowfullscreen
              loading="lazy"
              referrerpolicy="strict-origin-when-cross-origin"
            />
          </div>
          <button
            v-else
            type="button"
            class="disco-pv__thumb"
            :aria-label="pv.title + 'の PV を見る'"
            @click="onClick(pv)"
          >
            <div v-if="!pv.youtubeId" class="disco-pv__placeholder">
              <UiIco name="play" :size="28" color="var(--murasaki-700)" />
              <span class="disco-pv__placeholder-text">準備中</span>
            </div>
            <img
              v-else
              :src="thumbUrl(pv.youtubeId)"
              :alt="pv.title"
              class="disco-pv__img"
              loading="lazy"
              decoding="async"
            />
            <span v-if="isPremiumPv(pv)" class="disco-pv__badge">プレミアム</span>
            <span v-if="pv.youtubeId" class="disco-pv__play" aria-hidden="true">
              <span class="disco-pv__play-btn">
                <UiIco name="play" :size="18" color="#fff" />
              </span>
            </span>
          </button>
        </div>
        <div class="disco-pv__body">
          <span class="disco-pv__year">{{ pv.year }}</span>
          <h3 class="disco-pv__title">{{ pv.title }}</h3>
          <p v-if="pv.note" class="disco-pv__note">{{ pv.note }}</p>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.disco-pv {
  margin-bottom: var(--sp-7);
}
.disco-pv__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--sp-4);
}
.disco-pv__card {
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
  overflow: hidden;
  text-align: left;
  transition: transform 0.2s, box-shadow 0.2s;
}
.disco-pv__card:hover {
  transform: translateY(-2px);
  box-shadow: var(--site-shadow-md);
}
.disco-pv__card--premium .disco-pv__thumb {
  filter: grayscale(0.35) brightness(0.9);
}
.disco-pv__media {
  position: relative;
  aspect-ratio: 16 / 9;
  background: linear-gradient(135deg, var(--site-bg-pink), var(--site-surface-muted));
  overflow: hidden;
}
.disco-pv__thumb {
  position: absolute;
  inset: 0;
  display: block;
  width: 100%;
  height: 100%;
  padding: 0;
  border: 0;
  cursor: pointer;
  background: transparent;
}
.disco-pv__embed {
  position: absolute;
  inset: 0;
}
.disco-pv__embed iframe {
  width: 100%;
  height: 100%;
  border: 0;
  display: block;
}
.disco-pv__placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 8px;
  background:
    radial-gradient(circle at center, rgba(93, 58, 107, 0.08) 0%, transparent 60%),
    linear-gradient(160deg, #f5ebe0, #fce8ec);
}
.disco-pv__placeholder-text {
  font-family: var(--ff-mincho);
  font-size: var(--font-size-caption);
  letter-spacing: 0.12em;
  color: var(--site-text-muted);
}
.disco-pv__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.disco-pv__badge {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 3px 8px;
  font-size: var(--font-size-badge);
  letter-spacing: 0.1em;
  color: #fff;
  background: var(--kin-600);
  border-radius: 4px;
  z-index: 1;
}
.disco-pv__play {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(40, 30, 25, 0.28);
  transition: background 0.2s;
}
.disco-pv__thumb:hover .disco-pv__play {
  background: rgba(40, 30, 25, 0.42);
}
.disco-pv__play-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(93, 58, 107, 0.85);
  border: 2px solid rgba(255, 255, 255, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.disco-pv__body {
  padding: var(--sp-4);
}
.disco-pv__year {
  font-family: var(--ff-mono);
  font-size: var(--font-size-badge);
  letter-spacing: 0.15em;
  color: var(--kin-600);
}
.disco-pv__title {
  margin: 6px 0 4px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-body);
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--site-text);
}
.disco-pv__note {
  margin: 0;
  font-size: var(--font-size-caption);
  line-height: 1.6;
  color: var(--site-text-muted);
}

@media (max-width: 900px) {
  .disco-pv__grid {
    grid-template-columns: 1fr;
  }
}
@media (min-width: 901px) and (max-width: 1100px) {
  .disco-pv__grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .disco-pv__card:last-child {
    grid-column: span 2;
    max-width: 50%;
    justify-self: center;
  }
}
</style>
