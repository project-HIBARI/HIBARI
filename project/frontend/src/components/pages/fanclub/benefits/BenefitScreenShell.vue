<script setup>
/**
 * 会員特典の個別画面ラッパー（公開ページへは遷移しない）
 */
import SectionTitle from '../../../ui/SectionTitle.vue'

defineProps({
  title: { type: String, required: true },
  sub: { type: String, default: '' },
})

defineEmits(['back'])
</script>

<template>
  <section class="benefit-screen">
    <button type="button" class="benefit-screen__back" @click="$emit('back')">
      ‹ 特典一覧に戻る
    </button>
    <SectionTitle :title="title" :sub="sub" size="md" />
    <div class="benefit-screen__body">
      <slot />
    </div>
  </section>
</template>

<style scoped>
.benefit-screen__back {
  display: inline-flex;
  align-items: center;
  margin: 0 0 var(--sp-4);
  padding: 0;
  border: 0;
  background: transparent;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-button);
  font-weight: 700;
  color: var(--murasaki-700);
  cursor: pointer;
}
.benefit-screen__back:hover {
  text-decoration: underline;
}
.benefit-screen__body {
  margin-top: var(--sp-5);
}
</style>
