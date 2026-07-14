<script setup>
/**
 * 部品名: 思い出 — タブ切替セクション
 * 用途: 思い出投稿と交流イベントのタブナビを表示する
 */
import TabBar from '../../ui/TabBar.vue'
import { aosAttrs } from '../../../lib/aos.js'

defineProps({
  active: { type: String, required: true },
})

const emit = defineEmits(['update:active'])
</script>

<template>
  <div class="mem-tabs">
    <TabBar
      v-bind="aosAttrs()"
      :dark="false"
      :tabs="[
        { id: 'memories', label: '思い出投稿', icon: 'chat' },
        { id: 'events', label: '交流イベント', icon: 'calendar' },
      ]"
      :active="active"
      @update:active="emit('update:active', $event)"
    />
    <slot />
  </div>
</template>
