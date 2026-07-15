<script setup>
/**
 * 部品名: 献花 — 花の種類選択モーダル
 */
import { toRef } from 'vue'
import ModalShell from '../../modals/ModalShell.vue'
import { FLOWER_TYPES } from '../../../lib/flowers.js'
import { useBodyScrollLock } from '../../../composables/useBodyScrollLock.js'
import FlowerCutout from './FlowerCutout.vue'

const props = defineProps({
  open: { type: Boolean, default: false },
  selectedIndex: { type: Number, default: 0 },
})

const emit = defineEmits(['close', 'select'])

useBodyScrollLock(toRef(props, 'open'))

function pickFlower(i) {
  emit('select', i)
  emit('close')
}
</script>

<template>
  <ModalShell
    v-if="open"
    title="花を選ぶ"
    wide
    @close="emit('close')"
  >
    <p class="msg-picker__lead">送りたい花をお選びください。</p>
    <div class="msg-picker__grid">
      <button
        v-for="(f, i) in FLOWER_TYPES"
        :key="f.id"
        type="button"
        class="msg-picker__flower"
        :class="{ 'msg-picker__flower--active': selectedIndex === i }"
        :aria-pressed="selectedIndex === i"
        :aria-label="f.name + 'を選択'"
        @click="pickFlower(i)"
      >
        <span class="msg-picker__check" aria-hidden="true">✓</span>
        <FlowerCutout :src="f.image" :alt="f.name" size="lg" />
        <span class="msg-picker__name">{{ f.name }}</span>
      </button>
    </div>
  </ModalShell>
</template>

<style scoped>
.msg-picker__lead {
  margin: 0 0 var(--sp-5);
  font-size: var(--font-size-button);
  line-height: 1.8;
  color: var(--site-text-muted);
}

.msg-picker__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--sp-3);
}

.msg-picker__flower {
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

.msg-picker__flower:hover {
  border-color: color-mix(in srgb, var(--kin-500) 50%, var(--site-border));
  transform: translateY(-2px);
}

.msg-picker__flower--active {
  border-color: var(--kin-500);
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--kin-500) 35%, transparent);
}

.msg-picker__check {
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

.msg-picker__flower--active .msg-picker__check {
  opacity: 1;
  transform: scale(1);
}

.msg-picker__name {
  font-family: var(--ff-mincho);
  font-size: var(--font-size-caption);
  letter-spacing: 0.08em;
  color: var(--site-text);
}

@media (max-width: 560px) {
  .msg-picker__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
