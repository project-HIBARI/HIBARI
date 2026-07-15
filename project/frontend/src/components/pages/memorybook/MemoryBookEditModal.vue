<script setup>
/**
 * 部品名: Music Memory Book — 思い出編集モーダル
 */
import { ref, watch, computed, toRef } from 'vue'
import ModalShell from '../../modals/ModalShell.vue'
import UiButton from '../../ui/UiButton.vue'
import MessageFlowerPickerModal from '../message/MessageFlowerPickerModal.vue'
import FlowerCutout from '../message/FlowerCutout.vue'
import { FLOWER_TYPES } from '../../../lib/flowers.js'
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
  memory: { type: Object, default: null },
  submitting: { type: Boolean, default: false },
  error: { type: String, default: '' },
})

const emit = defineEmits(['close', 'save'])

useBodyScrollLock(toRef(props, 'open'))

const formError = ref('')
const pickerOpen = ref(false)

const flowerForm = ref({
  flowerIndex: 0,
  content: '',
  name: '',
  location: '',
})

const postForm = ref({
  title: '',
  content: '',
  name: '',
  location: '',
})

const isFlower = computed(() => props.memory?.category === 'flowers')
const modalTitle = computed(() =>
  isFlower.value ? '献花の記録を編集' : '思い出の投稿を編集',
)

const selectedFlower = computed(() => FLOWER_TYPES[flowerForm.value.flowerIndex] ?? FLOWER_TYPES[0])

watch(
  () => [props.open, props.memory],
  () => {
    if (!props.open || !props.memory) return
    formError.value = ''
    pickerOpen.value = false

    const raw = props.memory.raw ?? {}
    if (props.memory.category === 'flowers') {
      const flowerIndex = Math.max(
        0,
        FLOWER_TYPES.findIndex((f) => f.name === raw.flower_type),
      )
      flowerForm.value = {
        flowerIndex: flowerIndex >= 0 ? flowerIndex : 0,
        content: raw.content || props.memory.body || '',
        name: raw.name && raw.name !== '匿名希望' ? raw.name : '',
        location: raw.location || '',
      }
      return
    }

    if (props.memory.category === 'posts') {
      postForm.value = {
        title: raw.title || props.memory.memo || '',
        content: raw.content || props.memory.body || '',
        name: raw.name || '',
        location: raw.location || '',
      }
    }
  },
  { immediate: true },
)

function onFlowerSelect(index) {
  flowerForm.value.flowerIndex = index
}

function validate() {
  if (isFlower.value) {
    if (!flowerForm.value.content.trim()) {
      formError.value = 'メッセージを入力してください。'
      return false
    }
    return true
  }

  if (!postForm.value.title.trim()) {
    formError.value = 'タイトルを入力してください。'
    return false
  }
  if (!postForm.value.content.trim()) {
    formError.value = '本文を入力してください。'
    return false
  }
  return true
}

function submit() {
  formError.value = ''
  if (!validate()) return

  if (isFlower.value) {
    emit('save', {
      category: 'flowers',
      payload: {
        content: flowerForm.value.content.trim(),
        flower_type: selectedFlower.value.name,
        name: flowerForm.value.name.trim() || '匿名希望',
        location: flowerForm.value.location || null,
      },
    })
    return
  }

  emit('save', {
    category: 'posts',
    payload: {
      title: postForm.value.title.trim(),
      content: postForm.value.content.trim(),
      name: postForm.value.name.trim() || null,
      location: postForm.value.location || null,
    },
  })
}
</script>

