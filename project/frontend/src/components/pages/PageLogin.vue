<script setup>
/**
 * ページ: ログイン
 * 構成: 背景装飾 / 見出し / フォームカード
 */
import LoginHeroBackground from './login/LoginHeroBackground.vue'
import LoginFormCard from './login/LoginFormCard.vue'

const emit = defineEmits(['open-auth', 'login-success'])
</script>

<template>
  <div class="page-login">
    <section class="page-login__hero" aria-labelledby="login-page-title">
      <LoginHeroBackground />

      <div class="page-login__inner">
        <header class="page-login__head">
          <h1 id="login-page-title" class="page-login__title">ログイン</h1>
          <p class="page-login__subtitle">Login</p>
          <p class="page-login__lead">
            会員の方は、登録したメールアドレスとパスワードでログインしてください。
          </p>
        </header>

        <LoginFormCard
          @open-auth="(m) => emit('open-auth', m)"
          @success="(user) => emit('login-success', user)"
        />
      </div>
    </section>
  </div>
</template>

<style scoped>
.page-login {
  color: var(--site-text);
  overflow-x: hidden;
}
.page-login__hero {
  position: relative;
  width: 100vw;
  max-width: none;
  left: 50%;
  margin-left: -50vw;
  min-height: min(780px, calc(100vh - 200px));
  padding: 56px 24px 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: visible;
}
.page-login__inner {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 520px;
}
.page-login__head {
  text-align: center;
  margin-bottom: 32px;
}
.page-login__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: clamp(32px, 4vw, 42px);
  font-weight: 800;
  letter-spacing: 0.12em;
  color: var(--murasaki-700);
  line-height: 1.3;
}
.page-login__subtitle {
  margin: 6px 0 16px;
  font-family: var(--ff-latin);
  font-style: italic;
  font-size: 15px;
  letter-spacing: 0.18em;
  color: var(--kin-600);
}
.page-login__lead {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.75;
  letter-spacing: 0.04em;
  color: var(--site-text-muted);
}

@media (max-width: 767px) {
  .page-login__hero {
    min-height: auto;
    padding: 32px 16px 40px;
  }
  .page-login__head {
    margin-bottom: 24px;
  }
  .page-login__inner {
    max-width: 100%;
  }
}
</style>
