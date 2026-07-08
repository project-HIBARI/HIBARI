/**
 * Flask API 向け fetch ラッパー（セッション Cookie 用に credentials を付与）
 */

export class ApiError extends Error {
  constructor(message, status = 0) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

/**
 * @param {string} path
 * @param {RequestInit} [options]
 */
export async function apiFetch(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  let response
  try {
    response = await fetch(path, {
      ...options,
      headers,
      credentials: 'include',
    })
  } catch {
    throw new ApiError('サーバーとの通信に失敗しました')
  }

  let data = null
  const text = await response.text()
  if (text) {
    try {
      data = JSON.parse(text)
    } catch {
      data = null
    }
  }

  if (!response.ok) {
    throw new ApiError(data?.error || 'サーバーとの通信に失敗しました', response.status)
  }

  return data
}
