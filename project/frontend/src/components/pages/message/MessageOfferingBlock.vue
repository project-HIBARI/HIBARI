<script setup>
/**
 * 部品名: 献花 — 投稿フォーム（インライン）
 */
import { ref, computed } from 'vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'
import { FLOWER_TYPES } from '../../../lib/flowers.js'
import { submitFlowerOffering } from '../../../api/flowers.js'
import { pageImageUrl, PAGE_IMAGES } from '../../../lib/pageImages.js'
import MessageFlowerPickerModal from './MessageFlowerPickerModal.vue'
import FlowerCutout from './FlowerCutout.vue'
import { aosAttrs } from '../../../lib/aos.js'

const emit = defineEmits(['submitted'])

const PREFECTURES = [
  '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県',
  '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県',
  '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県',
  '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県',
  '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県',
  '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県',
  '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県',
]

const selFlower = ref(0)
const flowerPicked = ref(false)
const pickerOpen = ref(false)
const formData = ref({ name: '', location: '', body: '', publish: true })
const submitting = ref(false)
const error = ref('')
const success = ref(false)

const previewImage = computed(() =>
  flowerPicked.value
    ? FLOWER_TYPES[selFlower.value].image
    : pageImageUrl(PAGE_IMAGES.kenka),
)
const previewAlt = computed(() =>
  flowerPicked.value ? FLOWER_TYPES[selFlower.value].name : '花を選ぶ',
)
const bodyLength = computed(() => formData.value.body.length)

function openPicker() {
  pickerOpen.value = true
}

function onFlowerSelect(i) {
  selFlower.value = i
  flowerPicked.value = true
}

async function submitOffering() {
  if (submitting.value) return
  error.value = ''
  if (!formData.value.body.trim()) {
    error.value = 'メッセージを入力してください。'
    return
  }
  if (!flowerPicked.value) {
    error.value = '花を選んでください。'
    return
  }
  submitting.value = true
  try {
    await submitFlowerOffering({
      name: formData.value.name.trim() || '匿名',
      location: formData.value.location || null,
      content: formData.value.body.trim(),
      flower_type: FLOWER_TYPES[selFlower.value].name,
    })
    success.value = true
    formData.value = { name: '', location: '', body: '', publish: true }
    flowerPicked.value = false
    selFlower.value = 0
    emit('submitted')
    window.setTimeout(() => {
      success.value = false
    }, 4000)
  } catch (err) {
    error.value = err.message || '献花の送信に失敗しました。'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <section id="message-offer" class="msg-offer" aria-labelledby="msg-offer-title">
    <header class="msg-offer__head" v-bind="aosAttrs()">
      <h2 id="msg-offer-title" class="msg-offer__title">
        献花を投稿する
        <UiIco name="flower" :size="18" color="var(--murasaki-600)" />
      </h2>
      <p class="msg-offer__lead">花と言葉を添えて、美空ひばりへ想いを届けましょう。</p>
    </header>

    <p v-if="success" class="msg-offer__success" role="status">
      献花ありがとうございます。メッセージを記録しました。
    </p>

    <template v-else>
        <form class="msg-offer__form" @submit.prevent="submitOffering">
          <div class="msg-offer__body">
            <div class="msg-offer__flower-col">
              <button
                type="button"
                class="msg-offer__flower-btn"
                aria-label="花を選ぶ・変更する"
                @click="openPicker"
              >
                <div class="msg-offer__flower-frame">
                  <FlowerCutout
                    :src="previewImage"
                    :alt="previewAlt"
                    :size="flowerPicked ? 'lg' : 'picker'"
                  />
                </div>
                <span class="msg-offer__flower-label">花を選ぶ・変更する</span>
              </button>
            </div>

            <div class="msg-offer__fields">
              <div class="msg-offer__row">
                <label class="msg-offer__field msg-offer__field--name">
                  <span class="msg-offer__label">お名前<span class="msg-offer__label-note">（ニックネーム可）</span></span>
                  <input
                    v-model="formData.name"
                    class="msg-offer__input"
                    placeholder="例：ひばりファン"
                    autocomplete="name"
                  />
                </label>
                <label class="msg-offer__field">
                  <span class="msg-offer__label">都道府県（任意）</span>
                  <select v-model="formData.location" class="msg-offer__input msg-offer__select" aria-label="都道府県">
                    <option value="">選択してください</option>
                    <option v-for="p in PREFECTURES" :key="p" :value="p">{{ p }}</option>
                  </select>
                </label>
              </div>

              <label class="msg-offer__field">
                <span class="msg-offer__label">メッセージ</span>
                <textarea
                  v-model="formData.body"
                  rows="5"
                  class="msg-offer__input msg-offer__textarea"
                  placeholder="美空ひばりへの想いを自由にお書きください。（最大300文字）"
                  maxlength="300"
                />
                <span class="msg-offer__count" aria-live="polite">{{ bodyLength }} / 300</span>
              </label>

              <label class="msg-offer__check">
                <input v-model="formData.publish" type="checkbox" class="msg-offer__checkbox" />
                <span class="msg-offer__check-text">
                  メッセージを公開する
                  <span class="msg-offer__check-sub">（チェックを外すと非公開になります）</span>
                </span>
              </label>

              <p v-if="error" class="msg-offer__error" role="alert">{{ error }}</p>

              <UiButton
                variant="primary"
                size="md"
                type="submit"
                class="msg-offer__submit"
                aria-label="献花を投稿する"
                :disabled="submitting"
              >
                {{ submitting ? '送信中…' : '献花を投稿する' }}
                <UiIco name="flower" :size="14" color="#fff" />
              </UiButton>
            </div>
          </div>
        </form>

      <p class="msg-offer__note">※ 投稿いただいた内容は、運営にて確認のうえ掲載いたします。</p>
    </template>

    <MessageFlowerPickerModal
      :open="pickerOpen"
      :selected-index="selFlower"
      @close="pickerOpen = false"
      @select="onFlowerSelect"
    />
  </section>
</template>

<style scoped>
.msg-offer {
  border-radius: 24px;
  border: 1px solid color-mix(in srgb, var(--kin-500) 35%, var(--site-border));
  background:
    radial-gradient(ellipse at 0% 0%, rgba(252, 232, 236, 0.5) 0%, transparent 50%),
    color-mix(in srgb, var(--site-surface) 92%, transparent);
  box-shadow: var(--site-shadow);
  padding: var(--sp-6) var(--sp-5);
}

.msg-offer__head {
  margin-bottom: var(--sp-5);
}

.msg-offer__title {
  margin: 0 0 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.25rem, 2.2vw, 1.5rem);
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--murasaki-800);
}

