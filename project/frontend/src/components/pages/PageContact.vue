<script setup>
/**
 * ページ: お問い合わせ
 */
import { reactive, ref } from 'vue'
import { submitContact } from '../../api/contact.js'

const categoryOptions = [
  'サイトについて',
  'サブスクリプションについて',
  'AI美空ひばりについて',
  'ディスコグラフィーについて',
  '思い出掲示板について',
  '献花について',
  'その他',
]

const form = reactive({
  name: '',
  email: '',
  category: '',
  subject: '',
  body: '',
})

const errors = reactive({
  name: '',
  email: '',
  category: '',
  subject: '',
  body: '',
})

const submitted = ref(false)
const submitting = ref(false)
const submitError = ref('')

function validate() {
  errors.name = ''
  errors.email = ''
  errors.category = ''
  errors.subject = ''
  errors.body = ''

  let ok = true

  if (!form.name.trim()) {
    errors.name = 'お名前を入力してください。'
    ok = false
  }

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!form.email.trim()) {
    errors.email = 'メールアドレスを入力してください。'
    ok = false
  } else if (!emailPattern.test(form.email.trim())) {
    errors.email = 'メールアドレスの形式が正しくありません。'
    ok = false
  }

  if (!form.category) {
    errors.category = 'お問い合わせ種別を選択してください。'
    ok = false
  }

  if (!form.subject.trim()) {
    errors.subject = '件名を入力してください。'
    ok = false
  }

  if (!form.body.trim()) {
    errors.body = 'お問い合わせ内容を入力してください。'
    ok = false
  }

  return ok
}

function onSubmit(event) {
  event.preventDefault()
  submitted.value = false
  submitError.value = ''

  if (!validate()) return

  submitting.value = true
  submitContact({
    name: form.name.trim(),
    email: form.email.trim(),
    category: form.category,
    subject: form.subject.trim(),
    body: form.body.trim(),
  })
    .then(() => {
      submitted.value = true
      window.scrollTo({ top: 0, behavior: 'smooth' })
    })
    .catch((err) => {
      submitError.value = err.message || '送信に失敗しました。'
    })
    .finally(() => {
      submitting.value = false
    })
}
</script>

