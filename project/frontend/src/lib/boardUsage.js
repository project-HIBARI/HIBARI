/**
 * 掲示板投稿の月間利用回数（localStorage）
 */
function monthKey() {
  const now = new Date()
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
}

function storageKey(accountId) {
  return `hibari-board-usage-${accountId || 'guest'}-${monthKey()}`
}

export function getBoardUsageCount(accountId) {
  if (typeof window === 'undefined') return 0
  try {
    return Number(localStorage.getItem(storageKey(accountId)) || 0)
  } catch {
    return 0
  }
}

export function incrementBoardUsage(accountId) {
  const next = getBoardUsageCount(accountId) + 1
  try {
    localStorage.setItem(storageKey(accountId), String(next))
  } catch {
    /* ignore */
  }
  return next
}
