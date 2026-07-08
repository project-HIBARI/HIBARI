import { apiRequest } from './client.js'

export function login(email, password) {
  return apiRequest('/api/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
}

export function registerAccount(payload) {
  return apiRequest('/api/accounts', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function fetchCurrentUser() {
  const response = await fetch('/api/me', {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
  })

  let data = null
  const contentType = response.headers.get('content-type') || ''
  if (contentType.includes('application/json')) {
    data = await response.json()
  }

  if (response.status === 401 || !data?.login) {
    return { login: false, user: null }
  }

  if (!response.ok) {
    const message = data?.error || `リクエストに失敗しました（${response.status}）`
    const error = new Error(message)
    error.status = response.status
    throw error
  }

  return data
}

export function logout() {
  return apiRequest('/api/logout', { method: 'POST' })
}
