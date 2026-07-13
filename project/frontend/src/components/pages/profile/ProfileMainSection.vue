<script setup>
/**
 * 部品名: 歩み — メインコンテンツ（サイドバー＋年表）
 * 用途: プロフィール情報と生涯年表を2カラムで表示する
 */
import ProfileSidebar from './ProfileSidebar.vue'
import ProfileTimeline from './ProfileTimeline.vue'

const emit = defineEmits(['open-gallery'])
</script>

<template>
  <div class="profile-main">
    <div class="profile-main__grid prof-grid">
      <ProfileSidebar />
      <ProfileTimeline @open-gallery="emit('open-gallery')" />
    </div>
  </div>
</template>

<style scoped>
.profile-main {
  padding: var(--sp-6);
  background: var(--site-surface-muted);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  box-shadow: var(--site-shadow);
  margin-bottom: var(--sp-2);
}
.profile-main__grid {
  display: grid;
  grid-template-columns: minmax(280px, 360px) 1fr;
  gap: var(--sp-7);
  align-items: start;
}

@media (max-width: 900px) {
  .profile-main__grid {
    grid-template-columns: 1fr;
  }
}
</style>
