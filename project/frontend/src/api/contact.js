import { apiRequest } from './client.js'

export function submitContact(payload) {
  return apiRequest('/api/contact', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
