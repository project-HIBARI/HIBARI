<script setup>
/**
 * 部品名: 掲示板 — 投稿フォーム（共通）
 */
import { ref, watch, onBeforeUnmount } from 'vue'
import UiButton from '../ui/UiButton.vue'
import MemberGate from '../common/MemberGate.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'
import { useBoardPost } from '../../composables/useBoardPost.js'
import { getMediaKind, validateBoardMediaFile, revokeMediaPreview } from '../../lib/boardMedia.js'

const songs = HIBARU_DATA.discography.map((d) => d.title)

const props = defineProps({
  postData: { type: Object, required: true },
  errors: { type: Object, default: () => ({}) },
  submitted: { type: Boolean, default: false },
  submitting: { type: Boolean, default: false },
  submitError: { type: String, default: '' },
  heading: { type: String, default: '思い出を寄せる' },
  compact: { type: Boolean, default: false },
})

const emit = defineEmits(['update:postData', 'submit', 'reset', 'need-auth'])

const { canPostNow, canUse, isLoggedIn, isGuest, limitMessage, guestResetLabel, loading, usageStatus, PERMISSION } = useBoardPost()

const mediaPreviewUrl = ref('')
const mediaError = ref('')

watch(
  () => props.postData.mediaFile,
  (file, prevFile) => {
    if (props.postData.mediaPreviewUrl) {
      revokeMediaPreview(props.postData.mediaPreviewUrl)
    }
    if (!file) {
      mediaPreviewUrl.value = ''
      if (props.postData.mediaPreviewUrl) {
        patch({ mediaPreviewUrl: '', mediaKind: null })
      }
      return
    }
    if (file !== prevFile) {
      const url = URL.createObjectURL(file)
      mediaPreviewUrl.value = url
      patch({
        mediaPreviewUrl: url,
        mediaKind: getMediaKind(file),
      })
    }
  },
  { immediate: true },
)

onBeforeUnmount(() => {
  revokeMediaPreview(mediaPreviewUrl.value)
  revokeMediaPreview(props.postData.mediaPreviewUrl)
})

function patch(partial) {
  emit('update:postData', { ...props.postData, ...partial })
}

function onMediaChange(event) {
  mediaError.value = ''
  const file = event.target.files?.[0]
  if (!file) return

  const validationError = validateBoardMediaFile(file)
  if (validationError) {
    mediaError.value = validationError
    event.target.value = ''
    return
  }

  patch({ mediaFile: file })
}

function clearMedia() {
  mediaError.value = ''
  revokeMediaPreview(mediaPreviewUrl.value)
  mediaPreviewUrl.value = ''
  patch({ mediaFile: null, mediaPreviewUrl: '', mediaKind: null })
}

function onSubmit() {
  if (!canPostNow.value) return
  if (mediaError.value) return
  emit('submit')
}
</script>

<template>
  <div class="board-form" :class="{ 'board-form--compact': compact }">
    <MemberGate
      v-if="isLoggedIn && !canUse(PERMISSION.BOARD_POST)"
      :permission="PERMISSION.BOARD_POST"
      feature="掲示板投稿"
      :compact="compact"
      @login="emit('need-auth', 'login')"
      @register="emit('need-auth', 'register')"
      @upgrade="emit('need-auth', 'register-premium')"
    />
    <div v-else-if="loading && !usageStatus" class="board-form__loading">
      利用状況を確認しています…
    </div>
    <div v-else-if="!canPostNow" class="board-form__limit">
      <p class="board-form__limit-title">
        {{ isGuest ? '投稿上限に達しました' : '今月の投稿上限に達しました' }}
      </p>
      <p class="board-form__limit-text">
        <template v-if="isGuest">
          非会員は10回まで投稿できます。{{ guestResetLabel }} に解除されます。
          会員登録後は月10回までご利用いただけます（プレミアムは無制限）。
        </template>
        <template v-else>
          一般会員は月10回まで投稿できます。プレミアム会員は無制限でご利用いただけます。
        </template>
      </p>
      <button
        v-if="!isGuest"
        type="button"
        class="board-form__limit-btn"
        @click="emit('need-auth', 'register-premium')"
      >
        プレミアムに登録 ›
      </button>
      <button
        v-else
        type="button"
        class="board-form__limit-btn"
        @click="emit('need-auth', 'register')"
      >
        会員登録 ›
      </button>
    </div>
    <template v-else>
      <div v-if="submitted" class="board-form__done">
        <div class="board-form__done-icon">✦</div>
        <div class="board-form__done-title">投稿ありがとうございます</div>
        <p class="board-form__done-text">会員の皆さまの思い出が、ひばりの記憶を紡いでいます。</p>
        <UiButton variant="outline" size="md" class="board-form__full" @click="emit('reset')">続けて投稿</UiButton>
      </div>
      <template v-else>
        <h2 class="board-form__heading">{{ heading }}</h2>
        <p class="board-form__note">{{ limitMessage }}</p>
        <div class="board-form__fields">
          <input
            :value="postData.name"
            class="board-form__input"
            placeholder="お名前（匿名可）"
            aria-label="お名前"
            @input="patch({ name: $event.target.value })"
          />
          <input
            :value="postData.pref"
            class="board-form__input"
            placeholder="都道府県"
            aria-label="都道府県"
            @input="patch({ pref: $event.target.value })"
          />
          <div>
            <input
              :value="postData.title"
              class="board-form__input"
              :class="{ 'board-form__input--error': errors.title }"
              placeholder="タイトル *"
              aria-label="タイトル"
              aria-required="true"
              @input="patch({ title: $event.target.value })"
            />
            <div v-if="errors.title" class="board-form__error" role="alert">{{ errors.title }}</div>
          </div>
          <div>
            <textarea
              :value="postData.body"
              rows="5"
              class="board-form__input board-form__textarea"
              :class="{ 'board-form__input--error': errors.body }"
              placeholder="本文 *"
              aria-label="本文"
              aria-required="true"
              @input="patch({ body: $event.target.value })"
            />
            <div v-if="errors.body" class="board-form__error" role="alert">{{ errors.body }}</div>
          </div>
          <select
            :value="postData.song"
            class="board-form__input"
            aria-label="心に残る一曲"
            @change="patch({ song: $event.target.value })"
          >
            <option value="">心に残る一曲を選ぶ</option>
            <option v-for="s in songs" :key="s" :value="s">{{ s }}</option>
          </select>

          <div class="board-form__media">
            <label class="board-form__media-label">
              <span class="board-form__media-title">画像・動画を添付（任意）</span>
              <span class="board-form__media-hint">画像 10MB / 動画 50MB まで</span>
              <input
                type="file"
                class="board-form__media-input"
                accept="image/jpeg,image/png,image/gif,image/webp,video/mp4,video/webm,video/quicktime"
                :disabled="submitting"
                @change="onMediaChange"
              />
              <span class="board-form__media-btn">ファイルを選択</span>
            </label>
            <p v-if="mediaError" class="board-form__error" role="alert">{{ mediaError }}</p>
            <div v-if="mediaPreviewUrl" class="board-form__preview">
              <img
                v-if="postData.mediaKind === 'image'"
                :src="mediaPreviewUrl"
                alt="添付画像のプレビュー"
                class="board-form__preview-image"
              />
              <video
                v-else-if="postData.mediaKind === 'video'"
                :src="mediaPreviewUrl"
                class="board-form__preview-video"
                controls
                playsinline
              />
              <button type="button" class="board-form__preview-remove" @click="clearMedia">
                添付を削除
              </button>
            </div>
          </div>

          <UiButton
            variant="primary"
            size="md"
            class="board-form__full"
            :disabled="submitting"
            @click="onSubmit"
          >
            {{ submitting ? '送信中…' : '投稿する' }}
          </UiButton>
          <p v-if="submitError" class="board-form__error" role="alert">{{ submitError }}</p>
        </div>
      </template>
    </template>
  </div>
