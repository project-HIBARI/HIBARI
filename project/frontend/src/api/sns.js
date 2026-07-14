import { apiRequest } from './client.js'

export function fetchSnsUsage() {
  return apiRequest('/api/sns/usage')
}

export function createSnsReport(payload) {
  return apiRequest('/api/sns/reports', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function toggleSnsBlock(accountId) {
  return apiRequest(`/api/sns/block/${accountId}`, { method: 'POST' })
}

export function fetchSnsBlocks() {
  return apiRequest('/api/sns/blocks')
}

export function fetchSnsStories() {
  return apiRequest('/api/sns/stories')
}

export function createSnsStory(payload) {
  return apiRequest('/api/sns/stories', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function deleteSnsStory(storyId) {
  return apiRequest(`/api/sns/stories/${storyId}`, { method: 'DELETE' })
}

export function recordSnsStoryView(storyId) {
  return apiRequest(`/api/sns/stories/${storyId}/view`, { method: 'POST' })
}

export function fetchSnsStoryViewers(storyId) {
  return apiRequest(`/api/sns/stories/${storyId}/viewers`)
}

export function fetchSnsStoryArchive() {
  return apiRequest('/api/sns/stories/mine')
}

export function fetchSnsProfile(accountId) {
  return apiRequest(`/api/sns/profile/${accountId}`)
}

export function updateSnsProfile(payload) {
  return apiRequest('/api/sns/profile/me', {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}

export async function uploadSnsAvatar(file) {
  const formData = new FormData()
  formData.append('file', file)
  const response = await fetch('/api/sns/profile/avatar/upload', {
    method: 'POST',
    credentials: 'include',
    body: formData,
  })
  let data = null
  const contentType = response.headers.get('content-type') || ''
  if (contentType.includes('application/json')) {
    data = await response.json()
  }
  if (!response.ok) {
    const message = data?.error || `アップロードに失敗しました（${response.status}）`
    const error = new Error(message)
    error.status = response.status
    error.data = data
    throw error
  }
  return data
}

export function fetchSnsProfilePosts(accountId, { type = 'all', beforeId = null, limit = 20 } = {}) {
  const params = new URLSearchParams({ type, limit: String(limit) })
  if (beforeId) params.set('before_id', String(beforeId))
  return apiRequest(`/api/sns/profile/${accountId}/posts?${params.toString()}`)
}

export function fetchSnsSavedPosts({ beforeId = null, limit = 20 } = {}) {
  const params = new URLSearchParams({ limit: String(limit) })
  if (beforeId) params.set('before_id', String(beforeId))
  return apiRequest(`/api/sns/saved?${params.toString()}`)
}

export function toggleSnsFollow(accountId) {
  return apiRequest(`/api/sns/follow/${accountId}`, { method: 'POST' })
}

export function fetchSnsFollowing(accountId) {
  return apiRequest(`/api/sns/follow/${accountId}/following`)
}

export function fetchSnsFollowers(accountId) {
  return apiRequest(`/api/sns/follow/${accountId}/followers`)
}

export function fetchDmThreads(box = 'inbox') {
  return apiRequest(`/api/sns/dm/threads?box=${box}`)
}

export function getOrCreateDmThread(recipientId) {
  return apiRequest('/api/sns/dm/threads', {
    method: 'POST',
    body: JSON.stringify({ recipient_id: recipientId }),
  })
}

export function fetchDmThread(threadId, { beforeId = null } = {}) {
  const params = new URLSearchParams()
  if (beforeId) params.set('before_id', String(beforeId))
  const qs = params.toString()
  return apiRequest(`/api/sns/dm/threads/${threadId}${qs ? `?${qs}` : ''}`)
}

export function markDmThreadRead(threadId) {
  return apiRequest(`/api/sns/dm/threads/${threadId}/read`, { method: 'POST' })
}

export function acceptDmRequest(threadId) {
  return apiRequest(`/api/sns/dm/threads/${threadId}/accept`, { method: 'POST' })
}

export function rejectDmRequest(threadId) {
  return apiRequest(`/api/sns/dm/threads/${threadId}/reject`, { method: 'POST' })
}

export function sendDm(payload) {
  return apiRequest('/api/sns/dm/send', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function sendDmInThread(threadId, payload) {
  return apiRequest(`/api/sns/dm/threads/${threadId}/messages`, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function deleteDmMessage(messageId) {
  return apiRequest(`/api/sns/dm/messages/${messageId}`, { method: 'DELETE' })
}

export function searchDmUsers(q) {
  return apiRequest(`/api/sns/dm/search?q=${encodeURIComponent(q)}`)
}

export function fetchDmUnreadCount() {
  return apiRequest('/api/sns/dm/unread-count')
}

export async function uploadDmMedia(file) {
  const formData = new FormData()
  formData.append('file', file)
  const response = await fetch('/api/sns/dm/media/upload', {
    method: 'POST',
    credentials: 'include',
    body: formData,
  })
  let data = null
  const contentType = response.headers.get('content-type') || ''
  if (contentType.includes('application/json')) {
    data = await response.json()
  }
  if (!response.ok) {
    const message = data?.error || `アップロードに失敗しました（${response.status}）`
    const error = new Error(message)
    error.status = response.status
    error.data = data
    throw error
  }
  return data
}

export function fetchSnsFeed({ type = 'all', beforeId = null, limit = 20 } = {}) {
  const params = new URLSearchParams({ type, limit: String(limit) })
  if (beforeId) params.set('before_id', String(beforeId))
  return apiRequest(`/api/sns/posts?${params.toString()}`)
}

export function fetchSnsPost(postId) {
  return apiRequest(`/api/sns/posts/${postId}`)
}

export function createSnsPost(payload) {
  return apiRequest('/api/sns/posts', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function updateSnsPost(postId, payload) {
  return apiRequest(`/api/sns/posts/${postId}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}

export function deleteSnsPost(postId) {
  return apiRequest(`/api/sns/posts/${postId}`, { method: 'DELETE' })
}

export function toggleSnsLike(postId) {
  return apiRequest(`/api/sns/posts/${postId}/like`, { method: 'POST' })
}

export function toggleSnsSave(postId) {
  return apiRequest(`/api/sns/posts/${postId}/save`, { method: 'POST' })
}

export function fetchSnsComments(postId, { beforeId = null } = {}) {
  const params = new URLSearchParams()
  if (beforeId) params.set('before_id', String(beforeId))
  const qs = params.toString()
  return apiRequest(`/api/sns/posts/${postId}/comments${qs ? `?${qs}` : ''}`)
}

export function createSnsComment(postId, body) {
  return apiRequest(`/api/sns/posts/${postId}/comments`, {
    method: 'POST',
    body: JSON.stringify({ body }),
  })
}

export function deleteSnsComment(commentId) {
  return apiRequest(`/api/sns/comments/${commentId}`, { method: 'DELETE' })
}

/**
 * SNS用メディア（画像・動画）をアップロード
 * @returns {Promise<{ path: string, media_type: 'image'|'video' }>}
 */
export async function uploadSnsMedia(file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch('/api/sns/media/upload', {
    method: 'POST',
    credentials: 'include',
    body: formData,
  })

  let data = null
  const contentType = response.headers.get('content-type') || ''
  if (contentType.includes('application/json')) {
    data = await response.json()
  }

  if (!response.ok) {
    const message = data?.error || `アップロードに失敗しました（${response.status}）`
    const error = new Error(message)
    error.status = response.status
    error.data = data
    throw error
  }

  return data
}
