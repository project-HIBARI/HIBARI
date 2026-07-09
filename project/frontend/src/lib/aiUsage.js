/**
 * AIひばり対話 — 利用回数（バックエンド API + セッション Cookie）
 */
import { consumeUsage, fetchUsage } from '../api/usage.js'

const FEATURE = 'ai-chat'

let statusRef = null

export function bindAiUsageRef(ref) {
  statusRef = ref
}

export async function refreshAiUsageStatus() {
  const status = await fetchUsage(FEATURE)
  if (statusRef) statusRef.value = status
  return status
}

export async function consumeAiUsage() {
  try {
    const status = await consumeUsage(FEATURE)
    if (statusRef) statusRef.value = status
    return status
  } catch (err) {
    if (err.status === 429 && err.data) {
      if (statusRef) statusRef.value = err.data
    }
    throw err
  }
}
