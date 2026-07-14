<script setup>
/**
 * 部品名: Music Memories ロゴ
 * 用途: 横長ロゴ / アイコンマークの表示
 */
import { SITE_LOGO_SRC, SITE_ICON_SRC, SITE_LOGO_ALT } from '../../constants/site.js'

defineProps({
  /** full = 横長ロゴ, mark = 正方形アイコン */
  variant: { type: String, default: 'full' },
  /** sm | md | lg */
  size: { type: String, default: 'md' },
})
</script>

<template>
  <img
    :src="variant === 'mark' ? SITE_ICON_SRC : SITE_LOGO_SRC"
    :alt="SITE_LOGO_ALT"
    class="mm-logo"
    :class="[`mm-logo--${variant}`, `mm-logo--${size}`]"
    decoding="async"
  />
</template>

<style scoped>
.mm-logo {
  display: block;
  width: auto;
  height: auto;
  object-fit: contain;
}

.mm-logo--full.mm-logo--sm {
  max-height: 36px;
}

.mm-logo--full.mm-logo--md {
  max-height: 48px;
}

.mm-logo--full.mm-logo--lg {
  max-height: 72px;
}

.mm-logo--full.mm-logo--hero {
  max-height: clamp(56px, 12vw, 88px);
}

.mm-logo--mark.mm-logo--sm {
  width: 32px;
  height: 32px;
  border-radius: 8px;
}

.mm-logo--mark.mm-logo--md {
  width: 40px;
  height: 40px;
  border-radius: 10px;
}

.mm-logo--mark.mm-logo--lg {
  width: 56px;
  height: 56px;
  border-radius: 12px;
}
</style>
