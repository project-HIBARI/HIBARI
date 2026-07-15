<script setup>
/**
 * 部品名: 思い出 — AI 美空ひばりカード
 * 用途: 思い出ページ下部から AI チャット機能へ誘導する
 */
import UiCard from '../../ui/UiCard.vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'

const emit = defineEmits(['open-ai'])
</script>

<template>
  <section class="memories-ai" aria-label="AI美空ひばり">
    <UiCard tone="purple" padding="lg" class="memories-ai__card">
      <div class="memories-ai__inner">
        <div class="memories-ai__copy">
          <span class="memories-ai__badge">新機能</span>
          <h3 class="memories-ai__title">AI美空ひばりに、思い出を語ってみよう</h3>
          <p class="memories-ai__desc">
            舞台の名場面やファンの記憶など、
            美空ひばりの思い出について AI 美空ひばりと会話できます。
          </p>
        </div>
        <UiButton variant="gold" size="md" class="memories-ai__btn" @click="emit('open-ai')">
          <UiIco name="chat" :size="16" color="var(--ink-900)" />
          AI美空ひばりと話す
        </UiButton>
      </div>
    </UiCard>
  </section>
</template>

<style scoped>
.memories-ai {
  margin-bottom: var(--sp-7);
}
.memories-ai__card {
  background:
    radial-gradient(ellipse at 0% 50%, rgba(255, 255, 255, 0.08) 0%, transparent 50%),
    linear-gradient(135deg, var(--murasaki-800) 0%, var(--murasaki-700) 100%);
}
.memories-ai__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-5);
  flex-wrap: wrap;
}
.memories-ai__badge {
  display: inline-block;
  padding: 3px 10px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 999px;
  font-size: var(--font-size-caption);
  letter-spacing: 0.08em;
  margin-bottom: 10px;
}
.memories-ai__title {
  margin: 0 0 8px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-subtitle);
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--paper-50);
}
.memories-ai__desc {
  margin: 0;
  font-size: var(--font-size-button);
  line-height: 1.75;
  color: rgba(255, 255, 255, 0.85);
  max-width: 520px;
}
.memories-ai__btn {
  flex-shrink: 0;
}

@media (max-width: 600px) {
  .memories-ai__inner {
    flex-direction: column;
    align-items: stretch;
  }
  .memories-ai__btn {
    width: 100%;
  }
}
</style>
