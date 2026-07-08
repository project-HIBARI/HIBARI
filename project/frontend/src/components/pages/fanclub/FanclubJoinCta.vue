<script setup>
/**
 * 部品名: ファンクラブ 加入CTA
 * 用途: ページ下部で「ファンクラブ加入」への導線をまとめて表示する
 */
import UiIco from '../../ui/UiIco.vue'

const emit = defineEmits(['join'])
</script>

<template>
  <section class="fc-cta">
    <span class="fc-cta__corner fc-cta__corner--tl" aria-hidden="true" />
    <span class="fc-cta__corner fc-cta__corner--tr" aria-hidden="true" />
    <span class="fc-cta__corner fc-cta__corner--bl" aria-hidden="true" />
    <span class="fc-cta__corner fc-cta__corner--br" aria-hidden="true" />

    <p class="fc-cta__lead">ひばりの世界を、もっと近くで。</p>
    <h2 class="fc-cta__title">ファンクラブに加入しませんか</h2>
    <p class="fc-cta__desc">
      加入手続きは数分で完了し、すぐに会員特典をご利用いただけます。
    </p>

    <button type="button" class="fc-cta__btn" @click="emit('join')">
      <UiIco name="heart" :size="18" color="#fff" />
      ファンクラブ加入
      <span aria-hidden="true">›</span>
    </button>
    <p class="fc-cta__note">加入には会員情報の登録が必要です。</p>
  </section>
</template>

<style scoped>
.fc-cta {
  position: relative;
  text-align: center;
  padding: 48px 24px;
  background: linear-gradient(135deg, var(--murasaki-800) 0%, var(--murasaki-700) 100%);
  border: 1px solid var(--kin-500);
  border-radius: var(--site-radius-lg);
  box-shadow: var(--site-shadow-md);
  color: var(--paper-50);
  overflow: hidden;
}
.fc-cta__corner {
  position: absolute;
  width: 26px;
  height: 26px;
  border-color: var(--kin-500);
  border-style: solid;
  opacity: 0.8;
}
.fc-cta__corner--tl {
  top: 12px;
  left: 12px;
  border-width: 2px 0 0 2px;
}
.fc-cta__corner--tr {
  top: 12px;
  right: 12px;
  border-width: 2px 2px 0 0;
}
.fc-cta__corner--bl {
  bottom: 12px;
  left: 12px;
  border-width: 0 0 2px 2px;
}
.fc-cta__corner--br {
  bottom: 12px;
  right: 12px;
  border-width: 0 2px 2px 0;
}
.fc-cta__lead {
  margin: 0 0 8px;
  font-family: var(--ff-mincho);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: var(--kin-400);
}
.fc-cta__title {
  margin: 0 0 14px;
  font-family: var(--ff-mincho);
  font-size: clamp(22px, 3vw, 30px);
  font-weight: 800;
  letter-spacing: 0.08em;
  color: #fff;
}
.fc-cta__desc {
  margin: 0 auto 28px;
  max-width: 520px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.85;
  color: rgba(255, 255, 255, 0.9);
}
.fc-cta__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 40px;
  font-family: var(--ff-sans-jp);
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.12em;
  color: #fff;
  background: linear-gradient(180deg, var(--kin-500), var(--kin-600));
  border: 1px solid var(--kin-600);
  border-radius: 999px;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
  transition: filter 0.2s, transform 0.1s;
}
.fc-cta__btn:hover {
  filter: brightness(1.08);
}
.fc-cta__btn:active {
  transform: translateY(1px);
}
.fc-cta__note {
  margin: 14px 0 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  color: rgba(255, 255, 255, 0.7);
}
</style>
