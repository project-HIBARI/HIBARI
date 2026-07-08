/**
 * 掲示板投稿 — 利用回数・権限チェック
 */
import { computed, ref } from 'vue'
import { useMemberAccess } from './useMemberAccess.js'
import { GENERAL_BOARD_POST_MONTHLY_LIMIT, PERMISSION } from '../constants/membership.js'
import { getBoardUsageCount, incrementBoardUsage } from '../lib/boardUsage.js'

export function useBoardPost() {
  const { canUse, isLoggedIn, isPremium, user } = useMemberAccess()
  const usageTick = ref(0)

  const usageCount = computed(() => {
    usageTick.value
    return getBoardUsageCount(user.value?.account_id)
  })

  const isUnlimited = computed(() => isPremium.value && canUse(PERMISSION.BOARD_POST_UNLIMITED))

  const remainingPosts = computed(() => {
    if (!isLoggedIn.value) return 0
    if (isUnlimited.value) return null
    return Math.max(GENERAL_BOARD_POST_MONTHLY_LIMIT - usageCount.value, 0)
  })

  const canPostNow = computed(() => {
    if (!isLoggedIn.value || !canUse(PERMISSION.BOARD_POST)) return false
    if (isUnlimited.value) return true
    return usageCount.value < GENERAL_BOARD_POST_MONTHLY_LIMIT
  })

  const limitMessage = computed(() => {
    if (!isLoggedIn.value) return '掲示板投稿は会員登録・ログイン後にご利用いただけます。'
    if (isUnlimited.value) return 'プレミアム会員: 掲示板投稿 無制限'
    return `一般会員: 今月あと ${remainingPosts.value} 回（月${GENERAL_BOARD_POST_MONTHLY_LIMIT}回まで）`
  })

  function recordPost() {
    if (!isUnlimited.value && user.value?.account_id) {
      incrementBoardUsage(user.value.account_id)
      usageTick.value += 1
    }
  }

  return {
    canUse,
    isLoggedIn,
    isPremium,
    isUnlimited,
    remainingPosts,
    canPostNow,
    limitMessage,
    usageCount,
    recordPost,
    PERMISSION,
  }
}
