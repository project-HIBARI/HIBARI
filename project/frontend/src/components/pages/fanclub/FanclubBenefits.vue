<script setup>
/**
 * 部品名: ファンクラブ 特典ハイライト
 */
const benefits = [
  { icon: '✦', title: '月刊ニュースレター', desc: '会員向けの最新情報・コラムを毎月お届けします。' },
  { icon: '★', title: 'チケット先行予約', desc: 'コンサートやイベントの先行予約にご利用いただけます。' },
  { icon: '💬', title: '掲示板投稿', desc: '思い出やメッセージを会員掲示板に投稿できます。' },
  { icon: '♪', title: 'AIひばり対話', desc: '一般会員は月10回、プレミアム会員は無制限で対話できます。' },
  { icon: '▶', title: 'プレミアム限定映像', desc: 'プレミアム会員だけの未公開映像・特別コンテンツ。', premium: true },
  { icon: '✧', title: '限定コンテンツ', desc: 'ハイレゾ音源や会員限定の特典コンテンツ。', premium: true },
  { icon: '◎', title: '優先申込＋会員割引', desc: 'イベントの優先申込と会員割引価格がご利用いただけます。', premium: true },
]
</script>

<template>
  <ul class="fc-benefits">
    <li
      v-for="b in benefits"
      :key="b.title"
      class="fc-benefits__item"
      :class="{ 'fc-benefits__item--premium': b.premium }"
    >
      <span class="fc-benefits__icon" aria-hidden="true">{{ b.icon }}</span>
      <h3 class="fc-benefits__title">
        {{ b.title }}
        <span v-if="b.premium" class="fc-benefits__tag">Premium</span>
      </h3>
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
.fc-benefits__item--premium {
  border-color: rgba(201, 169, 97, 0.45);
  background: linear-gradient(180deg, #fffaf6 0%, var(--site-surface) 100%);
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
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}
.fc-benefits__tag {
  font-family: var(--ff-sans-jp);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--kin-600);
}
.fc-benefits__desc {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  line-height: 1.7;
  color: var(--site-text-muted);
}

@media (max-width: 1100px) {
  .fc-benefits {
    grid-template-columns: repeat(3, 1fr);
  }
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
