<script setup>
/**
 * ページ: チケット先行予約
 * 用途: 放送・イベント一覧から選択したイベントの先行予約フォームと完了画面
 */
import { computed, reactive, ref, watch } from 'vue'
import PageHead from '../ui/PageHead.vue'
import UiCard from '../ui/UiCard.vue'
import UiButton from '../ui/UiButton.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'
import { useMemberAccess } from '../../composables/useMemberAccess.js'
import { EVENT_HERO_IMAGES, pageImageUrl } from '../../lib/pageImages.js'

const props = defineProps({
  eventId: { type: String, default: null },
})

const emit = defineEmits(['back'])

const { user, isPremium } = useMemberAccess()

/** イベント別の料金（デモ）。EventsListModal と同じ設定 */
const tourPricing = {
  b3: { regular: '¥8,800', member: '¥7,500', premium: '¥6,600' },
}

const event = computed(() => HIBARU_DATA.homeSchedule.find((ev) => ev.id === props.eventId) || null)

const heroImage = computed(() => {
  const filename = EVENT_HERO_IMAGES[props.eventId]
  return filename ? pageImageUrl(filename) : null
})

const fee = computed(() => {
  const p = tourPricing[props.eventId]
  if (!p) return null
  return {
    label: isPremium.value ? 'プレミアム会員価格' : '一般会員価格',
    value: isPremium.value ? p.premium : p.member,
    regular: p.regular,
  }
})

const form = reactive({
  name: user.value?.name || '',
  email: user.value?.email || '',
  count: 1,
  note: '',
})

watch(
  () => props.eventId,
  () => {
    submitted.value = false
  },
)

const submitting = ref(false)
const submitted = ref(false)
const reservationCode = ref('')

const canSubmit = computed(() => form.name.trim() !== '' && form.email.trim() !== '' && form.count >= 1)

