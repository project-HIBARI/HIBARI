<script setup>
/**
 * 部品名: ファンクラブ プランカード
 * 用途: 会員プラン（名称・料金・特典）を表示し、加入導線ボタンを持つ
 * props: plan = { name, price, unit, features[], locked[], recommended? }
 */
import UiButton from '../../ui/UiButton.vue'

defineProps({
  plan: { type: Object, required: true },
})

const emit = defineEmits(['join'])
</script>

<template>
  <article class="fc-plan" :class="{ 'fc-plan--premium': plan.recommended }">
    <span v-if="plan.recommended" class="fc-plan__badge">おすすめ</span>

    <h3 class="fc-plan__name">{{ plan.name }}</h3>
    <p class="fc-plan__price">
      {{ plan.price }}<span class="fc-plan__unit">{{ plan.unit }}</span>
    </p>

    <ul class="fc-plan__features">
      <li v-for="f in plan.features" :key="f" class="fc-plan__feat">
        <span class="fc-plan__check" aria-hidden="true">✓</span>{{ f }}
      </li>
      <li v-for="f in plan.locked" :key="'l' + f" class="fc-plan__feat fc-plan__feat--locked">
        <span class="fc-plan__check" aria-hidden="true">🔒</span>{{ f }}
      </li>
    </ul>

    <UiButton
      :variant="plan.recommended ? 'primary' : 'outline'"
      size="lg"
      class="fc-plan__btn"
      @click="emit('join', plan)"
    >
      このプランで加入する ›
    </UiButton>
  </article>
</template>

<style scoped>
.fc-plan {
  position: relative;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  padding: 28px 24px 24px;
  background: var(--site-surface);
  height: 100%;
}
.fc-plan--premium {
  border-color: var(--kin-500);
  background: linear-gradient(135deg, var(--site-bg-pink) 0%, var(--site-surface) 100%);
  box-shadow: var(--site-shadow-md);
}
.fc-plan__badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--kin-500);
  color: var(--ink-900);
  padding: 3px 16px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-caption);
  font-weight: 700;
  letter-spacing: 0.08em;
  border-radius: var(--site-radius-sm);
}
.fc-plan__name {
  margin: 0 0 6px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-emphasis);
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--site-text);
}
.fc-plan__price {
  margin: 0 0 20px;
  font-family: var(--ff-latin);
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--kin-600);
  line-height: 1.1;
}
.fc-plan__unit {
  margin-left: 4px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-button);
  font-weight: 500;
  color: var(--site-text-muted);
}
.fc-plan__features {
  list-style: none;
  padding: 0;
  margin: 0 0 24px;
  flex: 1 1 auto;
}
.fc-plan__feat {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-button);
  line-height: 1.6;
  color: var(--site-text-muted);
  padding: 7px 0;
  border-bottom: 1px solid var(--site-border);
}
.fc-plan__check {
  flex-shrink: 0;
  color: var(--murasaki-600);
  font-size: var(--font-size-caption);
}
.fc-plan__feat--locked {
  color: var(--site-text-light);
  text-decoration: line-through;
  opacity: 0.6;
}
.fc-plan__feat--locked .fc-plan__check {
  text-decoration: none;
}
.fc-plan__btn {
  width: 100%;
  justify-content: center;
}
</style>
