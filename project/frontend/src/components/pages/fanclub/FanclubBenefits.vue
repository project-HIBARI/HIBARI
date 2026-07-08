<script setup>
/**
 * 部品名: ファンクラブ 特典ハイライト
 * 用途: 会員特典を4項目のアイコン付きグリッドで紹介する
 */
const benefits = [
  { icon: '▶', title: '限定コンテンツ', desc: '未公開映像・ハイレゾ音源など会員限定の特典を配信。' },
  { icon: '★', title: 'チケット先行予約', desc: 'コンサートやイベントの先行予約・優先申込に対応。' },
  { icon: '✦', title: '会員誌デジタル版', desc: '月刊ニュースレターと会員誌をデジタルでお届け。' },
  { icon: '♪', title: 'AIひばり対話', desc: 'AIによるひばりとの対話・新曲制作支援をご利用可能。' },
]
</script>

<template>
  <ul class="fc-benefits">
    <li v-for="b in benefits" :key="b.title" class="fc-benefits__item">
      <span class="fc-benefits__icon" aria-hidden="true">{{ b.icon }}</span>
      <h3 class="fc-benefits__title">{{ b.title }}</h3>
      <p class="fc-benefits__desc">{{ b.desc }}</p>
    </li>
  </ul>
</template>

<style scoped>
.fc-benefits {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--sp-4);
}
.fc-benefits__item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 10px;
  padding: 24px 18px;
  background: var(--site-surface);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
}
.fc-benefits__icon {
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  border: 1px solid var(--kin-500);
  background: var(--murasaki-100);
  color: var(--kin-600);
  font-size: 20px;
}
.fc-benefits__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--site-text);
}
.fc-benefits__desc {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  line-height: 1.7;
  color: var(--site-text-muted);
}

@media (max-width: 900px) {
  .fc-benefits {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 480px) {
  .fc-benefits {
    grid-template-columns: 1fr;
  }
}
</style>
