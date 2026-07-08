<script setup>
/**
 * 部品名: フッター
 * 役割: 公式 SNS・各種リンク・著作権表示（全ページ共通・1行構成）
 */
import SocialLinks from '../common/SocialLinks.vue'

const footerLinks = [
  { label: 'よくある質問', href: '#' },
  { label: 'お問い合わせ', href: '#' },
  { label: '利用規約', href: '#' },
  { label: 'プライバシーポリシー', href: '#' },
]
</script>

<template>
  <footer role="contentinfo" class="app-footer">
    <div class="app-footer__inner">
      <SocialLinks variant="footer" class="app-footer__sns" />

      <nav class="app-footer__links" aria-label="フッターリンク">
        <template v-for="(l, i) in footerLinks" :key="l.label">
          <span v-if="i > 0" class="app-footer__sep" aria-hidden="true">|</span>
          <a :href="l.href" @click.prevent>{{ l.label }}</a>
        </template>
      </nav>

      <div class="app-footer__copy">© Misora Hibari Official Fan Site</div>
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
  justify-self: start;
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
    justify-self: center;
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
