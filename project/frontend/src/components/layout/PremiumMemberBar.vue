<script setup>
/**
 * 部品名: プレミアム会員お知らせバー
 * 役割: サブスクリプション / ファンクラブ特典への導線（全ページ上部）
 */
const emit = defineEmits(['open-fanclub'])
</script>

<template>
  <div class="premium-bar" role="complementary">
    <button type="button" class="premium-bar__btn" @click="emit('open-fanclub')">
      <span class="premium-bar__icon">✦</span>
      サブスクリプションサービス · プレミアム会員特典を見る
      <span class="premium-bar__arrow">›</span>
    </button>
  </div>
</template>

<style scoped>
.premium-bar__btn {
  background: transparent;
  border: 0;
  cursor: pointer;
  font-family: var(--ff-mincho);
  font-size: 12px;
  letter-spacing: 0.12em;
  color: var(--murasaki-700);
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.premium-bar__btn:hover {
  color: var(--murasaki-800);
}
.premium-bar__icon {
  color: var(--kin-600);
}
.premium-bar__arrow {
  font-size: 16px;
  line-height: 1;
}
</style>
