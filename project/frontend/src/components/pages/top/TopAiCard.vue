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
  <!-- ヒーロー右側に配置する AI チャット風カード -->
  <aside class="top-ai-card" aria-label="AI美空ひばり">
    <span class="top-ai-card__badge">新機能</span>
    <h3 class="top-ai-card__title">AI美空ひばり</h3>
    <p class="top-ai-card__desc">美空ひばりと、いつでも会話を楽しめます。</p>

    <div class="top-ai-card__avatar" aria-hidden="true">
      <span class="top-ai-card__avatar-inner">雲</span>
    </div>

    <div class="top-ai-card__bubbles">
      <p class="top-ai-card__bubble">こんにちは！今日どんなお話をしましょうか？</p>
      <p class="top-ai-card__bubble top-ai-card__bubble--alt">ひばりさんの好きな歌は？</p>
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
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  padding: 24px 22px;
  box-shadow: var(--site-shadow-md);
  max-width: 300px;
}
.top-ai-card__badge {
  display: inline-block;
  padding: 3px 10px;
  background: var(--murasaki-100);
  color: var(--murasaki-700);
  border: 1px solid var(--murasaki-400);
  border-radius: 999px;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  letter-spacing: 0.08em;
  margin-bottom: 10px;
}
.top-ai-card__title {
  margin: 0 0 6px;
  font-family: var(--ff-mincho);
  font-size: 20px;
  font-weight: 700;
  color: var(--murasaki-700);
  letter-spacing: 0.06em;
}
.top-ai-card__desc {
  margin: 0 0 16px;
  font-size: 12px;
  line-height: 1.7;
  color: var(--site-text-muted);
}
.top-ai-card__avatar {
  position: absolute;
  top: 20px;
  right: 18px;
  width: 52px;
  height: 52px;
  border-radius: 50%;
  border: 2px solid var(--kin-500);
  background: linear-gradient(135deg, var(--site-bg-pink), var(--site-surface-muted));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(60, 40, 30, 0.1);
}
.top-ai-card__avatar-inner {
  font-family: var(--ff-mincho);
  font-size: 18px;
  font-weight: 700;
  color: var(--murasaki-700);
}
.top-ai-card__bubbles {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 18px;
}
.top-ai-card__bubble {
  margin: 0;
  padding: 10px 12px;
  background: var(--site-surface-muted);
  border: 1px solid var(--site-border);
  border-radius: 12px 12px 12px 4px;
  font-size: 12px;
  line-height: 1.6;
  color: var(--site-text);
}
.top-ai-card__bubble--alt {
  align-self: flex-end;
  border-radius: 12px 12px 4px 12px;
  background: var(--murasaki-100);
  border-color: rgba(122, 80, 136, 0.2);
  max-width: 85%;
}
.top-ai-card__btn {
  width: 100%;
}

@media (max-width: 767px) {
  .top-ai-card {
    max-width: none;
  }
}
</style>
