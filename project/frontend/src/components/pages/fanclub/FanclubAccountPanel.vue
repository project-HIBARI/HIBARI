<script setup>
/**
 * 部品名: ファンクラブ アカウント管理
 * 用途: 会員ページでプロフィール表示・編集・パスワード変更・ログアウト
 */
import { ref, reactive, watch, onMounted } from 'vue'
import UiButton from '../../ui/UiButton.vue'
import RegisterField from '../register/RegisterField.vue'
import { fetchAccount, updateAccount, changeAccountPassword, updateAccountPayment, updateAccountMembership } from '../../../api/account.js'
import { useMemberAccess } from '../../../composables/useMemberAccess.js'
import { MEMBERSHIP_LABELS } from '../../../constants/membership.js'
import RegisterOptionGroup from '../register/RegisterOptionGroup.vue'
import PaymentCreditForm from '../register/payment/PaymentCreditForm.vue'
import PaymentBankForm from '../register/payment/PaymentBankForm.vue'
import PaymentConveniForm from '../register/payment/PaymentConveniForm.vue'
import PaymentCarrierForm from '../register/payment/PaymentCarrierForm.vue'

const emit = defineEmits(['need-login', 'logout', 'user-updated'])

const { isLoggedIn, membership, isPremium, user, setUser, logout } = useMemberAccess()

const loading = ref(true)
const profileError = ref('')
const profileSuccess = ref('')
const passwordError = ref('')
const passwordSuccess = ref('')
const paymentError = ref('')
const paymentSuccess = ref('')
const membershipError = ref('')
const membershipSuccess = ref('')
const savingProfile = ref(false)
const savingPassword = ref(false)
const savingPayment = ref(false)
const savingMembership = ref(false)
const currentPaymentMethod = ref(null)
const currentPaymentDetails = ref(null)

const paymentOptions = [
  { value: 'credit', label: 'クレジットカード', desc: 'VISA / Master / JCB / AMEX', icon: 'credit' },
  { value: 'bank', label: '銀行振込', desc: '毎月末締め・翌月払い', icon: 'bank' },
  { value: 'conveni', label: 'コンビニ払い', desc: '払込票でお支払い', icon: 'conveni' },
  { value: 'carrier', label: 'キャリア決済', desc: '携帯電話料金と合算', icon: 'carrier' },
]

const paymentLabels = {
  credit: 'クレジットカード',
  bank: '銀行振込',
  conveni: 'コンビニ払い',
  carrier: 'キャリア決済',
}

const profile = reactive({
  name: '',
  email: '',
  address: '',
})

const passwordForm = reactive({
  current: '',
  next: '',
  confirm: '',
})

const passwordErrors = reactive({
  current: '',
  next: '',
  confirm: '',
})

const paymentForm = reactive({
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
})

const paymentErrors = reactive({ payment: '' })

function currentPaymentSummary() {
  if (!currentPaymentMethod.value) return '未設定'
  const label = paymentLabels[currentPaymentMethod.value] || currentPaymentMethod.value
  const d = currentPaymentDetails.value
  if (!d) return label
  if (currentPaymentMethod.value === 'credit' && d.card_masked) {
    return `${label}（${d.card_masked}）`
  }
  if (currentPaymentMethod.value === 'bank' && d.bank_name) {
    return `${label}（${d.bank_name}）`
  }
  if (currentPaymentMethod.value === 'conveni' && d.conveni_store) {
    return `${label}（${d.conveni_store}）`
  }
  if (currentPaymentMethod.value === 'carrier' && d.carrier_name) {
    return `${label}（${d.carrier_name}）`
  }
  return label
}

async function loadAccount() {
  if (!isLoggedIn.value) {
    loading.value = false
    return
  }
  loading.value = true
  profileError.value = ''
  try {
    const data = await fetchAccount()
    const account = data.account || data.user
    profile.name = account.name || ''
    profile.email = account.email || ''
    profile.address = account.address || ''
    currentPaymentMethod.value = account.payment_method || null
    currentPaymentDetails.value = account.payment_details || null
    paymentForm.payment = account.payment_method || ''
  } catch (err) {
    if (err.status === 401) {
      emit('need-login')
    } else {
      profileError.value = err.message || 'アカウント情報の取得に失敗しました。'
    }
  } finally {
    loading.value = false
  }
}

