<script setup>
/**
 * 部品名: ディスコグラフィ — 音声DL拡張子選択モーダル
 * 用途: プレミアム会員向けに .mp3 / .wav の偽造ファイルをダウンロードする
 *       権限がない場合はプレミアム案内を表示する
 */
import { ref, computed, watch } from 'vue'
import ModalShell from '../../modals/ModalShell.vue'
import { useMemberAccess } from '../../../composables/useMemberAccess.js'
import { PERMISSION } from '../../../constants/membership.js'

const props = defineProps({
  song: { type: Object, default: null },
})

const emit = defineEmits(['close', 'need-auth'])

const { canUse, isLoggedIn } = useMemberAccess()

const format = ref('mp3')

const canDownload = computed(() => canUse(PERMISSION.AUDIO_DOWNLOAD))

const modalTitle = computed(() =>
  canDownload.value ? '楽曲ダウンロード' : 'ダウンロード',
)

watch(
  () => props.song,
  () => {
    format.value = 'mp3'
  },
)

function sanitizeFilename(name) {
  return String(name || 'song').replace(/[\\/:*?"<>|]/g, '').trim() || 'song'
}

function downloadFakeAudio(title, ext) {
  const filename = `${sanitizeFilename(title)}.${ext}`
  const mime = ext === 'wav' ? 'audio/wav' : 'audio/mpeg'
  const bytes = new Uint8Array([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07])
  const blob = new Blob([bytes], { type: mime })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
}

function onDownload() {
  if (!props.song || !canDownload.value) return
  downloadFakeAudio(props.song.title, format.value)
  emit('close')
}

function onSubscribe() {
  emit('need-auth', isLoggedIn.value ? 'register-premium' : 'login')
  emit('close')
}
</script>

<template>
  <ModalShell v-if="song" :title="modalTitle" @close="emit('close')">
    <div v-if="!canDownload" class="disco-dl disco-dl--gate">
      <p class="disco-dl__gate-msg">この機能はプレミアム会員限定です</p>
      <button type="button" class="disco-dl__submit motion-button" @click="onSubscribe">
        プレミアム会員購読
      </button>
    </div>

    <div v-else class="disco-dl">
      <p class="disco-dl__song">{{ song.title }}</p>
      <p class="disco-dl__hint">ダウンロードする形式を選択してください</p>

      <fieldset class="disco-dl__formats">
        <legend class="sr-only">ファイル形式</legend>
        <label class="disco-dl__option" :class="{ 'disco-dl__option--on': format === 'mp3' }">
          <input v-model="format" type="radio" name="disco-dl-format" value="mp3" />
          <span class="disco-dl__ext">.mp3</span>
          <span class="disco-dl__label">軽量</span>
        </label>
        <label class="disco-dl__option" :class="{ 'disco-dl__option--on': format === 'wav' }">
          <input v-model="format" type="radio" name="disco-dl-format" value="wav" />
          <span class="disco-dl__ext">.wav</span>
          <span class="disco-dl__label">高音質</span>
        </label>
      </fieldset>

      <button type="button" class="disco-dl__submit motion-button" @click="onDownload">
        ダウンロード
      </button>
    </div>
  </ModalShell>
</template>

<style scoped>
.disco-dl__gate-msg {
  margin: 0 0 var(--sp-5);
  font-family: var(--ff-mincho);
  font-size: var(--font-size-body);
  font-weight: 700;
  letter-spacing: 0.04em;
  line-height: 1.7;
  color: var(--site-text);
  text-align: center;
}
.disco-dl__song {
  margin: 0 0 var(--sp-2);
  font-family: var(--ff-mincho);
  font-size: var(--font-size-emphasis);
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--site-text);
}
.disco-dl__hint {
  margin: 0 0 var(--sp-5);
  font-size: var(--font-size-button);
  color: var(--site-text-muted);
}
.disco-dl__formats {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 0 0 var(--sp-5);
  padding: 0;
  border: 0;
  min-width: 0;
}
.disco-dl__option {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  column-gap: 10px;
  width: 100%;
  box-sizing: border-box;
  min-width: 0;
  padding: 12px 14px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  background: var(--site-surface);
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
  text-align: left;
  overflow: hidden;
}
.disco-dl__option:hover {
  border-color: var(--murasaki-400);
}
.disco-dl__option--on {
  border-color: var(--murasaki-500);
  background: rgba(232, 223, 240, 0.45);
}
.disco-dl__option input {
  margin: 0;
  grid-column: 1;
  accent-color: var(--murasaki-700);
}
.disco-dl__ext {
  grid-column: 2;
  font-family: var(--ff-mono);
  font-size: var(--font-size-small);
  font-weight: 700;
  color: var(--site-text);
  text-align: left;
  min-width: 0;
}
.disco-dl__label {
  grid-column: 3;
  font-size: var(--font-size-button);
  color: var(--site-text-muted);
  white-space: nowrap;
  text-align: right;
}
.disco-dl__submit {
  display: block;
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--murasaki-500);
  border-radius: var(--site-radius-lg);
  background: var(--murasaki-700);
  color: #fff;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-body);
  letter-spacing: 0.12em;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
}
.disco-dl__submit:hover {
  background: var(--murasaki-800, #4a2f63);
  border-color: var(--murasaki-700);
}
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>
