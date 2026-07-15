<script setup>
/**
 * 部品名: 支払い詳細 — クレジットカード
 * 入力: カード番号 / 有効期限(MM/YY) / セキュリティコード / カード名義
 * 特徴: 入力値を整形（数字のみ・区切り挿入・大文字化）して form へ反映
 */
import RegisterField from '../RegisterField.vue'
import PaymentBrandIcon from './PaymentBrandIcon.vue'

const props = defineProps({
  form: { type: Object, required: true },
  errors: { type: Object, required: true },
})

/** 数字のみ抽出し4桁ごとに半角スペースで区切る（最大16桁） */
function formatCardNumber(v) {
  const digits = (v || '').replace(/\D/g, '').slice(0, 16)
  return digits.replace(/(.{4})/g, '$1 ').trim()
}

/** MM/YY 形式に整形（最大4桁） */
function formatExpiry(v) {
  const digits = (v || '').replace(/\D/g, '').slice(0, 4)
  if (digits.length <= 2) return digits
  return `${digits.slice(0, 2)}/${digits.slice(2)}`
}

/** 数字のみ（最大4桁） */
function formatCvc(v) {
  return (v || '').replace(/\D/g, '').slice(0, 4)
}

/** 半角英字・スペースのみ、大文字化 */
function formatCardName(v) {
  return (v || '').replace(/[^a-zA-Z\s]/g, '').toUpperCase().slice(0, 40)
}

function set(key, value) {
  props.form[key] = value
}
</script>

<template>
  <div class="pay-credit">
    <div class="pay-credit__brands" aria-hidden="true">
      <PaymentBrandIcon brand="credit" :size="36" />
      <span class="pay-credit__brand-text">VISA / Master / JCB / AMEX 対応</span>
    </div>
    <RegisterField
      id="pay-card-number"
      :model-value="form.cardNumber"
      label="カード番号"
      inputmode="numeric"
      placeholder="1234 5678 9012 3456"
      autocomplete="cc-number"
      :maxlength="19"
      :error="errors.cardNumber"
      required
      @update:model-value="(v) => set('cardNumber', formatCardNumber(v))"
    />

    <div class="pay-credit__row">
      <RegisterField
        id="pay-card-expiry"
        :model-value="form.cardExpiry"
        label="有効期限"
        inputmode="numeric"
        placeholder="MM/YY"
        autocomplete="cc-exp"
        :maxlength="5"
        :error="errors.cardExpiry"
        required
        @update:model-value="(v) => set('cardExpiry', formatExpiry(v))"
      />
      <RegisterField
        id="pay-card-cvc"
        :model-value="form.cardCvc"
        label="セキュリティコード"
        type="password"
        inputmode="numeric"
        placeholder="3〜4桁"
        autocomplete="cc-csc"
        :maxlength="4"
        :error="errors.cardCvc"
        required
        @update:model-value="(v) => set('cardCvc', formatCvc(v))"
      />
    </div>

    <RegisterField
      id="pay-card-name"
      :model-value="form.cardName"
      label="カード名義"
      placeholder="TARO YAMADA"
      autocomplete="cc-name"
      hint="カード券面のとおり半角英字でご入力ください。"
      :error="errors.cardName"
      required
      @update:model-value="(v) => set('cardName', formatCardName(v))"
    />
  </div>
</template>

<style scoped>
.pay-credit {
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.pay-credit__brands {
  display: flex;
  align-items: center;
  gap: 12px;
}
.pay-credit__brand-text {
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  color: var(--site-text-muted);
}
.pay-credit__row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 14px;
  min-width: 0;
}

@media (max-width: 767px) {
  .pay-credit__row {
    grid-template-columns: minmax(0, 1fr);
  }
}
</style>
