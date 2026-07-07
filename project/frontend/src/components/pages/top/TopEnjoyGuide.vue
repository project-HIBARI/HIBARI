<script setup>
/**
 * 部品名: ホーム — サイトの楽しみ方
 * 用途: 「サイトの楽しみ方」CTA のスクロール先。各機能の案内を表示する
 */
import UiCard from '../../ui/UiCard.vue'
import SectionTitle from '../../ui/SectionTitle.vue'

const emit = defineEmits(['navigate'])

const guides = [
  { icon: '♪', title: 'ディスコグラフィー', desc: '代表曲から年代別に楽曲を探せます。', target: 'disco' },
  { icon: '歴', title: '歩み', desc: '年表とプロフィールで生涯をたどります。', target: 'profile' },
  { icon: '縁', title: 'ゆかりの地', desc: '地図からゆかりの場所を巡れます。', target: 'map' },
  { icon: '✦', title: 'AI美空ひばり', desc: 'いつでも気軽に会話を楽しめます。', target: 'ai' },
]
</script>

<template>
  <section id="home-enjoy-guide" class="top-enjoy" aria-label="サイトの楽しみ方">
    <SectionTitle title="サイトの楽しみ方" sub="How to enjoy" size="lg" />

    <div class="top-enjoy__grid">
      <UiCard
        v-for="g in guides"
        :key="g.title"
        tone="pink"
        padding="md"
        class="top-enjoy__card"
      >
        <button type="button" class="top-enjoy__btn" @click="emit('navigate', g.target)">
          <span class="top-enjoy__icon">{{ g.icon }}</span>
          <span class="top-enjoy__card-title">{{ g.title }}</span>
          <span class="top-enjoy__card-desc">{{ g.desc }}</span>
        </button>
      </UiCard>
    </div>
  </section>
</template>

<style scoped>
.top-enjoy {
  scroll-margin-top: 120px;
}
.top-enjoy__grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
}
.top-enjoy__card {
  height: 100%;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.top-enjoy__card:hover {
  transform: translateY(-2px);
  box-shadow: var(--site-shadow-md);
}
.top-enjoy__btn {
  width: 100%;
  min-height: 140px;
  background: transparent;
  border: 0;
  padding: 4px 0 0;
  cursor: pointer;
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.top-enjoy__icon {
  font-family: var(--ff-mincho);
  font-size: 30px;
  font-weight: 700;
  color: var(--murasaki-600);
  line-height: 1;
}
.top-enjoy__card-title {
  font-family: var(--ff-mincho);
  font-size: 16px;
  font-weight: 700;
  color: var(--site-text);
  letter-spacing: 0.05em;
}
.top-enjoy__card-desc {
  font-size: 12px;
  line-height: 1.75;
  color: var(--site-text-muted);
}

@media (max-width: 1024px) {
  .top-enjoy__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 767px) {
  .top-enjoy__grid {
    grid-template-columns: 1fr;
  }
}
</style>
