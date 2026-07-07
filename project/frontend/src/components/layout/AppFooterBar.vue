<script setup>
/**
 * 部品名: フッター
 * 役割: 公式 SNS・各種リンク・著作権表示（全ページ共通）
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
  <div class="app-footer-wrap">
    <SocialLinks />

    <footer role="contentinfo" class="app-footer">
      <div class="footer-grid">
        <nav class="app-footer__links app-footer__links--start" aria-label="フッターリンク">
          <template v-for="(l, i) in footerLinks" :key="l.label">
            <span v-if="i > 0" class="app-footer__sep" aria-hidden="true">|</span>
            <a :href="l.href" @click.prevent>{{ l.label }}</a>
          </template>
        </nav>

        <div class="app-footer__copy">© Misora Hibari Official Fan Site</div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.app-footer-wrap {
  margin-top: 0;
}
.footer-grid {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 24px;
  align-items: center;
}
.app-footer__sep {
  color: var(--site-border);
  margin: 0 4px;
  user-select: none;
}
.app-footer__links {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0;
}
.app-footer__links--start {
  justify-content: flex-start;
}
.app-footer__copy {
  text-align: right;
}

@media (max-width: 767px) {
  .footer-grid {
    grid-template-columns: 1fr;
    text-align: center;
  }
  .app-footer__links--start {
    justify-content: center;
  }
  .app-footer__copy {
    text-align: center;
  }
}
</style>
