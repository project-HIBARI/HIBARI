<script setup>
/**
 * 部品名: 献花 — 花の選択とフォーム
 * 用途: 献花ページで花の選択とメッセージ入力フォームを表示する
 */
import { ref } from 'vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'

const flowers = ['白百合', '紅薔薇', '白菊', 'かすみ草', '桔梗', '小手毬']
const flowerEmoji = ['🌸', '🌹', '🌼', '🌿', '🔔', '🍃']

const selFlower = ref(0)
const particles = ref([])
const formData = ref({ name: '', location: '', body: '' })

function pickFlower(i) {
  selFlower.value = i
  particles.value = Array.from({ length: 12 }, (_, k) => ({
    id: Date.now() + k,
    x: Math.random() * 100,
    y: Math.random() * 100,
    emoji: flowerEmoji[i],
    size: 14 + Math.random() * 20,
  }))
  window.setTimeout(() => {
    particles.value = []
  }, 1600)
}
</script>

<template>
  <section class="msg-offer">
    <div
      v-for="p in particles"
      :key="p.id"
      class="msg-offer__particle"
      :style="{ left: p.x + '%', top: p.y + '%', fontSize: p.size + 'px' }"
    >
      {{ p.emoji }}
    </div>
    <h3 class="msg-offer__title">献花する</h3>
    <p class="msg-offer__lead">お花を選び、短いメッセージをお書きください。</p>
    <div class="msg-offer__flowers">
      <button
        v-for="(f, i) in flowers"
        :key="f"
        type="button"
        class="msg-offer__flower"
        :class="{ 'msg-offer__flower--active': selFlower === i }"
        :aria-pressed="selFlower === i"
        :aria-label="f + 'を選択'"
        @click="pickFlower(i)"
      >
        <span class="msg-offer__emoji">{{ flowerEmoji[i] }}</span>
        {{ f }}
      </button>
    </div>
    <div class="msg-offer__row">
      <input v-model="formData.name" class="msg-offer__input" placeholder="お名前（匿名可）" aria-label="お名前" />
      <input v-model="formData.location" class="msg-offer__input" placeholder="お住まい" aria-label="お住まい" />
    </div>
    <textarea
      v-model="formData.body"
      rows="4"
      class="msg-offer__input msg-offer__textarea"
      placeholder="ひばりさんへ、一言——"
      aria-label="メッセージ"
    />
    <UiButton variant="primary" size="md" aria-label="献花する">
      献花する <UiIco name="flower" :size="14" color="#fff" />
    </UiButton>
  </section>
</template>

<style scoped>
.msg-offer {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, var(--site-bg-pink) 0%, var(--site-surface) 100%);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  padding: var(--sp-6);
  margin-bottom: var(--sp-7);
  box-shadow: var(--site-shadow);
}
.msg-offer__particle {
  position: absolute;
  pointer-events: none;
  animation: particleFade 1.5s ease-out forwards;
}
.msg-offer__title {
  font-family: var(--ff-mincho);
  font-size: 22px;
  margin: 0 0 8px;
  color: var(--site-text);
}
.msg-offer__lead {
  font-size: 13px;
  color: var(--site-text-muted);
  margin: 0 0 var(--sp-5);
}
.msg-offer__flowers {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 10px;
  margin-bottom: var(--sp-5);
}
.msg-offer__flower {
  background: var(--site-surface);
  border: 1px solid var(--site-border);
  color: var(--site-text);
  padding: 14px 6px;
  cursor: pointer;
  font-family: var(--ff-mincho);
  font-size: 12px;
  letter-spacing: 0.08em;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  border-radius: var(--site-radius-sm);
  transition: background 0.2s, border-color 0.2s;
}
.msg-offer__flower:hover {
  border-color: var(--murasaki-400);
}
.msg-offer__flower--active {
  background: var(--murasaki-700);
  color: #fff;
  border-color: var(--murasaki-800);
}
.msg-offer__emoji {
  font-size: 20px;
}
.msg-offer__row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 12px;
}
.msg-offer__input {
  width: 100%;
  background: var(--site-surface);
  border: 1px solid var(--site-border-strong);
  color: var(--site-text);
  padding: 10px 12px;
  font-family: var(--ff-serif);
  font-size: 13px;
  border-radius: var(--site-radius-sm);
  outline: none;
}
.msg-offer__input:focus {
  border-color: var(--murasaki-400);
}
.msg-offer__textarea {
  resize: vertical;
  margin-bottom: var(--sp-4);
}

@media (max-width: 768px) {
  .msg-offer__flowers {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 480px) {
  .msg-offer__flowers {
    grid-template-columns: repeat(2, 1fr);
  }
  .msg-offer__row {
    grid-template-columns: 1fr;
  }
}
</style>
