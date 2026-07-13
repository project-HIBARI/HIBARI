<script setup>
/**
 * 部品名: 献花 — AI 美空ひばりカード
 * 用途: 献花ページ下部から AI チャット機能へ誘導する
 */
import UiCard from '../../ui/UiCard.vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'

const emit = defineEmits(['open-ai'])
</script>

<template>
  <section class="message-ai" aria-label="AI美空ひばり">
    <UiCard tone="purple" padding="lg" class="message-ai__card">
      <div class="message-ai__inner">
        <div class="message-ai__copy">
          <span class="message-ai__badge">新機能</span>
          <h3 class="message-ai__title">AI美空ひばりに、想いを伝えてみよう</h3>
          <p class="message-ai__desc">
            好きな曲のエピソードや献花の想いなど、
            美空ひばりへのメッセージについて AI 美空ひばりと会話できます。
          </p>
        </div>
        <UiButton variant="gold" size="md" class="message-ai__btn" @click="emit('open-ai')">
          <UiIco name="chat" :size="16" color="var(--ink-900)" />
          AI美空ひばりと話す
        </UiButton>
      </div>
    </UiCard>
  </section>
</template>

<style scoped>
.message-ai {
  margin-bottom: var(--sp-7);
}
.message-ai__card {
  background:
    radial-gradient(ellipse at 0% 50%, rgba(255, 255, 255, 0.08) 0%, transparent 50%),
    linear-gradient(135deg, var(--murasaki-800) 0%, var(--murasaki-700) 100%);
}
.message-ai__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-5);
  flex-wrap: wrap;
}
.message-ai__badge {
  display: inline-block;
  padding: 3px 10px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 999px;
  font-size: 11px;
  letter-spacing: 0.08em;
  margin-bottom: 10px;
}
.message-ai__title {
  margin: 0 0 8px;
  font-family: var(--ff-mincho);
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--paper-50);
}
.message-ai__desc {
  margin: 0;
  font-size: 13px;
  line-height: 1.75;
  color: rgba(255, 255, 255, 0.85);
  max-width: 520px;
}
.message-ai__btn {
  flex-shrink: 0;
}

@media (max-width: 600px) {
  .message-ai__inner {
    flex-direction: column;
    align-items: stretch;
  }
  .message-ai__btn {
    width: 100%;
  }
}
</style>
