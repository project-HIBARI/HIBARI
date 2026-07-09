/**
 * 掲示板投稿 — 利用回数（バックエンド API + セッション Cookie）
 */
import { fetchUsage } from '../api/usage.js'

const FEATURE = 'board-post'

let statusRef = null

export function bindBoardUsageRef(ref) {
  statusRef = ref
}

export async function refreshBoardUsageStatus() {
  const status = await fetchUsage(FEATURE)
  if (statusRef) statusRef.value = status
  return status
}
