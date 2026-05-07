import { watch, onUnmounted } from 'vue'

/**
 * モバイルドロワー等で背面スクロールを止める
 * @param {import('vue').Ref<boolean>} lockedRef true の間だけ body を固定
 */
export function useBodyScrollLock(lockedRef) {
  watch(
    lockedRef,
    (v) => {
      document.body.style.overflow = v ? 'hidden' : ''
    },
    { immediate: true },
  )
  onUnmounted(() => {
    document.body.style.overflow = ''
  })
}
