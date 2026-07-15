<script setup>
/**
 * 部品名: ログイン / 新規登録 準備中モーダル
 * 用途: ヘッダーの「ログイン」「新規登録」クリック時に表示（API 未接続）
 */
import ModalShell from './ModalShell.vue'
import UiButton from '../ui/UiButton.vue'

defineProps({
  /** login / register / search */
  mode: { type: String, default: 'login' },
})

const emit = defineEmits(['close'])

const titles = {
  login: 'ログイン',
  register: '新規登録',
  'forgot-password': 'パスワード再設定',
  terms: '利用規約',
  privacy: 'プライバシーポリシー',
  search: 'サイト内検索',
}

const messages = {
  login: 'ログイン機能は現在準備中です。',
  register: '新規会員登録機能は現在準備中です。',
  'forgot-password': 'パスワード再設定機能は現在準備中です。',
  terms: '利用規約ページは現在準備中です。',
  privacy: 'プライバシーポリシーページは現在準備中です。',
  search: 'サイト内検索機能は現在準備中です。',
}
</script>

<template>
  <ModalShell :title="titles[mode] || '会員機能'" @close="emit('close')">
    <div class="auth-notice">
      <div class="auth-notice__badge">近日公開</div>
      <p class="auth-notice__text">
        {{ messages[mode] || 'この機能は現在準備中です。' }}<br />
        公開まで今しばらくお待ちください。
      </p>
      <p v-if="!['search'].includes(mode)" class="auth-notice__note">
        ファンクラブ特典や会員限定コンテンツのご案内は、Music Memories トップページよりご確認いただけます。
      </p>
      <UiButton variant="primary" size="md" @click="emit('close')">閉じる</UiButton>
    </div>
  </ModalShell>
</template>

<style scoped>
.auth-notice {
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: flex-start;
}
.auth-notice__badge {
  display: inline-block;
  padding: 4px 12px;
  background: var(--murasaki-100);
  color: var(--murasaki-700);
  border: 1px solid var(--murasaki-400);
  border-radius: 999px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  letter-spacing: 0.1em;
}
.auth-notice__text {
  margin: 0;
  font-size: var(--font-size-small);
  line-height: 1.9;
  color: var(--site-text);
}
.auth-notice__note {
  margin: 0;
  font-size: var(--font-size-caption);
  line-height: 1.8;
  color: var(--site-text-muted);
}
</style>
