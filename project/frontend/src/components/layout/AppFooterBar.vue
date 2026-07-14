<script setup>
/**
 * 部品名: フッター
 * 役割: 公式 SNS・各種リンク・著作権表示（全ページ共通・1行構成）
 */
import { SITE_NAME } from '../../constants/site.js'

const emit = defineEmits(['navigate'])

/** @param {string} filename */
function socialIconUrl(filename) {
  return `/images/social/${filename}`
}

const footerSocialLinks = [
  {
    id: 'x',
    href: 'https://x.com/hibariofficial',
    icon: 'icons8-x.png',
    ariaLabel: 'X公式アカウント',
  },
  {
    id: 'youtube',
    href: 'https://www.youtube.com/channel/UCeh9shE_yLGPBeX2jdf9uXw',
    icon: 'icons8-youtube.png',
    ariaLabel: 'YouTube公式チャンネル',
  },
  {
    id: 'line',
    href: 'https://page.line.me/106urppz',
    icon: 'icons8-line.png',
    ariaLabel: 'LINE公式アカウント',
  },
  {
    id: 'website',
    href: 'https://www.misorahibari.com/',
    icon: 'icons8-website-96.png',
    ariaLabel: '美空ひばり公式サイト',
  },
  {
    id: 'label',
    href: 'https://columbia.jp/artist-info/hibari/',
    icon: 'Company-Logo_NipponColumbia-1280x1280.png',
    ariaLabel: '日本コロムビア 美空ひばりページ',
  },
]

const footerLinks = [
  { label: 'よくある質問', page: 'faq' },
  { label: 'お問い合わせ', page: 'contact' },
  { label: '利用規約', page: 'terms' },
  { label: 'プライバシーポリシー', page: 'privacy-policy' },
]

function onLinkClick(link, event) {
  if (link.page) {
    event.preventDefault()
    emit('navigate', link.page)
    return
  }
  event.preventDefault()
}
</script>

<template>
  <footer role="contentinfo" class="app-footer">
    <div class="app-footer__inner">
      <section class="app-footer__sns" aria-labelledby="app-footer-sns-title">
        <p id="app-footer-sns-title" class="app-footer__sns-label">公式SNS</p>
        <ul class="app-footer__sns-list">
          <li v-for="item in footerSocialLinks" :key="item.id" class="app-footer__sns-item">
            <a
              :href="item.href"
              class="app-footer__sns-link"
              :aria-label="item.ariaLabel"
              :title="item.ariaLabel"
              target="_blank"
              rel="noopener noreferrer"
            >
              <img
                :src="socialIconUrl(item.icon)"
                alt=""
                class="app-footer__sns-icon"
                width="34"
                height="34"
                decoding="async"
                draggable="false"
              />
            </a>
          </li>
        </ul>
      </section>

      <nav class="app-footer__links" aria-label="フッターリンク">
        <template v-for="(l, i) in footerLinks" :key="l.label">
          <span v-if="i > 0" class="app-footer__sep" aria-hidden="true">|</span>
          <a :href="l.href || '#'" @click="onLinkClick(l, $event)">{{ l.label }}</a>
        </template>
      </nav>

      <div class="app-footer__copy">© {{ SITE_NAME }}</div>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  border-top: 1px solid var(--site-border);
  background: linear-gradient(180deg, #fffefb 0%, var(--site-bg) 100%);
  color: var(--site-text-muted);
  font-family: var(--ff-sans-jp);
  font-size: 12px;
}

.app-footer__inner {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 24px 32px;
  max-width: 1520px;
  margin: 0 auto;
  padding: 20px 40px;
}

.app-footer__sns {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-self: start;
}

.app-footer__sns-label {
  margin: 0;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--site-text-light);
  white-space: nowrap;
}

.app-footer__sns-list {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.app-footer__sns-item {
  flex: 0 0 auto;
}

.app-footer__sns-link {
  display: inline-block;
  flex-shrink: 0;
  line-height: 0;
  transition: opacity 0.2s ease;
}

.app-footer__sns-link:hover {
  opacity: 0.85;
}

.app-footer__sns-link:focus-visible {
  outline: 2px solid var(--murasaki-500);
  outline-offset: 2px;
  border-radius: 2px;
}

.app-footer__sns-icon {
  width: 34px;
  height: 34px;
  object-fit: contain;
  display: block;
}

.app-footer__links {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0;
}

.app-footer__sep {
  color: var(--site-text-light);
  margin: 0 10px;
  user-select: none;
}

.app-footer__links a {
  color: var(--site-text-muted);
  text-decoration: none;
  font-size: 12px;
  letter-spacing: 0.04em;
  white-space: nowrap;
}

.app-footer__links a:hover {
  color: var(--murasaki-700);
}

.app-footer__copy {
  justify-self: end;
  font-size: 11px;
  letter-spacing: 0.06em;
  color: var(--site-text-light);
  white-space: nowrap;
}

@media (max-width: 1023px) {
  .app-footer__inner {
    grid-template-columns: 1fr;
    justify-items: center;
    text-align: center;
    gap: 16px;
    padding: 24px 24px;
  }

  .app-footer__sns {
    flex-direction: column;
    align-items: center;
    gap: 10px;
    justify-self: center;
  }

  .app-footer__sns-list {
    justify-content: center;
  }

  .app-footer__links {
    justify-content: center;
  }

  .app-footer__copy {
    justify-self: center;
    text-align: center;
  }
}
</style>
