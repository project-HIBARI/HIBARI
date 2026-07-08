<script setup>
/**
 * 部品名: 登録ステップ2「お支払い方法」
 * 入力: 支払い方法（単一選択）
 */
import RegisterOptionGroup from './RegisterOptionGroup.vue'

defineProps({
  form: { type: Object, required: true },
  errors: { type: Object, required: true },
})

const paymentOptions = [
  { value: 'credit', label: 'クレジットカード', desc: 'VISA / Master / JCB / AMEX' },
  { value: 'bank', label: '銀行振込', desc: '毎月末締め・翌月払い' },
  { value: 'conveni', label: 'コンビニ払い', desc: '払込票を郵送します' },
  { value: 'carrier', label: 'キャリア決済', desc: '携帯電話料金と合算' },
]
</script>

<template>
  <div class="reg-step">
    <header class="reg-step__head">
      <h2 class="reg-step__title">お支払い方法</h2>
      <p class="reg-step__desc">ファンクラブ会費のお支払い方法をお選びください。</p>
    </header>

    <div class="reg-step__body">
      <RegisterOptionGroup
        v-model="form.payment"
        name="reg-payment"
        label="支払い方法"
        :options="paymentOptions"
        :columns="1"
        :error="errors.payment"
        required
      />
      <p class="reg-step__note">
        ※ 実際の決済は行われません（デモ表示）。会費や特典の詳細はファンクラブ案内をご確認ください。
      </p>
    </div>
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
.reg-step__body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.reg-step__note {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  line-height: 1.7;
  color: var(--site-text-light);
}
</style>
