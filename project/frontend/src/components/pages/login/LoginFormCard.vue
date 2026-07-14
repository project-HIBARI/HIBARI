<script setup>
/**
 * 部品名: ログインフォームカード
 * 用途: 金枠・角飾り付きのログインフォーム UI
 */
import { ref } from 'vue'
import UiIco from '../../ui/UiIco.vue'
import { useAuth } from '../../../composables/useAuth.js'

defineProps({
  platform: { type: Boolean, default: false },
})

const emit = defineEmits(['open-auth', 'success'])

const { login } = useAuth()

const email = ref('')
const password = ref('')
const remember = ref(false)
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

async function onSubmit(e) {
  e.preventDefault()
  if (loading.value) return

  error.value = ''
  const emailVal = email.value.trim()
  const passwordVal = password.value

  if (!emailVal) {
    error.value = 'メールアドレスを入力してください。'
    return
  }
  if (!passwordVal) {
    error.value = 'パスワードを入力してください。'
    return
  }

  loading.value = true
  try {
    const result = await login(emailVal, passwordVal)
    emit('success', result.user)
  } catch (err) {
    if (err.status === 401) {
      error.value = 'メールアドレスまたはパスワードが正しくありません。'
    } else if (
      err.status === 0 ||
      err.message?.includes('サーバーに接続できません') ||
      err.message?.includes('Failed to fetch') ||
      err.message?.includes('NetworkError')
    ) {
      error.value =
        'サーバーに接続できません。別のターミナルで `cd project` → `python app.py` を実行してください。'
    } else {
      error.value = err.message || 'ログインに失敗しました。'
    }
  } finally {
    loading.value = false
  }
}

function onForgotPassword() {
  emit('open-auth', 'forgot-password')
}
</script>

