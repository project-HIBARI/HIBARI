<script setup>
/**
 * 部品名: 思い出投稿 — 編集モーダル
 */
import { ref, watch, toRef } from 'vue'
import ModalShell from '../../modals/ModalShell.vue'
import UiButton from '../../ui/UiButton.vue'
import { useBodyScrollLock } from '../../../composables/useBodyScrollLock.js'

const PREFECTURES = [
  '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県',
  '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県',
  '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県',
  '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県',
  '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県',
  '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県',
  '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県',
]

const props = defineProps({
  open: { type: Boolean, default: false },
  post: { type: Object, default: null },
  submitting: { type: Boolean, default: false },
  error: { type: String, default: '' },
})

const emit = defineEmits(['close', 'save'])

useBodyScrollLock(toRef(props, 'open'))

const formError = ref('')
const form = ref({
  title: '',
  content: '',
  name: '',
  location: '',
})

watch(
  () => [props.open, props.post],
  () => {
    if (!props.open || !props.post) return
    formError.value = ''
    form.value = {
      title: props.post.title || '',
      content: props.post.body || '',
      name: props.post.author === '匿名' ? '' : (props.post.author || ''),
      location: props.post.location || '',
    }
  },
  { immediate: true },
)

function submit() {
  if (!form.value.title.trim()) {
    formError.value = 'タイトルを入力してください。'
    return
  }
  if (!form.value.content.trim()) {
    formError.value = '本文を入力してください。'
    return
  }
  emit('save', {
    postId: props.post.postId,
    title: form.value.title.trim(),
    content: form.value.content.trim(),
    name: form.value.name.trim() || null,
    location: form.value.location.trim() || null,
  })
}
</script>

<template>
  <ModalShell v-if="open" title="思い出の投稿を編集" @close="emit('close')">
    <p class="mem-edit__lead">内容を編集して保存できます。</p>
    <form class="mem-edit__form" @submit.prevent="submit">
      <label class="mem-edit__field">
        <span class="mem-edit__label">タイトル</span>
        <input v-model="form.title" class="mem-edit__input" />
      </label>
      <label class="mem-edit__field">
        <span class="mem-edit__label">本文</span>
        <textarea v-model="form.content" rows="6" class="mem-edit__input mem-edit__textarea" />
      </label>
      <div class="mem-edit__row">
        <label class="mem-edit__field">
          <span class="mem-edit__label">お名前（任意）</span>
          <input v-model="form.name" class="mem-edit__input" />
        </label>
        <label class="mem-edit__field">
          <span class="mem-edit__label">都道府県（任意）</span>
          <select v-model="form.location" class="mem-edit__input">
            <option value="">選択してください</option>
            <option v-for="pref in PREFECTURES" :key="pref" :value="pref">{{ pref }}</option>
          </select>
        </label>
      </div>
      <p v-if="formError || error" class="mem-edit__error" role="alert">{{ formError || error }}</p>
      <div class="mem-edit__actions">
        <UiButton variant="ghost" size="sm" type="button" :disabled="submitting" @click="emit('close')">
          キャンセル
        </UiButton>
        <UiButton variant="primary" size="sm" type="submit" :disabled="submitting">
          {{ submitting ? '保存中…' : '保存する' }}
        </UiButton>
      </div>
    </form>
  </ModalShell>
</template>

<style scoped>
.mem-edit__lead {
  margin: 0 0 var(--sp-5);
  font-size: var(--font-size-button);
  line-height: 1.8;
  color: var(--site-text-muted);
}
.mem-edit__form {
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
}
.mem-edit__row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--sp-4);
}
.mem-edit__field {
  display: block;
}
.mem-edit__label {
  display: block;
  margin-bottom: 6px;
  font-size: var(--font-size-caption);
  color: var(--site-text-muted);
}
.mem-edit__input {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 12px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-small);
  color: var(--site-text);
  background: #fff;
}
.mem-edit__textarea {
  resize: vertical;
  line-height: 1.7;
}
.mem-edit__error {
  margin: 0;
  font-size: var(--font-size-caption);
  color: var(--beni-600, #9b2c2c);
}
.mem-edit__actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 4px;
}
@media (max-width: 560px) {
  .mem-edit__row {
    grid-template-columns: 1fr;
  }
}
</style>
