<script setup>
/**
 * 部品名: ホーム — ビデオプロモーション
 * 用途: ヒーロー中央に特別映像を表示する
 */
import { ref } from 'vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const promo = HIBARU_DATA.homePromoVideo

const videoRef = ref(null)
const isPlaying = ref(false)

function playVideo() {
  const el = videoRef.value
  if (!el) return
  el.scrollIntoView({ behavior: 'smooth', block: 'center' })
  el.play().catch(() => {})
}
</script>

<template>
  <div class="home-promo" aria-label="ビデオプロモーション">
    <span class="home-promo__label">{{ promo.label }}</span>
    <h2 class="home-promo__title">{{ promo.title }}</h2>
    <p class="home-promo__desc">{{ promo.description }}</p>

    <div class="home-promo__frame">
      <div class="home-promo__media-wrap">
        <video
          ref="videoRef"
          class="home-promo__media"
          :src="promo.src"
          controls
          playsinline
          preload="metadata"
          @play="isPlaying = true"
          @pause="isPlaying = false"
        />

        <div class="home-promo__overlay" :class="{ 'home-promo__overlay--hidden': isPlaying }" aria-hidden="true">
          <span class="home-promo__tag">PROMOTION MOVIE</span>
          <span class="home-promo__site">Official Fan Site</span>
          <button type="button" class="home-promo__play" aria-label="動画を再生" @click="playVideo">
            <UiIco name="play" :size="28" color="#fff" />
          </button>
        </div>
      </div>
    </div>

    <UiButton variant="primary" size="md" class="home-promo__cta" @click="playVideo">
      {{ promo.cta }}
    </UiButton>
  </div>
</template>

<style scoped>
.home-promo {
  width: 100%;
  max-width: 400px;
}
.home-promo__label {
  display: inline-block;
  padding: 3px 12px;
  margin-bottom: 10px;
  font-family: var(--ff-sans-jp);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: var(--murasaki-700);
  background: var(--murasaki-100);
  border: 1px solid rgba(122, 80, 136, 0.2);
  border-radius: 999px;
}
.home-promo__title {
  margin: 0 0 8px;
  font-family: var(--ff-mincho);
  font-size: clamp(16px, 1.8vw, 19px);
  font-weight: 700;
  line-height: 1.55;
  letter-spacing: 0.06em;
  color: var(--site-text);
}
.home-promo__desc {
  margin: 0 0 14px;
  font-size: 12px;
  line-height: 1.75;
  color: var(--site-text-muted);
  letter-spacing: 0.03em;
}
.home-promo__frame {
  border-radius: var(--site-radius-lg);
  overflow: hidden;
  border: 3px solid rgba(255, 255, 255, 0.95);
  box-shadow: 0 12px 36px rgba(60, 40, 30, 0.14);
  background:
    radial-gradient(ellipse at 30% 20%, rgba(252, 232, 236, 0.6) 0%, transparent 55%),
    linear-gradient(145deg, #2a1520 0%, #1a0a12 100%);
}
.home-promo__media-wrap {
  position: relative;
  aspect-ratio: 16 / 9;
  background: #1a1018;
}
.home-promo__media {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  background: #120810;
}
.home-promo__overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(
    180deg,
    rgba(20, 10, 18, 0.35) 0%,
    rgba(20, 10, 18, 0.55) 100%
  );
  pointer-events: none;
  transition: opacity 0.35s ease;
}
.home-promo__overlay--hidden {
  opacity: 0;
}
.home-promo__tag {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 4px 10px;
  font-family: var(--ff-latin);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.18em;
  color: rgba(255, 255, 255, 0.92);
  border: 1px solid rgba(255, 255, 255, 0.35);
  border-radius: 2px;
}
.home-promo__site {
  position: absolute;
  bottom: 12px;
  right: 12px;
  font-family: var(--ff-latin);
  font-size: 9px;
  letter-spacing: 0.14em;
  color: rgba(255, 255, 255, 0.75);
}
.home-promo__play {
  pointer-events: auto;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.85);
  background: rgba(90, 50, 100, 0.75);
  backdrop-filter: blur(4px);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s, background 0.2s;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}
.home-promo__play:hover {
  transform: scale(1.06);
  background: rgba(90, 50, 100, 0.9);
}
.home-promo__cta {
  width: 100%;
  margin-top: 14px;
  justify-content: center;
}

@media (max-width: 767px) {
  .home-promo {
    max-width: none;
  }
}
</style>
