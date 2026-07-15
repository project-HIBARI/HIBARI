<script setup>
/**
 * 部品名: Music Memories スマホ用フルスクリーンナビ
 * 役割: ファンクラブサイトの AppDrawerNav と同様の全画面オーバーレイナビ
 */
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
  open: { type: Boolean, default: false },
  items: { type: Array, required: true },
  page: { type: String, required: true },
})

const emit = defineEmits(['close', 'navigate'])

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
    <Transition name="mm-drawer">
      <div
        v-if="open"
        role="dialog"
        aria-modal="true"
        aria-label="ナビゲーション"
        class="mm-drawer"
        :class="{ 'mm-drawer--active': panelActive }"
      >
        <div class="mm-drawer__overlay" aria-hidden="true" @click="emit('close')" />

        <div class="mm-drawer__sheet">
          <p class="mm-drawer__label mm-drawer__stagger" :style="{ '--drawer-i': 0 }">Menu</p>

          <nav class="mm-drawer__nav" aria-label="モバイルナビゲーション">
            <button
              v-for="(n, index) in items"
              :key="n.id"
              type="button"
              class="mm-drawer__link mm-drawer__stagger"
              :class="{ 'mm-drawer__link--active': page === n.id }"
              :style="{ '--drawer-i': index + 1 }"
              :aria-current="page === n.id ? 'page' : undefined"
              @click="emit('navigate', n.id)"
            >
              <span class="mm-drawer__link-text">{{ n.label }}</span>
              <span v-if="page === n.id" class="mm-drawer__link-mark" aria-hidden="true" />
            </button>
          </nav>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.mm-drawer {
  position: fixed;
  inset: 0;
  z-index: 200;
  pointer-events: auto;
}

.mm-drawer__overlay {
  position: absolute;
  inset: 0;
  background: rgba(12, 8, 14, 0.55);
  backdrop-filter: blur(4px);
  opacity: 0;
  transition: opacity 0.5s ease;
}

.mm-drawer--active .mm-drawer__overlay {
  opacity: 1;
}

.mm-drawer__sheet {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  padding: clamp(88px, 18vh, 120px) clamp(24px, 7vw, 64px) clamp(32px, 6vh, 48px);
  background: linear-gradient(165deg, #1c131f 0%, #160f18 48%, #120c14 100%);
  overflow-y: auto;
  overscroll-behavior: contain;
  transform: translateY(-3%);
  opacity: 0;
  transition:
    transform 0.62s cubic-bezier(0.22, 1, 0.36, 1),
    opacity 0.5s ease;
}

.mm-drawer--active .mm-drawer__sheet {
  transform: translateY(0);
  opacity: 1;
}

.mm-drawer__label {
  margin: 0 0 clamp(20px, 4vh, 36px);
  font-family: var(--ff-latin, var(--ff-sans-jp));
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: #c8a96b;
  opacity: 1;
}

.mm-drawer__nav {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-bottom: clamp(24px, 5vh, 40px);
}

.mm-drawer__link {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  min-height: 56px;
  margin: 0;
  padding: clamp(14px, 2.8vh, 20px) 0;
  border: 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.14);
  background: transparent;
  text-align: left;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.92);
  opacity: 1;
  transition:
    color 0.2s ease,
    background-color 0.2s ease,
    padding-left 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}

.mm-drawer__link:hover,
.mm-drawer__link:focus-visible {
  padding-left: 8px;
  color: #ffffff;
  background: rgba(255, 255, 255, 0.06);
}

.mm-drawer__link:focus-visible {
  outline: 2px solid #c8a96b;
  outline-offset: -2px;
}

.mm-drawer__link-text {
  font-family: var(--ff-sans-jp);
  font-size: clamp(20px, 5vw, 28px);
  font-weight: 600;
  letter-spacing: 0.08em;
  line-height: 1.35;
  opacity: 1;
}

.mm-drawer__link-mark {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #e0bd75;
  flex-shrink: 0;
}

.mm-drawer__link--active {
  color: #e0bd75;
}

.mm-drawer__stagger {
  opacity: 0;
  transform: translateY(18px);
  transition:
    opacity 0.55s cubic-bezier(0.22, 1, 0.36, 1),
    transform 0.55s cubic-bezier(0.22, 1, 0.36, 1);
  transition-delay: calc(0.06s + var(--drawer-i, 0) * 0.055s);
}

.mm-drawer--active .mm-drawer__stagger {
  opacity: 1;
  transform: translateY(0);
}

.mm-drawer-enter-active,
.mm-drawer-leave-active {
  transition: opacity 0.42s ease;
}

.mm-drawer-enter-from,
.mm-drawer-leave-to {
  opacity: 0;
}

.mm-drawer-leave-active .mm-drawer__sheet {
  transform: translateY(-2%);
  opacity: 0;
  transition:
    transform 0.38s cubic-bezier(0.55, 0, 0.45, 1),
    opacity 0.32s ease;
}

.mm-drawer-leave-active .mm-drawer__overlay {
  opacity: 0;
  transition: opacity 0.32s ease;
}

.mm-drawer-leave-active .mm-drawer__stagger {
  opacity: 0;
  transform: translateY(10px);
  transition-duration: 0.22s;
  transition-delay: 0s;
}

@media (prefers-reduced-motion: reduce) {
  .mm-drawer__sheet,
  .mm-drawer__overlay,
  .mm-drawer__stagger,
  .mm-drawer__link {
    transition: none !important;
    animation: none !important;
    transform: none !important;
    opacity: 1 !important;
  }
}
</style>
