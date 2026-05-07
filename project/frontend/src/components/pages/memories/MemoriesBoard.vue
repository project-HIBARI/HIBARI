<script setup>
/**
 * 部品名: 思い出掲示板 — 投稿リスト
 */
defineProps({
  items: { type: Array, required: true },
})

const emit = defineEmits(['like'])
</script>

<template>
  <div style="display: flex; flex-direction: column; gap: 28px">
    <article
      v-for="m in items"
      :key="m.id"
      style="border: 1px solid rgba(201,169,97,0.2); border-left: 4px solid var(--beni-500); padding: 24px 28px; position: relative; background: rgba(250,245,234,0.03)"
    >
      <div
        style="position: absolute; top: -11px; right: 20px; background: var(--beni-700); color: var(--kin-500); padding: 3px 12px; font-family: var(--ff-mono); font-size: 10px; letter-spacing: 0.15em; border: 1px solid var(--kin-500)"
      >
        ♪ {{ m.song }}
      </div>
      <h3 style="font-family: var(--ff-mincho); font-size: 20px; margin: 0 0 12px; letter-spacing: 0.06em">{{ m.title }}</h3>
      <p style="font-size: 14px; line-height: 2.1; color: var(--paper-100); margin: 0">{{ m.body }}</p>
      <div style="margin-top: 16px; padding-top: 12px; border-top: 1px solid rgba(201,169,97,0.2); display: flex; justify-content: space-between; align-items: center">
        <span style="font-size: 12px; color: var(--paper-300)">{{ m.author }}（{{ m.age }}歳・{{ m.location }}）</span>
        <div style="display: flex; gap: 16px; align-items: center">
          <button
            type="button"
            style="background: transparent; border: 0; cursor: pointer; color: var(--paper-300); display: flex; align-items: center; gap: 5px; font-family: var(--ff-mono); font-size: 12px"
            aria-label="いいね"
            @click="emit('like', m.id)"
          >
            ♡ {{ m.displayLikes }}
          </button>
          <span style="color: var(--paper-300); font-family: var(--ff-mono); font-size: 12px">💬 {{ m.comments }}</span>
          <span style="font-family: var(--ff-mono); font-size: 11px; color: var(--paper-300)">{{ m.date }}</span>
        </div>
      </div>
    </article>
  </div>
</template>
