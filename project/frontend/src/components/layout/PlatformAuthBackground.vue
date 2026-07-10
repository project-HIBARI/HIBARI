<script setup>
/**
 * Music Memories 認証ページ用背景
 */
</script>

<template>
  <div class="platform-auth-bg" aria-hidden="true">
    <div class="platform-auth-bg__gradient" />
    <div class="platform-auth-bg__glow platform-auth-bg__glow--left" />
    <div class="platform-auth-bg__glow platform-auth-bg__glow--right" />
    <div class="platform-auth-bg__grid" />
  </div>
</template>

<style scoped>
.platform-auth-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.platform-auth-bg__gradient {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 70% 55% at 50% -5%, rgba(122, 80, 136, 0.28), transparent 58%),
    linear-gradient(180deg, #1a1418 0%, #231b22 45%, #2a2228 100%);
}

.platform-auth-bg__glow {
  position: absolute;
  width: min(480px, 60vw);
  height: min(480px, 60vw);
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.35;
}

.platform-auth-bg__glow--left {
  top: 10%;
  left: -8%;
  background: var(--murasaki-700);
}

.platform-auth-bg__glow--right {
  bottom: 5%;
  right: -10%;
  background: var(--kin-600);
}

.platform-auth-bg__grid {
  position: absolute;
  inset: 0;
  opacity: 0.06;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.5) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.5) 1px, transparent 1px);
  background-size: 48px 48px;
}
</style>
