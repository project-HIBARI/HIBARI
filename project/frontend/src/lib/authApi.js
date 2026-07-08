/**
 * 認証 API（Flask /api/* エンドポイント）
 */
import { apiFetch } from './api.js'

/**
 * @returns {Promise<{ login: boolean, user?: { account_id: number, name: string, email: string } }>}
 */
export async function fetchMe() {
  let response
  try {
    response = await fetch('/api/me', { credentials: 'include' })
  } catch {
    return { login: false }
  }

  let data = null
  const text = await response.text()
  if (text) {
    try {
      data = JSON.parse(text)
    } catch {
      return { login: false }
    }
  }

  if (!response.ok || !data?.login) {
    return { login: false }
  }

  return data
}

/**
 * @param {string} email
 * @param {string} password
 */
export function login(email, password) {
  return apiFetch('/api/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
}

/**
 * @param {string} name
 * @param {string} email
 * @param {string} password
 */
export function register(name, email, password) {
  return apiFetch('/api/accounts', {
    method: 'POST',
    body: JSON.stringify({ name, email, password }),
  })
}

export function logout() {
  return apiFetch('/api/logout', { method: 'POST' })
}
