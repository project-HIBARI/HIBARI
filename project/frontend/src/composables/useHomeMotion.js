/**
 * ホーム画面専用 — IntersectionObserver + script 段階表示
 */
import { nextTick, onMounted, onUnmounted } from 'vue'
import { prefersReducedMotion, whenSiteReady } from './useSiteReady.js'

const SECTION_SELECTOR = '.home-motion-section'
const STAGGER_SELECTOR = '.home-motion-stagger'
const ALL_SELECTORS = `${SECTION_SELECTOR}, ${STAGGER_SELECTOR}`

const STAGGER_STEP_MS = 140

function isInViewport(el, marginRatio = 0.06) {
  const rect = el.getBoundingClientRect()
  const margin = window.innerHeight * marginRatio
  return rect.top < window.innerHeight - margin && rect.bottom > margin
}

export function useHomeMotion(rootRef) {
  let observer = null
  let cleanupReady = null
  let mutationObserver = null
  const staggerTimers = []

  function clearStaggerTimers() {
    staggerTimers.forEach(clearTimeout)
    staggerTimers.length = 0
  }

  function revealStaggerChildren(container) {
    const items = container.querySelectorAll(':scope > .home-motion-stagger__item, :scope > .home-motion-stagger-item, :scope > *')
    if (!items.length) return

    if (prefersReducedMotion()) {
      items.forEach((item) => item.classList.add('is-stagger-visible'))
      return
    }

    items.forEach((item, index) => {
      const delay = index * STAGGER_STEP_MS
      if (delay === 0) {
        item.classList.add('is-stagger-visible')
        return
      }
      const timer = window.setTimeout(() => {
        item.classList.add('is-stagger-visible')
      }, delay)
      staggerTimers.push(timer)
    })
  }

  function revealElement(el) {
    if (!el || el.classList.contains('is-visible')) return
    el.classList.add('is-visible')
    observer?.unobserve(el)

    if (el.classList.contains('home-motion-stagger')) {
      requestAnimationFrame(() => revealStaggerChildren(el))
    }
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
        rootMargin: '0px 0px -4% 0px',
        threshold: [0, 0.06, 0.12],
      },
    )

    scanTargets()
    requestAnimationFrame(scanTargets)
    window.setTimeout(scanTargets, 120)
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
    clearStaggerTimers()
  })
}