function validateProfile() {
  profileError.value = ''
  if (!profile.name.trim()) {
    profileError.value = '氏名を入力してください。'
    return false
  }
  if (!profile.email.trim()) {
    profileError.value = 'メールアドレスを入力してください。'
    return false
  }
  return true
}

async function saveProfile() {
  if (!validateProfile() || savingProfile.value) return
  savingProfile.value = true
  profileSuccess.value = ''
  profileError.value = ''
  try {
    const data = await updateAccount({
      name: profile.name.trim(),
      email: profile.email.trim(),
      address: profile.address.trim(),
    })
    const account = data.account || data.user
    if (account) {
      setUser(account)
      emit('user-updated', account)
    }
    profileSuccess.value = 'アカウント情報を更新しました。'
  } catch (err) {
    profileError.value = err.message || '更新に失敗しました。'
  } finally {
    savingProfile.value = false
  }
}

function validatePassword() {
  passwordErrors.current = ''
  passwordErrors.next = ''
  passwordErrors.confirm = ''
  let ok = true
  if (!passwordForm.current) {
    passwordErrors.current = '現在のパスワードを入力してください。'
    ok = false
  }
  if (!passwordForm.next) {
    passwordErrors.next = '新しいパスワードを入力してください。'
    ok = false
  } else if (passwordForm.next.length < 8) {
    passwordErrors.next = '8文字以上で設定してください。'
    ok = false
  }
  if (passwordForm.next !== passwordForm.confirm) {
    passwordErrors.confirm = 'パスワードが一致しません。'
    ok = false
  }
  return ok
}

async function savePassword() {
  if (!validatePassword() || savingPassword.value) return
  savingPassword.value = true
  passwordSuccess.value = ''
  passwordError.value = ''
  try {
    await changeAccountPassword({
      current_password: passwordForm.current,
      new_password: passwordForm.next,
    })
    passwordForm.current = ''
    passwordForm.next = ''
    passwordForm.confirm = ''
    passwordSuccess.value = 'パスワードを変更しました。'
  } catch (err) {
    passwordError.value = err.message || 'パスワードの変更に失敗しました。'
  } finally {
    savingPassword.value = false
  }
}

function buildPaymentDetails() {
  if (paymentForm.payment === 'credit') {
    return {
      card_number: paymentForm.cardNumber,
      card_expiry: paymentForm.cardExpiry,
      card_name: paymentForm.cardName,
    }
  }
  if (paymentForm.payment === 'bank') {
    return {
      bank_name: paymentForm.bankName,
      bank_branch: paymentForm.bankBranch,
      bank_account_type: paymentForm.bankAccountType,
      bank_account_number: paymentForm.bankAccountNumber,
      bank_account_holder: paymentForm.bankAccountHolder,
    }
  }
  if (paymentForm.payment === 'conveni') {
    return { conveni_store: paymentForm.conveniStore }
  }
  if (paymentForm.payment === 'carrier') {
    return { carrier_name: paymentForm.carrierName }
  }
  return {}
}

async function savePayment() {
  paymentErrors.payment = ''
  paymentError.value = ''
  paymentSuccess.value = ''
  if (!paymentForm.payment) {
    paymentErrors.payment = '支払い方法を選択してください。'
    return
  }
  savingPayment.value = true
  try {
    const data = await updateAccountPayment({
      payment_method: paymentForm.payment,
      payment_details: buildPaymentDetails(),
    })
    currentPaymentMethod.value = data.payment_method
    currentPaymentDetails.value = data.payment_details
    paymentSuccess.value = data.message || '支払い方法を更新しました。'
    paymentForm.cardNumber = ''
    paymentForm.cardCvc = ''
  } catch (err) {
    paymentError.value = err.message || '支払い方法の更新に失敗しました。'
  } finally {
    savingPayment.value = false
  }
}

async function changePlan(toPremium) {
  if (savingMembership.value) return
  membershipError.value = ''
  membershipSuccess.value = ''
  savingMembership.value = true
  try {
    const data = await updateAccountMembership({ is_premium: toPremium })
    if (data.account) {
      setUser(data.account)
      emit('user-updated', data.account)
    }
    membershipSuccess.value = data.message || '会員プランを変更しました。'
  } catch (err) {
    membershipError.value = err.message || 'プランの変更に失敗しました。'
  } finally {
    savingMembership.value = false
  }
}

