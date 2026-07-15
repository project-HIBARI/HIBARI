<script setup>
/**
 * 部品名: スマホ用フルスクリーンナビ（HAERA風）
 * 役割: 全画面オーバーレイ・段階表示・ハンバーガー連動
 */
import { ref, watch, nextTick } from 'vue'
import UiButton from '../ui/UiButton.vue'
import TextSizeControl from '../ui/TextSizeControl.vue'
import HeaderSearch from './HeaderSearch.vue'
import MusicMemoriesLogo from '../brand/MusicMemoriesLogo.vue'
import { SITE_NAME } from '../../constants/site.js'

const props = defineProps({
  open: { type: Boolean, default: false },
  items: { type: Array, required: true },
  page: { type: String, required: true },
  isLoggedIn: { type: Boolean, default: false },
  userName: { type: String, default: '' },
  showPlatformBack: { type: Boolean, default: false },
  authOnPlatformOnly: { type: Boolean, default: false },
})

const emit = defineEmits([
  'close',
  'navigate',
  'open-modal',
  'open-auth',
  'open-account',
  'logout',
  'exit-platform',
])

const panelActive = ref(false)
/** タップ直後の sticky :hover が一瞬残るのを抑止 */
const closing = ref(false)
/** 入場 stagger 完了後にホバー用 transition へ切り替える */
const settled = ref(false)
let settleTimer = 0

watch(
  () => props.open,
  async (open) => {
    if (settleTimer) {
      window.clearTimeout(settleTimer)
      settleTimer = 0
    }
    if (open) {
      closing.value = false
      settled.value = false
      await nextTick()
      requestAnimationFrame(() => {
        panelActive.value = true
      })
      // 最大 index 付近の入場が終わる頃に settled
      settleTimer = window.setTimeout(() => {
        settled.value = true
        settleTimer = 0
      }, 850)
    } else {
      panelActive.value = false
      settled.value = false
    }
  },
)

function onNavigate(id) {
  closing.value = true
  if (typeof document !== 'undefined' && document.activeElement instanceof HTMLElement) {
    document.activeElement.blur()
  }
  emit('navigate', id)
  emit('close')
}

function onAction(emitName, payload) {
  closing.value = true
  if (typeof document !== 'undefined' && document.activeElement instanceof HTMLElement) {
    document.activeElement.blur()
  }
  if (payload !== undefined) emit(emitName, payload)
  else emit(emitName)
  emit('close')
}
</script>

