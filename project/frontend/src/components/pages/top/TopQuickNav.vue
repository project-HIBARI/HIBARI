<script setup>
/**
 * 部品名: ホーム — クイックアクセスナビ＋パーソナライズ帯
 * 用途: 主要ページへの導線を常時表示し、ログイン状態に応じたメッセージを出し分ける
 */
import { computed } from 'vue'
import { useAuth } from '../../../composables/useAuth.js'
import { MEMBERSHIP_LABELS } from '../../../constants/membership.js'

const emit = defineEmits(['navigate', 'open-auth'])

const { isLoggedIn, isFanclubMember, isPremium, membership } = useAuth()

const LINKS = [
  { id: 'news', label: 'ニュース', icon: '📰' },
  { id: 'disco', label: 'ディスコグラフィ', icon: '💿' },
  { id: 'map', label: 'ゆかりの地', icon: '🗺️' },
  { id: 'memories', label: '思い出', icon: '📖' },
  { id: 'message', label: '献花', icon: '🌸' },
  { id: 'fanclub', label: 'ファンクラブ', icon: '🎫' },
]

const status = computed(() => {
  if (!isLoggedIn.value) {
    return {
      text: 'はじめての方へ｜無料会員登録でニュースレターやAIひばり対話などの特典をチェック',
      ctaLabel: '無料会員登録',
      ctaMode: 'register',
    }
  }
  if (!isFanclubMember.value) {
    return {
      text: 'ファンクラブに入会すると、限定映像やチケット先行予約などの特典が広がります',
      ctaLabel: 'ファンクラブを見る',
      ctaMode: 'fanclub',
    }
  }
  if (isPremium.value) {
    return {
      text: `${MEMBERSHIP_LABELS.premium}としてご利用中です｜いつもありがとうございます`,
      ctaLabel: 'マイページ',
      ctaMode: 'profile-page',
    }
  }
  return {
    text: `${MEMBERSHIP_LABELS[membership.value] || MEMBERSHIP_LABELS.general}としてご利用中｜プレミアムでさらに特典が広がります`,
    ctaLabel: 'プレミアムを見る',
    ctaMode: 'upgrade',
  }
})

function onCta() {
  const mode = status.value.ctaMode
  if (mode === 'register') {
    emit('open-auth', 'register')
  } else if (mode === 'fanclub') {
    emit('navigate', 'fanclub')
  } else if (mode === 'profile-page') {
    emit('navigate', 'fanclub-site')
  } else if (mode === 'upgrade') {
    emit('open-auth', 'register-premium')
  }
}
</script>

<template>
  <nav class="quick-nav home-motion-section" aria-label="主要ページへのクイックアクセス">
    <div class="quick-nav__inner">
      <div class="quick-nav__status">
        <span class="quick-nav__status-dot" :class="{ 'is-member': isFanclubMember }" aria-hidden="true" />
        <p class="quick-nav__status-text">{{ status.text }}</p>
        <button type="button" class="quick-nav__status-cta" @click="onCta">
          {{ status.ctaLabel }} <span aria-hidden="true">›</span>
        </button>
      </div>

      <ul class="quick-nav__links">
        <li v-for="l in LINKS" :key="l.id">
          <button type="button" class="quick-nav__link" @click="emit('navigate', l.id)">
            <span class="quick-nav__link-icon" aria-hidden="true">{{ l.icon }}</span>
            <span class="quick-nav__link-label">{{ l.label }}</span>
          </button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<style scoped>
.quick-nav {
  background: rgba(255, 251, 248, 0.92);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  margin: 0 var(--sp-6) var(--sp-7);
}
.quick-nav__inner {
  padding: 14px var(--sp-6);
}
.quick-nav__status {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 8px;
  margin-bottom: 8px;
  border-bottom: 1px dashed var(--site-border);
}
.quick-nav__status-dot {
  flex-shrink: 0;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--site-text-light);
}
.quick-nav__status-dot.is-member {
  background: var(--kin-500);
  box-shadow: 0 0 0 3px rgba(201, 169, 97, 0.22);
}
.quick-nav__status-text {
  flex: 1;
  min-width: 0;
  margin: 0;
  font-size: 12px;
  line-height: 1.6;
  color: var(--site-text-muted);
  letter-spacing: 0.02em;
}
.quick-nav__status-cta {
  flex-shrink: 0;
  background: transparent;
  border: 0;
  padding: 4px 2px;
  cursor: pointer;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  font-weight: 600;
  color: var(--murasaki-700);
  white-space: nowrap;
  transition: color 0.25s ease, transform 0.25s ease;
}
.quick-nav__status-cta:hover {
  color: var(--murasaki-800);
  transform: translateX(2px);
}
.quick-nav__links {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  gap: 8px;
  list-style: none;
  margin: 0;
  padding: 0 0 2px;
  scrollbar-width: thin;
}
.quick-nav__link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  border-radius: 999px;
  border: 1px solid var(--site-border);
  background: var(--site-surface);
  color: var(--site-text);
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  letter-spacing: 0.03em;
  white-space: nowrap;
  cursor: pointer;
  transition: background 0.25s ease, border-color 0.25s ease, transform 0.25s ease, box-shadow 0.25s ease;
}
.quick-nav__link:hover {
  background: var(--murasaki-100);
  border-color: var(--murasaki-400);
  color: var(--murasaki-800);
  transform: translateY(-2px);
  box-shadow: var(--site-shadow);
}
.quick-nav__link-icon {
  font-size: 13px;
  line-height: 1;
}

@media (max-width: 767px) {
  .quick-nav {
    margin: 0 var(--sp-4) var(--sp-6);
  }
  .quick-nav__inner {
    padding: 10px var(--sp-4);
  }
  .quick-nav__status {
    flex-wrap: wrap;
  }
  .quick-nav__status-text {
    flex-basis: 100%;
    order: 2;
  }
  .quick-nav__status-cta {
    order: 1;
    margin-left: auto;
  }
}

@media (prefers-reduced-motion: reduce) {
  .quick-nav__link:hover {
    transform: none;
  }
}
</style>
