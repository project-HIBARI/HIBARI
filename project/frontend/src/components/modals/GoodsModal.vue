<script setup>
/**
 * 部品名: グッズ案内モーダル
 */
import ModalShell from './ModalShell.vue'
import { btnBeni } from '../../utils/hibaru.js'

const emit = defineEmits(['close'])

const goods = [
  { title: '川の流れのように 37周年記念盤', type: 'CD', price: '¥3,300', member: '¥2,970 (会員10%OFF)' },
  { title: '美空ひばり 公式フォトブック 2024', type: '書籍', price: '¥4,400', member: '¥3,960 (会員10%OFF)' },
  { title: '不死鳥コンサート Blu-ray', type: 'BD', price: '¥8,800', member: '¥7,920 (会員10%OFF)' },
]
</script>

<template>
  <ModalShell title="✦ グッズ" @close="emit('close')">
    <div class="goods-modal__list">
      <article v-for="(g, i) in goods" :key="i" class="goods-modal__item">
        <div class="goods-modal__thumb">{{ g.type }}</div>
        <div class="goods-modal__body">
          <h3 class="goods-modal__title">{{ g.title }}</h3>
          <p class="goods-modal__price">{{ g.price }}</p>
          <p class="goods-modal__member">✦ {{ g.member }}</p>
        </div>
        <button type="button" class="goods-modal__buy" :style="btnBeni">購入</button>
      </article>
    </div>
    <p class="goods-modal__note">
      ※ 実際の購入は
      <a href="http://misorahibari-shop.com" target="_blank" rel="noopener noreferrer">公式ショッピングサイト</a>
      をご利用ください。
    </p>
  </ModalShell>
</template>

<style scoped>
.goods-modal__list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.goods-modal__item {
  display: grid;
  grid-template-columns: 80px 1fr auto;
  gap: 16px;
  align-items: center;
  border: 1px solid rgba(201, 169, 97, 0.25);
  padding: 20px;
}
.goods-modal__thumb {
  width: 80px;
  height: 80px;
  background: rgba(201, 169, 97, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(201, 169, 97, 0.2);
  font-family: var(--ff-mono);
  font-size: 10px;
  color: var(--kin-500);
  text-align: center;
}
.goods-modal__title {
  margin: 0 0 6px;
  font-family: var(--ff-mincho);
  font-size: 15px;
  font-weight: 700;
  color: var(--site-text);
}
.goods-modal__price {
  margin: 0;
  font-family: var(--ff-mono);
  font-size: 13px;
  color: var(--site-text-muted);
}
.goods-modal__member {
  margin: 3px 0 0;
  font-size: 11px;
  color: var(--kin-600);
}
.goods-modal__buy {
  font-size: 11px !important;
  padding: 10px 16px !important;
  white-space: nowrap;
}
.goods-modal__note {
  font-size: 12px;
  color: var(--site-text-muted);
  line-height: 1.8;
  margin-top: 16px;
}
.goods-modal__note a {
  color: var(--kin-600);
}

@media (max-width: 480px) {
  .goods-modal__item {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 16px;
  }
  .goods-modal__thumb {
    margin: 0 auto;
  }
  .goods-modal__buy {
    width: 100%;
    justify-content: center;
  }
}
</style>
