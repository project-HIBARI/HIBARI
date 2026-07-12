/**
 * SNS週間投稿回数制限 — 利用状況の取得・表示用（消費はサーバー側の投稿APIが行う）
 */
import { ref, computed } from 'vue'
import { useAuth } from './useAuth.js'
import { fetchSnsUsage } from '../api/sns.js'

const usageStatus = ref(null)
const usageLoading = ref(false)
let refreshScheduled = false

async function refreshSnsUsageStatus() {
  if (refreshScheduled) return
  refreshScheduled = true
  usageLoading.value = true
  try {
    usageStatus.value = await fetchSnsUsage()
  } catch {
    usageStatus.value = null
  } finally {
    usageLoading.value = false
    refreshScheduled = false
  }
}

export function useSnsUsage() {
  const { isLoggedIn, membership } = useAuth()

  const limit = computed(() => usageStatus.value?.limit ?? null)
  const used = computed(() => usageStatus.value?.used ?? 0)
  const remaining = computed(() => usageStatus.value?.remaining ?? null)
  const isUnlimited = computed(() => usageStatus.value != null && usageStatus.value.limit === null)
  const canPostNow = computed(() => usageStatus.value?.can_post ?? true)
  const nextResetLabel = computed(() => usageStatus.value?.next_reset_label ?? '')

  const remainingMessage = computed(() => {
    if (!isLoggedIn.value) return ''
    if (usageStatus.value == null) return '利用状況を確認しています…'
    if (isUnlimited.value) return '今週は無制限に投稿できます'
    if (remaining.value > 0) return `今週はあと${remaining.value}回投稿できます`
    return '今週の投稿可能回数に達しました'
  })

  const upgradeMessage = computed(() => {
    if (membership.value === 'general') {
      return 'プレミアム会員なら投稿回数が無制限になります。'
    }
    return '月額500円会員なら週5回、プレミアム会員なら無制限で投稿できます。'
  })

  return {
    usageStatus,
    loading: usageLoading,
    limit,
    used,
    remaining,
    isUnlimited,
    canPostNow,
    nextResetLabel,
    remainingMessage,
    upgradeMessage,
    refreshUsage: refreshSnsUsageStatus,
  }
}
