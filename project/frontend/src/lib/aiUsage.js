/**
 * AIひばり対話の月間利用回数（デモ: localStorage）
 */
function monthKey() {
  const now = new Date()
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
}

function storageKey(accountId) {
  return `hibari-ai-usage-${accountId || 'guest'}-${monthKey()}`
}

export function getAiUsageCount(accountId) {
  if (typeof window === 'undefined') return 0
  try {
    return Number(localStorage.getItem(storageKey(accountId)) || 0)
  } catch {
    return 0
  }
}

export function incrementAiUsage(accountId) {
  const next = getAiUsageCount(accountId) + 1
  try {
    localStorage.setItem(storageKey(accountId), String(next))
  } catch {
    /* ignore */
  }
  return next
}
