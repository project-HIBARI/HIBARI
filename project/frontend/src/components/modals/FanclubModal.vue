<script setup>
/**
 * 部品名: ファンクラブ案内モーダル
 */
import ModalShell from './ModalShell.vue'
import UiButton from '../ui/UiButton.vue'
import { MEMBERSHIP_PLANS } from '../../constants/membership.js'

const emit = defineEmits(['close', 'register'])

const plans = MEMBERSHIP_PLANS
</script>

<template>
  <ModalShell title="✦ ファンクラブ" @close="emit('close')">
    <div class="fc-modal__plans">
      <article
        v-for="p in plans"
        :key="p.id"
        class="fc-modal__plan"
        :class="{ 'fc-modal__plan--premium': p.recommended }"
      >
        <span v-if="p.recommended" class="fc-modal__badge">おすすめ</span>
        <h3 class="fc-modal__name">{{ p.name }}</h3>
        <p class="fc-modal__price">{{ p.price }}{{ p.unit }}</p>
        <ul class="fc-modal__features">
          <li v-for="f in p.features" :key="f" class="fc-modal__feat">✓ {{ f }}</li>
          <li v-for="f in p.locked" :key="'l' + f" class="fc-modal__feat fc-modal__feat--locked">🔒 {{ f }}</li>
        </ul>
        <UiButton variant="primary" size="md" class="fc-modal__btn" @click="emit('register', p.id)">
          このプランで登録
        </UiButton>
      </article>
    </div>
    <p class="fc-modal__note">
      ※ プランは新規会員登録時に選択できます。特典は会員区分に応じてご利用いただけます。
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
  font-size: var(--font-size-caption);
  font-weight: 700;
  border-radius: var(--site-radius-sm);
}
.fc-modal__name {
  font-family: var(--ff-mincho);
  font-size: var(--font-size-emphasis);
  font-weight: 700;
  margin: 0 0 4px;
  color: var(--site-text);
}
.fc-modal__price {
  font-family: var(--ff-latin);
  font-size: var(--font-size-title);
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
  font-size: var(--font-size-caption);
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
  font-size: var(--font-size-caption);
  color: var(--site-text-muted);
  line-height: 1.8;
  margin: 0;
}

@media (max-width: 767px) {
  .fc-modal__plans {
    grid-template-columns: 1fr;
  }
}
</style>
