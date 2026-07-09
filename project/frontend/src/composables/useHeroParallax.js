/**
 * ホームヒーロー — スクロール / マウス連動パララックス
 */
import { computed, onBeforeUnmount, onMounted, ref, shallowRef } from 'vue'
import { prefersReducedMotion, whenSiteReady } from './useSiteReady.js'

export function useHeroParallax(heroRef) {
  const reduced = prefersReducedMotion()
  const scrollProgress = ref(0)
  const mouseX = ref(0.5)
  const mouseY = ref(0.5)
  const heroActive = ref(false)

  let targetMouseX = 0.5
  let targetMouseY = 0.5
  let currentMouseX = 0.5
  let currentMouseY = 0.5
  let scrollTicking = false
  let mouseRafId = null
  let cleanupReady = null

  function applyVars() {
    const el = heroRef.value
    if (!el) return
    const bgScale = 1.04 + scrollProgress.value * 0.05
    const overlayOpacity = 0.68 + scrollProgress.value * 0.22
    el.style.setProperty('--hero-scroll-progress', scrollProgress.value.toFixed(4))
    el.style.setProperty('--hero-mouse-x', mouseX.value.toFixed(4))
    el.style.setProperty('--hero-mouse-y', mouseY.value.toFixed(4))
    el.style.setProperty('--hero-bg-scale', bgScale.toFixed(4))
    el.style.setProperty('--hero-overlay-opacity', overlayOpacity.toFixed(4))
  }

  function updateScroll() {
    scrollTicking = false
    const el = heroRef.value
    if (!el) return
    const rect = el.getBoundingClientRect()
    const height = Math.max(rect.height, 1)
    const progress = Math.min(1, Math.max(0, -rect.top / height))
    scrollProgress.value = progress
    applyVars()
  }

  function onScroll() {
    if (scrollTicking) return
    scrollTicking = true
    requestAnimationFrame(updateScroll)
  }

  function tickMouse() {
    const ease = reduced ? 1 : 0.07
    currentMouseX += (targetMouseX - currentMouseX) * ease
    currentMouseY += (targetMouseY - currentMouseY) * ease
    mouseX.value = currentMouseX
    mouseY.value = currentMouseY
    applyVars()
    mouseRafId = requestAnimationFrame(tickMouse)
  }

  function onMouseMove(event) {
    if (reduced) return
    const el = heroRef.value
    if (!el) return
    const rect = el.getBoundingClientRect()
    if (!rect.width || !rect.height) return
    targetMouseX = Math.min(1, Math.max(0, (event.clientX - rect.left) / rect.width))
    targetMouseY = Math.min(1, Math.max(0, (event.clientY - rect.top) / rect.height))
  }

  function onMouseLeave() {
    targetMouseX = 0.5
    targetMouseY = 0.42
  }

  function startMotion() {
    heroActive.value = true
    applyVars()
    updateScroll()
    if (!reduced) {
      mouseRafId = requestAnimationFrame(tickMouse)
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    window.addEventListener('mousemove', onMouseMove, { passive: true })
    heroRef.value?.addEventListener('mouseleave', onMouseLeave)
  }

  function stopMotion() {
    window.removeEventListener('scroll', onScroll)
    window.removeEventListener('mousemove', onMouseMove)
    heroRef.value?.removeEventListener('mouseleave', onMouseLeave)
    if (mouseRafId != null) {
      cancelAnimationFrame(mouseRafId)
      mouseRafId = null
    }
  }

  const heroStyle = computed(() => ({
    '--hero-scroll-progress': scrollProgress.value,
    '--hero-mouse-x': mouseX.value,
    '--hero-mouse-y': mouseY.value,
    '--hero-bg-scale': 1.04 + scrollProgress.value * 0.05,
    '--hero-overlay-opacity': 0.68 + scrollProgress.value * 0.22,
  }))

  onMounted(() => {
    cleanupReady = whenSiteReady(() => {
      requestAnimationFrame(startMotion)
    })
  })

  onBeforeUnmount(() => {
    cleanupReady?.()
    stopMotion()
  })

  return {
    heroStyle,
    heroActive,
    scrollProgress,
    reduced: shallowRef(reduced),
  }
}
