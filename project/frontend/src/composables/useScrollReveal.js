/**
 * セクションのスクロール reveal（Intersection Observer）
 * DOM 描画後に監視を開始し、表示域に入った要素へ is-visible を付与する
 */
import { nextTick, onMounted, onUnmounted } from 'vue'

const REVEAL_SELECTOR = [
  '.motion-section',
  '.site-reveal',
  '.motion-stagger',
  '.site-reveal-stagger',
].join(',')

export function useScrollReveal(rootRef, selector = REVEAL_SELECTOR) {
  let observer = null

  function observeTargets() {
    const root = rootRef?.value
    const scope = root ?? document
    const targets = scope.querySelectorAll?.(selector) ?? document.querySelectorAll(selector)
    if (!targets.length || !observer) return

    targets.forEach((el) => {
      if (!el.classList.contains('is-visible')) {
        observer.observe(el)
      }
    })
  }

  onMounted(() => {
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible')
            observer?.unobserve(entry.target)
          }
        })
      },
      {
        root: null,
        rootMargin: '0px 0px -4% 0px',
        threshold: 0.08,
      },
    )

    nextTick(() => {
      observeTargets()
      // 子コンポーネントの描画待ち（1フレーム）
      requestAnimationFrame(observeTargets)
    })
  })

  onUnmounted(() => {
    observer?.disconnect()
    observer = null
  })
}
