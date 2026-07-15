<script setup>
/**
 * 部品名: SNSプロフィール編集モーダル（自己紹介・プロフィール画像）
 */
import { ref } from 'vue'
import ModalShell from '../../modals/ModalShell.vue'
import UiButton from '../../ui/UiButton.vue'
import { updateSnsProfile, uploadSnsAvatar } from '../../../api/sns.js'

const props = defineProps({
  bio: { type: String, default: '' },
  avatarPath: { type: String, default: null },
})

const emit = defineEmits(['close', 'updated'])

const MAX_BIO = 500
const bioInput = ref(props.bio)
const avatarPreview = ref(props.avatarPath)
const avatarFile = ref(null)
const saving = ref(false)
const errorMessage = ref('')

function onAvatarChange(e) {
  const file = e.target.files?.[0]
  e.target.value = ''
  if (!file) return
  avatarFile.value = file
  avatarPreview.value = URL.createObjectURL(file)
}

async function save() {
  if (saving.value) return
  errorMessage.value = ''
  saving.value = true
  try {
    let avatarPath = null
    if (avatarFile.value) {
      const uploaded = await uploadSnsAvatar(avatarFile.value)
      avatarPath = uploaded.avatar_path
    }
    await updateSnsProfile({ bio: bioInput.value.trim() })
    emit('updated', { bio: bioInput.value.trim(), avatarPath })
  } catch (err) {
    errorMessage.value = err?.message || '更新に失敗しました'
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <ModalShell title="プロフィールを編集" @close="emit('close')">
    <div class="sns-profile-edit">
      <div class="sns-profile-edit__avatar-row">
        <span class="sns-profile-edit__avatar">
          <img v-if="avatarPreview" :src="avatarPreview" alt="プロフィール画像プレビュー" />
          <span v-else>{{ '?' }}</span>
        </span>
        <label class="sns-profile-edit__avatar-btn">
          画像を変更
          <input type="file" accept="image/*" hidden @change="onAvatarChange" />
        </label>
      </div>

      <label class="sns-profile-edit__label" for="sns-profile-bio">自己紹介</label>
      <textarea
        id="sns-profile-bio"
        v-model="bioInput"
        class="sns-profile-edit__textarea"
        :maxlength="MAX_BIO"
        rows="4"
        placeholder="自己紹介を入力（任意）"
      />
      <p class="sns-profile-edit__count">{{ bioInput.length }} / {{ MAX_BIO }}</p>

      <p v-if="errorMessage" class="sns-profile-edit__error">{{ errorMessage }}</p>

      <div class="sns-profile-edit__actions">
        <UiButton type="button" variant="ghost" size="md" :disabled="saving" @click="emit('close')">キャンセル</UiButton>
        <UiButton type="button" variant="primary" size="md" :disabled="saving" @click="save">
          {{ saving ? '保存中…' : '保存する' }}
        </UiButton>
      </div>
    </div>
  </ModalShell>
</template>

<style scoped>
.sns-profile-edit {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.sns-profile-edit__avatar-row {
  display: flex;
  align-items: center;
  gap: 14px;
}
.sns-profile-edit__avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--murasaki-600);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-subtitle);
  flex-shrink: 0;
}
.sns-profile-edit__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sns-profile-edit__avatar-btn {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  border: 1px solid var(--murasaki-400);
  border-radius: 999px;
  color: var(--murasaki-700);
  font-size: var(--font-size-caption);
  cursor: pointer;
}
.sns-profile-edit__label {
  font-size: var(--font-size-caption);
  color: var(--site-text-muted);
}
.sns-profile-edit__textarea {
  width: 100%;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  padding: 12px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-small);
  line-height: 1.7;
  resize: vertical;
  color: var(--site-text);
}
.sns-profile-edit__count {
  margin: -4px 0 0;
  text-align: right;
  font-size: var(--font-size-caption);
  color: var(--site-text-light);
}
.sns-profile-edit__error {
  margin: 0;
  color: var(--beni-600);
  font-size: var(--font-size-caption);
}
.sns-profile-edit__actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
