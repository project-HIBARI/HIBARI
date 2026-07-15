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
      <span class="premium-bar__text premium-bar__text--full">サブスクリプションサービス · プレミアム会員特典を見る</span>
      <span class="premium-bar__text premium-bar__text--short">プレミアム会員特典を見る</span>
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
  font-size: var(--font-size-caption);
  letter-spacing: 0.12em;
  color: var(--murasaki-700);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
  width: 100%;
  max-width: 100%;
  padding: 0 8px;
  line-height: 1.5;
}
.premium-bar__btn:hover {
  color: var(--murasaki-800);
}
.premium-bar__icon {
  color: var(--kin-600);
  flex-shrink: 0;
}
.premium-bar__text--short {
  display: none;
}
.premium-bar__arrow {
  font-size: var(--font-size-body);
  line-height: 1;
  flex-shrink: 0;
}

@media (max-width: 767px) {
  .premium-bar__btn {
    font-size: var(--font-size-caption);
    letter-spacing: 0.06em;
  }
  .premium-bar__text--full {
    display: none;
  }
  .premium-bar__text--short {
    display: inline;
  }
}
</style>