.msg-offer__lead {
  margin: 0;
  font-size: var(--font-size-caption);
  line-height: 1.8;
  color: var(--murasaki-700);
}

.msg-offer__success {
  margin: 0;
  padding: var(--sp-5) 0;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-small);
  line-height: 1.9;
  color: var(--murasaki-700);
  text-align: center;
}

.msg-offer__body {
  display: grid;
  grid-template-columns: minmax(0, 132px) minmax(0, 1fr);
  gap: var(--sp-4);
  align-items: start;
}

.msg-offer__flower-col {
  min-width: 0;
}

.msg-offer__flower-btn {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  width: 100%;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
  text-align: center;
}

.msg-offer__flower-frame {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 160px;
  padding: var(--sp-2);
  border: 1px solid var(--kin-500);
  border-radius: var(--site-radius-md);
  background: rgba(255, 255, 255, 0.75);
  transition: box-shadow 0.25s, border-color 0.25s;
}

.msg-offer__flower-btn:hover .msg-offer__flower-frame {
  border-color: var(--kin-600);
  box-shadow: 0 6px 20px rgba(201, 169, 97, 0.2);
}

.msg-offer__flower-label {
  margin-top: 8px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-badge);
  letter-spacing: 0.04em;
  color: var(--murasaki-700);
  line-height: 1.5;
}

.msg-offer__form {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-width: 0;
}

.msg-offer__fields {
  display: flex;
  flex-direction: column;
  gap: var(--sp-3);
  min-width: 0;
  width: 100%;
}

.msg-offer__row {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr);
  gap: var(--sp-3);
  align-items: end;
}

.msg-offer__field {
  display: block;
  margin: 0;
  position: relative;
  min-width: 0;
}

.msg-offer__label {
  display: block;
  margin-bottom: 6px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-badge);
  line-height: 1.4;
  letter-spacing: 0;
  color: var(--site-text-muted);
  white-space: normal;
  overflow-wrap: anywhere;
}

.msg-offer__label-note {
  letter-spacing: 0;
}

.msg-offer__input {
  width: 100%;
  box-sizing: border-box;
  background: var(--site-surface);
  border: 1px solid var(--site-border-strong);
  color: var(--site-text);
  padding: 10px 12px;
  font-family: var(--ff-serif);
  font-size: var(--font-size-button);
  border-radius: var(--site-radius-sm);
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.msg-offer__input:focus {
  border-color: var(--murasaki-400);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--murasaki-400) 15%, transparent);
}

.msg-offer__select {
  appearance: auto;
}

.msg-offer__textarea {
  resize: vertical;
  min-height: 120px;
  line-height: 1.8;
}

.msg-offer__count {
  display: block;
  margin-top: 6px;
  text-align: right;
  font-family: var(--ff-mono);
  font-size: var(--font-size-badge);
  color: var(--site-text-light);
}

.msg-offer__check {
  display: grid;
  grid-template-columns: 18px minmax(0, 1fr);
  align-items: start;
  column-gap: 10px;
  width: 100%;
  margin: 0;
  font-size: var(--font-size-caption);
  line-height: 1.7;
  color: var(--site-text-muted);
  cursor: pointer;
}

.msg-offer__check-text {
  display: block;
  width: 100%;
  min-width: 0;
  white-space: normal;
  word-break: normal;
  overflow-wrap: break-word;
  letter-spacing: 0;
}

.msg-offer__check-sub {
  display: inline;
}

.msg-offer__checkbox {
  width: 16px;
  height: 16px;
  margin: 2px 0 0;
}

.msg-offer__error {
  margin: 0;
  font-size: var(--font-size-caption);
  color: var(--beni-600);
}

.msg-offer__submit {
  width: 100%;
  margin-top: var(--sp-1);
}

.msg-offer__note {
  margin: var(--sp-5) 0 0;
  font-size: var(--font-size-badge);
  line-height: 1.7;
  color: var(--site-text-light);
  text-align: center;
}

@media (max-width: 1023px) {
  .msg-offer__body {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--sp-4);
  }

  .msg-offer__row {
    grid-template-columns: minmax(0, 1fr);
    align-items: stretch;
  }

  .msg-offer__flower-frame {
    min-height: 140px;
    max-width: min(132px, 100%);
    margin: 0 auto;
  }
}
</style>