function submit() {
  if (!canSubmit.value || submitting.value) return
  submitting.value = true
  reservationCode.value = `HB-${Date.now().toString(36).toUpperCase()}`
  window.setTimeout(() => {
    submitting.value = false
    submitted.value = true
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, 500)
}
</script>

<template>
  <div class="page-preorder">
    <PageHead kanji="予" title="チケット先行予約" sub="Ticket Preorder" />

    <p v-if="!event" class="page-preorder__empty">
      対象のイベントが見つかりませんでした。
      <button type="button" class="page-preorder__back-link" @click="emit('back')">一覧に戻る</button>
    </p>

    <template v-else>
      <img
        v-if="heroImage"
        :src="heroImage"
        :alt="event.title"
        class="page-preorder__hero"
      />

      <UiCard v-if="!submitted" tone="pink" padding="lg" class="page-preorder__card">
        <div class="page-preorder__event">
          <div class="page-preorder__event-head">
            <span class="page-preorder__date">{{ event.date }}</span>
            <span v-if="event.time" class="page-preorder__time">{{ event.time }}</span>
          </div>
          <h2 class="page-preorder__title">{{ event.title }}</h2>
          <p class="page-preorder__note">{{ event.note }}</p>
          <p v-if="fee" class="page-preorder__fee">
            {{ fee.label }}: <strong>{{ fee.value }}</strong>
            <span class="page-preorder__fee-regular">（一般 {{ fee.regular }}）</span>
          </p>
        </div>

        <hr class="page-preorder__rule" />

        <form class="page-preorder__form" @submit.prevent="submit">
          <label class="page-preorder__field">
            <span class="page-preorder__label">お名前<em>必須</em></span>
            <input v-model="form.name" type="text" class="page-preorder__input" placeholder="山田 花子" required />
          </label>
          <label class="page-preorder__field">
            <span class="page-preorder__label">メールアドレス<em>必須</em></span>
            <input v-model="form.email" type="email" class="page-preorder__input" placeholder="example@mail.com" required />
          </label>
          <label class="page-preorder__field page-preorder__field--sm">
            <span class="page-preorder__label">枚数<em>必須</em></span>
            <input v-model.number="form.count" type="number" min="1" max="6" class="page-preorder__input" required />
          </label>
          <label class="page-preorder__field">
            <span class="page-preorder__label">ご要望・備考</span>
            <textarea v-model="form.note" rows="3" class="page-preorder__input page-preorder__textarea" placeholder="車椅子スペース希望 など（任意）" />
          </label>

          <div class="page-preorder__actions">
            <UiButton variant="ghost" size="md" type="button" @click="emit('back')">戻る</UiButton>
            <UiButton variant="primary" size="md" type="submit" :disabled="!canSubmit || submitting">
              {{ submitting ? '送信中…' : '先行予約を申し込む' }}
            </UiButton>
          </div>
        </form>
      </UiCard>

      <UiCard v-else tone="white" padding="lg" class="page-preorder__done">
        <div class="page-preorder__done-icon" aria-hidden="true">✓</div>
        <h2 class="page-preorder__done-title">先行予約を受け付けました</h2>
        <p class="page-preorder__done-lead">
          {{ event.title }}の先行予約が完了しました。<br />
          詳細のご案内は登録のメールアドレス宛にお送りします。
        </p>
        <dl class="page-preorder__summary">
          <div class="page-preorder__summary-row">
            <dt>予約番号</dt>
            <dd>{{ reservationCode }}</dd>
          </div>
          <div class="page-preorder__summary-row">
            <dt>お名前</dt>
            <dd>{{ form.name }}</dd>
          </div>
          <div class="page-preorder__summary-row">
            <dt>メールアドレス</dt>
            <dd>{{ form.email }}</dd>
          </div>
          <div class="page-preorder__summary-row">
            <dt>枚数</dt>
            <dd>{{ form.count }}枚</dd>
          </div>
        </dl>
        <UiButton variant="primary" size="md" @click="emit('back')">ファンクラブサイトに戻る</UiButton>
      </UiCard>
    </template>
  </div>
</template>

<style scoped>
.page-preorder {
  color: var(--site-text);
  max-width: 640px;
  margin: 0 auto;
}
.page-preorder__empty {
  font-size: 14px;
  color: var(--site-text-muted);
}
.page-preorder__hero {
  display: block;
  width: 100%;
  height: auto;
  aspect-ratio: 2832 / 411;
  object-fit: cover;
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--site-border);
  box-shadow: var(--site-shadow);
  margin-bottom: var(--sp-5);
}
.page-preorder__back-link {
  background: transparent;
  border: 0;
  padding: 0;
  margin-left: 6px;
  color: var(--murasaki-700);
  font-weight: 700;
  cursor: pointer;
  text-decoration: underline;
}
.page-preorder__event-head {
  display: flex;
  gap: 10px;
  align-items: baseline;
}
.page-preorder__date {
  font-family: var(--ff-mincho);
  font-size: 20px;
  font-weight: 700;
  color: var(--murasaki-700);
}
.page-preorder__time {
  font-size: 13px;
  color: var(--site-text-muted);
}
.page-preorder__title {
  margin: 10px 0 6px;
  font-family: var(--ff-mincho);
  font-size: 20px;
  color: var(--site-text);
}
.page-preorder__note {
  margin: 0;
  font-size: 13px;
  color: var(--site-text-muted);
}
.page-preorder__fee {
  margin: 12px 0 0;
  font-size: 14px;
  color: var(--kin-600);
}
.page-preorder__fee-regular {
  margin-left: 6px;
  font-size: 12px;
  color: var(--site-text-light);
}
.page-preorder__rule {
  margin: var(--sp-5) 0;
  border: 0;
  border-top: 1px solid var(--site-border);
}
.page-preorder__form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.page-preorder__field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.page-preorder__label {
  font-size: 12px;
  color: var(--site-text-muted);
  display: flex;
  align-items: center;
  gap: 6px;
}
.page-preorder__label em {
  font-style: normal;
  font-size: 10px;
  color: var(--beni-500, #c0392b);
  border: 1px solid currentColor;
  border-radius: 999px;
  padding: 1px 6px;
}
.page-preorder__input {
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
.page-preorder__input:focus {
  border-color: var(--murasaki-400);
}
.page-preorder__field--sm {
  max-width: 140px;
}
.page-preorder__textarea {
  resize: vertical;
}
.page-preorder__actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 8px;
}
.page-preorder__done {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 14px;
}
.page-preorder__done-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: var(--murasaki-100);
  border: 1px solid var(--kin-500);
  color: var(--murasaki-700);
  font-size: 26px;
}
.page-preorder__done-title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 20px;
  font-weight: 800;
  color: var(--murasaki-700);
}
.page-preorder__done-lead {
  margin: 0;
  font-size: 13px;
  line-height: 1.8;
  color: var(--site-text-muted);
}
.page-preorder__summary {
  width: 100%;
  margin: 4px 0;
  border-top: 1px solid var(--site-border);
  border-bottom: 1px solid var(--site-border);
}
.page-preorder__summary-row {
  display: flex;
  gap: 12px;
  padding: 10px 4px;
  text-align: left;
}
.page-preorder__summary-row + .page-preorder__summary-row {
  border-top: 1px solid var(--site-border);
}
.page-preorder__summary-row dt {
  flex: 0 0 96px;
  font-size: 12px;
  color: var(--site-text-light);
}
.page-preorder__summary-row dd {
  margin: 0;
  flex: 1 1 auto;
  font-size: 13px;
  color: var(--site-text);
  word-break: break-all;
}

@media (max-width: 480px) {
  .page-preorder__actions {
    flex-direction: column-reverse;
  }
  .page-preorder__actions > * {
    width: 100%;
  }
}
</style>
