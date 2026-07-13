<script setup>
/**
 * ページ: 歩み（プロフィール＋年表）
 * 構成: ヒーロー / サイドバー＋年表 / AI / 関連導線
 */
import ProfileHeroSection from './profile/ProfileHeroSection.vue'
import ProfileMainSection from './profile/ProfileMainSection.vue'
import ProfileAiCard from './profile/ProfileAiCard.vue'
import ProfileRelatedCards from './profile/ProfileRelatedCards.vue'

const emit = defineEmits(['open-auth', 'open-modal', 'navigate'])
</script>

<template>
  <div class="page-profile">
    <ProfileHeroSection @open-ai="emit('open-modal', 'ai')" />

    <ProfileMainSection @open-gallery="emit('open-auth', 'gallery')" />

    <ProfileAiCard @open-ai="emit('open-modal', 'ai')" />

    <ProfileRelatedCards
      @navigate="(id) => emit('navigate', id)"
      @coming-soon="(mode) => emit('open-auth', mode)"
    />
  </div>
</template>

<style scoped>
.page-profile {
  color: var(--site-text);
}
</style>