<template>
  <Teleport to="body">
    <Transition name="drawer">
      <div
        v-if="open"
        role="dialog"
        aria-modal="true"
        aria-label="ナビゲーション"
        class="drawer"
        :class="{
          'drawer--active': panelActive,
          'drawer--closing': closing,
          'drawer--settled': settled,
        }"
      >
        <div class="drawer__overlay" aria-hidden="true" @click="emit('close')" />

        <div class="drawer__sheet">
          <p class="drawer__label drawer__stagger" :style="{ '--drawer-i': 0 }">Menu</p>

          <button
            v-if="showPlatformBack"
            type="button"
            class="drawer__platform-back drawer__stagger"
            :style="{ '--drawer-i': 0.5 }"
            @click="onAction('exit-platform')"
          >
            <MusicMemoriesLogo variant="mark" size="sm" class="drawer__platform-back-icon" />
            {{ SITE_NAME }} へ戻る
          </button>

          <nav class="drawer__nav" aria-label="モバイルナビゲーション">
            <button
              v-for="(n, index) in items"
              :key="n.id"
              type="button"
              class="drawer__link drawer__stagger"
              :class="{ 'drawer__link--active': page === n.id }"
              :style="{ '--drawer-i': index + 1 }"
              :aria-current="page === n.id ? 'page' : undefined"
              @click="onNavigate(n.id)"
            >
              <span class="drawer__link-text">{{ n.label }}</span>
              <span v-if="page === n.id" class="drawer__link-mark" aria-hidden="true" />
            </button>
          </nav>

          <div class="drawer__extras">
            <div v-if="isLoggedIn && authOnPlatformOnly" class="drawer__user drawer__stagger" :style="{ '--drawer-i': items.length + 2 }">
              <p class="drawer__user-name">{{ userName || '会員' }} さん</p>
              <p class="drawer__user-note">アカウント設定は Music Memories で行えます</p>
            </div>
            <div v-else-if="isLoggedIn" class="drawer__user drawer__stagger" :style="{ '--drawer-i': items.length + 2 }">
              <p class="drawer__user-name">{{ userName || '会員' }} さん</p>
              <div class="drawer__user-actions">
                <UiButton variant="outline" size="md" @click="onAction('open-account')">
                  アカウント設定
                </UiButton>
                <UiButton variant="ghost" size="md" @click="emit('logout')">ログアウト</UiButton>
              </div>
            </div>
            <div v-else-if="!authOnPlatformOnly" class="drawer__auth drawer__stagger" :style="{ '--drawer-i': items.length + 2 }">
              <UiButton variant="outline" size="md" @click="onAction('open-auth', 'login')">ログイン</UiButton>
              <UiButton variant="primary" size="md" @click="onAction('open-auth', 'register')">ファンクラブ加入</UiButton>
            </div>

            <div class="drawer__search drawer__stagger" :style="{ '--drawer-i': items.length + 3 }">
              <HeaderSearch @navigate="onNavigate" />
            </div>

            <div class="drawer__text-size drawer__stagger" :style="{ '--drawer-i': items.length + 4 }">
              <TextSizeControl tone="ink" variant="default" />
            </div>

            <div class="drawer__sub-links">
              <button
                type="button"
                class="drawer__sub drawer__stagger"
                :style="{ '--drawer-i': items.length + 5 }"
                @click="onAction('open-modal', 'fanclub')"
              >
                ファンクラブ
              </button>
              <button
                type="button"
                class="drawer__sub drawer__stagger"
                :style="{ '--drawer-i': items.length + 6 }"
                @click="onAction('open-modal', 'ai')"
              >
                AI美空ひばり
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.drawer {
  position: fixed;
  inset: 0;
  z-index: 200;
  pointer-events: auto;
}

.drawer__overlay {
  position: absolute;
  inset: 0;
  background: rgba(28, 22, 18, 0.42);
  backdrop-filter: blur(4px);
  opacity: 0;
  pointer-events: auto;
  transition: opacity 0.5s ease;
  z-index: 0;
}

.drawer--active .drawer__overlay {
  opacity: 1;
}

.drawer__sheet {
  position: absolute;
  inset: 0;
  z-index: 1;
  display: flex;
  flex-direction: column;
  padding: clamp(88px, 18vh, 120px) clamp(24px, 7vw, 64px) clamp(32px, 6vh, 48px);
  background: linear-gradient(165deg, #fffefb 0%, #f8f3ec 48%, #f3ebe3 100%);
  overflow-y: auto;
  overscroll-behavior: contain;
  pointer-events: auto;
  transform: translateY(-3%);
  opacity: 0;
  transition:
    transform 0.62s cubic-bezier(0.22, 1, 0.36, 1),
    opacity 0.5s ease;
}

.drawer--active .drawer__sheet {
  transform: translateY(0);
  opacity: 1;
}

.drawer__label {
  margin: 0 0 clamp(20px, 4vh, 36px);
  font-family: var(--ff-latin);
  font-size: var(--font-size-caption);
  font-weight: 500;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: var(--site-text-muted);
}

.drawer__platform-back {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin: -12px 0 clamp(16px, 3vh, 24px);
  padding: 8px 14px;
  min-height: 44px;
  border: 1px solid var(--site-border);
  border-radius: 999px;
  background: var(--site-surface);
  color: var(--murasaki-700);
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-navigation);
  letter-spacing: 0.06em;
  cursor: pointer;
  transition:
    transform 0.2s cubic-bezier(0.22, 1, 0.36, 1),
    box-shadow 0.2s ease,
    background-color 0.2s ease,
    border-color 0.2s ease;
  -webkit-tap-highlight-color: transparent;
}