<template>
  <div class="page-contact">
    <div class="page-contact__decor" aria-hidden="true">
      <span class="page-contact__arc page-contact__arc--1" />
      <span class="page-contact__arc page-contact__arc--2" />
      <span class="page-contact__star page-contact__star--1">✦</span>
      <span class="page-contact__star page-contact__star--2">✦</span>
    </div>

    <div class="page-contact__inner">
      <header class="page-contact__head">
        <div class="page-contact__ornament page-contact__ornament--top" aria-hidden="true">
          <span class="page-contact__ornament-line" />
          <span class="page-contact__ornament-mark">❧</span>
          <span class="page-contact__ornament-line" />
        </div>
        <h1 class="page-contact__title">お問い合わせ</h1>
        <p class="page-contact__lead">
          当サイトに関するご質問・ご意見・ご要望などをお寄せください。<br />
          内容を確認のうえ、担当者よりご連絡いたします。
        </p>
        <div class="page-contact__ornament" aria-hidden="true">
          <span class="page-contact__ornament-line" />
          <span class="page-contact__ornament-diamond">◆</span>
          <span class="page-contact__ornament-line" />
        </div>
      </header>

      <p v-if="submitted" class="page-contact__notice" role="status">
        お問い合わせを受け付けました。内容を確認のうえ、担当者よりご連絡いたします。
      </p>
      <p v-if="submitError" class="page-contact__error-banner" role="alert">{{ submitError }}</p>

      <form class="page-contact__card" novalidate @submit="onSubmit">
        <div class="page-contact__field">
          <label class="page-contact__label" for="contact-name">
            お名前<span class="page-contact__required">（必須）</span>
          </label>
          <input
            id="contact-name"
            v-model="form.name"
            type="text"
            class="page-contact__input"
            :class="{ 'page-contact__input--error': errors.name }"
            placeholder="例）美空 花子"
            autocomplete="name"
          />
          <p v-if="errors.name" class="page-contact__error" role="alert">{{ errors.name }}</p>
        </div>

        <div class="page-contact__field">
          <label class="page-contact__label" for="contact-email">
            メールアドレス<span class="page-contact__required">（必須）</span>
          </label>
          <input
            id="contact-email"
            v-model="form.email"
            type="email"
            class="page-contact__input"
            :class="{ 'page-contact__input--error': errors.email }"
            placeholder="例）misora@example.com"
            autocomplete="email"
          />
          <p v-if="errors.email" class="page-contact__error" role="alert">{{ errors.email }}</p>
        </div>

        <div class="page-contact__field">
          <label class="page-contact__label" for="contact-category">
            お問い合わせ種別<span class="page-contact__required">（必須）</span>
          </label>
          <div class="page-contact__select-wrap">
            <select
              id="contact-category"
              v-model="form.category"
              class="page-contact__select"
              :class="{ 'page-contact__input--error': errors.category }"
            >
              <option value="" disabled>選択してください</option>
              <option v-for="opt in categoryOptions" :key="opt" :value="opt">{{ opt }}</option>
            </select>
          </div>
          <p v-if="errors.category" class="page-contact__error" role="alert">{{ errors.category }}</p>
        </div>

        <div class="page-contact__field">
          <label class="page-contact__label" for="contact-subject">
            件名<span class="page-contact__required">（必須）</span>
          </label>
          <input
            id="contact-subject"
            v-model="form.subject"
            type="text"
            class="page-contact__input"
            :class="{ 'page-contact__input--error': errors.subject }"
            placeholder="例）サイトについてのご質問"
          />
          <p v-if="errors.subject" class="page-contact__error" role="alert">{{ errors.subject }}</p>
        </div>

        <div class="page-contact__field">
          <label class="page-contact__label" for="contact-body">
            お問い合わせ内容<span class="page-contact__required">（必須）</span>
          </label>
          <textarea
            id="contact-body"
            v-model="form.body"
            rows="7"
            class="page-contact__textarea"
            :class="{ 'page-contact__input--error': errors.body }"
            placeholder="お問い合わせ内容をご入力ください。"
          />
          <p v-if="errors.body" class="page-contact__error" role="alert">{{ errors.body }}</p>
        </div>

        <p class="page-contact__privacy">
          ※ ご入力いただいた個人情報は、お問い合わせへの対応以外の目的では使用いたしません。
        </p>

        <div class="page-contact__actions">
          <button type="submit" class="page-contact__submit" :disabled="submitting">
            {{ submitting ? '送信中…' : '送信する' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.page-contact {
  position: relative;
  overflow: hidden;
  color: var(--site-text);
  background: linear-gradient(180deg, #fffefb 0%, var(--site-bg) 100%);
  padding: 48px 24px 72px;
}

.page-contact__decor {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.page-contact__arc {
  position: absolute;
  border: 1px solid rgba(201, 169, 97, 0.18);
  border-radius: 50%;
}

.page-contact__arc--1 {
  width: 280px;
  height: 280px;
  top: 12%;
  right: -80px;
}

.page-contact__arc--2 {
  width: 200px;
  height: 200px;
  top: 28%;
  right: 40px;
}

.page-contact__star {
  position: absolute;
  color: rgba(201, 169, 97, 0.35);
  font-size: 12px;
  line-height: 1;
}

.page-contact__star--1 {
  top: 18%;
  right: 120px;
}

.page-contact__star--2 {
  top: 34%;
  right: 200px;
  font-size: 10px;
}

.page-contact__inner {
  position: relative;
  z-index: 1;
  max-width: 860px;
  margin: 0 auto;
  text-align: center;
}

.page-contact__head {
  margin-bottom: 32px;
}

.page-contact__ornament {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  max-width: 320px;
  margin: 0 auto;
}

.page-contact__ornament--top {
  margin-bottom: 16px;
  max-width: 200px;
}

.page-contact__ornament-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--kin-500), transparent);
}

.page-contact__ornament-diamond,
.page-contact__ornament-mark {
  flex-shrink: 0;
  font-size: 10px;
  line-height: 1;
  color: var(--kin-600);
}

.page-contact__ornament-mark {
  font-size: 14px;
}

.page-contact__title {
  margin: 0 0 20px;
  font-family: var(--ff-mincho);
  font-size: clamp(28px, 4vw, 36px);
  font-weight: 700;
  letter-spacing: 0.12em;
  color: var(--murasaki-800);
}

.page-contact__lead {
  margin: 0 0 20px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 2;
  letter-spacing: 0.04em;
  color: var(--site-text-muted);
}

.page-contact__notice {
  margin: 0 0 20px;
  padding: 12px 16px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.7;
  color: var(--murasaki-700);
  background: var(--murasaki-100);
  border: 1px solid var(--murasaki-300);
  border-radius: var(--site-radius-sm);
}

.page-contact__error-banner {
  margin: 0 0 20px;
  padding: 12px 16px;
  font-size: 13px;
  color: var(--beni-600);
  background: #fff5f4;
  border: 1px solid var(--beni-300);
  border-radius: var(--site-radius-sm);
}

.page-contact__card {
  text-align: left;
  margin: 0 auto;
  max-width: 820px;
  padding: 36px 40px 40px;
  background: var(--site-surface);
  border: 1px solid rgba(201, 169, 97, 0.25);
  border-radius: var(--site-radius-lg);
  box-shadow: 0 8px 32px rgba(60, 40, 30, 0.06);
}

.page-contact__field {
  margin-bottom: 22px;
}

.page-contact__label {
  display: block;
  margin-bottom: 8px;
  font-family: var(--ff-mincho);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--murasaki-800);
}

