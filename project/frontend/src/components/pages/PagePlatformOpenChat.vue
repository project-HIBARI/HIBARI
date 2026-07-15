<script setup>
/**
 * ページ: Music Memories オープンチャット
 */
import FanclubOpenChat from './fanclub/FanclubOpenChat.vue'

const emit = defineEmits(['need-auth'])
</script>

<template>
  <div class="page-platform-chat">
    <header class="page-platform-chat__head">
      <h1 class="page-platform-chat__title">オープンチャット</h1>
      <p class="page-platform-chat__lead">
        複数アーティストのファンが集まり、音楽の思い出を語り合える交流スペースです。
      </p>
    </header>
    <FanclubOpenChat
      chat-scope="platform"
      platform-theme
      @need-auth="(mode) => emit('need-auth', mode)"
    />
  </div>
</template>

<style scoped>
.page-platform-chat {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px 64px;
}

.page-platform-chat__head {
  margin-bottom: 24px;
}

.page-platform-chat__title {
  margin: 0 0 10px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.5rem, 4vw, 2rem);
  color: #f8f4ef;
  letter-spacing: 0.08em;
}

.page-platform-chat__lead {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-small);
  line-height: 1.8;
  color: rgba(248, 244, 239, 0.7);
}

@media (max-width: 767px) {
  .page-platform-chat {
    padding: 16px 12px calc(var(--bottom-nav-height, 66px) + env(safe-area-inset-bottom, 0px) + 16px);
  }

  .page-platform-chat__head {
    margin-bottom: 12px;
  }

  .page-platform-chat__lead {
    display: none;
  }
}
</style>
