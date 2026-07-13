<script setup>
/**
 * 部品名: SNS投稿作成モーダル
 * 用途: ストーリーズ / 写真・動画 / ひとこと の投稿種別選択 → フォーム → 公開
 */
import { ref, computed } from 'vue'
import ModalShell from '../../modals/ModalShell.vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'
import { useSnsUsage } from '../../../composables/useSnsUsage.js'
import { createSnsPost, uploadSnsMedia, createSnsStory } from '../../../api/sns.js'

const props = defineProps({
  /** 指定すると種別選択ステップを飛ばして直接フォームを開く（story | photo | text） */
  initialType: { type: String, default: null },
})

const emit = defineEmits(['close', 'created', 'limit-reached'])

const { usageStatus, canPostNow, remainingMessage, nextResetLabel, refreshUsage } = useSnsUsage()
refreshUsage()

const step = ref(props.initialType ? 'form' : 'type') // type | form
const postType = ref(props.initialType || 'photo') // story | photo | text
const body = ref('')
const hashtagsInput = ref('')
const commentsEnabled = ref(true)
const files = ref([]) // [{ file, previewUrl, kind }]
const submitting = ref(false)
const uploadingLabel = ref('')
const errorMessage = ref('')

const MAX_TEXT = 300
const MAX_PHOTO_BODY = 2200
const MAX_STORY_CAPTION = 300
const MAX_LEN = computed(() => {
  if (postType.value === 'text') return MAX_TEXT
  if (postType.value === 'story') return MAX_STORY_CAPTION
  return MAX_PHOTO_BODY
})

const hasVideo = computed(() => files.value.some((f) => f.kind === 'video'))

function pickType(type) {
  postType.value = type
  step.value = 'form'
}

function onFileChange(e) {
  errorMessage.value = ''
  const picked = Array.from(e.target.files || [])
  e.target.value = ''
  if (!picked.length) return

  const maxImages = postType.value === 'photo' ? 4 : 1
  for (const file of picked) {
    const isVideo = file.type.startsWith('video/')
    const isImage = file.type.startsWith('image/')
    if (!isVideo && !isImage) continue

    if (isVideo) {
      if (postType.value === 'text') {
        errorMessage.value = 'ひとこと投稿に動画は添付できません'
        continue
      }
      files.value = [{ file, previewUrl: URL.createObjectURL(file), kind: 'video' }]
      continue
    }

    if (hasVideo.value) {
      errorMessage.value = '動画と画像は同時に投稿できません'
      continue
    }
    if (files.value.length >= maxImages) {
      errorMessage.value = `画像は${maxImages}枚まで選択できます`
      continue
    }
    files.value = [...files.value, { file, previewUrl: URL.createObjectURL(file), kind: 'image' }]
  }
}

function removeFile(index) {
  files.value = files.value.filter((_, i) => i !== index)
}