</template>

<style scoped>
.board-form__heading {
  font-family: var(--ff-mincho);
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 4px;
  color: var(--murasaki-700);
}
.board-form--compact .board-form__heading {
  font-size: 16px;
}
.board-form__note {
  margin: 0 0 var(--sp-4);
  font-size: 11px;
  line-height: 1.6;
  color: var(--site-text-muted);
}
.board-form__fields {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.board-form__input {
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
.board-form__input:focus {
  border-color: var(--murasaki-400);
}
.board-form__input--error {
  border-color: var(--beni-500);
}
.board-form__textarea {
  resize: vertical;
}
.board-form__error {
  font-size: 11px;
  color: var(--beni-600);
  margin-top: 3px;
}
.board-form__full {
  width: 100%;
  justify-content: center;
}
.board-form__media {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.board-form__media-label {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 4px;
  cursor: pointer;
}
.board-form__media-title {
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  font-weight: 600;
  color: var(--site-text);
}
.board-form__media-hint {
  font-size: 10px;
  color: var(--site-text-light);
}
.board-form__media-input {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}
.board-form__media-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  padding: 10px 14px;
  border: 1px dashed var(--site-border-strong);
  border-radius: var(--site-radius-sm);
  background: var(--site-surface-muted);
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  color: var(--murasaki-700);
  transition: border-color 0.2s, background 0.2s;
}
.board-form__media-label:hover .board-form__media-btn {
  border-color: var(--murasaki-400);
  background: var(--murasaki-100);
}
.board-form__preview {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.board-form__preview-image,
.board-form__preview-video {
  width: 100%;
  max-height: 220px;
  object-fit: contain;
  border-radius: var(--site-radius-sm);
  border: 1px solid var(--site-border);
  background: #000;
}
.board-form__preview-remove {
  align-self: flex-start;
  padding: 0;
  border: 0;
  background: transparent;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  color: var(--beni-600);
  cursor: pointer;
  text-decoration: underline;
}
.board-form__done {
  text-align: center;
  padding: var(--sp-4) 0;
}
.board-form__done-icon {
  font-size: 36px;
  margin-bottom: 12px;
  color: var(--kin-600);
}
.board-form__done-title {
  font-family: var(--ff-mincho);
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 12px;
  color: var(--site-text);
}
.board-form__done-text {
  font-size: 13px;
  color: var(--site-text-muted);
  line-height: 1.8;
  margin: 0 0 var(--sp-4);
}
.board-form__limit {
  padding: 16px 14px;
  text-align: center;
  background: var(--site-surface-muted);
  border: 1px dashed var(--site-border-strong);
  border-radius: var(--site-radius-md);
}
.board-form__loading {
  padding: 20px 14px;
  text-align: center;
  font-size: 13px;
  color: var(--site-text-muted);
}
.board-form__limit-title {
  margin: 0 0 8px;
  font-family: var(--ff-mincho);
  font-size: 15px;
  font-weight: 700;
  color: var(--site-text);
}
.board-form__limit-text {
  margin: 0 0 14px;
  font-size: 12px;
  line-height: 1.7;
  color: var(--site-text-muted);
}
.board-form__limit-btn {
  padding: 8px 16px;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  color: #fff;
  background: var(--murasaki-700);
  border: 1px solid var(--murasaki-800);
  border-radius: 999px;
  cursor: pointer;
}
</style>
