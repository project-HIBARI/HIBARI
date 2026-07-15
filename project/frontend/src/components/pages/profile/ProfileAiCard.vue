<script setup>
/**
 * 部品名: 歩み — AI 美空ひばりカード
 * 用途: 歩みページ下部から AI チャット機能へ誘導する
 */
import UiCard from '../../ui/UiCard.vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'

const emit = defineEmits(['open-ai'])
</script>

<template>
  <section class="profile-ai" aria-label="AI美空ひばり">
    <UiCard tone="purple" padding="lg" class="profile-ai__card">
      <div class="profile-ai__inner">
        <div class="profile-ai__copy">
          <span class="profile-ai__badge">新機能</span>
          <h3 class="profile-ai__title">AI美空ひばりに、歩みを聞いてみよう</h3>
          <p class="profile-ai__desc">
            デビューの舞台やレコード大賞のエピソードなど、
            美空ひばりの生涯について AI 美空ひばりと会話できます。
          </p>
        </div>
        <UiButton variant="gold" size="md" class="profile-ai__btn" @click="emit('open-ai')">
          <UiIco name="chat" :size="16" color="var(--ink-900)" />
          AI美空ひばりと話す
        </UiButton>
      </div>
    </UiCard>
  </section>
</template>

<style scoped>
.profile-ai {
  margin-bottom: var(--sp-7);
}
.profile-ai__card {
  background:
    radial-gradient(ellipse at 0% 50%, rgba(255, 255, 255, 0.08) 0%, transparent 50%),
    linear-gradient(135deg, var(--murasaki-800) 0%, var(--murasaki-700) 100%);
}
.profile-ai__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-5);
  flex-wrap: wrap;
}
.profile-ai__badge {
  display: inline-block;
  padding: 3px 10px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 999px;
  font-size: var(--font-size-caption);
  letter-spacing: 0.08em;
  margin-bottom: 10px;
}
.profile-ai__title {
  margin: 0 0 8px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-subtitle);
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--paper-50);
}
.profile-ai__desc {
  margin: 0;
  font-size: var(--font-size-button);
  line-height: 1.75;
  color: rgba(255, 255, 255, 0.85);
  max-width: 520px;
}
.profile-ai__btn {
  flex-shrink: 0;
}

@media (max-width: 600px) {
  .profile-ai__inner {
    flex-direction: column;
    align-items: stretch;
  }
  .profile-ai__btn {
    width: 100%;
  }
}
</style>
