<script setup>
/**
 * 部品名: 登録フォーム用 入力フィールド
 * 用途: ラベル + 入力欄 + パスワード表示切替 + エラー表示 を共通化
 * 特徴: v-model 対応（modelValue）、type=password の場合は表示切替ボタンを内蔵
 */
import { ref } from 'vue'
import UiIco from '../../ui/UiIco.vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
  /** input の id（label との紐付けに使用） */
  id: { type: String, required: true },
  label: { type: String, required: true },
  /** text / email / password / tel など */
  type: { type: String, default: 'text' },
  placeholder: { type: String, default: '' },
  autocomplete: { type: String, default: 'off' },
  /** モバイルキーボード種別（numeric など） */
  inputmode: { type: String, default: undefined },
  /** 最大文字数 */
  maxlength: { type: Number, default: undefined },
  /** バリデーションエラー文言（空なら非表示） */
  error: { type: String, default: '' },
  /** 補足説明 */
  hint: { type: String, default: '' },
  required: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue'])

const showPassword = ref(false)

function currentType() {
  if (props.type !== 'password') return props.type
  return showPassword.value ? 'text' : 'password'
}
</script>

<template>
  <div class="reg-field">
    <label class="reg-field__label" :for="id">
      {{ label }}
      <span v-if="required" class="reg-field__required" aria-hidden="true">必須</span>
    </label>

    <div class="reg-field__control" :class="{ 'reg-field__control--pw': type === 'password' }">
      <input
        :id="id"
        :type="currentType()"
        :value="modelValue"
        :placeholder="placeholder"
        :autocomplete="autocomplete"
        :inputmode="inputmode"
        :maxlength="maxlength"
        :aria-invalid="!!error"
        class="reg-field__input"
        :class="{ 'reg-field__input--error': !!error }"
        @input="emit('update:modelValue', $event.target.value)"
      />
      <button
        v-if="type === 'password'"
        type="button"
        class="reg-field__toggle"
        :aria-label="showPassword ? 'パスワードを隠す' : 'パスワードを表示'"
        @click="showPassword = !showPassword"
      >
        <UiIco :name="showPassword ? 'eye-off' : 'eye'" :size="18" color="var(--site-text-light)" />
      </button>
    </div>

    <p v-if="hint && !error" class="reg-field__hint">{{ hint }}</p>
    <p v-if="error" class="reg-field__error">{{ error }}</p>
  </div>
</template>

<style scoped>
.reg-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.reg-field__label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.04em;
  color: var(--murasaki-700);
}
.reg-field__required {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #fff;
  background: var(--murasaki-700);
  padding: 1px 7px;
  border-radius: 999px;
}
.reg-field__control {
  position: relative;
}
.reg-field__input {
  width: 100%;
  padding: 14px 16px;
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  color: var(--site-text);
  background: #f5f2ee;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
  transition: border-color 0.2s, box-shadow 0.2s;
}
.reg-field__control--pw .reg-field__input {
  padding-right: 48px;
}
.reg-field__input::placeholder {
  color: var(--site-text-muted);
  opacity: 1;
}
.reg-field__input:focus {
  outline: none;
  border-color: var(--murasaki-400);
  box-shadow: 0 0 0 3px rgba(122, 80, 136, 0.12);
}
.reg-field__input--error {
  border-color: #c0453b;
  background: #fdf3f2;
}
.reg-field__input--error:focus {
  box-shadow: 0 0 0 3px rgba(192, 69, 59, 0.14);
}
.reg-field__toggle {
  position: absolute;
  top: 50%;
  right: 12px;
  transform: translateY(-50%);
  background: transparent;
  border: 0;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.reg-field__hint {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  line-height: 1.6;
  color: var(--site-text) !important;
}
.reg-field__error {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  line-height: 1.6;
  color: #c0453b;
}
</style>
