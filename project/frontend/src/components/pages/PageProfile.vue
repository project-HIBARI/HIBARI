<script setup>
/**
 * ページ: 歩み（プロフィール＋年表）
 * 構成: ヒーロー / 数値バー / サイドバー＋年表 / 関連導線
 */
import ProfileHeroSection from './profile/ProfileHeroSection.vue'
import ProfileStatsBar from './profile/ProfileStatsBar.vue'
import ProfileSidebar from './profile/ProfileSidebar.vue'
import ProfileTimeline from './profile/ProfileTimeline.vue'
import ProfileRelatedCards from './profile/ProfileRelatedCards.vue'

const emit = defineEmits(['open-auth', 'open-modal', 'navigate'])
</script>

<template>
  <div class="page-profile">
    <ProfileHeroSection @open-ai="emit('open-modal', 'ai')" />

    <ProfileStatsBar />

    <div class="page-profile__main">
      <div class="page-profile__grid prof-grid">
        <ProfileSidebar />
        <ProfileTimeline @open-gallery="emit('open-auth', 'gallery')" />
      </div>
    </div>

    <ProfileRelatedCards
      @navigate="(id) => emit('navigate', id)"
      @coming-soon="(mode) => emit('open-auth', mode)"
    />
  </div>
</template>

<style scoped>
.page-profile__main {
  padding: var(--sp-6);
  background: var(--site-surface-muted);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  box-shadow: var(--site-shadow);
  margin-bottom: var(--sp-2);
}
.page-profile__grid {
  display: grid;
  grid-template-columns: minmax(280px, 360px) 1fr;
  gap: var(--sp-7);
  align-items: start;
}
</style>
