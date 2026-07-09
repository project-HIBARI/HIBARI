/**
 * セクションのスクロール reveal（Intersection Observer）
 * イントロ完了（.site-shell--ready）後に監視を開始し、表示域に入った要素へ is-visible を付与する
 */
import { nextTick, onMounted, onUnmounted } from 'vue'
import { whenSiteReady } from './useSiteReady.js'

const REVEAL_SELECTOR = [
  '.motion-section',
  '.site-reveal',
  '.motion-stagger',
  '.site-reveal-stagger',
].join(',')

function isInViewport(el, bottomMarginRatio = 0.04) {
  const rect = el.getBoundingClientRect()
  const bottomMargin = window.innerHeight * bottomMarginRatio
  return rect.top < window.innerHeight - bottomMargin && rect.bottom > bottomMargin
}

export function useScrollReveal(rootRef, selector = REVEAL_SELECTOR) {
  let observer = null
  let cleanupReady = null

  function observeTargets() {
    const root = rootRef?.value
    const scope = root ?? document
    const targets = scope.querySelectorAll?.(selector) ?? document.querySelectorAll(selector)
    if (!targets.length) return

    targets.forEach((el) => {
      if (el.classList.contains('is-visible')) return

      if (isInViewport(el)) {
        el.classList.add('is-visible')
        return
      }

      observer?.observe(el)
    })
  }

  function bootstrap() {
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
        rootMargin: '0px 0px -2% 0px',
        threshold: 0.05,
      },
    )

    observeTargets()
    requestAnimationFrame(observeTargets)
  }

  onMounted(() => {
    nextTick(() => {
      cleanupReady = whenSiteReady(bootstrap)
    })
  })

  onUnmounted(() => {
    cleanupReady?.()
    observer?.disconnect()
    observer = null
  })
}

