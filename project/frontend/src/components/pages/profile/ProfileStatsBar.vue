<script setup>
/**
 * 部品名: 歩み — 生涯ハイライト数値バー
 * 用途: 歩みページ上部に享年・録音曲数など主要数値を横並びで表示する
 */
import UiCard from '../../ui/UiCard.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const stats = HIBARU_DATA.profile.stats
</script>

<template>
  <!-- プロフィール主要数値を一覧表示するバー -->
  <section class="profile-stats" aria-label="生涯ハイライト">
    <UiCard tone="pink" padding="md" class="profile-stats__card">
      <ul class="profile-stats__list">
        <li v-for="(s, i) in stats" :key="i" class="profile-stats__item">
          <span class="profile-stats__label">{{ s.label }}</span>
          <span class="profile-stats__value">
            <span class="profile-stats__num">{{ s.value }}</span>
            <span class="profile-stats__unit">{{ s.unit }}</span>
          </span>
        </li>
      </ul>
    </UiCard>
  </section>
</template>

<style scoped>
.profile-stats {
  margin-bottom: var(--sp-6);
}
.profile-stats__card {
  background:
    radial-gradient(ellipse at 10% 50%, rgba(252, 232, 236, 0.6) 0%, transparent 50%),
    radial-gradient(ellipse at 90% 50%, rgba(245, 235, 224, 0.5) 0%, transparent 45%),
    linear-gradient(135deg, var(--site-bg-pink) 0%, var(--site-surface) 100%);
}
.profile-stats__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--sp-4);
}
.profile-stats__item {
  text-align: center;
  padding: var(--sp-3) var(--sp-2);
  border-right: 1px solid var(--site-border);
}
.profile-stats__item:last-child {
  border-right: 0;
}
.profile-stats__label {
  display: block;
  font-family: var(--ff-mincho);
  font-size: 12px;
  letter-spacing: 0.1em;
  color: var(--site-text-muted);
  margin-bottom: 6px;
}
.profile-stats__value {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 2px;
}
.profile-stats__num {
  font-family: var(--ff-latin);
  font-size: 32px;
  font-weight: 700;
  color: var(--murasaki-600);
  line-height: 1;
}
.profile-stats__unit {
  font-family: var(--ff-mincho);
  font-size: 13px;
  color: var(--kin-600);
  letter-spacing: 0.06em;
}

@media (max-width: 767px) {
  .profile-stats__list {
    grid-template-columns: repeat(2, 1fr);
  }
  .profile-stats__item {
    border-right: 0;
    border-bottom: 1px solid var(--site-border);
    padding-bottom: var(--sp-4);
  }
  .profile-stats__item:nth-child(odd) {
    border-right: 1px solid var(--site-border);
  }
  .profile-stats__item:nth-last-child(-n + 2) {
    border-bottom: 0;
    padding-bottom: var(--sp-3);
  }
  .profile-stats__num {
    font-size: 26px;
  }
}
</style>
