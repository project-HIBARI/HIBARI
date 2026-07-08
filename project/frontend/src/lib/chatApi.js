/**
 * AIチャット API クライアント（Flask バックエンド連携）
 * セッション Cookie ベースの認証を想定（credentials: 'include'）
 */

async function request(url, options = {}) {
  const res = await fetch(url, {
    credentials: 'include',
    ...options,
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    const err = new Error(data.error || 'リクエストに失敗しました')
    err.status = res.status
    err.data = data
    throw err
  }
  return data
}

/** チャットルーム一覧 */
export function fetchRooms() {
  return request('/api/rooms')
}

/** ルーム内メッセージ一覧 */
export function fetchMessages(roomId) {
  return request(`/api/messages/${roomId}`)
}

/**
 * メッセージ送信 → AI応答
 * @param {{ message: string, roomId?: number|null }} params
 */
export function sendChatMessage({ message, roomId = null }) {
  const form = new FormData()
  form.append('message', message)
  if (roomId) form.append('room_id', String(roomId))
  return request('/api/chat', { method: 'POST', body: form })
}

/** ログイン状態確認 */
export function fetchMe() {
  return request('/api/me')
}
