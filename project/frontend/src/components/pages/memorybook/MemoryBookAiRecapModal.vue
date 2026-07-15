<script setup>
/**
 * 部品名: Music Memory Book — AI年別振り返りモーダル
 */
import { ref, watch, toRef } from 'vue'
import ModalShell from '../../modals/ModalShell.vue'
import UiButton from '../../ui/UiButton.vue'
import { useBodyScrollLock } from '../../../composables/useBodyScrollLock.js'
import { fetchYearRecap } from '../../../api/memoryBook.js'
import { buildYearRecapFallback } from '../../../lib/memoryBookRecap.js'

const props = defineProps({
  open: { type: Boolean, default: false },
  year: { type: Number, required: true },
  summary: { type: Object, default: () => ({}) },
  timeline: { type: Array, default: () => [] },
})

const emit = defineEmits(['close'])

useBodyScrollLock(toRef(props, 'open'))

const loading = ref(false)
const recap = ref('')
const source = ref('')

watch(
  () => [props.open, props.year, props.summary, props.timeline],
  async () => {
    if (!props.open) return
    loading.value = true
    recap.value = ''
    source.value = ''

    try {
      const data = await fetchYearRecap({
        year: props.year,
        summary: props.summary,
        timeline: props.timeline,
      })
      recap.value = data.recap || ''
      source.value = data.source || 'ai'
    } catch {
      recap.value = buildYearRecapFallback({
        year: props.year,
        summary: props.summary,
        timeline: props.timeline,
      })
      source.value = 'template'
    } finally {
      loading.value = false
    }
  },
  { immediate: true },
)
</script>

<template>
  <ModalShell
    v-if="open"
    :title="`${year}年の振り返り`"
    wide
    @close="emit('close')"
  >
    <p class="mmb-recap__lead">
      {{ year }}年の思い出をもとに、1年の振り返りをお届けします。
    </p>

    <div v-if="loading" class="mmb-recap__loading">振り返りを生成しています…</div>

    <article v-else class="mmb-recap__body">
      <p class="mmb-recap__text">{{ recap }}</p>
      <p class="mmb-recap__note">
        {{ source === 'ai' ? '※ AIが生成した振り返りです' : '※ 記録された思い出から自動生成した振り返りです' }}
      </p>
    </article>

    <div class="mmb-recap__actions">
      <UiButton variant="primary" size="sm" @click="emit('close')">閉じる</UiButton>
    </div>
  </ModalShell>
</template>

<style scoped>
.mmb-recap__lead {
  margin: 0 0 var(--sp-5);
  font-size: var(--font-size-button);
  line-height: 1.8;
  color: var(--site-text-muted);
}

.mmb-recap__loading {
  padding: var(--sp-8) var(--sp-4);
  text-align: center;
  font-size: var(--font-size-small);
  color: var(--site-text-muted);
}

.mmb-recap__body {
  padding: var(--sp-6);
  border-radius: var(--site-radius-lg);
  border: 1px solid rgba(122, 80, 136, 0.2);
  background: linear-gradient(135deg, var(--murasaki-100) 0%, rgba(252, 232, 236, 0.45) 100%);
}

.mmb-recap__text {
  margin: 0 0 var(--sp-4);
  font-size: var(--font-size-body);
  line-height: 2.1;
  color: var(--site-text);
  white-space: pre-line;
}

.mmb-recap__note {
  margin: 0;
  font-size: var(--font-size-badge);
  color: var(--site-text-light);
}

.mmb-recap__actions {
  display: flex;
  justify-content: flex-end;
  margin-top: var(--sp-5);
}
</style>
