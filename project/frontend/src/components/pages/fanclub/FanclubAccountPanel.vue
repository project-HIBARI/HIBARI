<script setup>
/**
 * 部品名: ファンクラブ アカウント管理
 * 用途: 会員ページでプロフィール表示・編集・パスワード変更・ログアウト
 */
import { ref, reactive, watch, onMounted } from 'vue'
import UiButton from '../../ui/UiButton.vue'
import RegisterField from '../register/RegisterField.vue'
import { fetchAccount, updateAccount, changeAccountPassword } from '../../../api/account.js'
import { useMemberAccess } from '../../../composables/useMemberAccess.js'
import { MEMBERSHIP_LABELS } from '../../../constants/membership.js'

const emit = defineEmits(['need-login', 'logout'])

const { isLoggedIn, membership, user, setUser, logout } = useMemberAccess()

const loading = ref(true)
const profileError = ref('')
const profileSuccess = ref('')
const passwordError = ref('')
const passwordSuccess = ref('')
const savingProfile = ref(false)
const savingPassword = ref(false)

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
    if (account) setUser(account)
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
        </dl>
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
</style>
