/**
 * 楽曲 API（songs テーブル）
 */
import { apiRequest } from './client.js'

/** 曲一覧を取得する */
export function fetchSongs() {
  return apiRequest('/api/songs')
}
