<script setup>
/**
 * 部品名: ゆかりの地 — AI 美空ひばりカード
 * 用途: ゆかりの地について AI チャット機能へ誘導する
 */
import UiCard from '../../ui/UiCard.vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'

const emit = defineEmits(['open-ai'])

const examples = [
  '「野毛の銅像はいつ建立されましたか？」',
  '「不死鳥コンサートはどこで開催されましたか？」',
  '「記念館の見学方法を教えてください」',
]
</script>

<template>
  <!-- ゆかりの地について AI と会話する導線カード -->
  <section class="places-ai" aria-label="AI美空ひばり">
    <UiCard tone="purple" padding="lg" class="places-ai__card">
      <div class="places-ai__inner">
        <div class="places-ai__copy">
          <span class="places-ai__badge">新機能</span>
          <h3 class="places-ai__title">AI美空ひばりにゆかりの地を聞く</h3>
          <p class="places-ai__desc">
            スポットの歴史や見学のヒントなど、ゆかりの地について
            AI 美空ひばりと会話できます。例えば…
          </p>
          <ul class="places-ai__examples">
            <li v-for="(ex, i) in examples" :key="i">{{ ex }}</li>
          </ul>
        </div>
        <UiButton variant="gold" size="md" class="places-ai__btn" @click="emit('open-ai')">
          <UiIco name="chat" :size="16" color="var(--ink-900)" />
          AIと話す
        </UiButton>
      </div>
    </UiCard>
  </section>
</template>

<style scoped>
.places-ai {
  margin-bottom: var(--sp-7);
}
.places-ai__card {
  background:
    radial-gradient(ellipse at 0% 50%, rgba(255, 255, 255, 0.08) 0%, transparent 50%),
    linear-gradient(135deg, var(--murasaki-800) 0%, var(--murasaki-700) 100%);
}
.places-ai__inner {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--sp-5);
  flex-wrap: wrap;
}
.places-ai__badge {
  display: inline-block;
  padding: 3px 10px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 999px;
  font-size: 11px;
  letter-spacing: 0.08em;
  margin-bottom: 10px;
}
.places-ai__title {
  margin: 0 0 8px;
  font-family: var(--ff-mincho);
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--paper-50);
}
.places-ai__desc {
  margin: 0 0 12px;
  font-size: 13px;
  line-height: 1.75;
  color: rgba(255, 255, 255, 0.85);
  max-width: 520px;
}
.places-ai__examples {
  margin: 0;
  padding: 0;
  list-style: none;
}
.places-ai__examples li {
  font-size: 12px;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.7);
  padding-left: 14px;
  position: relative;
}
.places-ai__examples li::before {
  content: '·';
  position: absolute;
  left: 0;
  color: var(--kin-400);
}
.places-ai__btn {
  flex-shrink: 0;
  align-self: center;
}

@media (max-width: 600px) {
  .places-ai__inner {
    flex-direction: column;
    align-items: stretch;
  }
  .places-ai__btn {
    width: 100%;
  }
}
</style>
