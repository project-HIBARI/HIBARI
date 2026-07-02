<script setup>
/**
 * 部品名: ホーム — AI美空ひばりカード
 * 用途: ヒーローエリア内で AI チャット機能への導線を表示する
 */
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'

const emit = defineEmits(['open-ai'])
</script>

<template>
  <aside class="top-ai-card" aria-label="AI美空ひばり">
    <span class="top-ai-card__badge">新機能</span>
    <div class="top-ai-card__head">
      <div>
        <h3 class="top-ai-card__title">AI美空ひばり</h3>
        <p class="top-ai-card__desc">美空ひばりと、いつでも会話を楽しめます。</p>
      </div>
      <div class="top-ai-card__avatar" aria-hidden="true">
        <span class="top-ai-card__avatar-inner">雲</span>
      </div>
    </div>

    <div class="top-ai-card__bubbles">
      <p class="top-ai-card__bubble">こんにちは！今日どんなお話をしましょうか？</p>
      <p class="top-ai-card__bubble top-ai-card__bubble--alt">ひばりさんの好きな歌は？</p>
      <p class="top-ai-card__bubble">また会えてうれしいわ。</p>
    </div>

    <UiButton variant="primary" size="md" class="top-ai-card__btn" @click="emit('open-ai')">
      <UiIco name="chat" :size="16" color="#fff" />
      AI美空ひばりと話す
    </UiButton>
  </aside>
</template>

<style scoped>
.top-ai-card {
  position: relative;
  background: linear-gradient(165deg, #fff 0%, #fff5f8 55%, #fceef2 100%);
  border: 1px solid rgba(122, 80, 136, 0.15);
  border-radius: var(--site-radius-lg);
  padding: 22px 20px 20px;
  box-shadow: 0 8px 28px rgba(90, 60, 80, 0.1);
  max-width: 320px;
  width: 100%;
}
.top-ai-card__badge {
  display: inline-block;
  padding: 3px 10px;
  background: var(--murasaki-700);
  color: #fff;
  border-radius: 999px;
  font-family: var(--ff-sans-jp);
  font-size: 10px;
  letter-spacing: 0.1em;
  margin-bottom: 12px;
}
.top-ai-card__head {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  margin-bottom: 14px;
}
.top-ai-card__title {
  margin: 0 0 6px;
  font-family: var(--ff-mincho);
  font-size: 21px;
  font-weight: 700;
  color: var(--murasaki-700);
  letter-spacing: 0.06em;
}
.top-ai-card__desc {
  margin: 0;
  font-size: 12px;
  line-height: 1.7;
  color: var(--site-text-muted);
}
.top-ai-card__avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 2px solid var(--kin-500);
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(60, 40, 30, 0.12);
  background: linear-gradient(135deg, var(--site-bg-pink), var(--site-surface-muted));
  display: flex;
  align-items: center;
  justify-content: center;
}
.top-ai-card__avatar-inner {
  font-family: var(--ff-mincho);
  font-size: 20px;
  font-weight: 700;
  color: var(--murasaki-700);
}
.top-ai-card__bubbles {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}
.top-ai-card__bubble {
  margin: 0;
  padding: 9px 12px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid var(--site-border);
  border-radius: 14px 14px 14px 4px;
  font-size: 11px;
  line-height: 1.55;
  color: var(--site-text);
  max-width: 92%;
}
.top-ai-card__bubble--alt {
  align-self: flex-end;
  border-radius: 14px 14px 4px 14px;
  background: var(--murasaki-100);
  border-color: rgba(122, 80, 136, 0.18);
  max-width: 88%;
}
.top-ai-card__btn {
  width: 100%;
  border-radius: 999px;
}

@media (max-width: 767px) {
  .top-ai-card {
    max-width: none;
  }
}
</style>
