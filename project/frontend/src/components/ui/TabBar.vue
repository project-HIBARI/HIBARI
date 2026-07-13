<script setup>
/**
 * 部品名: タブバー（ページ内サブナビ）
 * 用途: ゆかりの地（地図/一覧）、思い出（投稿/イベント）、AI モーダルなど
 */
import UiIco from './UiIco.vue'

defineProps({
  tabs: { type: Array, required: true },
  active: { type: String, required: true },
  /** true なら墨背景向けの明るい文字色 */
  dark: { type: Boolean, default: true },
  /** true なら角丸ピル型セグメントコントロール表示（SNS画面向け） */
  pill: { type: Boolean, default: false },
})

const emit = defineEmits(['update:active'])
</script>

<template>
  <nav class="tab-bar" :class="{ 'tab-bar--light': !dark, 'tab-bar--pill': pill }" role="tablist">
    <button
      v-for="t in tabs"
      :key="t.id"
      type="button"
      role="tab"
      class="tab-bar__btn"
      :class="{ 'tab-bar__btn--active': t.id === active }"
      :aria-selected="t.id === active"
      @click="emit('update:active', t.id)"
    >
      <UiIco v-if="t.icon" :name="t.icon" :size="14" />
      {{ t.label }}
      <span v-if="t.badge" class="tab-bar__badge">{{ t.badge }}</span>
    </button>
  </nav>
</template>

<style scoped>
.tab-bar {
  display: flex;
  gap: 2px;
  border-bottom: 1px solid rgba(201, 169, 97, 0.2);
  font-family: var(--ff-mincho);
  font-size: 14px;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
.tab-bar::-webkit-scrollbar {
  display: none;
}
.tab-bar--light {
  border-bottom-color: rgba(26, 20, 16, 0.12);
}
.tab-bar__btn {
  flex: 0 0 auto;
  background: transparent;
  border: 0;
  padding: 10px 14px;
  color: var(--paper-300);
  border-bottom: 2px solid transparent;
  cursor: pointer;
  margin-bottom: -1px;
  font-weight: 400;
  font-family: inherit;
  font-size: inherit;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
}
.tab-bar--light .tab-bar__btn {
  color: var(--ink-500);
}
.tab-bar__btn--active {
  color: var(--beni-500);
  border-bottom-color: var(--beni-500);
  font-weight: 700;
}
.tab-bar--light .tab-bar__btn--active {
  color: var(--murasaki-700);
  border-bottom-color: var(--murasaki-600);
}
.tab-bar__badge {
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: 999px;
  background: #c0453b;
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  line-height: 16px;
}

@media (max-width: 767px) {
  .tab-bar {
    font-size: 13px;
  }
  .tab-bar__btn {
    padding: 10px 12px;
  }
}

/* ピル型セグメントコントロール（SNS画面） */
.tab-bar--pill {
  border-bottom: 0;
  gap: 4px;
  padding: 4px;
  border-radius: 999px;
  background: var(--sns-card, rgba(255, 255, 255, 0.05));
  border: 1px solid var(--sns-border, rgba(255, 255, 255, 0.1));
}
.tab-bar--pill .tab-bar__btn {
  border-bottom: 0;
  margin-bottom: 0;
  border-radius: 999px;
  padding: 8px 16px;
  font-family: var(--ff-sans-jp);
  font-weight: 500;
  color: var(--sns-text-muted, rgba(248, 244, 239, 0.6));
}
.tab-bar--pill .tab-bar__btn--active {
  color: var(--sns-ivory, #fff);
  background: var(--sns-purple, var(--murasaki-600));
  border-bottom: 0;
  box-shadow: inset 0 -2px 0 var(--sns-gold, var(--kin-500));
}
</style>
