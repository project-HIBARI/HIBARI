<script setup>
/**
 * 部品名: フッター
 * 役割: 公式 SNS・各種リンク・著作権表示（全ページ共通）
 */
const footerLinks = [
  { label: 'よくある質問', href: '#' },
  { label: 'お問い合わせ', href: '#' },
  { label: '利用規約', href: '#' },
  { label: 'プライバシーポリシー', href: '#' },
]

const snsItems = [
  { label: 'YouTube', abbr: 'YT' },
  { label: 'X', abbr: 'X' },
  { label: 'Instagram', abbr: 'IG' },
  { label: 'LINE', abbr: 'LN' },
  { label: 'Facebook', abbr: 'FB' },
]
</script>

<template>
  <footer role="contentinfo" class="app-footer">
    <div class="footer-grid">
      <div class="app-footer__sns">
        <span class="app-footer__sns-label">公式SNS</span>
        <a
          v-for="s in snsItems"
          :key="s.label"
          href="#"
          class="app-footer__sns-link"
          :aria-label="s.label"
          @click.prevent
        >{{ s.abbr }}</a>
      </div>

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
.footer-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
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
  justify-content: center;
  gap: 0;
}

@media (max-width: 767px) {
  .footer-grid {
    grid-template-columns: 1fr;
    text-align: center;
  }
  .app-footer__sns {
    justify-content: center;
  }
  .app-footer__links {
    justify-content: center;
  }
}
</style>
