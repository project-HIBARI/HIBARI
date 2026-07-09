<script setup>
/**
 * 部品名: アカウント設定モーダル
 * 用途: ヘッダーからプロフィール・支払方法・プラン変更
 */
import ModalShell from './ModalShell.vue'
import FanclubAccountPanel from '../pages/fanclub/FanclubAccountPanel.vue'

const emit = defineEmits(['close', 'need-login', 'logout', 'user-updated'])

function onLogout() {
  emit('logout')
  emit('close')
}
</script>

<template>
  <ModalShell title="アカウント設定" wide @close="emit('close')">
    <FanclubAccountPanel
      @need-login="emit('need-login')"
      @logout="onLogout"
      @user-updated="emit('user-updated', $event)"
    />
  </ModalShell>
</template>
