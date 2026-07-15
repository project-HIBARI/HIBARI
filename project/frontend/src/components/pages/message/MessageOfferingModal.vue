<script setup>
/**
 * 部品名: 献花 — 献花フォームモーダル
 */
import { ref, toRef } from 'vue'
import ModalShell from '../../modals/ModalShell.vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'
import { FLOWER_TYPES } from '../../../lib/flowers.js'
import { submitFlowerOffering } from '../../../api/flowers.js'
import { useBodyScrollLock } from '../../../composables/useBodyScrollLock.js'
import FlowerCutout from './FlowerCutout.vue'

const props = defineProps({
  open: { type: Boolean, default: false },
})

const emit = defineEmits(['close', 'submitted'])

useBodyScrollLock(toRef(props, 'open'))

const selFlower = ref(0)
const particles = ref([])
const formData = ref({ name: '', body: '' })
const submitting = ref(false)
const error = ref('')
const success = ref(false)

function pickFlower(i) {
  selFlower.value = i
  particles.value = Array.from({ length: 10 }, (_, k) => ({
    id: Date.now() + k,
    x: 10 + Math.random() * 80,
    y: 20 + Math.random() * 60,
    emoji: FLOWER_TYPES[i].emoji,
    size: 14 + Math.random() * 16,
  }))
  window.setTimeout(() => {
    particles.value = []
  }, 1400)
}

function resetForm() {
  selFlower.value = 0
  formData.value = { name: '', body: '' }
  error.value = ''
  success.value = false
}

function close() {
  resetForm()
  emit('close')
}

async function submitOffering() {
  if (submitting.value) return
  error.value = ''
  if (!formData.value.body.trim()) {
    error.value = 'メッセージを入力してください。'
    return
  }
  submitting.value = true
  try {
    await submitFlowerOffering({
      name: formData.value.name.trim() || '匿名',
      location: null,
      content: formData.value.body.trim(),
      flower_type: FLOWER_TYPES[selFlower.value].name,
    })
    success.value = true
    emit('submitted')
    window.setTimeout(() => close(), 1800)
  } catch (err) {
    error.value = err.message || '献花の送信に失敗しました。'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <ModalShell
    v-if="open"
    title="献花する"
    wide
    @close="close"
  >
    <div class="msg-modal__body">
      <div
        v-for="p in particles"
        :key="p.id"
        class="msg-modal__particle"
        :style="{ left: p.x + '%', top: p.y + '%', fontSize: p.size + 'px' }"
        aria-hidden="true"
      >
        {{ p.emoji }}
      </div>

      <p v-if="success" class="msg-modal__success" role="status">
        献花ありがとうございます。想いを記録しました。
      </p>

      <template v-else>
        <p class="msg-modal__lead">花を選び、メッセージをお書きください。</p>

        <fieldset class="msg-modal__flowers">
          <legend class="msg-modal__legend">花を選ぶ</legend>
          <button
            v-for="(f, i) in FLOWER_TYPES"
            :key="f.id"
            type="button"
            class="msg-modal__flower"
            :class="{ 'msg-modal__flower--active': selFlower === i }"
            :aria-pressed="selFlower === i"
            :aria-label="f.name + 'を選択'"
            @click="pickFlower(i)"
          >
            <span class="msg-modal__flower-check" aria-hidden="true">✓</span>
            <FlowerCutout :src="f.image" :alt="f.name" size="lg" />
            <span class="msg-modal__flower-name">{{ f.name }}</span>
          </button>
        </fieldset>

        <label class="msg-modal__field">
          <span class="msg-modal__label">お名前（匿名可）</span>
          <input
            v-model="formData.name"
            class="msg-modal__input"
            placeholder="お名前"
            autocomplete="name"
          />
        </label>

        <label class="msg-modal__field">
          <span class="msg-modal__label">メッセージ</span>
          <textarea
            v-model="formData.body"
            rows="4"
            class="msg-modal__input msg-modal__textarea"
            placeholder="ひばりさんへ、一言——"
            maxlength="300"
          />
        </label>

        <p v-if="error" class="msg-modal__error" role="alert">{{ error }}</p>

        <UiButton
          variant="gold"
          size="lg"
          class="msg-modal__submit"
          aria-label="献花を送信する"
          :disabled="submitting"
          @click="submitOffering"
        >
          {{ submitting ? '送信中…' : '献花を送る' }}
          <UiIco name="flower" :size="14" color="var(--ink-900)" />
        </UiButton>
      </template>
    </div>
  </ModalShell>
</template>

<style scoped>
.msg-modal__body {
  position: relative;
  overflow: hidden;
}

.msg-modal__particle {
  position: absolute;
  pointer-events: none;
  animation: particleFade 1.4s ease-out forwards;
  z-index: 2;
}

.msg-modal__lead {
  margin: 0 0 var(--sp-5);
  font-size: var(--font-size-button);
  line-height: 1.8;
  color: var(--site-text-muted);
}

.msg-modal__success {
  margin: var(--sp-6) 0;
  text-align: center;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-body);
  line-height: 1.9;
  color: var(--murasaki-700);
}

.msg-modal__flowers {
  margin: 0 0 var(--sp-5);
  padding: 0;
  border: 0;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--sp-3);
}

