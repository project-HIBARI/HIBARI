import { apiRequest } from './client.js'

export function applyToEvent(eventKey, payload) {
  return apiRequest(`/api/events/${encodeURIComponent(eventKey)}/apply`, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function fetchMyEventApplications() {
  return apiRequest('/api/events/applications')
}