async function onLogout() {
  await logout()
  emit('logout')
}

watch(isLoggedIn, (loggedIn) => {
  if (loggedIn) loadAccount()
})

onMounted(() => {
  if (isLoggedIn.value) loadAccount()
  else loading.value = false
})
</script>

<template>
  <div class="fc-account">
    <div v-if="!isLoggedIn" class="fc-account__guest">
      <p class="fc-account__guest-text">
        アカウント情報の確認・変更にはログインが必要です。
      </p>
      <UiButton variant="primary" size="md" @click="emit('need-login')">
        ログインする
      </UiButton>
    </div>

    <div v-else-if="loading" class="fc-account__loading">読み込み中…</div>

    <template v-else>
      <section class="fc-account__summary">
        <h3 class="fc-account__heading">会員情報</h3>
        <dl class="fc-account__dl">
          <div class="fc-account__row">
            <dt>会員ID</dt>
            <dd>{{ user?.account_id ?? '—' }}</dd>
          </div>
          <div class="fc-account__row">
            <dt>会員プラン</dt>
            <dd>{{ MEMBERSHIP_LABELS[membership] }}</dd>
          </div>
          <div class="fc-account__row">
            <dt>氏名</dt>
            <dd>{{ profile.name || '—' }}</dd>
          </div>
          <div class="fc-account__row">
            <dt>メールアドレス</dt>
            <dd>{{ profile.email || '—' }}</dd>
          </div>
          <div class="fc-account__row">
            <dt>住所</dt>
            <dd>{{ profile.address || '—' }}</dd>
          </div>
          <div class="fc-account__row">
            <dt>支払い方法</dt>
            <dd>{{ currentPaymentSummary() }}</dd>
          </div>
        </dl>
      </section>

      <section class="fc-account__section">
        <h3 class="fc-account__heading">会員プラン</h3>
        <p class="fc-account__plan-text">
          現在: <strong>{{ MEMBERSHIP_LABELS[membership] }}</strong>
        </p>
        <div class="fc-account__plan-actions">
          <UiButton
            v-if="!isPremium"
            variant="primary"
            size="md"
            :disabled="savingMembership"
            @click="changePlan(true)"
          >
            プレミアムに変更
          </UiButton>
          <UiButton
            v-else
            variant="outline"
            size="md"
            :disabled="savingMembership"
            @click="changePlan(false)"
          >
            一般会員に変更
          </UiButton>
        </div>
        <p v-if="membershipError" class="fc-account__error">{{ membershipError }}</p>
        <p v-if="membershipSuccess" class="fc-account__success">{{ membershipSuccess }}</p>
      </section>

      <section class="fc-account__section">
        <h3 class="fc-account__heading">支払い方法の変更</h3>
        <form class="fc-account__form" @submit.prevent="savePayment">
          <RegisterOptionGroup
            v-model="paymentForm.payment"
            name="acct-payment"
            label="支払い方法"
            :options="paymentOptions"
            :columns="1"
            :error="paymentErrors.payment"
            required
          />
          <div v-if="paymentForm.payment" class="fc-account__payment-detail">
            <PaymentCreditForm v-if="paymentForm.payment === 'credit'" :form="paymentForm" :errors="paymentErrors" />
            <PaymentBankForm v-else-if="paymentForm.payment === 'bank'" :form="paymentForm" :errors="paymentErrors" />
            <PaymentConveniForm v-else-if="paymentForm.payment === 'conveni'" :form="paymentForm" :errors="paymentErrors" />
            <PaymentCarrierForm v-else-if="paymentForm.payment === 'carrier'" :form="paymentForm" :errors="paymentErrors" />
          </div>
          <p v-if="paymentError" class="fc-account__error">{{ paymentError }}</p>
          <p v-if="paymentSuccess" class="fc-account__success">{{ paymentSuccess }}</p>
          <UiButton variant="outline" size="md" type="submit" :disabled="savingPayment">
            {{ savingPayment ? '更新中…' : '支払い方法を更新' }}
          </UiButton>
        </form>
      </section>

      <section class="fc-account__section">
        <h3 class="fc-account__heading">プロフィール編集</h3>
        <form class="fc-account__form" @submit.prevent="saveProfile">
          <RegisterField
            id="acct-name"
            v-model="profile.name"
            label="氏名"
            placeholder="お名前"
            autocomplete="name"
            required
          />
          <RegisterField
            id="acct-email"
            v-model="profile.email"
            label="メールアドレス"
            type="email"
            placeholder="example@misorahibari.com"
            autocomplete="email"
            required
          />
          <RegisterField
            id="acct-address"
            v-model="profile.address"
            label="住所"
            placeholder="都道府県・市区町村・番地"
            autocomplete="street-address"
          />
          <p v-if="profileError" class="fc-account__error">{{ profileError }}</p>
          <p v-if="profileSuccess" class="fc-account__success">{{ profileSuccess }}</p>
          <UiButton variant="primary" size="md" type="submit" :disabled="savingProfile">
            {{ savingProfile ? '保存中…' : '変更を保存' }}
          </UiButton>
        </form>
      </section>

      <section class="fc-account__section">
        <h3 class="fc-account__heading">パスワード変更</h3>
        <form class="fc-account__form" @submit.prevent="savePassword">
          <RegisterField
            id="acct-pw-current"
            v-model="passwordForm.current"
            label="現在のパスワード"
            type="password"
            autocomplete="current-password"
            :error="passwordErrors.current"
            required
          />
          <RegisterField
            id="acct-pw-next"
            v-model="passwordForm.next"
            label="新しいパスワード"
            type="password"
            autocomplete="new-password"
            hint="半角英数字8文字以上"
            :error="passwordErrors.next"
            required
          />
          <RegisterField
            id="acct-pw-confirm"
            v-model="passwordForm.confirm"
            label="新しいパスワード（確認）"
            type="password"
            autocomplete="new-password"
            :error="passwordErrors.confirm"
            required
          />
          <p v-if="passwordError" class="fc-account__error">{{ passwordError }}</p>
          <p v-if="passwordSuccess" class="fc-account__success">{{ passwordSuccess }}</p>
          <UiButton variant="outline" size="md" type="submit" :disabled="savingPassword">
            {{ savingPassword ? '変更中…' : 'パスワードを変更' }}
          </UiButton>
        </form>
      </section>

      <section class="fc-account__section fc-account__section--logout">
        <UiButton variant="ghost" size="md" @click="onLogout">ログアウト</UiButton>
      </section>
    </template>
  </div>
