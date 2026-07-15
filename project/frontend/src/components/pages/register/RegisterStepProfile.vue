<script setup>
/**
 * 部品名: 登録ステップ1「基本情報」
 * 入力: 氏名 / 住所 / 性別
 */
import RegisterField from './RegisterField.vue'
import RegisterOptionGroup from './RegisterOptionGroup.vue'

defineProps({
  form: { type: Object, required: true },
  errors: { type: Object, required: true },
})

const genderOptions = [
  { value: 'female', label: '女性' },
  { value: 'male', label: '男性' },
  { value: 'other', label: 'その他' },
  { value: 'no-answer', label: '回答しない' },
]
</script>

<template>
  <div class="reg-step">
    <header class="reg-step__head">
      <h2 class="reg-step__title">基本情報</h2>
      <p class="reg-step__desc">お客様のお名前とお住まい、性別をご入力ください。</p>
    </header>

    <div class="reg-step__body">
      <RegisterField
        id="reg-name"
        v-model="form.name"
        label="氏名"
        placeholder="美空 ひばり"
        autocomplete="name"
        :error="errors.name"
        required
      />
      <RegisterField
        id="reg-address"
        v-model="form.address"
        label="住所"
        placeholder="例）東京都千代田区〇〇 1-2-3"
        autocomplete="street-address"
        :error="errors.address"
        required
      />
      <RegisterOptionGroup
        v-model="form.gender"
        name="reg-gender"
        label="性別"
        :options="genderOptions"
        :columns="2"
        :error="errors.gender"
        required
      />
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
  gap: 20px;
}
</style>
