<script setup>
/**
 * 部品名: ゆかりの地 — ヒーローエリア
 * 用途: ページ冒頭のタイトル・肖像・地図装飾・AI導線を表示する
 */
import heroImg from '../../../assets/hero.png'
import TopAiCard from '../top/TopAiCard.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const emit = defineEmits(['open-ai'])

const spotCount = HIBARU_DATA.places.length
const regionCount = HIBARU_DATA.placeRegions.filter((r) => r.key !== 'all').length
</script>

<template>
  <!-- ゆかりの地ページのファーストビュー（デザイン準拠） -->
  <section class="places-hero" aria-label="ゆかりの地紹介">
    <div class="places-hero__bg" aria-hidden="true">
      <span class="places-hero__pin places-hero__pin--1" />
      <span class="places-hero__pin places-hero__pin--2" />
      <span class="places-hero__pin places-hero__pin--3" />
      <span class="places-hero__route" />
    </div>

    <div class="places-hero__inner">
      <div class="places-hero__copy">
        <p class="places-hero__eyebrow">PLACES · PILGRIMAGE · MISORA HIBARI</p>
        <h1 class="places-hero__title">ゆかりの地</h1>
        <p class="places-hero__desc">
          美空ひばりが歩んだ軌跡を訪ねる旅<br />
          歌声が生まれ、思い出が残る場所をめぐります。
        </p>

        <ul class="places-hero__stats" aria-label="スポットサマリー">
          <li class="places-hero__stat">
            <span class="places-hero__stat-num">{{ spotCount }}</span>
            <span class="places-hero__stat-label">スポット</span>
          </li>
          <li class="places-hero__stat">
            <span class="places-hero__stat-num">{{ regionCount }}</span>
            <span class="places-hero__stat-label">地方</span>
          </li>
          <li class="places-hero__stat">
            <span class="places-hero__stat-num">全国</span>
            <span class="places-hero__stat-label">巡礼マップ</span>
          </li>
        </ul>

        <p class="places-hero__scroll" aria-hidden="true">
          <span class="places-hero__scroll-line" />
          SCROLL
        </p>
      </div>

      <div class="places-hero__visual">
        <img :src="heroImg" alt="美空ひばり" class="places-hero__photo" />
      </div>

      <TopAiCard @open-ai="emit('open-ai')" />
    </div>
  </section>
</template>

<style scoped>
.places-hero {
  position: relative;
  margin-bottom: var(--sp-7);
  padding: var(--sp-7) var(--sp-5);
  border-radius: var(--site-radius-lg);
  overflow: hidden;
}
.places-hero__bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 20% 60%, rgba(252, 232, 236, 0.9) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 25%, rgba(245, 235, 224, 0.75) 0%, transparent 45%),
    repeating-radial-gradient(circle at 10% 90%, rgba(201, 169, 97, 0.05) 0 1px, transparent 1px 20px),
    linear-gradient(135deg, var(--site-bg-warm) 0%, var(--site-bg-pink) 55%, var(--site-surface-muted) 100%);
  border: 1px solid var(--site-border);
}
.places-hero__pin {
  position: absolute;
  width: 14px;
  height: 18px;
  background: var(--beni-600);
  border: 1.5px solid var(--kin-500);
  border-radius: 50% 50% 50% 0;
  transform: rotate(-45deg);
  opacity: 0.35;
}
.places-hero__pin--1 { top: 18%; right: 22%; }
.places-hero__pin--2 { top: 42%; right: 38%; opacity: 0.25; transform: rotate(-45deg) scale(0.8); }
.places-hero__pin--3 { bottom: 20%; right: 15%; opacity: 0.2; transform: rotate(-45deg) scale(0.65); }
.places-hero__route {
  position: absolute;
  top: 30%;
  right: 12%;
  width: 180px;
  height: 120px;
  border: 1px dashed rgba(122, 80, 136, 0.2);
  border-radius: 40% 60% 50% 40%;
  transform: rotate(-8deg);
}
.places-hero__inner {
  position: relative;
  display: grid;
  grid-template-columns: 1fr minmax(200px, 260px) auto;
  gap: var(--sp-6);
  align-items: center;
  z-index: 1;
}
.places-hero__eyebrow {
  margin: 0 0 10px;
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.28em;
  color: var(--kin-600);
}
.places-hero__title {
  margin: 0 0 14px;
  font-family: var(--ff-mincho);
  font-size: clamp(32px, 4vw, 42px);
  font-weight: 800;
  letter-spacing: 0.1em;
  color: var(--site-text);
}
.places-hero__desc {
  margin: 0 0 var(--sp-5);
  font-size: 13px;
  line-height: 1.9;
  color: var(--site-text-muted);
}
.places-hero__stats {
  list-style: none;
  margin: 0 0 var(--sp-5);
  padding: 0;
  display: flex;
  gap: var(--sp-4);
  flex-wrap: wrap;
}
.places-hero__stat {
  text-align: center;
  padding: var(--sp-3) var(--sp-4);
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  min-width: 80px;
}
.places-hero__stat-num {
  display: block;
  font-family: var(--ff-latin);
  font-size: 20px;
  font-weight: 700;
  color: var(--murasaki-600);
  line-height: 1.2;
}
.places-hero__stat-label {
  display: block;
  margin-top: 4px;
  font-family: var(--ff-mincho);
  font-size: 11px;
  letter-spacing: 0.1em;
  color: var(--site-text-muted);
}
.places-hero__scroll {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--ff-latin);
  font-size: 10px;
  letter-spacing: 0.3em;
  color: var(--kin-600);
}
.places-hero__scroll-line {
  display: block;
  width: 1px;
  height: 32px;
  background: linear-gradient(180deg, var(--kin-500), transparent);
}
.places-hero__visual {
  display: flex;
  justify-content: center;
}
.places-hero__photo {
  width: 100%;
  max-width: 240px;
  height: auto;
  aspect-ratio: 4 / 5;
  object-fit: cover;
  border-radius: var(--site-radius-lg);
  border: 3px solid rgba(255, 255, 255, 0.9);
  box-shadow: var(--site-shadow-md);
}

@media (max-width: 1024px) {
  .places-hero__inner {
    grid-template-columns: 1fr;
    gap: var(--sp-7);
  }
  .places-hero__visual {
    order: -1;
  }
  .places-hero__scroll {
    display: none;
  }
}
</style>
