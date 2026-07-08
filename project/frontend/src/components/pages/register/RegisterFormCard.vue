<script setup>
/**
 * 部品名: 新規登録フォームカード（ステップ形式ウィザード）
 * 流れ: 1.基本情報(氏名/住所/性別) → 2.お支払い → 3.アカウント(メール/パスワード) → 完了
 * 完了後: ファンクラブサイトへ誘導（complete イベント）
 * 備考: Phase 1 は API 未接続（入力検証と画面遷移のみ）
 */
import { reactive, ref, computed } from 'vue'
import UiIco from '../../ui/UiIco.vue'
import RegisterStepIndicator from './RegisterStepIndicator.vue'
import RegisterStepProfile from './RegisterStepProfile.vue'
import RegisterStepPayment from './RegisterStepPayment.vue'
import RegisterStepAccount from './RegisterStepAccount.vue'
import RegisterComplete from './RegisterComplete.vue'
import RegisterTermsModal from './RegisterTermsModal.vue'

const emit = defineEmits(['navigate', 'open-auth', 'complete'])

const stepLabels = ['基本情報', 'お支払い', 'アカウント']
const step = ref(0)
const submitted = ref(false)
const showTerms = ref(false)

const form = reactive({
  name: '',
  address: '',
  gender: '',
  // 支払い方法と各方式の詳細
  payment: '',
  cardNumber: '',
  cardExpiry: '',
  cardCvc: '',
  cardName: '',
  bankName: '',
  conveniStore: '',
  carrierName: '',
  // アカウント
  email: '',
  password: '',
  passwordConfirm: '',
  agreeTerms: false,
})

const errors = reactive({
  name: '',
  address: '',
  gender: '',
  payment: '',
  cardNumber: '',
  cardExpiry: '',
  cardCvc: '',
  cardName: '',
  bankName: '',
  conveniStore: '',
  carrierName: '',
  email: '',
  password: '',
  passwordConfirm: '',
  agreeTerms: '',
})

const isDone = computed(() => submitted.value)

function clearErrors(keys) {
  keys.forEach((k) => (errors[k] = ''))
}

function validateProfile() {
  clearErrors(['name', 'address', 'gender'])
  let ok = true
  if (!form.name.trim()) {
    errors.name = '氏名を入力してください。'
    ok = false
  }
  if (!form.address.trim()) {
    errors.address = '住所を入力してください。'
    ok = false
  }
  if (!form.gender) {
    errors.gender = '性別を選択してください。'
    ok = false
  }
  return ok
}

function validatePayment() {
  clearErrors([
    'payment',
    'cardNumber',
    'cardExpiry',
    'cardCvc',
    'cardName',
    'bankName',
    'conveniStore',
    'carrierName',
  ])
  if (!form.payment) {
    errors.payment = '支払い方法を選択してください。'
    return false
  }

  let ok = true
  if (form.payment === 'credit') {
    const digits = form.cardNumber.replace(/\D/g, '')
    if (digits.length < 14) {
      errors.cardNumber = 'カード番号を正しく入力してください。'
      ok = false
    }
    const m = form.cardExpiry.match(/^(\d{2})\/(\d{2})$/)
    if (!m || Number(m[1]) < 1 || Number(m[1]) > 12) {
      errors.cardExpiry = '有効期限を MM/YY 形式で入力してください。'
      ok = false
    }
    if (form.cardCvc.length < 3) {
      errors.cardCvc = 'セキュリティコードを入力してください。'
      ok = false
    }
    if (!form.cardName.trim()) {
      errors.cardName = 'カード名義を入力してください。'
      ok = false
    }
  } else if (form.payment === 'bank') {
    if (!form.bankName) {
      errors.bankName = '金融機関を選択してください。'
      ok = false
    }
  } else if (form.payment === 'conveni') {
    if (!form.conveniStore) {
      errors.conveniStore = 'コンビニを選択してください。'
      ok = false
    }
  } else if (form.payment === 'carrier') {
    if (!form.carrierName) {
      errors.carrierName = 'キャリアを選択してください。'
      ok = false
    }
  }
  return ok
}

function validateAccount() {
  clearErrors(['email', 'password', 'passwordConfirm', 'agreeTerms'])
  let ok = true
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!form.email.trim()) {
    errors.email = 'メールアドレスを入力してください。'
    ok = false
  } else if (!emailPattern.test(form.email)) {
    errors.email = 'メールアドレスの形式が正しくありません。'
    ok = false
  }
  if (!form.password) {
    errors.password = 'パスワードを入力してください。'
    ok = false
  } else if (form.password.length < 8) {
    errors.password = 'パスワードは8文字以上で入力してください。'
    ok = false
  }
  if (!form.passwordConfirm) {
    errors.passwordConfirm = '確認用パスワードを入力してください。'
    ok = false
  } else if (form.password !== form.passwordConfirm) {
    errors.passwordConfirm = 'パスワードが一致しません。'
    ok = false
  }
  if (!form.agreeTerms) {
    errors.agreeTerms = '利用規約への同意が必要です。'
    ok = false
  }
  return ok
}

const validators = [validateProfile, validatePayment, validateAccount]

