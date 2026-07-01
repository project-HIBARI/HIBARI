<script setup>
/**
 * 部品名: ゆかりの地 — ヒーローエリア
 * 用途: ページ冒頭のコピー・地図装飾・AI導線リンクを表示
 */
import UiCard from '../../ui/UiCard.vue'
import UiIco from '../../ui/UiIco.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const emit = defineEmits(['open-ai'])

const spotCount = HIBARU_DATA.places.length
const regionCount = HIBARU_DATA.placeRegions.filter((r) => r.key !== 'all').length
</script>

<template>
  <!-- ゆかりの地ページのファーストビュー -->
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
        <h2 class="places-hero__title">ゆかりの地</h2>
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
      </div>

      <UiCard tone="pink" padding="md" class="places-hero__ai">
        <p class="places-hero__ai-label">AI GUIDE · 新機能</p>
        <p class="places-hero__ai-title">ゆかりの地について<br />AI美空ひばりに聞く</p>
        <p class="places-hero__ai-desc">
          「野毛の銅像はいつ建てられた？」「記念館の見学方法は？」など、
          スポットについて AI と会話できます。
        </p>
        <button type="button" class="places-hero__ai-link" @click="emit('open-ai')">
          <UiIco name="chat" :size="15" color="var(--murasaki-700)" />
          AIと話す
          <span aria-hidden="true">›</span>
        </button>
      </UiCard>
    </div>
  </section>
</template>

<style scoped>
.places-hero {
  position: relative;
  margin-bottom: var(--sp-7);
  padding: var(--sp-6) var(--sp-5);
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
  grid-template-columns: 1.2fr 1fr;
  gap: var(--sp-6);
  align-items: center;
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
  font-size: clamp(26px, 3.5vw, 34px);
  font-weight: 700;
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
  margin: 0;
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
.places-hero__ai {
  background:
    radial-gradient(ellipse at 100% 0%, rgba(243, 235, 246, 0.85) 0%, transparent 55%),
    var(--site-surface);
}
.places-hero__ai-label {
  margin: 0 0 var(--sp-3);
  font-family: var(--ff-latin);
  font-size: 10px;
  letter-spacing: 0.25em;
  color: var(--kin-600);
}
.places-hero__ai-title {
  margin: 0 0 10px;
  font-family: var(--ff-mincho);
  font-size: 18px;
  font-weight: 700;
  line-height: 1.5;
  letter-spacing: 0.06em;
  color: var(--site-text);
}
.places-hero__ai-desc {
  margin: 0 0 var(--sp-4);
  font-size: 12px;
  line-height: 1.75;
  color: var(--site-text-muted);
}
.places-hero__ai-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 0;
  border: 0;
  background: transparent;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  font-weight: 500;
  color: var(--murasaki-700);
  cursor: pointer;
  letter-spacing: 0.06em;
}
.places-hero__ai-link:hover {
  text-decoration: underline;
}

@media (max-width: 900px) {
  .places-hero__inner {
    grid-template-columns: 1fr;
  }
}
</style>
