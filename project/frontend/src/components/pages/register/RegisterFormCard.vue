<script setup>
/**
 * 部品名: 新規登録フォームカード（ステップ形式ウィザード）
 * 流れ: 0.プラン選択 → 1.基本情報 → 2.お支払い → 3.アカウント → 完了
 * 完了後: ファンクラブサイトへ誘導（complete イベント）
 */
import { reactive, ref, computed, watch } from 'vue'
import UiIco from '../../ui/UiIco.vue'
import RegisterStepIndicator from './RegisterStepIndicator.vue'
import RegisterStepPlan from './RegisterStepPlan.vue'
import RegisterStepProfile from './RegisterStepProfile.vue'
import RegisterStepPayment from './RegisterStepPayment.vue'
import RegisterStepAccount from './RegisterStepAccount.vue'
import RegisterComplete from './RegisterComplete.vue'
import RegisterTermsModal from './RegisterTermsModal.vue'
import { registerAccount } from '../../../api/auth.js'
import { MEMBERSHIP, MEMBERSHIP_LABELS } from '../../../constants/membership.js'

const props = defineProps({
  initialPlan: { type: String, default: MEMBERSHIP.GENERAL },
  platform: { type: Boolean, default: false },
})

const emit = defineEmits(['navigate', 'open-auth', 'complete'])

const stepLabels = ['プラン選択', '基本情報', 'お支払い', 'アカウント']
const step = ref(0)
const submitted = ref(false)
const showTerms = ref(false)
const submitting = ref(false)
const submitError = ref('')
const registeredUser = ref(null)

const form = reactive({
  membershipPlan: props.initialPlan || MEMBERSHIP.GENERAL,
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
  bankBranch: '',
  bankAccountType: '',
  bankAccountNumber: '',
  bankAccountHolder: '',
  conveniStore: '',
  carrierName: '',
  // アカウント
  email: '',
  password: '',
  passwordConfirm: '',
  agreeTerms: false,
})

const errors = reactive({
  membershipPlan: '',
  name: '',
  address: '',
  gender: '',
  payment: '',
  cardNumber: '',
  cardExpiry: '',
  cardCvc: '',
  cardName: '',
  bankName: '',
  bankBranch: '',
  bankAccountType: '',
  bankAccountNumber: '',
  bankAccountHolder: '',
  conveniStore: '',
  carrierName: '',
  email: '',
  password: '',
  passwordConfirm: '',
  agreeTerms: '',
})

const isDone = computed(() => submitted.value)

watch(
  () => props.initialPlan,
  (plan) => {
    if (plan && !submitted.value) {
      form.membershipPlan = plan
    }
  },
)

