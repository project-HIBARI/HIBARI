/**
 * ホーム画面専用 — IntersectionObserver によるセクション reveal
 */
import { nextTick, onMounted, onUnmounted } from 'vue'
import { whenSiteReady } from './useSiteReady.js'

const SECTION_SELECTOR = '.home-motion-section'
const STAGGER_SELECTOR = '.home-motion-stagger'
const ALL_SELECTORS = `${SECTION_SELECTOR}, ${STAGGER_SELECTOR}`

function isInViewport(el, marginRatio = 0.06) {
  const rect = el.getBoundingClientRect()
  const margin = window.innerHeight * marginRatio
  return rect.top < window.innerHeight - margin && rect.bottom > margin
}

export function useHomeMotion(rootRef) {
  let observer = null
  let cleanupReady = null
  let mutationObserver = null

  function revealElement(el) {
    if (!el || el.classList.contains('is-visible')) return
    el.classList.add('is-visible')
    observer?.unobserve(el)
  }

  function scanTargets() {
    const root = rootRef?.value
    if (!root) return
    const targets = root.querySelectorAll(ALL_SELECTORS)
    targets.forEach((el) => {
      if (el.classList.contains('is-visible')) return
      if (isInViewport(el)) {
        revealElement(el)
      } else {
        observer?.observe(el)
      }
    })
  }

  function bootstrap() {
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            revealElement(entry.target)
          }
        })
      },
      {
        root: null,
        rootMargin: '0px 0px -5% 0px',
        threshold: [0, 0.08, 0.15],
      },
    )

    scanTargets()
    requestAnimationFrame(scanTargets)
  }

  onMounted(() => {
    nextTick(() => {
      cleanupReady = whenSiteReady(() => {
        bootstrap()

        mutationObserver = new MutationObserver(() => {
          requestAnimationFrame(scanTargets)
        })
        if (rootRef.value) {
          mutationObserver.observe(rootRef.value, { childList: true, subtree: true })
        }
      })
    })
  })

  onUnmounted(() => {
    cleanupReady?.()
    mutationObserver?.disconnect()
    observer?.disconnect()
    observer = null
  })
}
