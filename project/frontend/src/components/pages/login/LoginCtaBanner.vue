<script setup>
/**
 * 部品名: ログインページ下部 CTA バナー
 * 用途: 「美空ひばりを、これからも共に。」訴求帯
 */
</script>

<template>
  <section class="login-cta" aria-label="サイトメッセージ">
    <div class="login-cta__lilies" aria-hidden="true">
      <svg viewBox="0 0 120 100" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="40" cy="70" rx="22" ry="35" fill="#fff" opacity="0.9" transform="rotate(-10 40 70)" />
        <ellipse cx="58" cy="65" rx="18" ry="30" fill="#fff" opacity="0.85" transform="rotate(8 58 65)" />
        <ellipse cx="25" cy="75" rx="16" ry="28" fill="#fff" opacity="0.8" transform="rotate(-25 25 75)" />
      </svg>
    </div>

    <div class="login-cta__copy">
      <h2 class="login-cta__title">美空ひばりを、これからも共に。</h2>
      <p class="login-cta__sub">美空ひばりの歌と想いを、未来へつなぎましょう。</p>
    </div>

    <div class="login-cta__silhouette" aria-hidden="true">
      <svg viewBox="0 0 80 120" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="40" cy="28" rx="18" ry="22" fill="var(--murasaki-600)" opacity="0.85" />
        <path
          d="M22 52 Q40 45 58 52 L62 95 Q40 88 18 95 Z"
          fill="var(--murasaki-700)"
          opacity="0.9"
        />
        <rect x="8" y="70" width="6" height="45" rx="3" fill="var(--murasaki-500)" opacity="0.7" />
        <ellipse cx="11" cy="68" rx="14" ry="10" fill="none" stroke="var(--murasaki-500)" stroke-width="2" opacity="0.7" />
      </svg>
    </div>
  </section>
</template>

<style scoped>
.login-cta {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
  width: 100vw;
  max-width: none;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  padding: 48px 64px;
  background: linear-gradient(
    90deg,
    #ebe4f2 0%,
    #e8e0ef 30%,
    #e5dce8 70%,
    #ebe4f2 100%
  );
  border-top: 1px solid rgba(122, 80, 136, 0.12);
  overflow: hidden;
}
.login-cta__lilies {
  flex-shrink: 0;
  width: 100px;
  opacity: 0.85;
}
.login-cta__lilies svg {
  width: 100%;
  height: auto;
}
.login-cta__copy {
  flex: 1;
  text-align: center;
  max-width: 640px;
}
.login-cta__title {
  margin: 0 0 10px;
  font-family: var(--ff-mincho);
  font-size: clamp(20px, 2.4vw, 28px);
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--murasaki-800);
}
.login-cta__sub {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  letter-spacing: 0.06em;
  color: var(--site-text-muted);
}
.login-cta__silhouette {
  flex-shrink: 0;
  width: 72px;
  opacity: 0.75;
}
.login-cta__silhouette svg {
  width: 100%;
  height: auto;
}

@media (max-width: 767px) {
  .login-cta {
    flex-direction: column;
    padding: 36px 24px;
    gap: 20px;
  }
  .login-cta__lilies,
  .login-cta__silhouette {
    width: 64px;
  }
}
</style>
