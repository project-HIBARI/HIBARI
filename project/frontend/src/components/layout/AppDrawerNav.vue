<script setup>
/**
 * 部品名: スマホ用フルスクリーンナビ（HAERA風）
 * 役割: 全画面オーバーレイ・段階表示・ハンバーガー連動
 */
import { ref, watch, nextTick } from 'vue'
import UiButton from '../ui/UiButton.vue'
import TextSizeControl from '../ui/TextSizeControl.vue'
import HeaderSearch from './HeaderSearch.vue'

const props = defineProps({
  open: { type: Boolean, default: false },
  items: { type: Array, required: true },
  page: { type: String, required: true },
  isLoggedIn: { type: Boolean, default: false },
  userName: { type: String, default: '' },
  showPlatformBack: { type: Boolean, default: false },
  authOnPlatformOnly: { type: Boolean, default: false },
})

const emit = defineEmits(['close', 'navigate', 'open-modal', 'open-auth', 'exit-platform'])

const panelActive = ref(false)

watch(
  () => props.open,
  async (open) => {
    if (open) {
      await nextTick()
      requestAnimationFrame(() => {
        panelActive.value = true
      })
    } else {
      panelActive.value = false
    }
  },
)
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
        :class="{ 'drawer--active': panelActive }"
      >
        <div class="drawer__overlay" aria-hidden="true" @click="emit('close')" />

        <div class="drawer__sheet">
          <p class="drawer__label drawer__stagger" :style="{ '--drawer-i': 0 }">Menu</p>

          <button
            v-if="showPlatformBack"
            type="button"
            class="drawer__platform-back drawer__stagger"
            :style="{ '--drawer-i': 0.5 }"
            @click="emit('exit-platform'); emit('close')"
          >
            ← Music Memories へ戻る
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
              @click="emit('navigate', n.id)"
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
                <UiButton variant="outline" size="md" @click="emit('open-account'); emit('close')">
                  アカウント設定
                </UiButton>
                <UiButton variant="ghost" size="md" @click="emit('logout'); emit('close')">ログアウト</UiButton>
              </div>
            </div>
            <div v-else-if="!authOnPlatformOnly" class="drawer__auth drawer__stagger" :style="{ '--drawer-i': items.length + 2 }">
              <UiButton variant="outline" size="md" @click="emit('open-auth', 'login')">ログイン</UiButton>
              <UiButton variant="primary" size="md" @click="emit('open-auth', 'register')">ファンクラブ加入</UiButton>
            </div>

            <div class="drawer__search drawer__stagger" :style="{ '--drawer-i': items.length + 3 }">
              <HeaderSearch @navigate="(p) => { emit('navigate', p); emit('close') }" />
            </div>

            <div class="drawer__text-size drawer__stagger" :style="{ '--drawer-i': items.length + 4 }">
              <TextSizeControl tone="ink" variant="default" />
            </div>

            <div class="drawer__sub-links">
              <button
                type="button"
                class="drawer__sub drawer__stagger"
                :style="{ '--drawer-i': items.length + 5 }"
                @click="emit('open-modal', 'fanclub')"
              >
                ファンクラブ
              </button>
              <button
                type="button"
                class="drawer__sub drawer__stagger"
                :style="{ '--drawer-i': items.length + 6 }"
                @click="emit('open-modal', 'ai')"
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
  transition: opacity 0.5s ease;
}

.drawer--active .drawer__overlay {
  opacity: 1;
}

.drawer__sheet {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  padding: clamp(88px, 18vh, 120px) clamp(24px, 7vw, 64px) clamp(32px, 6vh, 48px);
  background: linear-gradient(165deg, #fffefb 0%, #f8f3ec 48%, #f3ebe3 100%);
  overflow-y: auto;
  overscroll-behavior: contain;
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
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: var(--site-text-muted);
}

.drawer__platform-back {
  align-self: flex-start;
  margin: -12px 0 clamp(16px, 3vh, 24px);
  padding: 8px 14px;
  border: 1px solid var(--site-border);
  border-radius: 999px;
  background: var(--site-surface);
  color: var(--murasaki-700);
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  letter-spacing: 0.06em;
  cursor: pointer;
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
  margin: 0;
  padding: clamp(14px, 2.8vh, 20px) 0;
  border: 0;
  border-bottom: 1px solid rgba(60, 40, 30, 0.08);
  background: transparent;
  text-align: left;
  cursor: pointer;
  color: var(--site-text);
  transition: color 0.25s ease, padding-left 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}

.drawer__link:hover {
  padding-left: 8px;
  color: var(--murasaki-700);
}

.drawer__link-text {
  font-family: var(--ff-mincho);
  font-size: clamp(22px, 5.2vw, 30px);
  font-weight: 600;
  letter-spacing: 0.12em;
  line-height: 1.35;
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
  font-size: 15px;
  letter-spacing: 0.08em;
  color: var(--murasaki-700);
}

.drawer__user-note {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
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
  cursor: pointer;
  font-family: var(--ff-mincho);
  font-size: 13px;
  letter-spacing: 0.1em;
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.drawer__sub:hover {
  opacity: 0.72;
  transform: translateX(4px);
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
  .drawer__sub {
    transition: none !important;
    animation: none !important;
    transform: none !important;
    opacity: 1 !important;
  }
}
</style>
