import { apiRequest } from './client.js'

export function fetchFlowerOfferings(options = {}) {
  const query = options.mine ? '?mine=1' : ''
  return apiRequest(`/api/flower-offerings${query}`)
}

export function fetchMyFlowerOfferings() {
  return fetchFlowerOfferings({ mine: true })
}

export function submitFlowerOffering(payload) {
  return apiRequest('/api/flower-offerings', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function updateFlowerOffering(flowerOfferingId, payload) {
  return apiRequest(`/api/flower-offerings/${flowerOfferingId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export function deleteFlowerOffering(flowerOfferingId) {
  return apiRequest(`/api/flower-offerings/${flowerOfferingId}`, { method: 'DELETE' })
}