.msg-modal__legend {
  width: 100%;
  margin-bottom: var(--sp-3);
  font-family: var(--ff-mincho);
  font-size: var(--font-size-button);
  letter-spacing: 0.1em;
  color: var(--site-text);
}

.msg-modal__flower {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: var(--sp-4) var(--sp-2) var(--sp-3);
  border-radius: 16px;
  border: 1px solid var(--site-border);
  background: color-mix(in srgb, var(--site-surface) 88%, transparent);
  cursor: pointer;
  transition: border-color 0.25s, box-shadow 0.25s, transform 0.25s;
}

.msg-modal__flower:hover {
  border-color: color-mix(in srgb, var(--kin-500) 50%, var(--site-border));
  transform: translateY(-2px);
}

.msg-modal__flower--active {
  border-color: var(--kin-500);
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--kin-500) 35%, transparent);
}

.msg-modal__flower-check {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--kin-500);
  color: #fff;
  font-size: var(--font-size-caption);
  line-height: 20px;
  text-align: center;
  opacity: 0;
  transform: scale(0.6);
  transition: opacity 0.2s, transform 0.2s;
}

.msg-modal__flower--active .msg-modal__flower-check {
  opacity: 1;
  transform: scale(1);
}

.msg-modal__flower-name {
  font-family: var(--ff-mincho);
  font-size: var(--font-size-caption);
  letter-spacing: 0.08em;
  color: var(--site-text);
}

.msg-modal__field {
  display: block;
  margin-bottom: var(--sp-4);
}

.msg-modal__label {
  display: block;
  margin-bottom: 6px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-caption);
  letter-spacing: 0.08em;
  color: var(--site-text-muted);
}

.msg-modal__input {
  width: 100%;
  background: var(--site-surface);
  border: 1px solid var(--site-border-strong);
  color: var(--site-text);
  padding: 12px 14px;
  font-family: var(--ff-serif);
  font-size: var(--font-size-small);
  border-radius: var(--site-radius-sm);
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.msg-modal__input:focus {
  border-color: var(--kin-500);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--kin-500) 18%, transparent);
}

.msg-modal__textarea {
  resize: vertical;
  min-height: 100px;
}

.msg-modal__error {
  margin: 0 0 var(--sp-4);
  font-size: var(--font-size-caption);
  color: var(--beni-600);
}

.msg-modal__submit {
  width: 100%;
  margin-top: var(--sp-2);
}

@media (max-width: 560px) {
  .msg-modal__flowers {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
