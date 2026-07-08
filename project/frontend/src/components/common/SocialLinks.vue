<script setup>
/**
 * 部品名: 公式SNSリンク
 * 用途: 全ページ共通のSNSアイコン導線
 */
import { socialLinks, socialIconUrl } from '../../lib/socialLinks.js'

defineProps({
  /** default: 中央ブロック / footer: フッター左寄せインライン */
  variant: { type: String, default: 'default' },
})
</script>

<template>
  <section
    class="social-links"
    :class="{ 'social-links--footer': variant === 'footer' }"
    aria-labelledby="social-links-title"
  >
    <p id="social-links-title" class="social-links__label">公式SNS</p>
    <p v-if="variant !== 'footer'" class="social-links__sub" aria-hidden="true">FOLLOW US</p>

    <ul class="social-links__list">
      <li v-for="item in socialLinks" :key="item.id" class="social-links__item">
        <a
          :href="item.href"
          class="social-links__link"
          :aria-label="item.label"
          target="_blank"
          rel="noopener noreferrer"
          @click="item.href === '#' ? $event.preventDefault() : undefined"
        >
          <img
            :src="socialIconUrl(item.icon)"
            alt=""
            class="social-links__icon"
            width="38"
            height="38"
            decoding="async"
            draggable="false"
          />
        </a>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.social-links {
  padding: 40px 24px 36px;
  text-align: center;
  background: linear-gradient(
    180deg,
    var(--site-surface-muted) 0%,
    var(--site-bg) 100%
  );
  border-top: 1px solid var(--site-border);
}

.social-links__label {
  margin: 0 0 4px;
  font-family: var(--ff-mincho);
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: var(--murasaki-700);
}

.social-links__sub {
  margin: 0 0 20px;
  font-family: var(--ff-latin);
  font-style: italic;
  font-size: 11px;
  letter-spacing: 0.22em;
  color: var(--kin-600);
}

.social-links__list {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.social-links__item {
  flex: 0 0 auto;
}

.social-links__link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  padding: 2px;
  border-radius: 50%;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.social-links__link:hover {
  transform: scale(1.08);
  opacity: 0.9;
}

.social-links__link:focus-visible {
  outline: 2px solid var(--murasaki-500);
  outline-offset: 3px;
}

.social-links__icon {
  display: block;
  width: 38px;
  height: 38px;
  flex-shrink: 0;
  object-fit: contain;
  aspect-ratio: 1 / 1;
}

/* フッター内インライン表示 */
.social-links--footer {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0;
  margin: 0;
  text-align: left;
  background: transparent;
  border: 0;
}

.social-links--footer .social-links__label {
  margin: 0;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--site-text-light);
  white-space: nowrap;
}

.social-links--footer .social-links__list {
  gap: 8px;
  justify-content: flex-start;
}

.social-links--footer .social-links__icon {
  width: 28px;
  height: 28px;
}

@media (max-width: 767px) {
  .social-links:not(.social-links--footer) {
    padding: 32px 16px 28px;
  }

  .social-links:not(.social-links--footer) .social-links__list {
    gap: 16px;
    max-width: 280px;
    margin: 0 auto;
  }

  .social-links--footer {
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }

  .social-links--footer .social-links__list {
    justify-content: center;
  }
}
</style>
