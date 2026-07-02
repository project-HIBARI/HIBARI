<script setup>
/**
 * 部品名: ファンクラブ案内モーダル
 * 用途: 会員プラン紹介をライトテーマで表示する
 */
import ModalShell from './ModalShell.vue'
import UiButton from '../ui/UiButton.vue'

const emit = defineEmits(['close'])

const plans = [
  {
    name: '一般会員',
    price: '¥500 / 月',
    features: ['月刊ニュースレター', 'チケット先行予約', '掲示板投稿', '月10回AIひばり対話'],
    locked: ['限定コンテンツ', 'AI新曲制作支援', '優先申込'],
  },
  {
    name: 'プレミアム会員',
    price: '¥1,500 / 月',
    features: ['上記すべて', 'プレミアム限定映像', '限定コンテンツ', 'AI新曲制作支援', 'AIひばり無制限', '優先申込 + 割引'],
    locked: [],
    recommended: true,
  },
]
</script>

<template>
  <ModalShell title="✦ ファンクラブ" @close="emit('close')">
    <div class="fc-modal__plans">
      <article
        v-for="p in plans"
        :key="p.name"
        class="fc-modal__plan"
        :class="{ 'fc-modal__plan--premium': p.recommended }"
      >
        <span v-if="p.recommended" class="fc-modal__badge">おすすめ</span>
        <h3 class="fc-modal__name">{{ p.name }}</h3>
        <p class="fc-modal__price">{{ p.price }}</p>
        <ul class="fc-modal__features">
          <li v-for="f in p.features" :key="f" class="fc-modal__feat">✓ {{ f }}</li>
          <li v-for="f in p.locked" :key="'l' + f" class="fc-modal__feat fc-modal__feat--locked">🔒 {{ f }}</li>
        </ul>
        <UiButton variant="primary" size="md" class="fc-modal__btn">入会する</UiButton>
      </article>
    </div>
    <p class="fc-modal__note">
      ※ 決済はプレースホルダーです。詳細は公式サイト（misorahibari.com）の
      <a href="https://www.misorahibari.com/fanclub.html" target="_blank" rel="noopener noreferrer" class="fc-modal__link">ファンクラブページ</a>
      をご確認ください。
    </p>
  </ModalShell>
</template>

<style scoped>
.fc-modal__plans {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}
.fc-modal__plan {
  position: relative;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  padding: 24px;
  background: var(--site-surface);
}
.fc-modal__plan--premium {
  border-color: var(--kin-500);
  background: linear-gradient(135deg, var(--site-bg-pink) 0%, var(--site-surface) 100%);
}
.fc-modal__badge {
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--kin-500);
  color: var(--ink-900);
  padding: 2px 14px;
  font-family: var(--ff-mincho);
  font-size: 11px;
  font-weight: 700;
  border-radius: var(--site-radius-sm);
}
.fc-modal__name {
  font-family: var(--ff-mincho);
  font-size: 17px;
  font-weight: 700;
  margin: 0 0 4px;
  color: var(--site-text);
}
.fc-modal__price {
  font-family: var(--ff-latin);
  font-size: 24px;
  font-weight: 700;
  color: var(--kin-600);
  margin: 0 0 16px;
}
.fc-modal__features {
  list-style: none;
  padding: 0;
  margin: 0;
}
.fc-modal__feat {
  font-size: 12px;
  color: var(--site-text-muted);
  padding: 4px 0;
  border-bottom: 1px solid var(--site-border);
}
.fc-modal__feat--locked {
  color: var(--site-text-light);
  text-decoration: line-through;
  opacity: 0.6;
}
.fc-modal__btn {
  width: 100%;
  justify-content: center;
  margin-top: 20px;
}
.fc-modal__note {
  font-size: 12px;
  color: var(--site-text-muted);
  line-height: 1.8;
  margin: 0;
}
.fc-modal__link {
  color: var(--murasaki-700);
}

@media (max-width: 480px) {
  .fc-modal__plans {
    grid-template-columns: 1fr;
  }
}
</style>