function parseHashtags() {
  return hashtagsInput.value
    .split(/[\s,、　]+/)
    .map((t) => t.trim().replace(/^#/, ''))
    .filter(Boolean)
    .slice(0, 10)
}

async function submit() {
  if (submitting.value) return
  errorMessage.value = ''

  if (!canPostNow.value) {
    emit('limit-reached', usageStatus.value)
    return
  }
  if (postType.value === 'text' && !body.value.trim() && files.value.length === 0) {
    errorMessage.value = '本文または画像を入力してください'
    return
  }
  if ((postType.value === 'photo' || postType.value === 'story') && files.value.length === 0) {
    errorMessage.value = '画像または動画を選択してください'
    return
  }
  if (body.value.length > MAX_LEN.value) {
    errorMessage.value = `本文は${MAX_LEN.value}文字以内で入力してください`
    return
  }

  submitting.value = true
  try {
    const media = []
    for (const item of files.value) {
      uploadingLabel.value = `アップロード中（${media.length + 1}/${files.value.length}）…`
      const uploaded = await uploadSnsMedia(item.file)
      media.push(uploaded)
    }
    uploadingLabel.value = ''

    if (postType.value === 'story') {
      await createSnsStory({
        media_type: media[0].media_type,
        file_path: media[0].path,
        caption: body.value.trim(),
      })
    } else {
      await createSnsPost({
        post_type: postType.value,
        body: body.value.trim(),
        hashtags: parseHashtags(),
        comments_enabled: commentsEnabled.value,
        media,
      })
    }

    emit('created')
  } catch (err) {
    uploadingLabel.value = ''
    if (err?.status === 429) {
      emit('limit-reached', err.data)
      return
    }
    errorMessage.value = err?.message || '投稿に失敗しました。もう一度お試しください。'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <ModalShell
    :title="step === 'type' ? '投稿する' : { photo: '写真・動画を投稿', text: 'ひとことを投稿', story: 'ストーリーズを投稿' }[postType]"
    @close="emit('close')"
  >
    <div v-if="step === 'type'" class="sns-create__type-list">
      <button type="button" class="sns-create__type-btn" @click="pickType('story')">
        <UiIco name="story-ring" :size="22" />
        <span>ストーリーズ</span>
      </button>
      <button type="button" class="sns-create__type-btn" @click="pickType('photo')">
        <UiIco name="image" :size="22" />
        <span>写真・動画を投稿</span>
      </button>
      <button type="button" class="sns-create__type-btn" @click="pickType('text')">
        <UiIco name="chat" :size="22" />
        <span>ひとことを投稿</span>
      </button>
    </div>

    <form v-else class="sns-create__form" @submit.prevent="submit">
      <p class="sns-create__usage">{{ remainingMessage }}</p>
      <p v-if="!canPostNow && nextResetLabel" class="sns-create__reset">次回リセット：{{ nextResetLabel }}</p>

      <div v-if="postType === 'photo' || postType === 'story'" class="sns-create__media-picker">
        <label class="sns-create__file-btn">
          <UiIco name="image" :size="18" />
          画像・動画を選択
          <input type="file" accept="image/*,video/*" :multiple="postType === 'photo'" hidden @change="onFileChange" />
        </label>
        <p class="sns-create__media-hint">
          {{ postType === 'story' ? '画像または動画を1件選択してください（投稿から24時間で自動的に非表示になります）' : '画像は最大4枚、または動画1件までです' }}
        </p>
        <div v-if="files.length" class="sns-create__previews">
          <div v-for="(item, i) in files" :key="i" class="sns-create__preview">
            <img v-if="item.kind === 'image'" :src="item.previewUrl" alt="添付プレビュー" />
            <video v-else :src="item.previewUrl" muted playsinline />
            <button type="button" class="sns-create__preview-remove" aria-label="削除" @click="removeFile(i)">
              <UiIco name="close" :size="12" />
            </button>
          </div>
        </div>
      </div>

      <textarea
        v-model="body"
        class="sns-create__textarea"
        :maxlength="MAX_LEN"
        :placeholder="postType === 'text' ? '今の気持ちをひとことで（最大300文字）' : postType === 'story' ? 'キャプション（任意）' : '思い出について書く（任意）'"
        rows="4"
      />
      <p class="sns-create__count">{{ body.length }} / {{ MAX_LEN }}</p>

      <div v-if="postType === 'text'" class="sns-create__media-picker sns-create__media-picker--text">
        <label class="sns-create__file-btn">
          <UiIco name="image" :size="18" />
          画像を1枚添付（任意）
          <input type="file" accept="image/*" hidden @change="onFileChange" />
        </label>
        <div v-if="files.length" class="sns-create__previews">
          <div v-for="(item, i) in files" :key="i" class="sns-create__preview">
            <img :src="item.previewUrl" alt="添付プレビュー" />
            <button type="button" class="sns-create__preview-remove" aria-label="削除" @click="removeFile(i)">
              <UiIco name="close" :size="12" />
            </button>
          </div>
        </div>
      </div>

      <template v-if="postType !== 'story'">
        <input v-model="hashtagsInput" type="text" class="sns-create__hashtags" placeholder="ハッシュタグ（スペース区切り、任意）" />

        <label class="sns-create__toggle">
          <input v-model="commentsEnabled" type="checkbox" />
          コメントを許可する
        </label>
      </template>

      <p class="sns-create__notice">
        第三者が権利を持つ画像・動画や、個人情報を含む内容を、許可なく投稿しないでください。
      </p>

      <p v-if="errorMessage" class="sns-create__error">{{ errorMessage }}</p>
      <p v-if="uploadingLabel" class="sns-create__uploading">{{ uploadingLabel }}</p>

      <div class="sns-create__actions">
        <UiButton type="button" variant="ghost" size="md" :disabled="submitting" @click="step = 'type'">戻る</UiButton>
        <UiButton type="submit" variant="primary" size="md" :disabled="submitting || !canPostNow">
          {{ submitting ? '公開中…' : '公開する' }}
        </UiButton>
      </div>
    </form>
  </ModalShell>
</template>

<style scoped>
.sns-create__type-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.sns-create__type-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: var(--site-radius-md);
  border: 1px solid var(--site-border);
  background: var(--site-surface);
  cursor: pointer;
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  color: var(--site-text);
  text-align: left;
}
.sns-create__type-btn:hover:not(:disabled) {
  border-color: var(--murasaki-400);
  background: var(--murasaki-100);
}
.sns-create__type-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.sns-create__type-btn small {
  margin-left: auto;
  color: var(--site-text-light);
  font-size: 11px;
}

.sns-create__form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.sns-create__usage {
  margin: 0;
  font-size: 13px;
  color: var(--murasaki-700);
  font-weight: 600;
}
.sns-create__reset {
  margin: 0;
  font-size: 12px;
  color: var(--site-text-muted);
}
.sns-create__textarea {
  width: 100%;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  padding: 12px;
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  line-height: 1.7;
  resize: vertical;
  color: var(--site-text);
}
.sns-create__count {
  margin: -4px 0 0;
  text-align: right;
  font-size: 11px;
  color: var(--site-text-light);
}
.sns-create__media-picker {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.sns-create__file-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  align-self: flex-start;
  padding: 8px 14px;
  border: 1px solid var(--murasaki-400);
  border-radius: 999px;
  color: var(--murasaki-700);
  font-size: 12px;
  cursor: pointer;
}
.sns-create__media-hint {
  margin: 0;
  font-size: 11px;
  color: var(--site-text-light);
}
.sns-create__previews {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.sns-create__preview {
  position: relative;
  width: 72px;
  height: 72px;
  border-radius: var(--site-radius-sm);
  overflow: hidden;
  border: 1px solid var(--site-border);
}
.sns-create__preview img,
.sns-create__preview video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sns-create__preview-remove {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 0;
  background: rgba(0, 0, 0, 0.6);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.sns-create__hashtags {
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
  padding: 10px 12px;
  font-size: 13px;
  color: var(--site-text);
}
.sns-create__toggle {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--site-text-muted);
}
.sns-create__notice {
  margin: 4px 0 0;
  padding: 10px 12px;
  border-radius: var(--site-radius-sm);
  background: var(--site-surface-muted);
  color: var(--site-text-muted);
  font-size: 11px;
  line-height: 1.7;
}
.sns-create__error {
  margin: 0;
  color: var(--beni-600);
  font-size: 12px;
}
.sns-create__uploading {
  margin: 0;
  color: var(--site-text-muted);
  font-size: 12px;
}
.sns-create__actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
}
</style>