function validatePlan() {
  clearErrors(['membershipPlan'])
  if (!form.membershipPlan) {
    errors.membershipPlan = '会員プランを選択してください。'
    return false
  }
  return true
}

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
    'bankBranch',
    'bankAccountType',
    'bankAccountNumber',
    'bankAccountHolder',
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
    if (!form.bankBranch.trim()) {
      errors.bankBranch = '支店名を入力してください。'
      ok = false
    }
    if (!form.bankAccountType) {
      errors.bankAccountType = '口座種別を選択してください。'
      ok = false
    }
    if (!/^\d{7}$/.test(form.bankAccountNumber)) {
      errors.bankAccountNumber = '口座番号は7桁の数字で入力してください。'
      ok = false
    }
    if (!form.bankAccountHolder.trim()) {
      errors.bankAccountHolder = '口座名義を入力してください。'
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

const validators = [validatePlan, validateProfile, validatePayment, validateAccount]

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

async function submit() {
  submitError.value = ''
  submitting.value = true
  try {
    const result = await registerAccount({
      name: form.name.trim(),
      email: form.email.trim(),
      password: form.password,
      address: form.address.trim(),
      is_premium: form.membershipPlan === MEMBERSHIP.PREMIUM,
    })
    submitted.value = true
    registeredUser.value = result.user
    scrollTop()
  } catch (err) {
    if (err.message?.includes('Failed to fetch') || err.message?.includes('NetworkError')) {
      submitError.value = 'サーバーに接続できません。バックエンド（Flask）が起動しているか確認してください。'
    } else {
      submitError.value = err.message || '会員登録に失敗しました。'
    }
  } finally {
    submitting.value = false
  }
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
  <div class="reg-card" :class="{ 'reg-card--platform': platform }">
    <span class="reg-card__corner reg-card__corner--tl" aria-hidden="true" />
    <span class="reg-card__corner reg-card__corner--tr" aria-hidden="true" />
    <span class="reg-card__corner reg-card__corner--bl" aria-hidden="true" />
    <span class="reg-card__corner reg-card__corner--br" aria-hidden="true" />

    <template v-if="!isDone">
      <RegisterStepIndicator :steps="stepLabels" :current="step" />

      <form class="reg-card__form" novalidate @submit="onSubmit">
        <RegisterStepPlan v-if="step === 0" :form="form" :errors="errors" />
        <RegisterStepProfile v-else-if="step === 1" :form="form" :errors="errors" />
        <RegisterStepPayment v-else-if="step === 2" :form="form" :errors="errors" />
        <RegisterStepAccount
          v-else-if="step === 3"
          :form="form"
          :errors="errors"
          @request-terms="showTerms = true"
        />

        <p v-if="submitError" class="reg-card__error" role="alert">{{ submitError }}</p>

        <div class="reg-card__actions">
          <button
            v-if="step > 0"
            type="button"
            class="reg-card__back"
            :disabled="submitting"
            @click="goBack"
          >
            <span aria-hidden="true">‹</span>
            戻る
          </button>
          <button type="submit" class="reg-card__next" :disabled="submitting">
            <template v-if="step < stepLabels.length - 1">
              次へ進む
              <span aria-hidden="true">›</span>
            </template>
            <template v-else>
              <UiIco name="flower" :size="16" color="#fff" />
              {{ submitting ? '登録中…' : 'この内容で登録する' }}
            </template>
          </button>
        </div>
      </form>

      <div class="reg-card__login">
        <hr class="reg-card__divider" />
        <h2 class="reg-card__login-title">既に会員登録がお済みの方</h2>
        <button type="button" class="reg-card__login-btn" @click="emit('open-auth', 'login')">
          ログインはこちら
          <span aria-hidden="true">›</span>
        </button>
      </div>
    </template>

    <RegisterComplete
      v-else
      :form="form"
      @go-fanclub="emit('complete', registeredUser)"
    />

    <RegisterTermsModal v-if="showTerms" @agree="onAgreeTerms" @close="showTerms = false" />
  </div>
</template>

<style scoped>
.reg-card {
  position: relative;
  width: 100%;
  max-width: 640px;
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
.reg-card__next:disabled,
.reg-card__back:disabled {
  opacity: 0.7;
  cursor: wait;
}
.reg-card__error {
  margin: 0;
  padding: 10px 12px;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  line-height: 1.6;
  color: #9b2c2c;
  background: #fff5f5;
  border: 1px solid #f0c4c4;
  border-radius: var(--site-radius-sm);
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

.reg-card--platform {
  background: rgba(32, 26, 32, 0.82);
  border: 1px solid rgba(201, 169, 97, 0.45);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(12px);
  border-radius: var(--site-radius-lg);
}

.reg-card--platform .reg-card__corner {
  border-color: var(--kin-400);
}

.reg-card--platform .reg-card__login-title {
  color: rgba(248, 244, 239, 0.88);
}

.reg-card--platform .reg-card__login-btn {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.2);
  color: #f8f4ef;
}

.reg-card--platform .reg-card__divider {
  background: rgba(255, 255, 255, 0.12);
}

.reg-card--platform .reg-card__back {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.18);
  color: #f8f4ef;
}

.reg-card--platform .reg-card__error {
  background: rgba(155, 44, 44, 0.2);
  border-color: rgba(240, 196, 190, 0.35);
  color: #ffb4a8;
}

.reg-card--platform :deep(.reg-step__label),
.reg-card--platform :deep(.reg-step__item),
.reg-card--platform :deep(.register-label),
.reg-card--platform :deep(.register-option__label),
.reg-card--platform :deep(.register-plan__name),
.reg-card--platform :deep(.register-plan__price),
.reg-card--platform :deep(h3),
.reg-card--platform :deep(h4),
.reg-card--platform :deep(p),
.reg-card--platform :deep(label),
.reg-card--platform :deep(.reg-done__title) {
  color: rgba(248, 244, 239, 0.88);
}

.reg-card--platform :deep(.reg-field__label),
.reg-card--platform :deep(.reg-opt__label),
.reg-card--platform :deep(.reg-opt__name),
.reg-card--platform :deep(.reg-field__hint),
.reg-card--platform :deep(.pay-bank__search-label),
.reg-card--platform :deep(.pay-bank__selected),
.reg-card--platform :deep(.pay-bank__note) {
  color: var(--site-text) !important;
}

.reg-card--platform :deep(.register-desc),
.reg-card--platform :deep(.register-plan__desc),
.reg-card--platform :deep(.reg-done__lead),
.reg-card--platform :deep(.reg-done__dt) {
  color: rgba(248, 244, 239, 0.58);
}

.reg-card--platform :deep(input:not([type='checkbox'])),
.reg-card--platform :deep(select),
.reg-card--platform :deep(textarea) {
  background: rgba(255, 255, 255, 0.92);
  border-color: rgba(255, 255, 255, 0.24);
  color: var(--site-text);
  -webkit-text-fill-color: var(--site-text);
}

.reg-card--platform :deep(input::placeholder),
.reg-card--platform :deep(textarea::placeholder) {
  color: var(--site-text-light);
  -webkit-text-fill-color: var(--site-text-light);
}

.reg-card--platform :deep(input:focus),
.reg-card--platform :deep(select:focus),
.reg-card--platform :deep(textarea:focus) {
  background: #fff;
  color: var(--site-text);
  -webkit-text-fill-color: var(--site-text);
}

.reg-card--platform :deep(.register-plan) {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.14);
}

.reg-card--platform :deep(.register-plan--active) {
  border-color: var(--kin-400);
  background: rgba(122, 80, 136, 0.25);
}

@media (max-width: 767px) {
  .reg-card {
    padding: 32px 20px 28px;
    max-width: 100%;
  }
}
</style>
