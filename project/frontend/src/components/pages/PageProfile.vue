<script setup>
/**
 * ページ: 歩み（プロフィール＋年表）
 * 構成: 数値バー / サイドバー（写真・基本情報・受賞歴） / 生涯年表
 */
import PageHead from '../ui/PageHead.vue'
import ProfileStatsBar from './profile/ProfileStatsBar.vue'
import ProfileSidebar from './profile/ProfileSidebar.vue'
import ProfileTimeline from './profile/ProfileTimeline.vue'

const emit = defineEmits(['open-auth'])
</script>

<template>
  <div class="page-profile">
    <PageHead kanji="歴" title="歩み" sub="Profile · MISORA HIBARI · 五十二年の軌跡" />

    <ProfileStatsBar />

    <div class="page-profile__grid prof-grid">
      <ProfileSidebar />
      <ProfileTimeline @open-gallery="emit('open-auth', 'gallery')" />
    </div>
  </div>
</template>

<style scoped>
.page-profile__grid {
  display: grid;
  grid-template-columns: minmax(280px, 360px) 1fr;
  gap: var(--sp-7);
  align-items: start;
}
</style>
