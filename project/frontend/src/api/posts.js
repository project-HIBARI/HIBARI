import { apiRequest } from './client.js'

export function createPost(payload) {
  return apiRequest('/api/posts', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function fetchPosts() {
  return apiRequest('/api/posts')
}
