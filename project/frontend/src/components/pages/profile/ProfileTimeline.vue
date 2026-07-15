<script setup>
/**
 * 部品名: 歩み — 生涯年表
 * 用途: 歩みページ右カラムに時系列の年表エントリを表示する
 */
import SectionTitle from '../../ui/SectionTitle.vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'
import { aosAttrs } from '../../../lib/aos.js'

const emit = defineEmits(['open-gallery'])

const timeline = HIBARU_DATA.timeline
</script>

<template>
  <!-- 美空ひばりの生涯を年表形式で表示するセクション -->
  <section class="profile-timeline" aria-label="生涯の歩み">
    <SectionTitle title="生涯の歩み" sub="Timeline · 1937—1989" size="lg" />

    <ol class="profile-timeline__list">
      <li
        v-for="(t, i) in timeline"
        :key="i"
        class="profile-timeline__item"
        :class="{ 'profile-timeline__item--last': i === timeline.length - 1 }"
        v-bind="aosAttrs(i * 80)"
      >
        <div class="profile-timeline__marker" aria-hidden="true">
          <span class="profile-timeline__dot" />
        </div>

        <article class="profile-timeline__card">
          <header class="profile-timeline__head">
            <div class="profile-timeline__year-block">
              <span class="profile-timeline__year">{{ t.year }}</span>
              <span class="profile-timeline__era">{{ t.era }}</span>
            </div>
            <span class="profile-timeline__age">{{ t.age }}歳</span>
          </header>

          <h3 class="profile-timeline__title">{{ t.title }}</h3>
          <p class="profile-timeline__body">{{ t.body }}</p>

          <UiButton
            variant="ghost"
            size="sm"
            class="profile-timeline__photo-btn"
            aria-label="写真を見る"
            @click="emit('open-gallery')"
          >
            <UiIco name="search" :size="13" color="var(--murasaki-600)" />
            写真を見る
          </UiButton>
        </article>
      </li>
    </ol>
  </section>
</template>

<style scoped>
.profile-timeline {
  min-width: 0;
}
.profile-timeline__list {
  list-style: none;
  margin: 0;
  padding: 0;
  position: relative;
}
.profile-timeline__item {
  display: grid;
  grid-template-columns: 32px 1fr;
  gap: var(--sp-4);
  position: relative;
  padding-bottom: var(--sp-5);
}
.profile-timeline__item:not(:last-child)::before {
  content: '';
  position: absolute;
  left: 15px;
  top: 24px;
  bottom: 0;
  width: 2px;
  background: linear-gradient(180deg, var(--kin-400) 0%, var(--murasaki-400) 100%);
  opacity: 0.5;
}
.profile-timeline__marker {
  display: flex;
  justify-content: center;
  padding-top: 6px;
}
.profile-timeline__dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--site-surface);
  border: 3px solid var(--murasaki-500);
  box-shadow: 0 0 0 3px var(--murasaki-100);
  flex-shrink: 0;
}
.profile-timeline__item--last .profile-timeline__dot {
  border-color: var(--kin-500);
  box-shadow: 0 0 0 3px rgba(201, 169, 97, 0.25);
  background: var(--kin-400);
}
.profile-timeline__card {
  background: var(--site-surface);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  padding: var(--sp-5);
  box-shadow: var(--site-shadow);
  transition: box-shadow 0.2s, border-color 0.2s;
}
.profile-timeline__card:hover {
  box-shadow: var(--site-shadow-md);
  border-color: var(--site-border-strong);
}
.profile-timeline__item--last .profile-timeline__card {
  background: linear-gradient(135deg, var(--site-bg-pink) 0%, var(--site-surface) 100%);
  border-color: rgba(201, 169, 97, 0.35);
}
.profile-timeline__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--sp-3);
  margin-bottom: var(--sp-3);
}
.profile-timeline__year-block {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.profile-timeline__year {
  font-family: var(--ff-latin);
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--kin-600);
  line-height: 1;
}
.profile-timeline__era {
  font-family: var(--ff-mincho);
  font-size: var(--font-size-caption);
  color: var(--site-text-light);
  letter-spacing: 0.12em;
}
.profile-timeline__age {
  flex-shrink: 0;
  padding: 4px 10px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-caption);
  letter-spacing: 0.06em;
  color: var(--murasaki-700);
  background: var(--murasaki-100);
  border: 1px solid rgba(122, 80, 136, 0.2);
  border-radius: var(--site-radius-sm);
}
.profile-timeline__title {
  margin: 0 0 var(--sp-3);
  font-family: var(--ff-mincho);
  font-size: var(--font-size-emphasis);
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--site-text);
  line-height: 1.5;
}
.profile-timeline__body {
  margin: 0;
  font-size: var(--font-size-small);
  line-height: 2;
  color: var(--site-text-muted);
}
.profile-timeline__photo-btn {
  margin-top: var(--sp-4);
}

@media (max-width: 767px) {
  .profile-timeline__item {
    grid-template-columns: 24px 1fr;
    gap: var(--sp-3);
  }
  .profile-timeline__item:not(:last-child)::before {
    left: 11px;
  }
  .profile-timeline__year {
    font-size: var(--font-size-title);
  }
  .profile-timeline__card {
    padding: var(--sp-4);
  }
  .profile-timeline__head {
    flex-direction: column;
    gap: var(--sp-2);
  }
}
</style>
