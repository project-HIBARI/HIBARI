<script setup>
/**
 * ページ: ファンクラブ会員サイト
 */
import { ref, watch, nextTick, computed } from 'vue'
import PageHead from '../ui/PageHead.vue'
import SectionTitle from '../ui/SectionTitle.vue'
import TabBar from '../ui/TabBar.vue'
import FanclubAiChat from './fanclub/FanclubAiChat.vue'
import FanclubBoard from './fanclub/FanclubBoard.vue'
import FanclubBenefits from './fanclub/FanclubBenefits.vue'
import BenefitScreenShell from './fanclub/benefits/BenefitScreenShell.vue'
import BenefitNewsletterPanel from './fanclub/benefits/BenefitNewsletterPanel.vue'
import BenefitEventsPanel from './fanclub/benefits/BenefitEventsPanel.vue'
import BenefitExclusivePanel from './fanclub/benefits/BenefitExclusivePanel.vue'
import BenefitPremiumVideoPanel from './fanclub/benefits/BenefitPremiumVideoPanel.vue'
import { useMemberAccess } from '../../composables/useMemberAccess.js'
import { MEMBERSHIP_LABELS, PERMISSION } from '../../constants/membership.js'
import { benefitToSection } from '../../lib/fanclubBenefits.js'

const props = defineProps({
  activeSection: { type: String, default: 'overview' },
})

const emit = defineEmits(['navigate', 'open-modal', 'open-auth', 'section-change'])

const { canUse, isLoggedIn, membership, isPremium } = useMemberAccess()

const section = ref(props.activeSection)
const pageRoot = ref(null)

const BENEFIT_PERMISSIONS = {
  news: { permission: PERMISSION.NEWSLETTER },
  events: { permission: PERMISSION.TICKET_PREORDER },
  'priority-events': { permission: PERMISSION.PRIORITY_DISCOUNT, premium: true },
  board: { permission: PERMISSION.BOARD_POST },
  ai: { permission: PERMISSION.AI_CHAT },
  disco: { permission: PERMISSION.PREMIUM_VIDEO, premium: true },
  gallery: { permission: PERMISSION.EXCLUSIVE_CONTENT, premium: true },
}

watch(
  () => props.activeSection,
  (value) => {
    section.value = value
  },
)

const sectionTabs = [
  { id: 'overview', label: 'トップ' },
  { id: 'board', label: '会員掲示板', icon: 'chat' },
  { id: 'chat', label: 'AIチャット', icon: 'flower' },
  { id: 'benefits', label: '特典一覧', icon: 'heart' },
]

const BENEFIT_SUB_SECTIONS = new Set([
  'benefits',
  'newsletter',
  'events',
  'priority-events',
  'exclusive-content',
  'premium-video',
])

const tabActive = computed(() =>
  BENEFIT_SUB_SECTIONS.has(section.value) ? 'benefits' : section.value,
)

const perks = [
  { feature: 'news', icon: '✦', label: '会員誌', desc: 'デジタル版を毎月配信' },
  { feature: 'events', icon: '★', label: '先行予約', desc: 'イベント・コンサート優先申込' },
  { feature: 'board', icon: '💬', label: '会員掲示板', desc: '月10回まで投稿（プレミアム無制限）' },
  { feature: 'ai', icon: '♪', label: 'AIひばり対話', desc: '月10回（プレミアム無制限）' },
  { feature: 'disco', icon: '▶', label: '限定動画', desc: '未公開映像をいつでも視聴', premium: true },
  { feature: 'gallery', icon: '✧', label: '限定コンテンツ', desc: 'ハイレゾ音源・会員ギャラリー', premium: true },
]

