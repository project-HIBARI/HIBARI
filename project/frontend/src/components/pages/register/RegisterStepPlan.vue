<script setup>
/**
 * 部品名: 登録ステップ0「プラン選択」
 * 用途: 一般会員 / プレミアム会員の選択
 */
import { MEMBERSHIP_PLANS } from '../../../constants/membership.js'

defineProps({
  form: { type: Object, required: true },
  errors: { type: Object, required: true },
})

const plans = MEMBERSHIP_PLANS
</script>

<template>
  <div class="reg-step">
    <header class="reg-step__head">
      <h2 class="reg-step__title">会員プランを選択</h2>
      <p class="reg-step__desc">ご希望のプランをお選びください。プランによって特典が異なります。</p>
    </header>

    <div class="reg-plan-grid">
      <label
        v-for="plan in plans"
        :key="plan.id"
        class="reg-plan"
        :class="{
          'reg-plan--active': form.membershipPlan === plan.id,
          'reg-plan--premium': plan.recommended,
        }"
      >
        <input
          v-model="form.membershipPlan"
          class="reg-plan__radio"
          type="radio"
          name="membership-plan"
          :value="plan.id"
        />
        <span v-if="plan.recommended" class="reg-plan__badge">おすすめ</span>
        <h3 class="reg-plan__name">{{ plan.name }}</h3>
        <p class="reg-plan__price">
          <span class="reg-plan__price-num">{{ plan.price }}</span>
          <span class="reg-plan__price-unit">{{ plan.unit }}</span>
        </p>
        <ul class="reg-plan__features">
          <li v-for="feature in plan.features" :key="feature">✓ {{ feature }}</li>
        </ul>
      </label>
    </div>

    <p v-if="errors.membershipPlan" class="reg-plan__error">{{ errors.membershipPlan }}</p>
  </div>
</template>

<style scoped>
.reg-step {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.reg-step__head {
  text-align: center;
}
.reg-step__title {
  margin: 0 0 6px;
  font-family: var(--ff-mincho);
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--murasaki-700);
}
.reg-step__desc {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  line-height: 1.7;
  color: var(--site-text-muted);
}
.reg-plan-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.reg-plan {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px 14px;
  background: #f5f2ee;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s, box-shadow 0.2s;
}
.reg-plan:hover {
  border-color: var(--murasaki-400);
}
.reg-plan--active {
  border: 3px solid #2563eb;
  background: #eff6ff;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.18);
}

.reg-plan--premium.reg-plan--active {
  border: 3px solid #d97706;
  background: #fff3cd;
  box-shadow: 0 0 0 4px rgba(217, 119, 6, 0.2);
}

/* 500円 */
.reg-plan--active .reg-plan__name,
.reg-plan--active .reg-plan__price-num {
  color: #1d4ed8;
}

.reg-plan--active .reg-plan__price-unit,
.reg-plan--active .reg-plan__features li {
  color: #1f2937;
}

/* 1500円*/
.reg-plan--premium.reg-plan--active .reg-plan__name,
.reg-plan--premium.reg-plan--active .reg-plan__price-num {
  color: #92400e;
}

.reg-plan--premium.reg-plan--active .reg-plan__price-unit,
.reg-plan--premium.reg-plan--active .reg-plan__features li {
  color: #451a03;
}
.reg-plan__radio {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}
.reg-plan__badge {
  align-self: flex-start;
  padding: 2px 10px;
  border-radius: 999px;
  background: var(--kin-500);
  color: var(--ink-900);
  font-family: var(--ff-mincho);
  font-size: 10px;
  font-weight: 700;
}
.reg-plan__name {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 16px;
  font-weight: 700;
  color: var(--site-text);
}
.reg-plan__price {
  margin: 0;
  display: flex;
  align-items: baseline;
  gap: 4px;
}
.reg-plan__price-num {
  font-family: var(--ff-latin);
  font-size: 22px;
  font-weight: 700;
  color: var(--kin-600);
}
.reg-plan__price-unit {
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  color: var(--site-text-muted);
}
.reg-plan__features {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.reg-plan__features li {
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  line-height: 1.55;
  color: var(--site-text-muted);
}
.reg-plan__error {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  color: #c0453b;
  text-align: center;
}

@media (max-width: 640px) {
  .reg-plan-grid {
    grid-template-columns: 1fr;
  }
}
</style>
