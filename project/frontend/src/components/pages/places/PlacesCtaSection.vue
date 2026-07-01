<script setup>
/**
 * 部品名: ゆかりの地 — CTA セクション
 * 用途: ファンクラブ・会員コンテンツ・イベントへの導線（準備中 UI）
 */
import SectionTitle from '../../ui/SectionTitle.vue'
import UiCard from '../../ui/UiCard.vue'
import UiButton from '../../ui/UiButton.vue'

const emit = defineEmits(['open-auth', 'navigate'])

const cards = [
  {
    id: 'fanclub',
    title: 'ファンクラブ',
    desc: '会員限定のゆかりの地ツアー情報や特典をお届けします。',
    badge: 'Coming Soon',
    mode: 'fanclub',
  },
  {
    id: 'member',
    title: '会員コンテンツ',
    desc: '写真ギャラリー・音声ガイドなど、会員向けの巡礼コンテンツ。',
    badge: '会員限定',
    mode: 'gallery',
  },
  {
    id: 'events',
    title: 'イベント情報',
    desc: 'ゆかりの地ツアー・ファン交流会などの最新イベント。',
    badge: '準備中',
    mode: 'events',
  },
]
</script>

<template>
  <!-- ファンクラブ・会員向け導線 -->
  <section class="places-cta" aria-label="会員向けコンテンツ">
    <SectionTitle title="もっと楽しむ" sub="Member & Events" size="md" />

    <div class="places-cta__grid">
      <UiCard v-for="c in cards" :key="c.id" tone="pink" padding="md" class="places-cta__card">
        <span class="places-cta__badge">{{ c.badge }}</span>
        <h3 class="places-cta__title">{{ c.title }}</h3>
        <p class="places-cta__desc">{{ c.desc }}</p>
        <UiButton variant="outline" size="sm" @click="emit('open-auth', c.mode)">
          詳しく見る
        </UiButton>
      </UiCard>
    </div>

    <p class="places-cta__note">
      ※ 会員機能は準備中です。SiteShell との連携は統合タスクで対応予定です。
    </p>
  </section>
</template>

<style scoped>
.places-cta {
  margin-bottom: var(--sp-6);
}
.places-cta__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--sp-4);
  margin-bottom: var(--sp-4);
}
.places-cta__card {
  display: flex;
  flex-direction: column;
  gap: var(--sp-3);
}
.places-cta__badge {
  display: inline-block;
  align-self: flex-start;
  padding: 2px 8px;
  font-size: 9px;
  letter-spacing: 0.12em;
  color: var(--murasaki-700);
  border: 1px solid rgba(122, 80, 136, 0.3);
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.6);
}
.places-cta__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 17px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--site-text);
}
.places-cta__desc {
  margin: 0;
  flex: 1;
  font-size: 12px;
  line-height: 1.75;
  color: var(--site-text-muted);
}
.places-cta__note {
  margin: 0;
  font-size: 11px;
  color: var(--site-text-light);
  text-align: center;
  letter-spacing: 0.04em;
}

@media (max-width: 1024px) {
  .places-cta__grid {
    grid-template-columns: 1fr;
  }
}
</style>
