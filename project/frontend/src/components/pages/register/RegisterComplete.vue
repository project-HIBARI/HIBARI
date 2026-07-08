<script setup>
/**
 * 部品名: 登録ステップ4「登録完了」
 * 用途: 登録完了メッセージ + 入力内容サマリ + ファンクラブサイトへの導線
 */
import { computed } from 'vue'
import UiIco from '../../ui/UiIco.vue'

const props = defineProps({
  form: { type: Object, required: true },
})

const emit = defineEmits(['go-fanclub'])

const genderLabels = {
  female: '女性',
  male: '男性',
  other: 'その他',
  'no-answer': '回答しない',
}
const paymentLabels = {
  credit: 'クレジットカード',
  bank: '銀行振込',
  conveni: 'コンビニ払い',
  carrier: 'キャリア決済',
}

const summary = computed(() => [
  { label: '氏名', value: props.form.name },
  { label: '住所', value: props.form.address },
  { label: '性別', value: genderLabels[props.form.gender] || '—' },
  { label: '支払い方法', value: paymentLabels[props.form.payment] || '—' },
  { label: 'メールアドレス', value: props.form.email },
])
</script>

<template>
  <div class="reg-done">
    <div class="reg-done__icon" aria-hidden="true">
      <UiIco name="flower" :size="34" color="var(--murasaki-700)" />
    </div>
    <h2 class="reg-done__title">会員登録が完了しました</h2>
    <p class="reg-done__lead">
      ようこそ、美空ひばりファンクラブへ。<br />
      続いてファンクラブサイトで特典コンテンツをお楽しみください。
    </p>

    <dl class="reg-done__summary">
      <div v-for="row in summary" :key="row.label" class="reg-done__row">
        <dt class="reg-done__dt">{{ row.label }}</dt>
        <dd class="reg-done__dd">{{ row.value || '—' }}</dd>
      </div>
    </dl>

    <button type="button" class="reg-done__cta" @click="emit('go-fanclub')">
      <UiIco name="heart" :size="16" color="#fff" />
      ファンクラブサイトへ進む
      <span aria-hidden="true">›</span>
    </button>
  </div>
</template>

<style scoped>
.reg-done {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 16px;
}
.reg-done__icon {
  width: 72px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: var(--murasaki-100);
  border: 1px solid var(--kin-500);
}
.reg-done__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 22px;
  font-weight: 800;
  letter-spacing: 0.06em;
  color: var(--murasaki-700);
}
.reg-done__lead {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.8;
  color: var(--site-text-muted);
}
.reg-done__summary {
  width: 100%;
  margin: 8px 0 4px;
  padding: 4px 0;
  border-top: 1px solid var(--site-border);
  border-bottom: 1px solid var(--site-border);
}
.reg-done__row {
  display: flex;
  gap: 12px;
  padding: 10px 4px;
  text-align: left;
}
.reg-done__row + .reg-done__row {
  border-top: 1px solid var(--site-border);
}
.reg-done__dt {
  flex: 0 0 96px;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  color: var(--site-text-light);
}
.reg-done__dd {
  margin: 0;
  flex: 1 1 auto;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  color: var(--site-text);
  word-break: break-all;
}
.reg-done__cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  margin-top: 8px;
  padding: 16px 24px;
  font-family: var(--ff-sans-jp);
  font-size: 15px;
  font-weight: 500;
  letter-spacing: 0.12em;
  color: #fff;
  background: var(--murasaki-700);
  border: 1px solid var(--murasaki-800);
  border-radius: 999px;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(93, 58, 107, 0.25);
  transition: background 0.2s;
}
.reg-done__cta:hover {
  background: var(--murasaki-800);
}
</style>
