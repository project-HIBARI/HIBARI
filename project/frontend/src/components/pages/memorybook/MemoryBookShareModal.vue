<script setup>
/**
 * 部品名: Music Memory Book — アルバム共有モーダル
 */
import { ref, computed, toRef } from 'vue'
import ModalShell from '../../modals/ModalShell.vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'
import { useBodyScrollLock } from '../../../composables/useBodyScrollLock.js'
import { buildYearAlbumSharePayload, shareYearAlbum } from '../../../lib/memoryBookShare.js'

const props = defineProps({
  open: { type: Boolean, default: false },
  year: { type: Number, required: true },
  summary: { type: Object, default: () => ({}) },
  timeline: { type: Array, default: () => [] },
})

const emit = defineEmits(['close'])

useBodyScrollLock(toRef(props, 'open'))

const sharing = ref(false)
const message = ref('')
const error = ref('')

const payload = computed(() =>
  buildYearAlbumSharePayload({
    year: props.year,
    summary: props.summary,
    timeline: props.timeline,
  }),
)

async function onShare() {
  sharing.value = true
  error.value = ''
  message.value = ''
  try {
    const result = await shareYearAlbum(payload.value)
    if (result.method === 'clipboard') {
      message.value = '共有テキストをクリップボードにコピーしました。'
    } else if (result.method === 'share') {
      message.value = '共有しました。'
      emit('close')
    }
  } catch (err) {
    error.value = err?.message || '共有に失敗しました。'
  } finally {
    sharing.value = false
  }
}

async function copyOnly() {
  sharing.value = true
  error.value = ''
  message.value = ''
  try {
    const text = `${payload.value.text}\n${payload.value.url}`
    await navigator.clipboard.writeText(text)
    message.value = 'クリップボードにコピーしました。'
  } catch {
    error.value = 'コピーに失敗しました。'
  } finally {
    sharing.value = false
  }
}
</script>

<template>
  <ModalShell
    v-if="open"
    :title="`${year}年のアルバムをシェア`"
    @close="emit('close')"
  >
    <p class="mmb-share__lead">アルバムの概要を共有できます。</p>

    <div class="mmb-share__preview">
      <p class="mmb-share__preview-title">{{ payload.title }}</p>
      <pre class="mmb-share__preview-text">{{ payload.text }}</pre>
      <p class="mmb-share__preview-url">{{ payload.url }}</p>
    </div>

    <p v-if="message" class="mmb-share__message" role="status">{{ message }}</p>
    <p v-if="error" class="mmb-share__error" role="alert">{{ error }}</p>

    <div class="mmb-share__actions">
      <UiButton variant="ghost" size="sm" @click="emit('close')">閉じる</UiButton>
      <UiButton variant="outline" size="sm" :disabled="sharing" @click="copyOnly">
        リンクをコピー
      </UiButton>
      <UiButton variant="primary" size="sm" :disabled="sharing" @click="onShare">
        <UiIco name="share" :size="14" color="#fff" />
        {{ sharing ? '共有中…' : '共有する' }}
      </UiButton>
    </div>
  </ModalShell>
</template>

<style scoped>
.mmb-share__lead {
  margin: 0 0 var(--sp-4);
  font-size: var(--font-size-button);
  line-height: 1.8;
  color: var(--site-text-muted);
}

.mmb-share__preview {
  padding: var(--sp-4);
  border-radius: var(--site-radius-md);
  border: 1px solid var(--site-border);
  background: var(--site-surface-muted);
  margin-bottom: var(--sp-4);
}

.mmb-share__preview-title {
  margin: 0 0 8px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-body);
  font-weight: 700;
  color: var(--murasaki-800);
}

.mmb-share__preview-text {
  margin: 0 0 10px;
  font-family: var(--ff-serif);
  font-size: var(--font-size-button);
  line-height: 1.8;
  white-space: pre-wrap;
  color: var(--site-text);
}

.mmb-share__preview-url {
  margin: 0;
  font-size: var(--font-size-caption);
  color: var(--site-text-light);
  word-break: break-all;
}

.mmb-share__message {
  margin: 0 0 var(--sp-3);
  font-size: var(--font-size-caption);
  color: var(--murasaki-700);
}

.mmb-share__error {
  margin: 0 0 var(--sp-3);
  font-size: var(--font-size-caption);
  color: var(--beni-600);
}

.mmb-share__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--sp-3);
  flex-wrap: wrap;
}
</style>