<template>
  <div class="login-card" :class="{ 'login-card--platform': platform }">
    <span class="login-card__corner login-card__corner--tl" aria-hidden="true" />
    <span class="login-card__corner login-card__corner--tr" aria-hidden="true" />
    <span class="login-card__corner login-card__corner--bl" aria-hidden="true" />
    <span class="login-card__corner login-card__corner--br" aria-hidden="true" />

    <form class="login-card__form" @submit="onSubmit">
      <div class="login-card__field">
        <label class="login-card__label" for="login-email">メールアドレス</label>
        <input
          id="login-email"
          v-model="email"
          type="email"
          class="login-card__input"
          placeholder="メールアドレスを入力してください"
          autocomplete="email"
        />
      </div>

      <div class="login-card__field">
        <label class="login-card__label" for="login-password">パスワード</label>
        <div class="login-card__password-wrap">
          <input
            id="login-password"
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            class="login-card__input login-card__input--password"
            placeholder="パスワードを入力してください"
            autocomplete="current-password"
          />
          <button
            type="button"
            class="login-card__toggle-pw"
            :aria-label="showPassword ? 'パスワードを隠す' : 'パスワードを表示'"
            @click="showPassword = !showPassword"
          >
            <UiIco :name="showPassword ? 'eye-off' : 'eye'" :size="18" color="var(--site-text-light)" />
          </button>
        </div>
      </div>

      <div class="login-card__row">
        <label class="login-card__check">
          <input v-model="remember" type="checkbox" class="login-card__checkbox" />
          <span>ログインしたままにする</span>
        </label>
        <button type="button" class="login-card__forgot" @click="onForgotPassword">
          パスワードをお忘れの方はこちら
        </button>
      </div>

      <p v-if="error" class="login-card__error" role="alert">{{ error }}</p>

      <button type="submit" class="login-card__submit" :disabled="loading">
        <UiIco name="flower" :size="16" color="#fff" />
        {{ loading ? 'ログイン中…' : 'ログイン' }}
      </button>
    </form>

    <div class="login-card__register">
      <hr class="login-card__divider" />
      <h2 class="login-card__register-title">会員登録がお済みでない方</h2>
      <p class="login-card__register-desc">
        新規会員登録で、限定コンテンツや会員特典をご利用いただけます。
      </p>
      <button type="button" class="login-card__register-btn" @click="emit('open-auth', 'register')">
        新規会員登録はこちら
        <span aria-hidden="true">›</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.login-card {
  position: relative;
  width: 100%;
  max-width: 520px;
  margin: 0 auto;
  padding: 40px 48px 36px;
  background: rgba(255, 254, 251, 0.92);
  border: 1px solid var(--kin-500);
  box-shadow: var(--site-shadow-md);
}
.login-card__corner {
  position: absolute;
  width: 28px;
  height: 28px;
  border-color: var(--kin-500);
  border-style: solid;
  opacity: 0.85;
}
.login-card__corner--tl {
  top: 10px;
  left: 10px;
  border-width: 2px 0 0 2px;
}
.login-card__corner--tr {
  top: 10px;
  right: 10px;
  border-width: 2px 2px 0 0;
}
.login-card__corner--bl {
  bottom: 10px;
  left: 10px;
  border-width: 0 0 2px 2px;
}
.login-card__corner--br {
  bottom: 10px;
  right: 10px;
  border-width: 0 2px 2px 0;
}
.login-card__corner::after {
  content: '❧';
  position: absolute;
  font-size: 14px;
  color: var(--kin-600);
  line-height: 1;
}
.login-card__corner--tl::after {
  top: -4px;
  left: -2px;
  transform: rotate(-45deg);
}
.login-card__corner--tr::after {
  top: -4px;
  right: -2px;
  transform: rotate(45deg) scaleX(-1);
}
.login-card__corner--bl::after {
  bottom: -4px;
  left: -2px;
  transform: rotate(45deg) scaleY(-1);
}
.login-card__corner--br::after {
  bottom: -4px;
  right: -2px;
  transform: rotate(-45deg) scale(-1);
}
.login-card__form {
  display: flex;
  flex-direction: column;
  gap: 22px;
}
.login-card__field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.login-card__label {
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.04em;
  color: var(--site-text);
}
.login-card__input {
  width: 100%;
  padding: 14px 16px;
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  color: var(--site-text);
  background: #f5f2ee;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
  transition: border-color 0.2s, box-shadow 0.2s;
}
.login-card__input::placeholder {
  color: var(--site-text-light);
}
.login-card__input:focus {
  outline: none;
  border-color: var(--murasaki-400);
  box-shadow: 0 0 0 3px rgba(122, 80, 136, 0.12);
}
.login-card__password-wrap {
  position: relative;
}
.login-card__input--password {
  padding-right: 48px;
}
.login-card__toggle-pw {
  position: absolute;
  top: 50%;
  right: 12px;
  transform: translateY(-50%);
  background: transparent;
  border: 0;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.login-card__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
.login-card__check {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  color: var(--site-text-muted);
  cursor: pointer;
}
.login-card__checkbox {
  width: 16px;
  height: 16px;
  accent-color: var(--murasaki-600);
  cursor: pointer;
}
.login-card__forgot {
  background: transparent;
  border: 0;
  padding: 0;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  color: var(--site-text-muted);
  text-decoration: underline;
  cursor: pointer;
  letter-spacing: 0.02em;
}
.login-card__forgot:hover {
  color: var(--murasaki-700);
}
.login-card__error {
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
.login-card__submit {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  margin-top: 4px;
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
.login-card__submit:hover {
  background: var(--murasaki-800);
}
.login-card__submit:disabled {
  opacity: 0.7;
  cursor: wait;
}
.login-card__register {
  margin-top: 28px;
  text-align: center;
}
.login-card__divider {
  border: 0;
  height: 1px;
  background: var(--site-border);
  margin: 0 0 24px;
}
.login-card__register-title {
  margin: 0 0 10px;
  font-family: var(--ff-mincho);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--site-text);
}
.login-card__register-desc {
  margin: 0 0 18px;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  line-height: 1.75;
  color: var(--site-text-muted);
}
.login-card__register-btn {
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
.login-card__register-btn:hover {
  border-color: var(--murasaki-400);
  background: var(--murasaki-100);
}

.login-card--platform {
  background: rgba(32, 26, 32, 0.82);
  border: 1px solid rgba(201, 169, 97, 0.45);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(12px);
  border-radius: var(--site-radius-lg);
}

.login-card--platform .login-card__corner {
  border-color: var(--kin-400);
}

.login-card--platform .login-card__corner::after {
  color: var(--kin-400);
}

.login-card--platform .login-card__label,
.login-card--platform .login-card__check span,
.login-card--platform .login-card__register-title {
  color: rgba(248, 244, 239, 0.88);
}

.login-card--platform .login-card__input {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.16);
  color: #f8f4ef;
}

.login-card--platform .login-card__input::placeholder {
  color: rgba(248, 244, 239, 0.38);
}

.login-card--platform .login-card__forgot {
  color: var(--kin-400);
}

.login-card--platform .login-card__register-desc {
  color: rgba(248, 244, 239, 0.58);
}

.login-card--platform .login-card__register-btn {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.2);
  color: #f8f4ef;
}

.login-card--platform .login-card__register-btn:hover {
  background: rgba(122, 80, 136, 0.35);
  border-color: var(--kin-400);
}

.login-card--platform .login-card__divider {
  background: rgba(255, 255, 255, 0.12);
}

.login-card--platform .login-card__error {
  background: rgba(155, 44, 44, 0.2);
  border-color: rgba(240, 196, 190, 0.35);
  color: #ffb4a8;
}

@media (max-width: 767px) {
  .login-card {
    padding: 32px 20px 28px;
    max-width: 100%;
  }
  .login-card__row {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
