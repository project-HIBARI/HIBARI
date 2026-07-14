<script setup>
/**
 * ページ: ログイン
 */
import LoginHeroBackground from './login/LoginHeroBackground.vue'
import PlatformAuthBackground from '../layout/PlatformAuthBackground.vue'
import LoginFormCard from './login/LoginFormCard.vue'
import MusicMemoriesLogo from '../brand/MusicMemoriesLogo.vue'
import { SITE_NAME, SITE_TAGLINE } from '../../constants/site.js'

defineProps({
  /** platform = Music Memories */
  variant: { type: String, default: 'platform' },
})

const emit = defineEmits(['open-auth', 'login-success'])
</script>

<template>
  <div class="page-login" :class="{ 'page-login--platform': variant === 'platform' }">
    <section class="page-login__hero" aria-labelledby="login-page-title">
      <PlatformAuthBackground v-if="variant === 'platform'" />
      <LoginHeroBackground v-else />

      <div class="page-login__inner">
        <header class="page-login__head">
          <div v-if="variant === 'platform'" class="page-login__brand-row">
            <MusicMemoriesLogo variant="full" size="hero" />
          </div>
          <h1 id="login-page-title" class="page-login__title">ログイン</h1>
          <p class="page-login__subtitle">Login</p>
          <p class="page-login__lead">
            <template v-if="variant === 'platform'">
              {{ SITE_NAME }} 会員の方は、登録したメールアドレスとパスワードでログインしてください。
            </template>
            <template v-else>
              会員の方は、登録したメールアドレスとパスワードでログインしてください。
            </template>
          </p>
          <p v-if="variant === 'platform'" class="page-login__tagline">{{ SITE_TAGLINE }}</p>
        </header>

        <LoginFormCard
          :platform="variant === 'platform'"
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

.page-login--platform {
  color: #f8f4ef;
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

.page-login--platform .page-login__hero {
  min-height: calc(100vh - 72px);
  padding: 72px 24px 80px;
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

.page-login__brand-row {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.page-login__brand-row :deep(.mm-logo--full) {
  max-height: clamp(52px, 10vw, 80px);
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

.page-login--platform .page-login__title {
  color: #f8f4ef;
}

.page-login__subtitle {
  margin: 6px 0 16px;
  font-family: var(--ff-latin);
  font-style: italic;
  font-size: 15px;
  letter-spacing: 0.18em;
  color: var(--kin-600);
}

.page-login--platform .page-login__subtitle {
  color: var(--kin-400);
}

.page-login__lead {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.75;
  letter-spacing: 0.04em;
  color: var(--site-text-muted);
}

.page-login--platform .page-login__lead {
  color: rgba(248, 244, 239, 0.72);
}

.page-login__tagline {
  margin: 12px 0 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  letter-spacing: 0.16em;
  color: rgba(201, 169, 97, 0.85);
}

@media (max-width: 767px) {
  .page-login__hero {
    min-height: auto;
    padding: 32px 16px 40px;
  }

  .page-login--platform .page-login__hero {
    padding: 56px 16px 48px;
  }

  .page-login__head {
    margin-bottom: 24px;
  }

  .page-login__inner {
    max-width: 100%;
  }
}
</style>
