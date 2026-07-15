<script setup>
/**
 * ページ: ニュース
 * 用途: 公式サイトのお知らせ・最新情報一覧（ログイン不要）
 */
import { ref } from 'vue'
import PageHead from '../ui/PageHead.vue'
import SectionTitle from '../ui/SectionTitle.vue'
import MemberGate from '../common/MemberGate.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'
import { SITE_NAME } from '../../constants/site.js'
import { useMemberAccess } from '../../composables/useMemberAccess.js'
import { useScrollReveal } from '../../composables/useScrollReveal.js'

const emit = defineEmits(['open-auth'])

const pageRoot = ref(null)
useScrollReveal(pageRoot)

const { canUse, PERMISSION } = useMemberAccess()
const items = HIBARU_DATA.news
</script>

<template>
  <div ref="pageRoot" class="page-news">
    <PageHead kanji="新" title="ニュース" sub="News · 最新のお知らせ" />

    <p class="page-news__intro motion-section site-reveal">
      {{ SITE_NAME }} 美空ひばり ファンクラブからのお知らせ、イベント情報、メディア出演などを掲載しています。
    </p>

    <section class="page-news__section site-reveal site-reveal--delay-1" aria-label="ニュース一覧">
      <SectionTitle title="最新情報" sub="Latest" size="md" />

      <ul class="page-news__list motion-stagger site-reveal-stagger">
        <li
          v-for="(n, i) in items"
          :key="i"
          class="page-news__item stagger-item motion-card"
          :style="{ '--stagger-i': i }"
        >
          <article class="page-news__card">
            <div class="page-news__meta">
              <time class="page-news__date">{{ n.date }}</time>
              <span v-if="n.isNew" class="page-news__new">NEW</span>
              <span v-if="n.label" class="page-news__label">{{ n.label }}</span>
            </div>
            <h2 class="page-news__title">{{ n.title }}</h2>
          </article>
        </li>
      </ul>
    </section>

    <section
      v-if="!canUse(PERMISSION.NEWSLETTER)"
      class="page-news__member site-reveal site-reveal--delay-2"
    >
      <SectionTitle title="月刊ニュースレター" sub="For Members" size="md" />
      <p class="page-news__member-lead">
        会員の方には、より詳しいコラムや限定情報を毎月お届けしています。
      </p>
      <MemberGate
        :permission="PERMISSION.NEWSLETTER"
        feature="月刊ニュースレター"
        @login="emit('open-auth', 'login')"
        @register="emit('open-auth', 'register')"
        @upgrade="emit('open-auth', 'register-premium')"
      />
    </section>
  </div>
</template>

<style scoped>
.page-news {
  color: var(--site-text);
}
.page-news__intro {
  margin: 0 0 var(--sp-7);
  max-width: 720px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-small);
  line-height: 1.9;
  color: var(--site-text-muted);
}
.page-news__section {
  margin-bottom: var(--sp-8);
}
.page-news__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.page-news__card {
  padding: 20px 22px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
  transition:
    transform 0.55s cubic-bezier(0.22, 1, 0.36, 1),
    box-shadow 0.55s cubic-bezier(0.22, 1, 0.36, 1),
    border-color 0.45s ease;
}
.page-news__item:hover .page-news__card {
  transform: translateY(-7px);
  box-shadow: 0 14px 36px rgba(60, 40, 30, 0.14);
  border-color: rgba(122, 80, 136, 0.28);
}
.page-news__item:hover .page-news__label {
  background: var(--murasaki-700);
  color: #fff;
}
.page-news__meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}
.page-news__date {
  font-family: var(--ff-mono);
  font-size: var(--font-size-caption);
  color: var(--site-text-light);
  letter-spacing: 0.04em;
  transition: color 0.45s ease;
}
.page-news__item:hover .page-news__date {
  color: var(--murasaki-600);
}
.page-news__new {
  display: inline-block;
  padding: 1px 7px;
  font-size: var(--font-size-badge);
  font-family: var(--ff-sans-jp);
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #fff;
  background: var(--beni-500);
  border-radius: 3px;
}
.page-news__label {
  font-size: var(--font-size-badge);
  color: var(--murasaki-700);
  background: var(--murasaki-100);
  padding: 2px 8px;
  border-radius: 4px;
  transition: background 0.45s ease, color 0.45s ease;
}
.page-news__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-body);
  font-weight: 700;
  line-height: 1.65;
  letter-spacing: 0.04em;
  color: var(--site-text);
}
.page-news__member {
  padding: var(--sp-6);
  border-radius: var(--site-radius-lg);
  background: linear-gradient(135deg, var(--site-bg-pink) 0%, var(--site-surface) 100%);
  border: 1px solid var(--site-border);
}
.page-news__member-lead {
  margin: 0 0 var(--sp-5);
  font-size: var(--font-size-button);
  line-height: 1.85;
  color: var(--site-text-muted);
}
</style>
