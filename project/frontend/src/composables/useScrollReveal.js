/**
 * セクションのスクロール reveal（Intersection Observer）
 */
import { onMounted, onUnmounted } from 'vue'

export function useScrollReveal(rootRef, selector = '.site-reveal') {
  let observer = null

  onMounted(() => {
    const root = rootRef?.value ?? document
    const targets = root.querySelectorAll?.(selector) ?? document.querySelectorAll(selector)
    if (!targets.length) return

    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible')
            observer?.unobserve(entry.target)
          }
        })
      },
      { root: null, rootMargin: '0px 0px -8% 0px', threshold: 0.12 },
    )

    targets.forEach((el) => observer.observe(el))
  })

  onUnmounted(() => {
    observer?.disconnect()
  })
}
