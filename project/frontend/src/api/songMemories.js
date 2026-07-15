/**
 * 楽曲の思い出（同じ曲で泣いた人マッチング）API
 */
import { apiRequest } from './client.js'

export function fetchSongMemories(songId) {
  return apiRequest(`/api/songs/${songId}/memories`)
}

export function fetchSongMemorySummary(songId) {
  return apiRequest(`/api/songs/${songId}/memories/summary`)
}

export function createSongMemory(songId, { memoryType, comment = '', visibility = 'public' } = {}) {
  return apiRequest(`/api/songs/${songId}/memories`, {
    method: 'POST',
    body: JSON.stringify({ memory_type: memoryType, comment, visibility }),
  })
}

export function fetchSongChatRoom(songId) {
  return apiRequest(`/api/open-chats/by-song/${songId}`)
}

export function fetchAccountSongMemories(accountId) {
  return apiRequest(`/api/accounts/${accountId}/song-memories`)
}
