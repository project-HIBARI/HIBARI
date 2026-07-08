<script setup>
/**
 * 部品名: 登録ステップ3「アカウント情報」
 * 入力: メールアドレス / パスワード / パスワード（確認） + 規約同意
 */
import RegisterField from './RegisterField.vue'

const props = defineProps({
  form: { type: Object, required: true },
  errors: { type: Object, required: true },
})

const emit = defineEmits(['request-terms'])

/** チェックボックス操作: 未同意ならモーダルを開く / 同意済みなら解除 */
function onToggleAgree() {
  if (props.form.agreeTerms) {
    props.form.agreeTerms = false
  } else {
    emit('request-terms')
  }
}
</script>

<template>
  <div class="reg-step">
    <header class="reg-step__head">
      <h2 class="reg-step__title">アカウント情報</h2>
      <p class="reg-step__desc">ログインに使用するメールアドレスとパスワードを設定してください。</p>
    </header>

    <div class="reg-step__body">
      <RegisterField
        id="reg-email"
        v-model="form.email"
        label="メールアドレス"
        type="email"
        placeholder="example@misorahibari.com"
        autocomplete="email"
        :error="errors.email"
        required
      />
      <RegisterField
        id="reg-password"
        v-model="form.password"
        label="パスワード"
        type="password"
        placeholder="8文字以上で入力してください"
        autocomplete="new-password"
        hint="半角英数字8文字以上でご設定ください。"
        :error="errors.password"
        required
      />
      <RegisterField
        id="reg-password-confirm"
        v-model="form.passwordConfirm"
        label="パスワード（確認）"
        type="password"
        placeholder="パスワードを再入力してください"
        autocomplete="new-password"
        :error="errors.passwordConfirm"
        required
      />

      <div class="reg-step__terms">
        <input
          id="reg-agree"
          type="checkbox"
          class="reg-step__checkbox"
          :checked="form.agreeTerms"
          @click.prevent="onToggleAgree"
        />
        <span>
          <button type="button" class="reg-step__link" @click="emit('request-terms')">利用規約</button>
          および
          <button type="button" class="reg-step__link" @click="emit('request-terms')">
            プライバシーポリシー
          </button>
          に同意します
        </span>
      </div>
      <p class="reg-step__terms-note">
        チェックを入れると規約が表示されます。最後までお読みいただくとご同意いただけます。
      </p>
      <p v-if="errors.agreeTerms" class="reg-step__error">{{ errors.agreeTerms }}</p>
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
  gap: 20px;
}
.reg-step__terms {
  display: inline-flex;
  align-items: flex-start;
  gap: 8px;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  line-height: 1.75;
  color: var(--site-text-muted);
  cursor: pointer;
}
.reg-step__checkbox {
  width: 16px;
  height: 16px;
  margin-top: 3px;
  flex-shrink: 0;
  accent-color: var(--murasaki-600);
  cursor: pointer;
}
.reg-step__terms-note {
  margin: -12px 0 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  line-height: 1.6;
  color: var(--site-text-light);
}
.reg-step__link {
  background: transparent;
  border: 0;
  padding: 0;
  font-family: inherit;
  font-size: inherit;
  color: var(--murasaki-700);
  text-decoration: underline;
  cursor: pointer;
}
.reg-step__link:hover {
  color: var(--murasaki-800);
}
.reg-step__error {
  margin: -12px 0 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  color: #c0453b;
}
</style>
