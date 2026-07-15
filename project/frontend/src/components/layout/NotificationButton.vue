<script setup>
/**
 * 部品名: 通知ベル（未読バッジ付き）
 * 役割: SNSヘッダー／モバイルヘッダーから通知センターを開く共通ボタン
 */
import UiIco from '../ui/UiIco.vue'

const props = defineProps({
  unreadCount: { type: Number, default: 0 },
  size: { type: Number, default: 20 },
})

defineEmits(['click'])

function badgeLabel(count) {
  if (count > 99) return '99+'
  return String(count)
}
</script>

<template>
  <button
    type="button"
    class="notification-button"
    :aria-label="unreadCount > 0 ? `通知（未読${unreadCount}件）` : '通知'"
    @click="$emit('click')"
  >
    <UiIco name="bell" :size="size" />
    <span v-if="unreadCount > 0" class="notification-button__badge" aria-hidden="true">
      {{ badgeLabel(unreadCount) }}
    </span>
    <span v-if="unreadCount > 0" class="sr-only">未読通知{{ unreadCount }}件</span>
  </button>
</template>

<style scoped>
.notification-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: transparent;
  border: 0;
  color: inherit;
}

.notification-button__badge {
  position: absolute;
  top: -6px;
  right: -8px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: 999px;
  background: var(--beni-600);
  color: #fff;
  font-size: var(--font-size-badge);
  line-height: 16px;
  text-align: center;
  border: 2px solid rgba(22, 15, 24, 0.96);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>
