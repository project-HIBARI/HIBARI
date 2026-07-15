<script setup>
/**
 * 部品名: 思い出 — 投稿タブ（タグフィルタ＋掲示板）
 * 用途: 思い出投稿一覧と曲タグフィルタを表示する
 */
import SectionTitle from '../../ui/SectionTitle.vue'
import MemoriesBoard from './MemoriesBoard.vue'
import { aosAttrs } from '../../../lib/aos.js'

defineProps({
  items: { type: Array, required: true },
  songs: { type: Array, required: true },
  tagFilter: { type: String, required: true },
  showMineFilter: { type: Boolean, default: true },
})

const emit = defineEmits(['update:tagFilter', 'like', 'edit', 'delete', 'need-auth'])

function onMineClick() {
  emit('update:tagFilter', 'mine')
}
</script>

<template>
  <section class="mem-panel" aria-label="思い出投稿">
    <SectionTitle title="思い出投稿" sub="Fan Memories" size="md" />

    <div class="mem-panel__tags" v-bind="aosAttrs(80)">
      <button
        type="button"
        class="mem-panel__tag"
        :class="{ 'mem-panel__tag--active': tagFilter === 'all' }"
        @click="emit('update:tagFilter', 'all')"
      >
        全て
      </button>
      <button
        v-if="showMineFilter"
        type="button"
        class="mem-panel__tag"
        :class="{ 'mem-panel__tag--active': tagFilter === 'mine' }"
        @click="onMineClick"
      >
        自分の投稿
      </button>
      <button
        v-for="s in songs.slice(0, 6)"
        :key="s"
        type="button"
        class="mem-panel__tag"
        :class="{ 'mem-panel__tag--active': tagFilter === s }"
        @click="emit('update:tagFilter', s)"
      >
        {{ s }}
      </button>
    </div>

    <MemoriesBoard
      :items="items"
      @like="emit('like', $event)"
      @edit="emit('edit', $event)"
      @delete="emit('delete', $event)"
    />
  </section>
</template>

<style scoped>
.mem-panel__tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: var(--sp-5);
}
.mem-panel__tag {
  background: var(--site-surface);
  color: var(--site-text-muted);
  border: 1px solid var(--site-border);
  padding: 6px 14px;
  cursor: pointer;
  font-family: var(--ff-mincho);
  font-size: 11px;
  letter-spacing: 0.06em;
  border-radius: var(--site-radius-sm);
  transition: background 0.2s, border-color 0.2s, color 0.2s;
}
.mem-panel__tag:hover {
  border-color: var(--murasaki-400);
  color: var(--murasaki-700);
}
.mem-panel__tag--active {
  background: var(--murasaki-700);
  color: #fff;
  border-color: var(--murasaki-800);
}
</style>
