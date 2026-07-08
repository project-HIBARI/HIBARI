<script setup>
/**
 * 部品名: 支払い詳細 — 銀行振込
 * 入力: 金融機関の選択
 */
import RegisterOptionGroup from '../RegisterOptionGroup.vue'

defineProps({
  form: { type: Object, required: true },
  errors: { type: Object, required: true },
})

const bankOptions = [
  { value: 'mizuho', label: 'みずほ銀行' },
  { value: 'mufg', label: '三菱UFJ銀行' },
  { value: 'smbc', label: '三井住友銀行' },
  { value: 'yucho', label: 'ゆうちょ銀行' },
  { value: 'other', label: 'その他の金融機関' },
]
</script>

<template>
  <div class="pay-bank">
    <RegisterOptionGroup
      v-model="form.bankName"
      name="pay-bank"
      label="金融機関"
      :options="bankOptions"
      :columns="2"
      :error="errors.bankName"
      required
    />
    <p class="pay-bank__note">
      ※ お申し込み後、振込先口座番号をメールでご案内します（毎月末締め・翌月払い）。
    </p>
  </div>
</template>

<style scoped>
.pay-bank {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.pay-bank__note {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  line-height: 1.7;
  color: var(--site-text-light);
}
</style>
