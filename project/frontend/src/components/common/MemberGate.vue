<script setup>
/**
 * 会員権限ゲート — 権限がない場合に案内を表示
 */
import { computed } from 'vue'
import { useMemberAccess } from '../../composables/useMemberAccess.js'

const props = defineProps({
  permission: { type: String, required: true },
  feature: { type: String, default: 'この機能' },
  compact: { type: Boolean, default: false },
})

const emit = defineEmits(['login', 'register', 'upgrade'])

const { getAccessState } = useMemberAccess()
const state = computed(() => getAccessState(props.permission))
</script>

<template>
  <slot v-if="state.allowed" />
  <div v-else class="member-gate" :class="{ 'member-gate--compact': compact }">
    <p class="member-gate__icon" aria-hidden="true">🔒</p>
    <p class="member-gate__title">{{ feature }}</p>
    <p class="member-gate__text">{{ state.message }}</p>
    <div class="member-gate__actions">
      <template v-if="state.reason === 'login'">
        <button type="button" class="member-gate__btn member-gate__btn--primary" @click="emit('login')">
          Music Memories でログイン
        </button>
      </template>
      <template v-else-if="state.reason === 'fanclub'">
        <button type="button" class="member-gate__btn member-gate__btn--primary" @click="emit('register')">
          Music Memories でファンクラブ加入
        </button>
      </template>
      <button
        v-else-if="state.reason === 'upgrade'"
        type="button"
        class="member-gate__btn member-gate__btn--primary"
        @click="emit('upgrade')"
      >
        Music Memories でプレミアム登録
      </button>
    </div>
  </div>
</template>

<style scoped>
.member-gate {
  padding: 20px 18px;
  text-align: center;
  background: var(--site-surface-muted);
  border: 1px dashed var(--site-border-strong);
  border-radius: var(--site-radius-md);
}
.member-gate--compact {
  padding: 14px 12px;
}
.member-gate__icon {
  margin: 0 0 8px;
  font-size: var(--font-size-subtitle);
}
.member-gate__title {
  margin: 0 0 6px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-body);
  font-weight: 700;
  color: var(--site-text);
}
.member-gate__text {
  margin: 0 0 14px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  line-height: 1.7;
  color: var(--site-text-muted);
}
.member-gate__actions {
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
}
.member-gate__btn {
  padding: 8px 16px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  border-radius: 999px;
  border: 1px solid var(--site-border-strong);
  background: var(--site-surface);
  color: var(--site-text);
  cursor: pointer;
}
.member-gate__btn--primary {
  background: var(--murasaki-700);
  border-color: var(--murasaki-800);
  color: #fff;
}
</style>
