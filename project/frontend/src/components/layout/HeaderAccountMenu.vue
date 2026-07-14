<script setup>
/**
 * 部品名: ヘッダー アカウントメニュー
 * 用途: ログイン状態に応じた認証 UI / アカウント設定への導線
 */
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { MEMBERSHIP_LABELS } from '../../constants/membership.js'

const props = defineProps({
  isLoggedIn: { type: Boolean, default: false },
  userName: { type: String, default: '' },
  membership: { type: String, default: 'general' },
})

const emit = defineEmits(['open-auth', 'open-account', 'logout', 'go-fanclub'])

const menuOpen = ref(false)
const rootRef = ref(null)

const planLabel = computed(() => MEMBERSHIP_LABELS[props.membership] || '一般会員')
const displayName = computed(() => props.userName || '会員')

function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

function closeMenu() {
  menuOpen.value = false
}

function onDocumentClick(event) {
  if (!rootRef.value?.contains(event.target)) {
    closeMenu()
  }
}

onMounted(() => {
  document.addEventListener('click', onDocumentClick)
})

onUnmounted(() => {
  document.removeEventListener('click', onDocumentClick)
})
</script>

<template>
  <div ref="rootRef" class="header-account">
    <template v-if="isLoggedIn">
      <button
        type="button"
        class="header-account__trigger"
        :aria-expanded="menuOpen"
        aria-haspopup="true"
        @click.stop="toggleMenu"
      >
        <span class="header-account__avatar" aria-hidden="true">{{ displayName.charAt(0) }}</span>
        <span class="header-account__name">{{ displayName }}</span>
        <span class="header-account__chevron" :class="{ 'header-account__chevron--open': menuOpen }">▾</span>
      </button>
      <div v-if="menuOpen" class="header-account__menu" role="menu">
        <p class="header-account__plan">{{ planLabel }}</p>
        <button type="button" class="header-account__item" role="menuitem" @click="emit('open-account'); closeMenu()">
          アカウント設定
        </button>
        <button type="button" class="header-account__item" role="menuitem" @click="emit('go-fanclub'); closeMenu()">
          ファンクラブサイト
        </button>
        <button type="button" class="header-account__item header-account__item--logout" role="menuitem" @click="emit('logout'); closeMenu()">
          ログアウト
        </button>
      </div>
    </template>
    <div v-else class="header-account__auth">
      <button
        type="button"
        class="header-account__btn header-account__btn--login"
        @click="emit('open-auth', 'login')"
      >
        ログイン
      </button>
      <button
        type="button"
        class="header-account__btn header-account__btn--register site-cta-accent"
        @click="emit('open-auth', 'register')"
      >
        新規会員登録
      </button>
    </div>
  </div>
</template>

<style scoped>
.header-account {
  position: relative;
}
.header-account__auth {
  display: flex;
  align-items: center;
  gap: 8px;
}
.header-account__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px 12px;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.06em;
  white-space: nowrap;
  border-radius: 999px;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s, color 0.2s, box-shadow 0.2s;
}
.header-account__btn--login {
  background: #fff;
  color: var(--site-text);
  border: 1px solid var(--kin-500);
}
.header-account__btn--login:hover {
  background: #fffefb;
  border-color: var(--kin-600);
}
.header-account__btn--register {
  background: var(--murasaki-700);
  color: #fff;
  border: 1px solid var(--murasaki-800);
}
.header-account__trigger {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 10px 4px 4px;
  border: 1px solid var(--site-border);
  border-radius: 999px;
  background: #fff;
  cursor: pointer;
  max-width: 180px;
}
.header-account__avatar {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--murasaki-700);
  color: #fff;
  font-size: 12px;
  font-weight: 700;
}
.header-account__name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  color: var(--site-text);
}
.header-account__chevron {
  font-size: 10px;
  color: var(--site-text-muted);
  transition: transform 0.2s;
}
.header-account__chevron--open {
  transform: rotate(180deg);
}
.header-account__menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 200px;
  padding: 8px 0;
  background: #fff;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  box-shadow: var(--site-shadow-md);
  z-index: 60;
}
.header-account__plan {
  margin: 0;
  padding: 8px 16px 10px;
  font-size: 11px;
  color: var(--murasaki-700);
  border-bottom: 1px solid var(--site-border);
}
.header-account__item {
  display: block;
  width: 100%;
  padding: 10px 16px;
  border: 0;
  background: transparent;
  text-align: left;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  color: var(--site-text);
  cursor: pointer;
}
.header-account__item:hover {
  background: var(--murasaki-100);
}
.header-account__item--logout {
  color: var(--beni-600);
  border-top: 1px solid var(--site-border);
  margin-top: 4px;
}
@media (min-width: 1100px) {
  .header-account__btn {
    padding: 6px 12px;
    font-size: 12px;
  }
}
@media (min-width: 1280px) {
  .header-account__btn {
    padding: 7px 16px;
    font-size: 13px;
  }
}
</style>
