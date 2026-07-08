/**
 * API クライアント（Flask セッション Cookie 用に credentials を付与）
 */
export async function apiRequest(path, options = {}) {
  const response = await fetch(path, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  })

  let data = null
  const contentType = response.headers.get('content-type') || ''
  if (contentType.includes('application/json')) {
    data = await response.json()
  }

  if (!response.ok) {
    const message = data?.error || `リクエストに失敗しました（${response.status}）`
    const error = new Error(message)
    error.status = response.status
    error.data = data
    throw error
  }

  return data
}
