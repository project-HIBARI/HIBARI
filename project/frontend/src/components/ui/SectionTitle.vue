<script setup>
/**
 * 部品名: セクション見出し
 * 用途: 各ページ内のブロックタイトル（最新ニュース、人気スポット等）を表示
 */
import { aosAttrs } from '../../lib/aos.js'

defineProps({
  title: { type: String, required: true },
  /** 右側に表示するリンクテキスト（省略可） */
  linkLabel: { type: String, default: '' },
  /** 英字サブタイトル */
  sub: { type: String, default: '' },
  /** sm / md / lg */
  size: { type: String, default: 'md' },
  /** AOS スクロールアニメーション */
  aos: { type: Boolean, default: true },
})

defineEmits(['link-click'])
</script>

<template>
  <div
    class="section-title"
    :class="`section-title--${size}`"
    v-bind="aos ? aosAttrs() : {}"
  >
    <div class="section-title__main">
      <h2 class="section-title__heading">{{ title }}</h2>
      <p v-if="sub" class="section-title__sub">{{ sub }}</p>
    </div>
    <button
      v-if="linkLabel"
      type="button"
      class="section-title__link"
      @click="$emit('link-click')"
    >
      {{ linkLabel }}
    </button>
  </div>
</template>

<style scoped>
.section-title {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--sp-4);
  margin-bottom: var(--sp-5);
  padding-bottom: var(--sp-3);
  border-bottom: 1px solid var(--site-border);
  min-width: 0;
}
.section-title__main {
  min-width: 0;
  flex: 1 1 auto;
}
.section-title__heading {
  margin: 0;
  font-family: var(--ff-mincho);
  font-weight: 700;
  color: var(--site-text);
  letter-spacing: 0.06em;
  line-height: 1.4;
  overflow-wrap: break-word;
  word-break: break-word;
}
.section-title--sm .section-title__heading {
  font-size: var(--font-size-body); /* 16px @ m */
}
.section-title--md .section-title__heading {
  font-size: var(--font-size-subtitle); /* 20px @ m */
}
.section-title--lg .section-title__heading {
  font-size: var(--font-size-title); /* 24px @ m */
}
.section-title__sub {
  margin: 0.25rem 0 0;
  font-family: var(--ff-latin);
  font-style: italic;
  font-size: var(--font-size-caption);
  line-height: 1.4;
  color: var(--kin-600);
  letter-spacing: 0.12em;
  overflow-wrap: break-word;
}
.section-title__link {
  background: transparent;
  border: 0;
  padding: 0;
  cursor: pointer;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  line-height: 1.4;
  color: var(--murasaki-700);
  letter-spacing: 0.04em;
  white-space: nowrap;
  flex-shrink: 0;
  align-self: flex-end;
}
.section-title__link:hover {
  text-decoration: underline;
}
.section-title__link:focus-visible {
  outline: 2px solid var(--murasaki-600);
  outline-offset: 2px;
}
</style>