function goNext() {
  if (!validators[step.value]()) return
  if (step.value < stepLabels.length - 1) {
    step.value += 1
    scrollTop()
  } else {
    submit()
  }
}

function goBack() {
  if (step.value > 0) {
    step.value -= 1
    scrollTop()
  }
}

function submit() {
  // Phase 1: API 未接続。ここで登録 API 呼び出しを行う想定。
  submitted.value = true
  scrollTop()
}

function scrollTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function onSubmit(e) {
  e.preventDefault()
  goNext()
}

function onAgreeTerms() {
  form.agreeTerms = true
  errors.agreeTerms = ''
  showTerms.value = false
}
</script>

<template>
  <div class="reg-card">
    <span class="reg-card__corner reg-card__corner--tl" aria-hidden="true" />
    <span class="reg-card__corner reg-card__corner--tr" aria-hidden="true" />
    <span class="reg-card__corner reg-card__corner--bl" aria-hidden="true" />
    <span class="reg-card__corner reg-card__corner--br" aria-hidden="true" />

    <template v-if="!isDone">
      <RegisterStepIndicator :steps="stepLabels" :current="step" />

      <form class="reg-card__form" novalidate @submit="onSubmit">
        <RegisterStepProfile v-if="step === 0" :form="form" :errors="errors" />
        <RegisterStepPayment v-else-if="step === 1" :form="form" :errors="errors" />
        <RegisterStepAccount
          v-else-if="step === 2"
          :form="form"
          :errors="errors"
          @request-terms="showTerms = true"
        />

        <div class="reg-card__actions">
          <button
            v-if="step > 0"
            type="button"
            class="reg-card__back"
            @click="goBack"
          >
            <span aria-hidden="true">‹</span>
            戻る
          </button>
          <button type="submit" class="reg-card__next">
            <template v-if="step < stepLabels.length - 1">
              次へ進む
              <span aria-hidden="true">›</span>
            </template>
            <template v-else>
              <UiIco name="flower" :size="16" color="#fff" />
              この内容で登録する
            </template>
          </button>
        </div>
      </form>

      <div class="reg-card__login">
        <hr class="reg-card__divider" />
        <h2 class="reg-card__login-title">既に会員登録がお済みの方</h2>
        <button type="button" class="reg-card__login-btn" @click="emit('navigate', 'login')">
          ログインはこちら
          <span aria-hidden="true">›</span>
        </button>
      </div>
    </template>

    <RegisterComplete v-else :form="form" @go-fanclub="emit('complete')" />

    <RegisterTermsModal v-if="showTerms" @agree="onAgreeTerms" @close="showTerms = false" />
  </div>
</template>

<style scoped>
.reg-card {
  position: relative;
  width: 100%;
  max-width: 520px;
  margin: 0 auto;
  padding: 40px 48px 36px;
  background: rgba(255, 254, 251, 0.92);
  border: 1px solid var(--kin-500);
  box-shadow: var(--site-shadow-md);
}
.reg-card__corner {
  position: absolute;
  width: 28px;
  height: 28px;
  border-color: var(--kin-500);
  border-style: solid;
  opacity: 0.85;
}
.reg-card__corner--tl {
  top: 10px;
  left: 10px;
  border-width: 2px 0 0 2px;
}
.reg-card__corner--tr {
  top: 10px;
  right: 10px;
  border-width: 2px 2px 0 0;
}
.reg-card__corner--bl {
  bottom: 10px;
  left: 10px;
  border-width: 0 0 2px 2px;
}
.reg-card__corner--br {
  bottom: 10px;
  right: 10px;
  border-width: 0 2px 2px 0;
}
.reg-card__form {
  display: flex;
  flex-direction: column;
  gap: 28px;
}
.reg-card__actions {
  display: flex;
  align-items: center;
  gap: 12px;
}
.reg-card__back {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  flex: 0 0 auto;
  padding: 16px 22px;
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  letter-spacing: 0.06em;
  color: var(--site-text);
  background: var(--site-surface);
  border: 1px solid var(--site-border-strong);
  border-radius: 999px;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}
.reg-card__back:hover {
  border-color: var(--murasaki-400);
  background: var(--murasaki-100);
}
.reg-card__next {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  flex: 1 1 auto;
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
.reg-card__next:hover {
  background: var(--murasaki-800);
}
.reg-card__login {
  margin-top: 28px;
  text-align: center;
}
.reg-card__divider {
  border: 0;
  height: 1px;
  background: var(--site-border);
  margin: 0 0 24px;
}
.reg-card__login-title {
  margin: 0 0 18px;
  font-family: var(--ff-mincho);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--site-text);
}
.reg-card__login-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 100%;
  max-width: 320px;
  padding: 12px 20px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  letter-spacing: 0.06em;
  color: var(--site-text);
  background: var(--site-surface);
  border: 1px solid var(--site-border-strong);
  border-radius: var(--site-radius-sm);
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}
.reg-card__login-btn:hover {
  border-color: var(--murasaki-400);
  background: var(--murasaki-100);
}

@media (max-width: 767px) {
  .reg-card {
    padding: 32px 20px 28px;
    max-width: 100%;
  }
}
</style>
