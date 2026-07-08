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

export function fetchCurrentUser() {
  return apiRequest('/api/me')
}

export function logout() {
  return apiRequest('/api/logout', { method: 'POST' })
}
