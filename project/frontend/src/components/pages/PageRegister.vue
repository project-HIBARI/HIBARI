<script setup>
/**
 * ページ: 新規会員登録
 * 構成: 背景装飾 / 見出し / フォームカード
 */
import LoginHeroBackground from './login/LoginHeroBackground.vue'
import RegisterFormCard from './register/RegisterFormCard.vue'

const emit = defineEmits(['navigate', 'open-auth'])
</script>

<template>
  <div class="page-login">
    <section class="page-login__hero" aria-labelledby="register-page-title">
      <LoginHeroBackground />

      <div class="page-login__inner">
        <header class="page-login__head">
          <h1 id="register-page-title" class="page-login__title">新規会員登録</h1>
          <p class="page-login__subtitle">Register</p>
          <p class="page-login__lead">
            会員登録を行うことで、限定コンテンツやイベント情報、ファンクラブ特典をご利用いただけます。
          </p>
        </header>

        <RegisterFormCard
          @navigate="(id) => emit('navigate', id)"
          @open-auth="(m) => emit('open-auth', m)"
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
  min-height: min(860px, calc(100vh - 200px));
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
  font-size: clamp(28px, 3.6vw, 40px);
  font-weight: 800;
  letter-spacing: 0.1em;
  color: var(--murasaki-700);
  line-height: 1.35;
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
