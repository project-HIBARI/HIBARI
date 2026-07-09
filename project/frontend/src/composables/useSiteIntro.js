/**
 * サイト起動時のイントロビデオ表示制御
 *
 * INTRO_EVERY_VISIT = true  … サイトを開くたびに表示（現在の既定）
 * INTRO_EVERY_VISIT = false … sessionStorage で同一セッション1回のみ
 */
import { ref, onMounted } from 'vue'

const INTRO_SESSION_KEY = 'hibari-site-intro-seen'

/** @type {boolean} 毎回表示する場合は true */
export const INTRO_EVERY_VISIT = true

export function useSiteIntro() {
  const introVisible = ref(false)
  const introLeaving = ref(false)

  onMounted(() => {
    if (!INTRO_EVERY_VISIT && sessionStorage.getItem(INTRO_SESSION_KEY)) {
      return
    }
    introVisible.value = true
    document.body.classList.add('site-intro-active')
  })

  function completeIntro() {
    if (introLeaving.value) return
    introLeaving.value = true
    window.setTimeout(() => {
      introVisible.value = false
      introLeaving.value = false
      document.body.classList.remove('site-intro-active')
      if (!INTRO_EVERY_VISIT) {
        sessionStorage.setItem(INTRO_SESSION_KEY, '1')
      }
    }, 680)
  }

  return {
    introVisible,
    introLeaving,
    completeIntro,
  }
}
