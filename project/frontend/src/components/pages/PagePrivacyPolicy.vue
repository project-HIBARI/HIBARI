<script setup>
/**
 * ページ: プライバシーポリシー
 */
const articles = [
  {
    title: '第1条（個人情報の取得）',
    body: '当サイトは、サービスの提供に必要な範囲で、適法かつ公正な手段により個人情報を取得します。',
    list: null,
  },
  {
    title: '第2条（利用目的）',
    body: '取得した個人情報は、以下の目的の範囲内で利用します。',
    list: [
      'サービスの提供および運営のため',
      '会員管理および本人確認のため',
      'お問い合わせへの対応のため',
      '新着情報やお知らせのご案内のため（ご同意いただいた場合）',
      'サービスの向上および改善のための分析のため',
    ],
  },
  {
    title: '第3条（第三者提供の制限）',
    body: '当サイトは、法令に基づく場合を除き、ユーザーの同意なく個人情報を第三者に提供しません。',
    list: null,
  },
  {
    title: '第4条（安全管理措置）',
    body: '当サイトは、個人情報の漏えい、滅失または毀損の防止その他の安全管理のため、適切な技術的・組織的措置を講じます。',
    list: null,
  },
  {
    title: '第5条（個人情報の開示・訂正・削除）',
    body: 'ユーザーご本人からの開示・訂正・削除等のご請求があった場合は、ご本人確認のうえ、法令に基づき適切に対応します。',
    list: null,
  },
  {
    title: '第6条（クッキーの利用）',
    body: '当サイトでは、サービスの利便性向上やアクセス解析のため、Cookieを使用することがあります。ブラウザの設定によりCookieの使用を拒否することも可能です。',
    list: null,
  },
  {
    title: '第7条（プライバシーポリシーの変更）',
    body: '本ポリシーの内容は、法令の改正やサービスの変更に伴い、予告なく変更することがあります。変更後は当サイトにてお知らせします。',
    list: null,
  },
  {
    title: '第8条（お問い合わせ窓口）',
    body: '個人情報の取り扱いに関するお問い合わせは、お問い合わせページよりご連絡ください。',
    list: null,
  },
]
</script>

<template>
  <div class="page-privacy">
    <div class="page-privacy__inner">
      <header class="page-privacy__head">
        <div class="page-privacy__ornament page-privacy__ornament--top" aria-hidden="true">
          <span class="page-privacy__ornament-line" />
          <span class="page-privacy__ornament-mark">❧</span>
          <span class="page-privacy__ornament-line" />
        </div>
        <h1 class="page-privacy__title">プライバシーポリシー</h1>
        <p class="page-privacy__lead">
          美空ひばり公式ファンサイト（以下「当サイト」）は、<br />
          ユーザーの個人情報の保護を重要な責務と考え、以下のとおりプライバシーポリシーを定め、<br />
          適切な取り組みを実施します。
        </p>
        <div class="page-privacy__ornament" aria-hidden="true">
          <span class="page-privacy__ornament-line" />
          <span class="page-privacy__ornament-diamond">◆</span>
          <span class="page-privacy__ornament-line" />
        </div>
      </header>

      <div class="page-privacy__body">
        <article
          v-for="(article, index) in articles"
          :key="article.title"
          class="page-privacy__article"
        >
          <div v-if="index > 0" class="page-privacy__divider" aria-hidden="true">
            <span class="page-privacy__divider-line" />
            <span class="page-privacy__divider-diamond">◆</span>
            <span class="page-privacy__divider-line" />
          </div>
          <h2 class="page-privacy__article-title">{{ article.title }}</h2>
          <p class="page-privacy__article-body">{{ article.body }}</p>
          <ul v-if="article.list" class="page-privacy__list">
            <li v-for="item in article.list" :key="item">{{ item }}</li>
          </ul>
        </article>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-privacy {
  color: var(--site-text);
  background: linear-gradient(180deg, #fffefb 0%, var(--site-bg) 100%);
  padding: 48px 24px 72px;
}

.page-privacy__inner {
  max-width: 860px;
  margin: 0 auto;
  text-align: center;
}

.page-privacy__head {
  margin-bottom: 40px;
}

.page-privacy__ornament {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  max-width: 320px;
  margin: 0 auto;
}

.page-privacy__ornament--top {
  margin-bottom: 16px;
  max-width: 200px;
}

.page-privacy__ornament-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--kin-500), transparent);
}

.page-privacy__ornament-diamond,
.page-privacy__ornament-mark {
  flex-shrink: 0;
  font-size: 10px;
  line-height: 1;
  color: var(--kin-600);
}

.page-privacy__ornament-mark {
  font-size: 14px;
}

.page-privacy__title {
  margin: 0 0 20px;
  font-family: var(--ff-mincho);
  font-size: clamp(26px, 3.8vw, 34px);
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--murasaki-800);
}

.page-privacy__lead {
  margin: 0 0 20px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 2;
  letter-spacing: 0.04em;
  color: var(--site-text-muted);
}

.page-privacy__body {
  text-align: center;
}

.page-privacy__article {
  padding: 0;
}

.page-privacy__divider {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin: 28px auto;
  max-width: 520px;
}

.page-privacy__divider-line {
  flex: 1;
  height: 0;
  border-top: 1px dotted rgba(201, 169, 97, 0.55);
}

.page-privacy__divider-diamond {
  flex-shrink: 0;
  font-size: 8px;
  line-height: 1;
  color: var(--kin-600);
}

.page-privacy__article-title {
  margin: 0 0 12px;
  font-family: var(--ff-mincho);
  font-size: clamp(17px, 2.2vw, 20px);
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--murasaki-800);
}

.page-privacy__article-body {
  margin: 0 auto 12px;
  max-width: 720px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 2;
  letter-spacing: 0.04em;
  color: var(--site-text-muted);
}

.page-privacy__article-body:last-child {
  margin-bottom: 0;
}

.page-privacy__list {
  margin: 0 auto;
  padding: 0;
  max-width: 560px;
  list-style: none;
  text-align: left;
}

.page-privacy__list li {
  position: relative;
  padding-left: 1.2em;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 2;
  letter-spacing: 0.04em;
  color: var(--site-text-muted);
}

.page-privacy__list li::before {
  content: '・';
  position: absolute;
  left: 0;
  color: var(--murasaki-600);
}

@media (max-width: 767px) {
  .page-privacy {
    padding: 36px 16px 56px;
  }

  .page-privacy__head {
    margin-bottom: 28px;
  }

  .page-privacy__divider {
    margin: 22px auto;
  }

  .page-privacy__article-body,
  .page-privacy__list li {
    font-size: 12px;
    line-height: 1.9;
  }

  .page-privacy__lead br {
    display: none;
  }
}
</style>