</template>

<style scoped>
.fc-account {
  display: flex;
  flex-direction: column;
  gap: var(--sp-6);
}
.fc-account__guest,
.fc-account__loading {
  padding: 32px 24px;
  text-align: center;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  background: var(--site-surface-muted);
}
.fc-account__guest-text {
  margin: 0 0 16px;
  font-size: 14px;
  line-height: 1.8;
  color: var(--site-text-muted);
}
.fc-account__summary,
.fc-account__section {
  padding: 24px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  background: var(--site-surface);
}
.fc-account__heading {
  margin: 0 0 16px;
  font-family: var(--ff-mincho);
  font-size: 16px;
  font-weight: 700;
  color: var(--murasaki-700);
}
.fc-account__dl {
  margin: 0;
}
.fc-account__row {
  display: flex;
  gap: 16px;
  padding: 10px 0;
  border-bottom: 1px solid var(--site-border);
}
.fc-account__row:last-child {
  border-bottom: 0;
}
.fc-account__row dt {
  flex: 0 0 120px;
  font-size: 12px;
  color: var(--site-text-light);
}
.fc-account__row dd {
  margin: 0;
  flex: 1;
  font-size: 13px;
  color: var(--site-text);
  word-break: break-all;
}
.fc-account__form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 480px;
}
.fc-account__error {
  margin: 0;
  font-size: 12px;
  color: #c0453b;
}
.fc-account__success {
  margin: 0;
  font-size: 12px;
  color: #2d6a4f;
}
.fc-account__section--logout {
  text-align: center;
  background: var(--site-surface-muted);
}
.fc-account__plan-text {
  margin: 0 0 12px;
  font-size: 13px;
  color: var(--site-text-muted);
}
.fc-account__plan-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.fc-account__payment-detail {
  margin-top: 8px;
}
</style>
