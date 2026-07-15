<script setup>
/**
 * 部品名: 支払い詳細 — コンビニ支払い
 * 入力: 利用するコンビニエンスストアの選択
 */
import RegisterOptionGroup from '../RegisterOptionGroup.vue'

defineProps({
  form: { type: Object, required: true },
  errors: { type: Object, required: true },
})

const conveniOptions = [
  { value: 'familymart', label: 'ファミリーマート', desc: 'Famiポートで払込', icon: 'familymart' },
  { value: 'seven', label: 'セブンイレブン', desc: 'レジで払込票を提示', icon: 'seven' },
  { value: 'lawson', label: 'ローソン', desc: 'Loppiで払込', icon: 'lawson' },
]
</script>

<template>
  <div class="pay-conveni">
    <RegisterOptionGroup
      v-model="form.conveniStore"
      name="pay-conveni"
      label="コンビニエンスストア"
      :options="conveniOptions"
      :columns="1"
      :error="errors.conveniStore"
      required
    />
    <p class="pay-conveni__note">
      お申し込み後に発行される払込番号を、選択した店舗でお支払いください。
    </p>
  </div>
</template>

<style scoped>
.pay-conveni {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.pay-conveni__note {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  line-height: 1.7;
  color: var(--site-text-light);
}
</style>
