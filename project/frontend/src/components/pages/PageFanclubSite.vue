<script setup>
/**
 * ページ: ファンクラブ会員サイト
 * 構成: 会員向けダッシュボード / AIひばりチャット
 * 導線: 登録完了後に遷移。チャットはバックエンド API 連携
 */
import PageHead from '../ui/PageHead.vue'
import SectionTitle from '../ui/SectionTitle.vue'
import FanclubAiChat from './fanclub/FanclubAiChat.vue'
import FanclubBenefits from './fanclub/FanclubBenefits.vue'

const emit = defineEmits(['navigate'])

const perks = [
  { icon: '▶', label: '限定動画', desc: '未公開映像をいつでも視聴' },
  { icon: '♪', label: 'ハイレゾ音源', desc: '高音質で楽曲をお楽しみ' },
  { icon: '★', label: '先行予約', desc: 'イベント・コンサート優先申込' },
  { icon: '✦', label: '会員誌', desc: 'デジタル版を毎月配信' },
]

function onNeedLogin() {
  emit('navigate', 'login')
}
</script>

<template>
  <div class="page-fc-site">
    <PageHead kanji="會" title="ファンクラブサイト" sub="Member Site · 会員限定コンテンツ" />

    <p class="page-fc-site__welcome">
      ファンクラブへようこそ。会員限定の特典と、AI美空ひばりとの対話をお楽しみください。
    </p>

    <section class="page-fc-site__perks">
      <ul class="page-fc-site__perk-grid">
        <li v-for="p in perks" :key="p.label" class="page-fc-site__perk">
          <span class="page-fc-site__perk-icon">{{ p.icon }}</span>
          <div>
            <h3 class="page-fc-site__perk-title">{{ p.label }}</h3>
            <p class="page-fc-site__perk-desc">{{ p.desc }}</p>
          </div>
        </li>
      </ul>
    </section>

    <section class="page-fc-site__chat-section">
      <SectionTitle title="AI美空ひばりと対話" sub="AI Chat" size="md" />
      <FanclubAiChat @need-login="onNeedLogin" />
    </section>

    <section class="page-fc-site__benefits">
      <SectionTitle title="会員特典一覧" sub="Your Benefits" size="md" />
      <FanclubBenefits />
    </section>
  </div>
</template>

<style scoped>
.page-fc-site {
  color: var(--site-text);
}
.page-fc-site__welcome {
  margin: 0 0 var(--sp-6);
  max-width: 720px;
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  line-height: 1.9;
  color: var(--site-text-muted);
}
.page-fc-site__perk-grid {
  list-style: none;
  margin: 0 0 var(--sp-8);
  padding: 0;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--sp-4);
}
.page-fc-site__perk {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 18px 16px;
  background: linear-gradient(135deg, var(--murasaki-100) 0%, var(--site-surface) 100%);
  border: 1px solid var(--kin-500);
  border-radius: var(--site-radius-md);
}
.page-fc-site__perk-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--murasaki-700);
  color: var(--kin-400);
  font-size: 16px;
}
.page-fc-site__perk-title {
  margin: 0 0 4px;
  font-family: var(--ff-mincho);
  font-size: 14px;
  font-weight: 700;
  color: var(--murasaki-700);
}
.page-fc-site__perk-desc {
  margin: 0;
  font-size: 11px;
  line-height: 1.6;
  color: var(--site-text-muted);
}
.page-fc-site__chat-section {
  margin-bottom: var(--sp-8);
}
.page-fc-site__benefits {
  margin-bottom: var(--sp-6);
}

@media (max-width: 900px) {
  .page-fc-site__perk-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 480px) {
  .page-fc-site__perk-grid {
    grid-template-columns: 1fr;
  }
}
</style>
