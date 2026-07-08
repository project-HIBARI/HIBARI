<script setup>
/**
 * @deprecated SiteHeader.vue を利用してください（後方互換の再エクスポート）
 */
import SiteHeader from './SiteHeader.vue'

defineProps({
  items: { type: Array, required: true },
  page: { type: String, required: true },
})

const emit = defineEmits(['logo', 'navigate', 'open-drawer', 'open-auth', 'open-search'])
</script>

<template>
  <SiteHeader
    :items="items"
    :page="page"
    @logo="emit('logo')"
    @navigate="emit('navigate', $event)"
    @open-drawer="emit('open-drawer')"
    @open-auth="emit('open-auth', $event)"
    @open-search="emit('open-search')"
  />
</template>
