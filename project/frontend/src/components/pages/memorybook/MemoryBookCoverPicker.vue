<script setup>
/**
 * 部品名: Music Memory Book — 表紙デザイン選択モーダル
 */
import { toRef } from 'vue'
import ModalShell from '../../modals/ModalShell.vue'
import UiButton from '../../ui/UiButton.vue'
import { COVER_DESIGNS } from '../../../lib/memoryBookCoverDesigns.js'
import { useBodyScrollLock } from '../../../composables/useBodyScrollLock.js'

const props = defineProps({
  open: { type: Boolean, default: false },
  year: { type: Number, required: true },
  selectedDesignId: { type: Number, default: 1 },
})

const emit = defineEmits(['close', 'select'])

useBodyScrollLock(toRef(props, 'open'))

function choose(designId) {
  emit('select', designId)
}
</script>

<template>
  <ModalShell
    v-if="open"
    :title="`${year}年のアルバム表紙を選ぶ`"
    wide
    @close="emit('close')"
  >
    <p class="mmb-cover-picker__lead">
      お好みの表紙デザインを選んでください。選んだデザインはこの年のアルバムに反映されます。
    </p>

    <div class="mmb-cover-picker__grid">
      <button
        v-for="design in COVER_DESIGNS"
        :key="design.id"
        type="button"
        class="mmb-cover-picker__item"
        :class="{ 'mmb-cover-picker__item--active': design.id === selectedDesignId }"
        @click="choose(design.id)"
      >
        <img
          :src="design.image"
          :alt="design.label"
          class="mmb-cover-picker__thumb"
          loading="lazy"
          decoding="async"
        />
        <span class="mmb-cover-picker__label">{{ design.label }}</span>
      </button>
    </div>

    <div class="mmb-cover-picker__actions">
      <UiButton variant="ghost" size="sm" @click="emit('close')">閉じる</UiButton>
    </div>
  </ModalShell>
</template>

<style scoped>
.mmb-cover-picker__lead {
  margin: 0 0 var(--sp-5);
  font-size: var(--font-size-button);
  line-height: 1.8;
  color: var(--site-text-muted);
}

.mmb-cover-picker__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--sp-4);
}

.mmb-cover-picker__item {
  padding: var(--sp-3);
  border: 2px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  background: color-mix(in srgb, var(--site-surface-muted) 50%, transparent);
  cursor: pointer;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
  text-align: center;
}

.mmb-cover-picker__item:hover {
  border-color: color-mix(in srgb, var(--kin-500) 50%, var(--site-border));
  transform: translateY(-2px);
}

.mmb-cover-picker__item--active {
  border-color: var(--kin-500);
  box-shadow: 0 0 0 1px var(--kin-500), var(--site-shadow-md);
}

.mmb-cover-picker__thumb {
  display: block;
  width: 100%;
  aspect-ratio: 2 / 3;
  object-fit: contain;
  object-position: center;
  background: transparent;
  border-radius: 6px;
  margin-bottom: 8px;
}

.mmb-cover-picker__label {
  font-family: var(--ff-mincho);
  font-size: var(--font-size-caption);
  color: var(--site-text);
}

.mmb-cover-picker__actions {
  display: flex;
  justify-content: flex-end;
  margin-top: var(--sp-5);
}
</style>
