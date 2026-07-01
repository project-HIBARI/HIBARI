<script setup>
/**
 * 部品名: 歩み — サイドバー（写真・基本情報・受賞歴）
 * 用途: 歩みページ左カラムにプロフィールカード群を sticky 表示する
 */
import Photo from '../../ui/Photo.vue'
import UiCard from '../../ui/UiCard.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const p = HIBARU_DATA.profile

const rows = [
  ['芸名', p.stageName],
  ['本名', p.realName],
  ['生誕', p.born],
  ['出生地', p.bornPlace],
  ['逝去', p.died],
  ['享年', `${p.age}歳`],
  ['デビュー', p.debut],
  ['所属', p.label],
  ['生涯録音', `${p.totalSongs}曲以上`],
  ['オリジナル', `${p.originalSongs}曲`],
]
</script>

<template>
  <!-- PC では sticky、スマホでは縦積みのプロフィールサイドバー -->
  <aside class="profile-sidebar" aria-label="基本プロフィール">
    <div class="profile-sidebar__photo-wrap">
      <Photo
        :w="360"
        :h="460"
        :caption="p.photoCaption"
        variant="sepia"
        class="profile-sidebar__photo"
      />
      <p class="profile-sidebar__bio">{{ p.bio }}</p>
    </div>

    <UiCard tone="white" padding="md" class="profile-sidebar__info">
      <h2 class="profile-sidebar__heading">基本プロフィール</h2>
      <dl class="profile-sidebar__dl">
        <template v-for="[k, v] in rows" :key="k">
          <dt class="profile-sidebar__dt">{{ k }}</dt>
          <dd class="profile-sidebar__dd">{{ v }}</dd>
        </template>
      </dl>
    </UiCard>

    <UiCard tone="warm" padding="md" class="profile-sidebar__awards">
      <h2 class="profile-sidebar__heading profile-sidebar__heading--gold">主な受賞歴</h2>
      <ul class="profile-sidebar__award-list">
        <li v-for="(a, i) in p.awards" :key="i" class="profile-sidebar__award-item">
          {{ a }}
        </li>
      </ul>
    </UiCard>
  </aside>
</template>

<style scoped>
.profile-sidebar {
  position: sticky;
  top: 120px;
  align-self: start;
  display: flex;
  flex-direction: column;
  gap: var(--sp-5);
}
.profile-sidebar__photo-wrap {
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
}
.profile-sidebar__photo {
  width: 100% !important;
  max-width: 360px;
  height: auto !important;
  aspect-ratio: 360 / 460;
  border-radius: var(--site-radius-lg);
  box-shadow: var(--site-shadow-md);
  border: 3px solid rgba(255, 255, 255, 0.9);
}
.profile-sidebar__bio {
  margin: 0;
  font-size: 13px;
  line-height: 2;
  color: var(--site-text-muted);
  letter-spacing: 0.04em;
  padding: var(--sp-4);
  background: var(--site-surface);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  border-left: 3px solid var(--murasaki-400);
}
.profile-sidebar__heading {
  margin: 0 0 var(--sp-4);
  font-family: var(--ff-mincho);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--murasaki-700);
  padding-bottom: var(--sp-3);
  border-bottom: 1px solid var(--site-border);
}
.profile-sidebar__heading--gold {
  color: var(--kin-600);
}
.profile-sidebar__dl {
  margin: 0;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 10px 16px;
  font-size: 13px;
}
.profile-sidebar__dt {
  font-family: var(--ff-mincho);
  font-weight: 700;
  color: var(--kin-600);
  letter-spacing: 0.06em;
}
.profile-sidebar__dd {
  margin: 0;
  color: var(--site-text);
  line-height: 1.6;
}
.profile-sidebar__award-list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.profile-sidebar__award-item {
  font-size: 13px;
  line-height: 1.75;
  color: var(--site-text);
  padding: 8px 0 8px 12px;
  border-left: 3px solid var(--murasaki-400);
  margin-bottom: 6px;
}
.profile-sidebar__award-item:last-child {
  margin-bottom: 0;
}

@media (max-width: 767px) {
  .profile-sidebar {
    position: static;
  }
  .profile-sidebar__photo {
    max-width: 100%;
  }
}
</style>
