<script setup>
/**
 * 部品名: セクション見出し
 * 用途: 各ページ内のブロックタイトル（最新ニュース、人気スポット等）を表示
 */
defineProps({
  title: { type: String, required: true },
  /** 右側に表示するリンクテキスト（省略可） */
  linkLabel: { type: String, default: '' },
  /** 英字サブタイトル */
  sub: { type: String, default: '' },
  /** sm / md / lg */
  size: { type: String, default: 'md' },
})

defineEmits(['link-click'])
</script>

<template>
  <div class="section-title" :class="`section-title--${size}`">
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
  gap: 16px;
  margin-bottom: var(--sp-5);
  padding-bottom: var(--sp-3);
  border-bottom: 1px solid var(--site-border);
}
.section-title__heading {
  margin: 0;
  font-family: var(--ff-mincho);
  font-weight: 700;
  color: var(--site-text);
  letter-spacing: 0.06em;
}
.section-title--sm .section-title__heading {
  font-size: 16px;
}
.section-title--md .section-title__heading {
  font-size: 20px;
}
.section-title--lg .section-title__heading {
  font-size: 24px;
}
.section-title__sub {
  margin: 4px 0 0;
  font-family: var(--ff-latin);
  font-style: italic;
  font-size: 12px;
  color: var(--kin-600);
  letter-spacing: 0.12em;
}
.section-title__link {
  background: transparent;
  border: 0;
  padding: 0;
  cursor: pointer;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  color: var(--murasaki-700);
  letter-spacing: 0.04em;
  white-space: nowrap;
}
.section-title__link:hover {
  text-decoration: underline;
}
</style>