function setSection(id) {
  section.value = id
  emit('section-change', id)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function onNeedLogin() {
  emit('open-auth', 'login')
}

function requireAccess(permission, premiumOnly = false) {
  if (!isLoggedIn.value) {
    emit('open-auth', 'login')
    return false
  }
  if (premiumOnly && !isPremium.value) {
    emit('open-auth', 'register-premium')
    return false
  }
  if (permission && !canUse(permission)) {
    emit('open-auth', premiumOnly ? 'register-premium' : 'register')
    return false
  }
  return true
}

function useFeature(feature) {
  const targetSection = benefitToSection(feature)
  if (!targetSection) {
    emit('open-auth', feature)
    return
  }

  const gate = BENEFIT_PERMISSIONS[feature]
  if (gate && !requireAccess(gate.permission, gate.premium)) return

  setSection(targetSection)
}

function backToBenefits() {
  setSection('benefits')
}

/** タブ切替後に特典カードを確実に表示 */
watch(section, () => {
  nextTick(() => {
    pageRoot.value?.querySelectorAll('.site-reveal-stagger, .fc-benefits').forEach((el) => {
      el.classList.add('is-visible')
    })
  })
})
</script>

<template>
  <div ref="pageRoot" class="page-fc-site">
    <PageHead kanji="會" title="ファンクラブサイト" sub="Member Site · 会員限定コンテンツ" />

    <TabBar
      :dark="false"
      :tabs="sectionTabs"
      :active="tabActive"
      @update:active="setSection"
    />

    <div v-if="section === 'overview'" class="page-fc-site__panel">
      <p v-if="isLoggedIn" class="page-fc-site__member">
        {{ MEMBERSHIP_LABELS[membership] }}としてログイン中 · 下記の特典をご利用いただけます
      </p>
      <p v-else class="page-fc-site__welcome">
        ファンクラブへようこそ。ログインすると会員限定の特典と、AI美空ひばりとの対話をお楽しみいただけます。
        <button type="button" class="page-fc-site__login-link" @click="emit('open-auth', 'login')">ログイン</button>
      </p>

      <section class="page-fc-site__perks">
        <ul class="page-fc-site__perk-grid is-visible">
          <li
            v-for="p in perks"
            :key="p.label"
            class="page-fc-site__perk motion-card"
            :class="{ 'page-fc-site__perk--highlight': p.feature === 'ai' || p.feature === 'board' }"
          >
            <button type="button" class="page-fc-site__perk-btn" @click="useFeature(p.feature)">
              <span class="page-fc-site__perk-icon">{{ p.icon }}</span>
              <div>
                <h3 class="page-fc-site__perk-title">
                  {{ p.label }}
                  <span v-if="p.premium" class="page-fc-site__perk-premium">Premium</span>
                </h3>
                <p class="page-fc-site__perk-desc">{{ p.desc }}</p>
              </div>
            </button>
          </li>
        </ul>
      </section>
    </div>

    <section v-else-if="section === 'board'" class="page-fc-site__panel">
      <SectionTitle title="会員掲示板" sub="Member Board · 会員限定" size="md" />
      <p class="page-fc-site__board-lead">
        ファンクラブ会員専用の掲示板です。思い出やメッセージを投稿して、仲間と交流できます。
      </p>
      <FanclubBoard @need-auth="(m) => emit('open-auth', m)" />
    </section>

    <section v-else-if="section === 'chat'" class="page-fc-site__panel">
      <SectionTitle title="AI美空ひばりと対話" sub="AI Chat" size="md" />
      <FanclubAiChat @need-login="onNeedLogin" />
    </section>

    <section v-else-if="section === 'benefits'" class="page-fc-site__panel">
      <p v-if="isLoggedIn" class="page-fc-site__member">
        {{ MEMBERSHIP_LABELS[membership] }}としてログイン中 · 各特典をタップしてご利用ください
      </p>
      <SectionTitle title="会員特典一覧" sub="Your Benefits" size="md" />
      <FanclubBenefits @use-feature="useFeature" />
    </section>

    <BenefitScreenShell
      v-else-if="section === 'newsletter'"
      title="月刊ニュースレター"
      sub="Member Newsletter"
      @back="backToBenefits"
    >
      <BenefitNewsletterPanel @need-auth="(m) => emit('open-auth', m)" />
    </BenefitScreenShell>

    <BenefitScreenShell
      v-else-if="section === 'events'"
      title="チケット先行予約"
      sub="Ticket Pre-order"
      @back="backToBenefits"
    >
      <BenefitEventsPanel
        @need-auth="(m) => emit('open-auth', m)"
        @navigate="(p) => emit('navigate', p)"
      />
    </BenefitScreenShell>

    <BenefitScreenShell
      v-else-if="section === 'priority-events'"
      title="優先申込＋会員割引"
      sub="Priority & Discount"
      @back="backToBenefits"
    >
      <BenefitEventsPanel
        premium-focus
        @need-auth="(m) => emit('open-auth', m)"
        @navigate="(p) => emit('navigate', p)"
      />
    </BenefitScreenShell>

    <BenefitScreenShell
      v-else-if="section === 'exclusive-content'"
      title="限定コンテンツ"
      sub="Exclusive Content"
      @back="backToBenefits"
    >
      <BenefitExclusivePanel @need-auth="(m) => emit('open-auth', m)" />
    </BenefitScreenShell>

    <BenefitScreenShell
      v-else-if="section === 'premium-video'"
      title="プレミアム限定映像"
      sub="Premium Video"
      @back="backToBenefits"
    >
      <BenefitPremiumVideoPanel @need-auth="(m) => emit('open-auth', m)" />
    </BenefitScreenShell>
  </div>
</template>

<style scoped>
.page-fc-site {
  color: var(--site-text);
}
.page-fc-site__panel {
  margin-top: var(--sp-5);
}
.page-fc-site__member {
  margin: 0 0 var(--sp-6);
  padding: 12px 16px;
  max-width: 720px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.7;
  color: var(--murasaki-700);
  background: var(--murasaki-100);
  border: 1px solid var(--murasaki-400);
  border-radius: var(--site-radius-md);
}
.page-fc-site__welcome {
  margin: 0 0 var(--sp-6);
  max-width: 720px;
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  line-height: 1.9;
  color: var(--site-text-muted);
}
.page-fc-site__login-link {
  background: transparent;
  border: 0;
  padding: 0;
  margin-left: 4px;
  color: var(--murasaki-700);
  font-weight: 700;
  cursor: pointer;
  text-decoration: underline;
}
.page-fc-site__board-lead {
  margin: 0 0 var(--sp-5);
  max-width: 720px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.8;
  color: var(--site-text-muted);
}
.page-fc-site__perk-grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--sp-4);
}
.page-fc-site__perk {
  border: 1px solid var(--kin-500);
  border-radius: var(--site-radius-md);
  background: linear-gradient(135deg, var(--murasaki-100) 0%, var(--site-surface) 100%);
  overflow: hidden;
}
.page-fc-site__perk-btn {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  width: 100%;
  padding: 18px 16px;
  border: 0;
  background: transparent;
  cursor: pointer;
  text-align: left;
}
.page-fc-site__perk-btn:hover {
  background: rgba(255, 255, 255, 0.35);
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
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}
.page-fc-site__perk-premium {
  font-family: var(--ff-sans-jp);
  font-size: 9px;
  font-weight: 700;
  color: var(--kin-600);
  letter-spacing: 0.06em;
}
.page-fc-site__perk-desc {
  margin: 0;
  font-size: 11px;
  line-height: 1.6;
  color: var(--site-text-muted);
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
