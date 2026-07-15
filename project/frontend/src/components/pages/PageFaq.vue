<script setup>
/**
 * ページ: よくある質問
 */
const faqItems = [
  {
    title: 'AI美空ひばりサブスクリプション登録',
    desc: '登録方法やプラン内容についてご案内します。',
  },
  {
    title: 'ディスコグラフィ',
    desc: '楽曲・アルバムの一覧や情報を確認できます。',
  },
  {
    title: '思い出掲示板',
    desc: 'ファン同士で思い出を共有できる掲示板です。',
  },
  {
    title: '献花',
    desc: '美空ひばりへ感謝の気持ちをお届けいただけます。',
  },
]
</script>

<template>
  <div class="page-faq">
    <div class="page-faq__inner">
      <header class="page-faq__head">
        <h1 class="page-faq__title">よくある質問</h1>
        <div class="page-faq__ornament" aria-hidden="true">
          <span class="page-faq__ornament-line" />
          <span class="page-faq__ornament-diamond">◆</span>
          <span class="page-faq__ornament-line" />
        </div>
      </header>

      <ul class="page-faq__list">
        <li v-for="(item, index) in faqItems" :key="item.title" class="page-faq__item">
          <div v-if="index > 0" class="page-faq__divider" aria-hidden="true">
            <span class="page-faq__divider-line" />
            <span class="page-faq__divider-diamond">◆</span>
            <span class="page-faq__divider-line" />
          </div>
          <h2 class="page-faq__item-title">{{ item.title }}</h2>
          <p class="page-faq__item-desc">{{ item.desc }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.page-faq {
  color: var(--site-text);
  background: linear-gradient(180deg, #fffefb 0%, var(--site-bg) 100%);
  padding: 56px 24px 72px;
}

.page-faq__inner {
  max-width: 820px;
  margin: 0 auto;
  text-align: center;
}

.page-faq__head {
  margin-bottom: 48px;
}

.page-faq__title {
  margin: 0 0 20px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.75rem, 4vw, 2.25rem);
  font-weight: 700;
  letter-spacing: 0.12em;
  color: var(--murasaki-800);
}

.page-faq__ornament {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  max-width: 280px;
  margin: 0 auto;
}

.page-faq__ornament-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--kin-500), transparent);
}

.page-faq__ornament-diamond {
  flex-shrink: 0;
  font-size: var(--font-size-badge);
  line-height: 1;
  color: var(--kin-600);
}

.page-faq__list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.page-faq__item {
  padding: 0;
}

.page-faq__divider {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin: 28px auto;
  max-width: 520px;
}

.page-faq__divider-line {
  flex: 1;
  height: 0;
  border-top: 1px dotted rgba(201, 169, 97, 0.55);
}

.page-faq__divider-diamond {
  flex-shrink: 0;
  font-size: var(--font-size-badge);
  line-height: 1;
  color: var(--kin-600);
}

.page-faq__item-title {
  margin: 0 0 10px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.125rem, 2.5vw, 1.375rem);
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--murasaki-800);
}

.page-faq__item-desc {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-button);
  line-height: 1.9;
  letter-spacing: 0.04em;
  color: var(--site-text-muted);
}

@media (max-width: 767px) {
  .page-faq {
    padding: 40px 20px 56px;
  }

  .page-faq__head {
    margin-bottom: 36px;
  }

  .page-faq__divider {
    margin: 22px auto;
  }
}
</style>
