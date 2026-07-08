<script setup>
/**
 * 部品名: 登録フォーム用 選択グループ
 * 用途: 性別・支払い方法などの単一選択（ラジオ）をカード風に共通化
 * 特徴: v-model 対応。options は { value, label, desc? } の配列
 */
const props = defineProps({
  modelValue: { type: String, default: '' },
  /** グループ名（ラジオの name 属性・id 接頭辞に使用） */
  name: { type: String, required: true },
  label: { type: String, required: true },
  options: { type: Array, required: true },
  /** 1行に並べる列数 */
  columns: { type: Number, default: 2 },
  error: { type: String, default: '' },
  required: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <fieldset class="reg-opt">
    <legend class="reg-opt__label">
      {{ label }}
      <span v-if="required" class="reg-opt__required" aria-hidden="true">必須</span>
    </legend>

    <div
      class="reg-opt__grid"
      :style="{ gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))` }"
    >
      <label
        v-for="opt in options"
        :key="opt.value"
        class="reg-opt__item"
        :class="{ 'reg-opt__item--active': modelValue === opt.value }"
      >
        <input
          class="reg-opt__radio"
          type="radio"
          :name="name"
          :value="opt.value"
          :checked="modelValue === opt.value"
          @change="emit('update:modelValue', opt.value)"
        />
        <span class="reg-opt__mark" aria-hidden="true" />
        <span class="reg-opt__text">
          <span class="reg-opt__name">{{ opt.label }}</span>
          <span v-if="opt.desc" class="reg-opt__desc">{{ opt.desc }}</span>
        </span>
      </label>
    </div>

    <p v-if="error" class="reg-opt__error">{{ error }}</p>
  </fieldset>
</template>

<style scoped>
.reg-opt {
  border: 0;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.reg-opt__label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 0;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.04em;
  color: var(--site-text);
}
.reg-opt__required {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #fff;
  background: var(--murasaki-600);
  padding: 1px 7px;
  border-radius: 999px;
}
.reg-opt__grid {
  display: grid;
  gap: 10px;
}
.reg-opt__item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  background: #f5f2ee;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s, box-shadow 0.2s;
}
.reg-opt__item:hover {
  border-color: var(--murasaki-400);
}
.reg-opt__item--active {
  border-color: var(--murasaki-600);
  background: var(--murasaki-100);
  box-shadow: 0 0 0 3px rgba(122, 80, 136, 0.1);
}
.reg-opt__radio {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}
.reg-opt__mark {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  border-radius: 999px;
  border: 1.5px solid var(--site-border-strong);
  background: #fff;
  transition: border-color 0.2s;
}
.reg-opt__item--active .reg-opt__mark {
  border-color: var(--murasaki-600);
  border-width: 5px;
}
.reg-opt__text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}
.reg-opt__name {
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  color: var(--site-text);
}
.reg-opt__desc {
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  line-height: 1.5;
  color: var(--site-text-light);
}
.reg-opt__error {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  color: #c0453b;
}

@media (max-width: 480px) {
  .reg-opt__grid {
    grid-template-columns: 1fr !important;
  }
}
</style>
