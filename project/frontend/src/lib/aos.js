/**
 * AOS（Animate On Scroll）— 初期化・属性ヘルパー
 */
import AOS from 'aos'
import { prefersReducedMotion } from '../composables/useSiteReady.js'

export const AOS_DURATION = 800
export const AOS_DELAY_STEP = 80

/** motion-page-enter（0.65s）完了後に再計算する余裕 */
const PAGE_ENTER_ANIM_MS = 700

let initialized = false
/** @type {ReturnType<typeof setTimeout>[]} */
let refreshTimers = []

function clearAosRefreshTimers() {
  refreshTimers.forEach((id) => clearTimeout(id))
  refreshTimers = []
}

/** @param {number} [delay] */
export function aosAttrs(delay = 0) {
  return {
    'data-aos': 'fade-up',
    'data-aos-duration': String(AOS_DURATION),
    'data-aos-once': 'true',
    ...(delay > 0 ? { 'data-aos-delay': String(delay) } : {}),
  }
}

export function initAos() {
  if (initialized) return
  AOS.init({
    duration: AOS_DURATION,
    once: true,
    easing: 'ease-out-cubic',
    offset: 48,
    disable: () => prefersReducedMotion(),
    debounceDelay: 50,
    throttleDelay: 99,
    mirror: false,
  })
  initialized = true
}

export function refreshAos() {
  if (!initialized) {
    initAos()
  }
  AOS.refresh()
}

export function refreshAosHard() {
  if (!initialized) {
    initAos()
  }
  AOS.refreshHard()
}

/**
 * SPA ページ遷移後に AOS を確実に再計算する。
 * 子コンポーネントのマウントと site-page-enter アニメ完了を待つ。
 */
export function scheduleAosRefresh() {
  if (typeof window === 'undefined' || prefersReducedMotion()) return

  clearAosRefreshTimers()

  const run = () => refreshAosHard()

  requestAnimationFrame(run)
  refreshTimers = [
    window.setTimeout(run, 80),
    window.setTimeout(run, 250),
    window.setTimeout(run, PAGE_ENTER_ANIM_MS),
    window.setTimeout(run, PAGE_ENTER_ANIM_MS + 350),
  ]
}

export function destroyAosScheduling() {
  clearAosRefreshTimers()
}
