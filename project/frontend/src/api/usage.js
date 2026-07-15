import { apiRequest } from './client.js'

/**
 * @param {'ai-chat'|'board-post'|'artist-diagnosis'} feature
 */
export function fetchUsage(feature) {
  return apiRequest(`/api/usage/${feature}`)
}

/**
 * @param {'ai-chat'|'board-post'|'artist-diagnosis'} feature
 */
export function consumeUsage(feature) {
  return apiRequest(`/api/usage/${feature}/consume`, { method: 'POST' })
}
