/**
 * API クライアント（Flask セッション Cookie 用に credentials を付与）
 */

function connectionError(message) {
  const error = new Error(message)
  error.status = 0
  return error
}

function isBackendUnavailable(status, data) {
  return status === 0 || status === 502 || status === 503 || (status === 500 && !data?.error)
}

export async function apiRequest(path, options = {}) {
  let response
  try {
    response = await fetch(path, {
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      ...options,
    })
  } catch {
    throw connectionError(
      'サーバーに接続できません。バックエンド（Flask）が起動しているか確認してください。',
    )
  }

  let data = null
  const contentType = response.headers.get('content-type') || ''
  if (contentType.includes('application/json')) {
    try {
      data = await response.json()
    } catch {
      data = null
    }
  }

  if (!response.ok) {
    let message = data?.error
    if (!message && isBackendUnavailable(response.status, data)) {
      message =
        'サーバーに接続できません。別のターミナルで `cd project` → `python app.py` を実行してください。'
    }
    if (!message) {
      message = `リクエストに失敗しました（${response.status}）`
    }
    const error = new Error(message)
    error.status = response.status
    error.data = data
    throw error
  }

  return data
}
