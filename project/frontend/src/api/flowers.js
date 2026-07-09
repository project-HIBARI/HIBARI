import { apiRequest } from './client.js'

export function fetchFlowerOfferings() {
  return apiRequest('/api/flower-offerings')
}

export function submitFlowerOffering(payload) {
  return apiRequest('/api/flower-offerings', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