.drawer__platform-back-icon,
.drawer__platform-back :deep(.mm-logo--mark.mm-logo--sm) {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  border-radius: 4px;
}

.drawer__nav {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-bottom: clamp(24px, 5vh, 40px);
}

.drawer__link {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  min-height: 48px;
  margin: 0 0 4px;
  padding: clamp(12px, 2.4vh, 18px) 14px;
  border: 0;
  border-radius: 12px;
  border-bottom: 1px solid rgba(60, 40, 30, 0.08);
  background: transparent;
  text-align: left;
  cursor: pointer;
  color: var(--site-text);
  -webkit-tap-highlight-color: transparent;
  transition:
    color 0.2s ease,
    padding-left 0.2s cubic-bezier(0.22, 1, 0.36, 1),
    transform 0.2s cubic-bezier(0.22, 1, 0.36, 1),
    background-color 0.2s ease,
    box-shadow 0.2s ease,
    border-color 0.2s ease;
}

.drawer__link-text {
  font-family: var(--ff-mincho);
  font-size: clamp(1.375rem, 5.2vw, 1.875rem);
  font-weight: 600;
  letter-spacing: 0.12em;
  line-height: 1.35;
  white-space: normal;
  overflow-wrap: anywhere;
}

.drawer__link-mark {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--kin-500);
  flex-shrink: 0;
}

.drawer__link--active {
  color: var(--murasaki-700);
}

.drawer__extras {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.drawer__auth,
.drawer__user {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.drawer__user-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.drawer__user-name {
  margin: 0 0 4px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-small);
  letter-spacing: 0.08em;
  color: var(--murasaki-700);
  overflow-wrap: anywhere;
}

.drawer__user-note {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  line-height: 1.6;
  color: var(--site-text-muted);
}

.drawer__search :deep(.header-search) {
  display: flex;
  max-width: none;
  width: 100%;
}

.drawer__sub-links {
  display: flex;
  flex-wrap: wrap;
  gap: 12px 20px;
  padding-top: 8px;
  border-top: 1px solid rgba(60, 40, 30, 0.1);
}

.drawer__sub {
  border: 0;
  background: transparent;
  color: var(--murasaki-700);
  padding: 6px 0;
  min-height: 44px;
  cursor: pointer;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-button);
  letter-spacing: 0.1em;
  -webkit-tap-highlight-color: transparent;
  transition: opacity 0.2s ease, transform 0.2s ease, color 0.2s ease;
}

.drawer__stagger {
  opacity: 0;
  transform: translateY(18px);
  transition:
    opacity 0.55s cubic-bezier(0.22, 1, 0.36, 1),
    transform 0.55s cubic-bezier(0.22, 1, 0.36, 1);
  transition-delay: calc(0.06s + var(--drawer-i, 0) * 0.055s);
}

.drawer--active .drawer__stagger {
  opacity: 1;
  transform: translateY(0);
}

/*
 * 入場アニメ完了後だけ delay を外し、ホバー用 transition を優先する。
 */
.drawer--active.drawer--settled .drawer__link.drawer__stagger,
.drawer--active.drawer--settled .drawer__platform-back.drawer__stagger,
.drawer--active.drawer--settled .drawer__sub.drawer__stagger {
  transition:
    color 0.2s ease,
    opacity 0.2s ease,
    padding-left 0.2s cubic-bezier(0.22, 1, 0.36, 1),
    transform 0.2s cubic-bezier(0.22, 1, 0.36, 1),
    background-color 0.2s ease,
    box-shadow 0.2s ease,
    border-color 0.2s ease;
  transition-delay: 0s;
}

/* 押下中（スマホ・デスクトップ共通） */
.drawer--active:not(.drawer--closing) .drawer__link:active {
  padding-left: 18px;
  color: var(--murasaki-700);
  background: rgba(93, 58, 107, 0.16);
  border-bottom-color: transparent;
  box-shadow:
    0 8px 20px rgba(60, 40, 30, 0.14),
    inset 3px 0 0 var(--kin-500);
  transform: translateY(-3px);
  z-index: 1;
}