.page-contact__required {
  font-size: 12px;
  font-weight: 500;
  color: var(--beni-600);
}

.page-contact__input,
.page-contact__select,
.page-contact__textarea {
  width: 100%;
  padding: 12px 14px;
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  color: var(--site-text);
  background: #faf8f5;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
  outline: none;
  transition: border-color 0.2s;
}

.page-contact__input:focus,
.page-contact__select:focus,
.page-contact__textarea:focus {
  border-color: var(--murasaki-400);
}

.page-contact__input--error {
  border-color: var(--beni-500);
}

.page-contact__select-wrap {
  position: relative;
}

.page-contact__select {
  appearance: none;
  cursor: pointer;
  padding-right: 36px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath fill='%236b5b6e' d='M1 1l5 5 5-5'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
}

.page-contact__textarea {
  resize: vertical;
  min-height: 160px;
  line-height: 1.8;
}

.page-contact__error {
  margin: 6px 0 0;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  color: var(--beni-600);
}

.page-contact__privacy {
  margin: 8px 0 28px;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  line-height: 1.8;
  color: var(--site-text-light);
  text-align: center;
}

.page-contact__actions {
  display: flex;
  justify-content: center;
}

.page-contact__submit {
  min-width: 280px;
  max-width: 100%;
  padding: 14px 48px;
  font-family: var(--ff-mincho);
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: #fff;
  background: linear-gradient(180deg, var(--murasaki-600) 0%, var(--murasaki-800) 100%);
  border: 1px solid var(--murasaki-800);
  border-radius: 999px;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(74, 47, 80, 0.2);
  transition: filter 0.2s, transform 0.1s;
}

.page-contact__submit:hover {
  filter: brightness(1.06);
}

.page-contact__submit:active {
  transform: translateY(1px);
}

@media (max-width: 767px) {
  .page-contact {
    padding: 36px 16px 56px;
  }

  .page-contact__card {
    padding: 24px 18px 28px;
  }

  .page-contact__submit {
    width: 100%;
    min-width: 0;
  }

  .page-contact__decor {
    opacity: 0.5;
  }
}
</style>