<template>
  <ModalShell
    v-if="open && memory"
    :title="modalTitle"
    wide
    @close="emit('close')"
  >
    <p class="mmb-edit__lead">内容を編集して保存できます。</p>

    <form class="mmb-edit__form" @submit.prevent="submit">
      <template v-if="isFlower">
        <div class="mmb-edit__flower-row">
          <button
            type="button"
            class="mmb-edit__flower-btn"
            aria-label="花を選ぶ・変更する"
            @click="pickerOpen = true"
          >
            <FlowerCutout :src="selectedFlower.image" :alt="selectedFlower.name" size="lg" />
            <span>{{ selectedFlower.name }}</span>
            <span class="mmb-edit__flower-change">花を変更</span>
          </button>
        </div>

        <label class="mmb-edit__field">
          <span class="mmb-edit__label">メッセージ</span>
          <textarea
            v-model="flowerForm.content"
            rows="5"
            class="mmb-edit__input mmb-edit__textarea"
            maxlength="300"
          />
        </label>

        <div class="mmb-edit__row">
          <label class="mmb-edit__field">
            <span class="mmb-edit__label">お名前（任意）</span>
            <input v-model="flowerForm.name" class="mmb-edit__input" />
          </label>
          <label class="mmb-edit__field">
            <span class="mmb-edit__label">都道府県（任意）</span>
            <select v-model="flowerForm.location" class="mmb-edit__input">
              <option value="">選択してください</option>
              <option v-for="pref in PREFECTURES" :key="pref" :value="pref">{{ pref }}</option>
            </select>
          </label>
        </div>
      </template>

      <template v-else>
        <label class="mmb-edit__field">
          <span class="mmb-edit__label">タイトル</span>
          <input v-model="postForm.title" class="mmb-edit__input" />
        </label>

        <label class="mmb-edit__field">
          <span class="mmb-edit__label">本文</span>
          <textarea v-model="postForm.content" rows="6" class="mmb-edit__input mmb-edit__textarea" />
        </label>

        <div class="mmb-edit__row">
          <label class="mmb-edit__field">
            <span class="mmb-edit__label">お名前（任意）</span>
            <input v-model="postForm.name" class="mmb-edit__input" />
          </label>
          <label class="mmb-edit__field">
            <span class="mmb-edit__label">都道府県（任意）</span>
            <select v-model="postForm.location" class="mmb-edit__input">
              <option value="">選択してください</option>
              <option v-for="pref in PREFECTURES" :key="pref" :value="pref">{{ pref }}</option>
            </select>
          </label>
        </div>
      </template>

      <p v-if="formError || error" class="mmb-edit__error" role="alert">
        {{ formError || error }}
      </p>

      <div class="mmb-edit__actions">
        <UiButton variant="ghost" size="sm" type="button" :disabled="submitting" @click="emit('close')">
          キャンセル
        </UiButton>
        <UiButton variant="primary" size="sm" type="submit" :disabled="submitting">
          {{ submitting ? '保存中…' : '保存する' }}
        </UiButton>
      </div>
    </form>

    <MessageFlowerPickerModal
      :open="pickerOpen"
      :selected-index="flowerForm.flowerIndex"
      @close="pickerOpen = false"
      @select="onFlowerSelect"
    />
  </ModalShell>
</template>

<style scoped>
.mmb-edit__lead {
  margin: 0 0 var(--sp-5);
  font-size: var(--font-size-button);
  line-height: 1.8;
  color: var(--site-text-muted);
}

.mmb-edit__form {
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
}

.mmb-edit__flower-row {
  display: flex;
  justify-content: center;
}

.mmb-edit__flower-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: var(--sp-4);
  border: 1px solid var(--site-border-strong);
  border-radius: var(--site-radius-lg);
  background: var(--site-surface-muted);
  cursor: pointer;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-button);
  color: var(--murasaki-700);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.mmb-edit__flower-btn:hover {
  border-color: var(--murasaki-400);
  box-shadow: var(--site-shadow);
}

.mmb-edit__flower-change {
  font-size: var(--font-size-caption);
  color: var(--site-text-muted);
}

.mmb-edit__row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--sp-4);
}

.mmb-edit__field {
  display: block;
}

.mmb-edit__label {
  display: block;
  margin-bottom: 6px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-caption);
  color: var(--site-text-muted);
}

.mmb-edit__input {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 12px;
  border: 1px solid var(--site-border-strong);
  border-radius: var(--site-radius-sm);
  background: var(--site-surface);
  font-family: var(--ff-serif);
  font-size: var(--font-size-button);
  color: var(--site-text);
}

.mmb-edit__input:focus {
  outline: none;
  border-color: var(--murasaki-400);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--murasaki-400) 15%, transparent);
}

.mmb-edit__textarea {
  resize: vertical;
  min-height: 120px;
  line-height: 1.8;
}

.mmb-edit__error {
  margin: 0;
  font-size: var(--font-size-caption);
  color: var(--beni-600);
}

.mmb-edit__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--sp-3);
  margin-top: var(--sp-2);
}

@media (max-width: 640px) {
  .mmb-edit__row {
    grid-template-columns: 1fr;
  }
}
</style>