.drawer--active:not(.drawer--closing) .drawer__platform-back:active {
  transform: translateY(-2px);
  background: #fff;
  border-color: var(--murasaki-400, #a67fb3);
  box-shadow: 0 6px 16px rgba(60, 40, 30, 0.12);
}

.drawer--active:not(.drawer--closing) .drawer__sub:active {
  opacity: 0.72;
  transform: translateX(4px);
}

/* ホバー（背景色＋浮き）。クリック直後は .drawer--closing で無効化 */
.drawer--active:not(.drawer--closing) .drawer__link:hover,
.drawer--active:not(.drawer--closing) .drawer__link:focus-visible {
  padding-left: 18px;
  color: var(--murasaki-700);
  background: rgba(93, 58, 107, 0.14);
  border-bottom-color: transparent;
  box-shadow:
    0 10px 24px rgba(60, 40, 30, 0.16),
    inset 3px 0 0 var(--kin-500);
  transform: translateY(-6px);
  z-index: 1;
}

.drawer--active:not(.drawer--closing) .drawer__platform-back:hover,
.drawer--active:not(.drawer--closing) .drawer__platform-back:focus-visible {
  transform: translateY(-3px);
  background: #fff;
  border-color: var(--murasaki-400, #a67fb3);
  box-shadow: 0 8px 18px rgba(60, 40, 30, 0.12);
}

.drawer--active:not(.drawer--closing) .drawer__sub:hover,
.drawer--active:not(.drawer--closing) .drawer__sub:focus-visible {
  opacity: 0.72;
  transform: translateX(4px);
}

/* 閉じる直後に sticky hover が残っても見た目を元に戻す */
.drawer--closing .drawer__link,
.drawer--closing .drawer__link:hover,
.drawer--closing .drawer__link:active,
.drawer--closing .drawer__link:focus-visible {
  padding-left: clamp(12px, 2.4vh, 18px);
  color: var(--site-text);
  background: transparent;
  border-bottom-color: rgba(60, 40, 30, 0.08);
  box-shadow: none;
  transform: translateY(0) !important;
  transition: none !important;
}

.drawer--closing .drawer__link--active {
  color: var(--murasaki-700);
}

.drawer--closing .drawer__platform-back,
.drawer--closing .drawer__platform-back:hover,
.drawer--closing .drawer__platform-back:active,
.drawer--closing .drawer__sub,
.drawer--closing .drawer__sub:hover,
.drawer--closing .drawer__sub:active {
  transform: none !important;
  box-shadow: none;
  transition: none !important;
}

.drawer-enter-active,
.drawer-leave-active {
  transition: opacity 0.42s ease;
}

.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
}

.drawer-leave-active .drawer__sheet {
  transform: translateY(-2%);
  opacity: 0;
  transition:
    transform 0.38s cubic-bezier(0.55, 0, 0.45, 1),
    opacity 0.32s ease;
}

.drawer-leave-active .drawer__overlay {
  opacity: 0;
  transition: opacity 0.32s ease;
}

.drawer-leave-active .drawer__stagger {
  opacity: 0;
  transform: translateY(10px);
  transition-duration: 0.22s;
  transition-delay: 0s;
}

@media (prefers-reduced-motion: reduce) {
  .drawer__sheet,
  .drawer__overlay,
  .drawer__stagger,
  .drawer__link,
  .drawer__sub,
  .drawer__platform-back {
    transition: none !important;
    animation: none !important;
    transform: none !important;
    opacity: 1 !important;
  }

  .drawer--active:not(.drawer--closing) .drawer__link:hover,
  .drawer--active:not(.drawer--closing) .drawer__link:focus-visible,
  .drawer--active:not(.drawer--closing) .drawer__link:active {
    transform: none !important;
  }
}
</style>
