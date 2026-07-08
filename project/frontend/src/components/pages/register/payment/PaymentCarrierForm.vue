<script setup>
/**
 * 部品名: 支払い詳細 — キャリア決済
 * 入力: 携帯キャリアの選択
 */
import RegisterOptionGroup from '../RegisterOptionGroup.vue'

defineProps({
  form: { type: Object, required: true },
  errors: { type: Object, required: true },
})

const carrierOptions = [
  { value: 'docomo', label: 'docomo', desc: 'ドコモ払い', icon: 'docomo' },
  { value: 'au', label: 'au', desc: 'auかんたん決済', icon: 'au' },
  { value: 'softbank', label: 'Softbank', desc: 'ソフトバンクまとめて支払い', icon: 'softbank' },
]
</script>

<template>
  <div class="pay-carrier">
    <RegisterOptionGroup
      v-model="form.carrierName"
      name="pay-carrier"
      label="携帯キャリア"
      :options="carrierOptions"
      :columns="3"
      :error="errors.carrierName"
      required
    />
    <p class="pay-carrier__note">
      会費は毎月の携帯電話料金と合算して請求されます。
    </p>
  </div>
</template>

<style scoped>
.pay-carrier {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.pay-carrier__note {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  line-height: 1.7;
  color: var(--site-text-light);
}
</style>
