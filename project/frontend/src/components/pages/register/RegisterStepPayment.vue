<script setup>
/**
 * 部品名: 登録ステップ2「お支払い方法」
 * 入力: 支払い方法（単一選択）＋ 選択方法に応じた詳細入力
 */
import RegisterOptionGroup from './RegisterOptionGroup.vue'
import PaymentCreditForm from './payment/PaymentCreditForm.vue'
import PaymentBankForm from './payment/PaymentBankForm.vue'
import PaymentConveniForm from './payment/PaymentConveniForm.vue'
import PaymentCarrierForm from './payment/PaymentCarrierForm.vue'

defineProps({
  form: { type: Object, required: true },
  errors: { type: Object, required: true },
})

const paymentOptions = [
  { value: 'credit', label: 'クレジットカード', desc: 'VISA / Master / JCB / AMEX', icon: 'credit' },
  { value: 'bank', label: '銀行振込', desc: '毎月末締め・翌月払い', icon: 'bank' },
  { value: 'conveni', label: 'コンビニ払い', desc: '払込票でお支払い', icon: 'conveni' },
  { value: 'carrier', label: 'キャリア決済', desc: '携帯電話料金と合算', icon: 'carrier' },
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

      <!-- 選択した支払い方法に応じた詳細入力 -->
      <transition name="reg-detail">
        <div v-if="form.payment" class="reg-step__detail">
          <PaymentCreditForm v-if="form.payment === 'credit'" :form="form" :errors="errors" />
          <PaymentBankForm v-else-if="form.payment === 'bank'" :form="form" :errors="errors" />
          <PaymentConveniForm v-else-if="form.payment === 'conveni'" :form="form" :errors="errors" />
          <PaymentCarrierForm v-else-if="form.payment === 'carrier'" :form="form" :errors="errors" />
        </div>
      </transition>
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
  font-size: var(--font-size-subtitle);
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--murasaki-700);
}
.reg-step__desc {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  line-height: 1.7;
  color: var(--site-text-muted);
}
.reg-step__body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.reg-step__detail {
  padding: 20px 18px;
  background: var(--murasaki-100);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
}
.reg-step__note {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  line-height: 1.7;
  color: var(--site-text-light);
}
.reg-detail-enter-active,
.reg-detail-leave-active {
  transition: opacity 0.2s ease;
}
.reg-detail-enter-from,
.reg-detail-leave-to {
  opacity: 0;
}
</style>
