<script setup>
/**
 * 部品名: イベント申込モーダル
 * 用途: 交流イベントの詳細表示と申込フォーム
 */
import { ref, computed, watch } from 'vue'
import ModalShell from './ModalShell.vue'
import UiButton from '../ui/UiButton.vue'
import RegisterField from '../pages/register/RegisterField.vue'
import { applyToEvent } from '../../api/events.js'
import { useMemberAccess } from '../../composables/useMemberAccess.js'
import { PERMISSION } from '../../constants/membership.js'

const props = defineProps({
  event: { type: Object, default: null },
})

const emit = defineEmits(['close', 'need-auth', 'navigate'])

const { isLoggedIn, user, isPremium, canUse } = useMemberAccess()

const form = ref({ name: '', email: '', note: '' })
const submitting = ref(false)
const error = ref('')
const success = ref(false)

const eventTypes = {
  nodojiman: 'のど自慢',
  karaoke: 'カラオケ',
  tour: 'ゆかりの地ツアー',
  photo: 'フォトコンテスト',
}

const eventKey = computed(() => {
  if (!props.event) return ''
  return String(props.event.id ?? props.event.key ?? '')
})

const typeLabel = computed(() => eventTypes[props.event?.type] || props.event?.type || '')

watch(
  () => props.event,
  () => {
    success.value = false
    error.value = ''
    form.value = {
      name: user.value?.name || '',
      email: user.value?.email || '',
      note: '',
    }
  },
  { immediate: true },
)

async function submitApply() {
  if (!props.event || submitting.value) return
  error.value = ''
  if (!form.value.name.trim()) {
    error.value = 'お名前を入力してください。'
    return
  }
  submitting.value = true
  try {
    await applyToEvent(eventKey.value, {
      name: form.value.name.trim(),
      email: form.value.email.trim() || null,
      note: form.value.note.trim() || null,
    })
    success.value = true
  } catch (err) {
    error.value = err.message || '申込に失敗しました。'
  } finally {
    submitting.value = false
  }
}

function goToMap() {
  emit('navigate', 'map')
  emit('close')
}
</script>

<template>
  <ModalShell v-if="event" :title="event.title" wide @close="emit('close')">
    <div class="event-apply">
      <div v-if="success" class="event-apply__success">
        <p class="event-apply__success-title">申込を受け付けました</p>
        <p class="event-apply__success-text">
          「{{ event.title }}」へのお申込みありがとうございます。確認メールをお送りする場合があります。
        </p>
        <UiButton variant="primary" size="md" @click="emit('close')">閉じる</UiButton>
      </div>
      <template v-else>
        <div class="event-apply__meta">
          <span v-if="typeLabel" class="event-apply__type">{{ typeLabel }}</span>
          <span v-if="event.partner" class="event-apply__partner">{{ event.partner }}</span>
        </div>
        <dl class="event-apply__dl">
          <div v-if="event.date"><dt>日時</dt><dd>{{ event.date }}<template v-if="event.time"> {{ event.time }}</template></dd></div>
          <div v-if="event.place"><dt>会場</dt><dd>{{ event.place }}</dd></div>
          <div v-if="event.capacity"><dt>定員</dt><dd>{{ event.capacity }}</dd></div>
          <div v-if="event.fee"><dt>料金</dt><dd>{{ event.fee }}</dd></div>
          <div v-if="event.note"><dt>備考</dt><dd>{{ event.note }}</dd></div>
        </dl>
        <p v-if="isLoggedIn && isPremium && canUse(PERMISSION.PRIORITY_DISCOUNT)" class="event-apply__benefit">
          プレミアム会員: 優先枠・会員割引が適用されます
        </p>
        <p v-else-if="isLoggedIn && canUse(PERMISSION.TICKET_PREORDER)" class="event-apply__benefit">
          一般会員: 会員価格が適用されます
        </p>
        <form class="event-apply__form" @submit.prevent="submitApply">
          <RegisterField
            id="evt-name"
            v-model="form.name"
            label="お名前"
            placeholder="お名前"
            autocomplete="name"
            required
          />
          <RegisterField
            id="evt-email"
            v-model="form.email"
            label="メールアドレス"
            type="email"
            placeholder="連絡先メール（任意）"
            autocomplete="email"
          />
          <RegisterField
            id="evt-note"
            v-model="form.note"
            label="メモ・同行人数など"
            placeholder="ご要望があればご記入ください"
          />
          <p v-if="error" class="event-apply__error">{{ error }}</p>
          <div class="event-apply__actions">
            <UiButton variant="primary" size="md" type="submit" :disabled="submitting">
              {{ submitting ? '送信中…' : '申し込む' }}
            </UiButton>
            <UiButton
              v-if="event.type === 'tour'"
              variant="outline"
              size="md"
              type="button"
              @click="goToMap"
            >
              ゆかりの地へ ›
            </UiButton>
          </div>
        </form>
      </template>
    </div>
  </ModalShell>
</template>

<style scoped>
.event-apply__meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.event-apply__type {
  font-size: 11px;
  color: #fff;
  background: var(--murasaki-700);
  padding: 4px 10px;
  border-radius: var(--site-radius-sm);
}
.event-apply__partner {
  font-size: 11px;
  border: 1px solid var(--kin-500);
  color: var(--kin-600);
  padding: 4px 8px;
  border-radius: var(--site-radius-sm);
}
.event-apply__dl {
  display: grid;
  grid-template-columns: 72px 1fr;
  gap: 8px 12px;
  margin: 0 0 20px;
  font-size: 13px;
}
.event-apply__dl dt {
  color: var(--kin-600);
  font-weight: 700;
}
.event-apply__dl dd {
  margin: 0;
  color: var(--site-text-muted);
}
.event-apply__benefit {
  margin: 0 0 16px;
  padding: 10px 12px;
  font-size: 12px;
  color: var(--murasaki-700);
  background: var(--murasaki-100);
  border-radius: var(--site-radius-sm);
}
.event-apply__form {
  display: flex;
  flex-direction: column;
  gap: 14px;
  max-width: 480px;
}
.event-apply__error {
  margin: 0;
  font-size: 12px;
  color: var(--beni-600);
}
.event-apply__actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.event-apply__success {
  text-align: center;
  padding: 24px 16px;
}
.event-apply__success-title {
  margin: 0 0 12px;
  font-family: var(--ff-mincho);
  font-size: 18px;
  font-weight: 700;
  color: var(--murasaki-700);
}
.event-apply__success-text {
  margin: 0 0 20px;
  font-size: 13px;
  line-height: 1.8;
  color: var(--site-text-muted);
}
</style>
