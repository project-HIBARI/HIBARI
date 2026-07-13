<script setup>
/**
 * 部品名: 思い出 — 投稿フォーム（サイド）
 */
import BoardPostForm from '../../board/BoardPostForm.vue'
import { aosAttrs } from '../../../lib/aos.js'

defineProps({
  submitted: { type: Boolean, default: false },
  submitting: { type: Boolean, default: false },
  submitError: { type: String, default: '' },
  postData: { type: Object, required: true },
  errors: { type: Object, default: () => ({}) },
})

const emit = defineEmits(['update:postData', 'submit', 'reset', 'need-auth'])
</script>

<template>
  <aside class="mem-post" v-bind="aosAttrs(200)" aria-label="思い出を投稿">
    <div class="mem-post__card">
      <BoardPostForm
        :post-data="postData"
        :errors="errors"
        :submitted="submitted"
        :submitting="submitting"
        :submit-error="submitError"
        @update:post-data="emit('update:postData', $event)"
        @submit="emit('submit')"
        @reset="emit('reset')"
        @need-auth="(m) => emit('need-auth', m)"
      />
    </div>
  </aside>
</template>

<style scoped>
.mem-post__card {
  position: sticky;
  top: 120px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  padding: var(--sp-5);
  background: linear-gradient(135deg, var(--site-bg-pink) 0%, var(--site-surface) 100%);
  box-shadow: var(--site-shadow);
}

@media (max-width: 767px) {
  .mem-post__card {
    position: static;
  }
}
</style>
