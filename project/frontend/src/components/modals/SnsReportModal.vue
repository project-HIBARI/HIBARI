<script setup>
/**
 * 部品名: SNS通報モーダル（投稿・コメント・ユーザー・DM共通）
 */
import { ref } from 'vue'
import ModalShell from './ModalShell.vue'
import UiButton from '../ui/UiButton.vue'
import { createSnsReport } from '../../api/sns.js'

const props = defineProps({
  targetType: { type: String, required: true }, // post | comment | user | dm_message
  targetId: { type: Number, required: true },
})

const emit = defineEmits(['close', 'reported'])

const REASONS = [
  'スパム・宣伝',
  '嫌がらせ・誹謗中傷',
  '不適切な内容',
  '著作権の侵害',
  '個人情報の掲載',
  'その他',
]

const selectedReason = ref('')
const detail = ref('')
const submitting = ref(false)
const errorMessage = ref('')
const done = ref(false)

const MAX_DETAIL = 500

async function submit() {
  if (submitting.value || !selectedReason.value) return
  submitting.value = true
  errorMessage.value = ''
  try {
    const reason = detail.value.trim() ? `${selectedReason.value}：${detail.value.trim()}` : selectedReason.value
    await createSnsReport({ target_type: props.targetType, target_id: props.targetId, reason })
    done.value = true
    emit('reported')
  } catch (err) {
    errorMessage.value = err?.message || '通報の送信に失敗しました'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <ModalShell title="通報する" @close="emit('close')">
    <div v-if="done" class="sns-report">
      <p class="sns-report__done">通報を受け付けました。ご報告ありがとうございます。</p>
      <UiButton variant="primary" size="md" @click="emit('close')">閉じる</UiButton>
    </div>
    <form v-else class="sns-report" @submit.prevent="submit">
      <p class="sns-report__label">通報理由を選択してください</p>
      <div class="sns-report__reasons">
        <label v-for="r in REASONS" :key="r" class="sns-report__reason">
          <input v-model="selectedReason" type="radio" name="sns-report-reason" :value="r" />
          {{ r }}
        </label>
      </div>

      <label class="sns-report__label" for="sns-report-detail">詳細（任意）</label>
      <textarea
        id="sns-report-detail"
        v-model="detail"
        class="sns-report__textarea"
        :maxlength="MAX_DETAIL"
        rows="3"
        placeholder="詳しい状況があればご記入ください"
      />

      <p v-if="errorMessage" class="sns-report__error">{{ errorMessage }}</p>

      <div class="sns-report__actions">
        <UiButton type="button" variant="ghost" size="md" :disabled="submitting" @click="emit('close')">キャンセル</UiButton>
        <UiButton type="submit" variant="primary" size="md" :disabled="submitting || !selectedReason">
          {{ submitting ? '送信中…' : '通報する' }}
        </UiButton>
      </div>
    </form>
  </ModalShell>
</template>

<style scoped>
.sns-report {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.sns-report__done {
  margin: 0;
  font-size: var(--font-size-small);
  color: var(--site-text);
}
.sns-report__label {
  font-size: var(--font-size-caption);
  color: var(--site-text-muted);
}
.sns-report__reasons {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.sns-report__reason {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: var(--font-size-button);
  color: var(--site-text);
  cursor: pointer;
}
.sns-report__textarea {
  width: 100%;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  padding: 10px 12px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-button);
  line-height: 1.7;
  resize: vertical;
  color: var(--site-text);
}
.sns-report__error {
  margin: 0;
  color: var(--beni-600);
  font-size: var(--font-size-caption);
}
.sns-report__actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
