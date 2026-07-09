/**
 * 掲示板投稿 — 利用回数（バックエンド API + セッション Cookie）
 * モジュール共有 state で複数コンポーネント間の不整合を防ぐ
 */
import { ref } from 'vue'
import { fetchUsage } from '../api/usage.js'

const FEATURE = 'board-post'

export const boardUsageStatus = ref(null)
export const boardUsageLoading = ref(false)

export async function refreshBoardUsageStatus() {
  boardUsageLoading.value = true
  try {
    const status = await fetchUsage(FEATURE)
    boardUsageStatus.value = status
    return status
  } catch (err) {
    boardUsageStatus.value = null
    throw err
  } finally {
    boardUsageLoading.value = false
  }
}
