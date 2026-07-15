<script setup>
/**
 * 部品名: 利用規約・プライバシーポリシー 同意モーダル
 * 用途: 規約全文を表示し、最下部までスクロールしないと「同意する」を押せない
 * イベント: agree（同意）/ close（閉じる）
 */
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { SITE_NAME } from '../../../constants/site.js'

const emit = defineEmits(['agree', 'close'])

const bodyRef = ref(null)
const reachedBottom = ref(false)

function onScroll() {
  const el = bodyRef.value
  if (!el) return
  // 最下部付近（誤差2px）まで到達したら同意可能に
  if (el.scrollTop + el.clientHeight >= el.scrollHeight - 2) {
    reachedBottom.value = true
  }
}

function onKey(e) {
  if (e.key === 'Escape') emit('close')
}

onMounted(async () => {
  document.body.style.overflow = 'hidden'
  window.addEventListener('keydown', onKey)
  await nextTick()
  // スクロール不要な高さの場合は最初から同意可能にする
  const el = bodyRef.value
  if (el && el.scrollHeight <= el.clientHeight + 2) {
    reachedBottom.value = true
  }
})

onUnmounted(() => {
  document.body.style.overflow = ''
  window.removeEventListener('keydown', onKey)
})
</script>

<template>
  <div class="terms" role="dialog" aria-modal="true" aria-label="利用規約・プライバシーポリシー">
    <div class="terms__overlay" @click="emit('close')" />

    <div class="terms__panel">
      <header class="terms__header">
        <h2 class="terms__title">利用規約・プライバシーポリシー</h2>
        <button type="button" class="terms__close" aria-label="閉じる" @click="emit('close')">✕</button>
      </header>
      <hr class="terms__rule" />

      <div ref="bodyRef" class="terms__body" @scroll="onScroll">
        <section class="terms__section">
          <h3 class="terms__h3">利用規約</h3>
          <p class="terms__p">第1条（適用）</p>
          <p class="terms__p">
            本規約は、{{ SITE_NAME }} が提供するファンクラブ会員向けサービス（以下「本サービス」といいます）の利用に関する条件を、本サービスを利用する会員（以下「会員」といいます）と当プラットフォームとの間で定めるものです。
          </p>
          <p class="terms__p">第2条（会員登録）</p>
          <p class="terms__p">
            会員登録を希望する方は、当会の定める方法により申込みを行い、当会がこれを承認することで会員登録が完了します。登録情報に虚偽があった場合、当会は登録を取り消すことができます。
          </p>
          <p class="terms__p">第3条（会費）</p>
          <p class="terms__p">
            会員は、選択したプランに応じた会費を、当会の定める支払い方法により支払うものとします。一度支払われた会費は、当会に別段の定めがある場合を除き、返金されません。
          </p>
          <p class="terms__p">第4条（禁止事項）</p>
          <p class="terms__p">
            会員は、本サービスの利用にあたり、法令または公序良俗に違反する行為、当会または第三者の権利を侵害する行為、限定コンテンツを無断で複製・配布する行為を行ってはなりません。
          </p>
          <p class="terms__p">第5条（退会）</p>
          <p class="terms__p">
            会員は、当会所定の手続きによりいつでも退会できます。退会後は、会員限定コンテンツおよび特典を利用できなくなります。
          </p>
          <p class="terms__p">第6条（免責）</p>
          <p class="terms__p">
            当会は、本サービスに関して会員に生じた損害について、当会の故意または重過失による場合を除き、責任を負わないものとします。
          </p>
        </section>

        <section class="terms__section">
          <h3 class="terms__h3">プライバシーポリシー</h3>
          <p class="terms__p">1. 取得する情報</p>
          <p class="terms__p">
            当会は、会員登録および本サービスの提供にあたり、氏名・住所・性別・メールアドレス・支払い情報等の個人情報を取得します。
          </p>
          <p class="terms__p">2. 利用目的</p>
          <p class="terms__p">
            取得した個人情報は、本サービスの提供、会費の請求、会員向けの各種案内、お問い合わせへの対応、サービス改善のために利用します。
          </p>
          <p class="terms__p">3. 第三者提供</p>
          <p class="terms__p">
            当会は、法令に基づく場合または会員の同意がある場合を除き、個人情報を第三者に提供しません。決済処理に必要な範囲で決済代行会社に提供することがあります。
          </p>
          <p class="terms__p">4. 安全管理</p>
          <p class="terms__p">
            当会は、個人情報の漏えい・滅失・毀損を防止するため、適切な安全管理措置を講じます。
          </p>
          <p class="terms__p">5. 開示・訂正・削除</p>
          <p class="terms__p">
            会員は、当会所定の手続きにより、自己の個人情報の開示・訂正・削除を請求することができます。
          </p>
          <p class="terms__p">6. お問い合わせ</p>
          <p class="terms__p">
            本ポリシーに関するお問い合わせは、当会の会員サポート窓口までご連絡ください。以上をもって、利用規約およびプライバシーポリシーの全文となります。内容をご確認のうえ、同意いただける場合は下部のボタンを押してください。
          </p>
        </section>
      </div>

      <footer class="terms__footer">
        <p v-if="!reachedBottom" class="terms__hint">
          最後までお読みいただくと「同意する」ボタンが有効になります。
        </p>
        <div class="terms__actions">
          <button type="button" class="terms__cancel" @click="emit('close')">閉じる</button>
          <button
            type="button"
            class="terms__agree"
            :disabled="!reachedBottom"
            @click="emit('agree')"
          >
            同意する
          </button>
        </div>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.terms {
  position: fixed;
  inset: 0;
  z-index: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.terms__overlay {
  position: absolute;
  inset: 0;
  background: rgba(40, 30, 25, 0.5);
}
.terms__panel {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 620px;
  max-height: 85vh;
  background: var(--site-surface) !important;
  border: 1px solid var(--kin-500);
  border-radius: var(--site-radius-lg);
  box-shadow: var(--site-shadow-md);
  overflow: hidden;
  color: var(--site-text) !important;
}
.terms__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 28px 0;
}
.terms__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--site-text) !important;
}
.terms__close {
  background: transparent;
  border: 0;
  color: var(--site-text-muted) !important;
  cursor: pointer;
  font-size: 20px;
  line-height: 1;
}
.terms__close:hover {
  color: var(--murasaki-700) !important;
}
.terms__rule {
  margin: 16px 28px 0;
  border: 0;
  height: 1px;
  background: var(--kin-500);
}
.terms__body {
  flex: 1 1 auto;
  overflow-y: auto;
  padding: 20px 28px;
}
.terms__section + .terms__section {
  margin-top: 28px;
  padding-top: 24px;
  border-top: 1px solid var(--site-border);
}
.terms__h3 {
  margin: 0 0 14px;
  font-family: var(--ff-mincho);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--murasaki-700) !important;
}
.terms__p {
  margin: 0 0 12px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.9;
  color: var(--site-text) !important;
}
.terms__footer {
  flex-shrink: 0;
  padding: 16px 28px 24px;
  border-top: 1px solid var(--site-border);
  background: var(--site-surface);
}
.terms__hint {
  margin: 0 0 12px;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  text-align: center;
  color: var(--kin-600);
}
.terms__actions {
  display: flex;
  gap: 12px;
}
.terms__cancel {
  flex: 0 0 auto;
  padding: 13px 24px;
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  letter-spacing: 0.06em;
  color: var(--site-text);
  background: var(--site-surface);
  border: 1px solid var(--site-border-strong);
  border-radius: 999px;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}
.terms__cancel:hover {
  border-color: var(--murasaki-400);
  background: var(--murasaki-100);
}
.terms__agree {
  flex: 1 1 auto;
  padding: 13px 24px;
  font-family: var(--ff-sans-jp);
  font-size: 15px;
  font-weight: 500;
  letter-spacing: 0.12em;
  color: #fff;
  background: var(--murasaki-700);
  border: 1px solid var(--murasaki-800);
  border-radius: 999px;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(93, 58, 107, 0.25);
  transition: background 0.2s;
}
.terms__agree:hover:not(:disabled) {
  background: var(--murasaki-800);
}
.terms__agree:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  box-shadow: none;
}

@media (max-width: 480px) {
  .terms {
    padding: 0;
    align-items: flex-end;
  }
  .terms__panel {
    max-height: 92vh;
    border-radius: var(--site-radius-lg) var(--site-radius-lg) 0 0;
  }
  .terms__header {
    padding: 20px 20px 0;
  }
  .terms__rule {
    margin: 12px 20px 0;
  }
  .terms__body {
    padding: 16px 20px;
  }
  .terms__footer {
    padding: 14px 20px 20px;
  }
}
</style>
