<script setup>
/**
 * ページ: 新規会員登録
 */
import LoginHeroBackground from './login/LoginHeroBackground.vue'
import PlatformAuthBackground from '../layout/PlatformAuthBackground.vue'
import RegisterFormCard from './register/RegisterFormCard.vue'
import MusicMemoriesLogo from '../brand/MusicMemoriesLogo.vue'
import { MEMBERSHIP } from '../../constants/membership.js'
import { SITE_NAME, SITE_TAGLINE } from '../../constants/site.js'

defineProps({
  initialPlan: { type: String, default: MEMBERSHIP.GENERAL },
  variant: { type: String, default: 'platform' },
})

const emit = defineEmits(['navigate', 'open-auth', 'complete'])
</script>

<template>
  <div class="page-login" :class="{ 'page-login--platform': variant === 'platform' }">
    <section class="page-login__hero" aria-labelledby="register-page-title">
      <PlatformAuthBackground v-if="variant === 'platform'" />
      <LoginHeroBackground v-else />

      <div class="page-login__inner page-login__inner--register">
        <header class="page-login__head">
          <div v-if="variant === 'platform'" class="page-login__brand-row">
            <MusicMemoriesLogo variant="full" size="hero" />
          </div>
          <h1 id="register-page-title" class="page-login__title">新規会員登録</h1>
          <p class="page-login__subtitle">Register</p>
          <p class="page-login__lead">
            {{ SITE_NAME }} でアカウントを作成し、ファンクラブ有料会員の特典をご利用いただけます。
          </p>
          <p v-if="variant === 'platform'" class="page-login__tagline">{{ SITE_TAGLINE }}</p>
        </header>

        <RegisterFormCard
          :initial-plan="initialPlan"
          :platform="variant === 'platform'"
          @navigate="(id) => emit('navigate', id)"
          @open-auth="(m) => emit('open-auth', m)"
          @complete="(user) => emit('complete', user)"
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
  min-height: min(860px, calc(100vh - 200px));
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

.page-login__inner--register {
  max-width: 680px;
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
  font-size: clamp(28px, 3.6vw, 40px);
  font-weight: 800;
  letter-spacing: 0.1em;
  color: var(--murasaki-700);
  line-height: 1.35;
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

  .page-login__inner,
  .page-login__inner--register {
    max-width: 100%;
  }
}
</style>
