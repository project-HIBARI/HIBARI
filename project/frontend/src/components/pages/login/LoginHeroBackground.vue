<script setup>
/**
 * 部品名: ログインページ背景
 * 用途: グラデーション → 百合（左） → 肖像（右）の装飾レイヤー
 */
const portraitSrc = '/images/login/misorahibari-mike-image.png'
const liliesSrc = '/images/login/yuri-white.png'
</script>

<template>
  <div class="login-bg" aria-hidden="true">
    <div class="login-bg__gradient" />
    <figure class="login-bg__lilies">
      <img
        :src="liliesSrc"
        alt=""
        class="login-bg__lilies-img"
        width="480"
        height="720"
        decoding="async"
      />
    </figure>
    <figure class="login-bg__portrait">
      <img
        :src="portraitSrc"
        alt=""
        class="login-bg__portrait-img"
        width="480"
        height="640"
        decoding="async"
      />
    </figure>
  </div>
</template>

<style scoped>
.login-bg {
  position: absolute;
  inset: 0;
  overflow: visible;
  pointer-events: none;
  z-index: 0;
}
.login-bg__gradient {
  position: absolute;
  inset: 0;
  z-index: 0;
  background: linear-gradient(
    135deg,
    #faf8f4 0%,
    #f7f2ec 35%,
    #f0ebf5 70%,
    #ebe4f0 100%
  );
}
.login-bg__lilies {
  position: absolute;
  left: 0;
  bottom: 0;
  z-index: 1;
  margin: 0;
  width: min(480px, 38vw);
  max-height: 92%;
  transform: translateX(-6%);
  pointer-events: none;
}
.login-bg__lilies-img {
  display: block;
  width: 100%;
  height: auto;
  max-width: min(480px, 38vw);
  max-height: 100%;
  object-fit: contain;
  object-position: bottom left;
}
.login-bg__portrait {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 2;
  margin: 0;
  width: min(480px, 35vw);
  transform: translateX(8%);
  pointer-events: none;
}
.login-bg__portrait-img {
  display: block;
  width: 100%;
  height: auto;
  max-width: min(480px, 35vw);
  object-fit: contain;
  object-position: top right;
}

@media (max-width: 1023px) {
  .login-bg__lilies {
    width: min(360px, 32vw);
    transform: translateX(-4%);
  }
  .login-bg__lilies-img {
    max-width: min(360px, 32vw);
  }
  .login-bg__portrait {
    width: min(360px, 28vw);
    transform: translateX(5%);
  }
  .login-bg__portrait-img {
    max-width: min(360px, 28vw);
  }
}

@media (max-width: 767px) {
  .login-bg__lilies {
    width: min(220px, 40vw);
    transform: translateX(-8%);
    opacity: 0.7;
  }
  .login-bg__lilies-img {
    max-width: min(220px, 40vw);
  }
  .login-bg__portrait {
    width: min(220px, 42vw);
    transform: translateX(12%);
    opacity: 0.45;
  }
  .login-bg__portrait-img {
    max-width: min(220px, 42vw);
  }
}

@media (max-width: 480px) {
  .login-bg__lilies {
    display: none;
  }
  .login-bg__portrait {
    display: none;
  }
}
</style>
