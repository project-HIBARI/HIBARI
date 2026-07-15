import { apiRequest } from './client.js'

/**
 * AIによる年別振り返り文を生成（失敗時は呼び出し側でフォールバック）
 */
export function fetchYearRecap(payload) {
  return apiRequest('/api/memory-book/year-recap', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
