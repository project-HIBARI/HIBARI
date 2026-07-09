<script setup>
/**
 * ページ: 利用規約
 */
import { SITE_NAME } from '../../constants/site.js'

const articles = [
  {
    title: '第1条（適用）',
    body: `本規約は、${SITE_NAME}（以下「当サイト」）の利用条件を定めるものです。`,
  },
  {
    title: '第2条（サービスの内容）',
    body: '当サイトは、複数のアーティストに関連する情報の提供、ファンクラブサービス、および会員向けサービスを提供します。',
  },
  {
    title: '第3条（会員登録）',
    body: '一部のサービスのご利用には、会員登録（無料または有料）が必要です。登録情報は正確にご入力ください。',
  },
  {
    title: '第4条（利用料金および支払い）',
    body: '有料サービスの利用には、所定の料金が発生します。料金は事前の告知なく変更される場合があります。',
  },
  {
    title: '第5条（禁止事項）',
    body: 'ユーザーは、当サイトの利用にあたり、法令や公序良俗に反する行為、他のユーザーや第三者の権利を侵害する行為を行ってはならないものとします。',
  },
  {
    title: '第6条（知的財産権）',
    body: '当サイトに掲載されている文章・画像・音源・動画等の著作権は、当サイトまたは正当な権利を有する第三者に帰属します。無断での転載・複製・改変を禁止します。',
  },
  {
    title: '第7条（免責事項）',
    body: '当サイトの情報は、可能な限り正確な内容の提供に努めますが、その内容の正確性や安全性を保証するものではありません。',
  },
  {
    title: '第8条（規約の変更）',
    body: '当サイトは、必要に応じて本規約を変更することができます。変更後の規約は、当サイトに掲載した時点より効力を生じるものとします。',
  },
  {
    title: '第9条（準拠法および管轄裁判所）',
    body: '本規約の解釈および適用は日本法に準拠します。本サイトの利用に関して紛争が生じた場合は、当社所在地を管轄する裁判所を専属的合意管轄とします。',
  },
]
</script>

<template>
  <div class="page-terms">
    <div class="page-terms__inner">
      <header class="page-terms__head">
        <div class="page-terms__ornament page-terms__ornament--top" aria-hidden="true">
          <span class="page-terms__ornament-line" />
          <span class="page-terms__ornament-mark">❧</span>
          <span class="page-terms__ornament-line" />
        </div>
        <h1 class="page-terms__title">利用規約</h1>
        <p class="page-terms__lead">
          本サイトをご利用いただく際の基本的なルールを定めています。<br />
          ご利用の前に、必ずご確認ください。
        </p>
        <div class="page-terms__ornament" aria-hidden="true">
          <span class="page-terms__ornament-line" />
          <span class="page-terms__ornament-diamond">◆</span>
          <span class="page-terms__ornament-line" />
        </div>
      </header>

      <div class="page-terms__body">
        <article
          v-for="(article, index) in articles"
          :key="article.title"
          class="page-terms__article"
        >
          <div v-if="index > 0" class="page-terms__divider" aria-hidden="true">
            <span class="page-terms__divider-line" />
            <span class="page-terms__divider-diamond">◆</span>
            <span class="page-terms__divider-line" />
          </div>
          <h2 class="page-terms__article-title">{{ article.title }}</h2>
          <p class="page-terms__article-body">{{ article.body }}</p>
        </article>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-terms {
  color: var(--site-text);
  background: linear-gradient(180deg, #fffefb 0%, var(--site-bg) 100%);
  padding: 48px 24px 72px;
}

.page-terms__inner {
  max-width: 860px;
  margin: 0 auto;
  text-align: center;
}

.page-terms__head {
  margin-bottom: 40px;
}

.page-terms__ornament {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  max-width: 320px;
  margin: 0 auto;
}

.page-terms__ornament--top {
  margin-bottom: 16px;
  max-width: 200px;
}

.page-terms__ornament-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--kin-500), transparent);
}

.page-terms__ornament-diamond,
.page-terms__ornament-mark {
  flex-shrink: 0;
  font-size: 10px;
  line-height: 1;
  color: var(--kin-600);
}

.page-terms__ornament-mark {
  font-size: 14px;
}

.page-terms__title {
  margin: 0 0 20px;
  font-family: var(--ff-mincho);
  font-size: clamp(28px, 4vw, 36px);
  font-weight: 700;
  letter-spacing: 0.12em;
  color: var(--murasaki-800);
}

.page-terms__lead {
  margin: 0 0 20px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 2;
  letter-spacing: 0.04em;
  color: var(--site-text-muted);
}

.page-terms__body {
  text-align: center;
}

.page-terms__article {
  padding: 0;
}

.page-terms__divider {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin: 28px auto;
  max-width: 520px;
}

.page-terms__divider-line {
  flex: 1;
  height: 0;
  border-top: 1px dotted rgba(201, 169, 97, 0.55);
}

.page-terms__divider-diamond {
  flex-shrink: 0;
  font-size: 8px;
  line-height: 1;
  color: var(--kin-600);
}

.page-terms__article-title {
  margin: 0 0 12px;
  font-family: var(--ff-mincho);
  font-size: clamp(17px, 2.2vw, 20px);
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--murasaki-800);
}

.page-terms__article-body {
  margin: 0 auto;
  max-width: 720px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 2;
  letter-spacing: 0.04em;
  color: var(--site-text-muted);
  white-space: pre-line;
}

@media (max-width: 767px) {
  .page-terms {
    padding: 36px 16px 56px;
  }

  .page-terms__head {
    margin-bottom: 28px;
  }

  .page-terms__divider {
    margin: 22px auto;
  }

  .page-terms__article-body {
    font-size: 12px;
    line-height: 1.9;
  }
}
</style>
