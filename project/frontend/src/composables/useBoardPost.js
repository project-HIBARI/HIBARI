/**
 * 掲示板投稿 — 利用回数・権限チェック（API 連携）
 */
import { computed, onMounted, ref } from 'vue'
import { useMemberAccess } from './useMemberAccess.js'
import { GENERAL_BOARD_POST_MONTHLY_LIMIT, PERMISSION } from '../constants/membership.js'
import { bindBoardUsageRef, refreshBoardUsageStatus } from '../lib/boardUsage.js'

export function useBoardPost() {
  const { canUse, isLoggedIn, isPremium } = useMemberAccess()
  const usageStatus = ref(null)
  const loading = ref(false)

  bindBoardUsageRef(usageStatus)

  const isGuest = computed(() => usageStatus.value?.is_guest ?? !isLoggedIn.value)

  const isUnlimited = computed(
    () => usageStatus.value?.limit == null && isLoggedIn.value && isPremium.value,
  )

  const postLimit = computed(() => usageStatus.value?.limit ?? GENERAL_BOARD_POST_MONTHLY_LIMIT)

  const remainingPosts = computed(() => {
    if (usageStatus.value?.remaining != null) return usageStatus.value.remaining
    if (isUnlimited.value) return null
    return postLimit.value
  })

  const canPostNow = computed(() => {
    if (usageStatus.value != null) return Boolean(usageStatus.value.can_use)
    if (isLoggedIn.value && !canUse(PERMISSION.BOARD_POST)) return false
    return false
  })

  const guestResetLabel = computed(() => usageStatus.value?.reset_label ?? '')

  const limitMessage = computed(() => {
    if (usageStatus.value?.is_guest) {
      if (canPostNow.value) {
        return `非会員: あと ${remainingPosts.value} 回投稿できます（10回まで・上限到達後1週間で解除）`
      }
      return `非会員: 投稿上限に達しました。${guestResetLabel.value} に解除されます。`
    }
    if (isLoggedIn.value && !canUse(PERMISSION.BOARD_POST)) {
      return '掲示板投稿は会員登録・ログイン後にご利用いただけます。'
    }
    if (usageStatus.value?.limit == null) return 'プレミアム会員: 掲示板投稿 無制限'
    if (canPostNow.value) {
      return `一般会員: 今月あと ${remainingPosts.value} 回（月${GENERAL_BOARD_POST_MONTHLY_LIMIT}回まで）`
    }
    return `一般会員: 今月の投稿上限（${GENERAL_BOARD_POST_MONTHLY_LIMIT}回）に達しました。`
  })

  async function refreshUsage() {
    loading.value = true
    try {
      await refreshBoardUsageStatus()
    } finally {
      loading.value = false
    }
  }

  async function recordPost() {
    await refreshUsage()
  }

  onMounted(() => {
    refreshUsage()
  })

  return {
    canUse,
    isLoggedIn,
    isGuest,
    isPremium,
    isUnlimited,
    remainingPosts,
    canPostNow,
    limitMessage,
    guestResetLabel,
    usageStatus,
    loading,
    refreshUsage,
    recordPost,
    PERMISSION,
  }
}
