/**
 * 数値のカウントアップアニメーション
 */
import { ref, watch, onUnmounted } from 'vue'

export function useCountUp(target, options = {}) {
  const { duration = 1800, start = 0 } = options
  const display = ref(start)
  let raf = null

  function animate(to) {
    if (raf) cancelAnimationFrame(raf)
    const from = display.value
    const diff = to - from
    if (diff === 0) return

    const t0 = performance.now()
    function tick(now) {
      const p = Math.min((now - t0) / duration, 1)
      const eased = 1 - (1 - p) ** 3
      display.value = Math.round(from + diff * eased)
      if (p < 1) raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
  }

  watch(
    () => (typeof target === 'function' ? target() : target?.value ?? target),
    (val) => {
      if (typeof val === 'number' && val >= 0) animate(val)
    },
    { immediate: true },
  )

  onUnmounted(() => {
    if (raf) cancelAnimationFrame(raf)
  })

  return display
}
