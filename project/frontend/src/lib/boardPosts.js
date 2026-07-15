/**
 * 思い出掲示板 — API投稿 → カード表示用データ変換
 */
import { HIBARU_DATA } from '../data/hibaruData.js'

function formatBoardDate(createdAt) {
  if (!createdAt) return ''
  const raw = String(createdAt)
  const normalized = raw.includes('T') ? raw : raw.replace(' ', 'T')
  const d = new Date(normalized)
  if (Number.isNaN(d.getTime())) return raw.slice(0, 10)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}.${m}.${day}`
}

function resolveSongLabel(songId) {
  if (songId == null || songId === '') return '思い出'
  const key = String(songId)
  const found = HIBARU_DATA.discography.find(
    (d) => String(d.id) === key || String(d.no) === key || d.title === key,
  )
  return found?.title || key
}

/**
 * @param {object} row GET /api/posts の1件
 * @param {Record<string, number>} [extraLikes]
 * @param {number|null} [currentAccountId]
 */
export function mapApiPostToBoardItem(row, extraLikes = {}, currentAccountId = null) {
  const id = `api-${row.post_id}`
  const likes = Number(row.like_count) || 0
  const accountId = row.account_id ?? null
  return {
    id,
    postId: row.post_id,
    accountId,
    isOwn: currentAccountId != null && accountId != null && Number(accountId) === Number(currentAccountId),
    song: resolveSongLabel(row.song_id),
    title: row.title || '',
    body: row.content || '',
    author: row.name || '匿名',
    age: row.age ?? null,
    location: row.location || '',
    likes,
    comments: 0,
    date: formatBoardDate(row.created_at),
    imageUrl: row.image_path || null,
    videoUrl: row.video_path || null,
    displayLikes: (extraLikes[id] ?? 0) + likes,
  }
}
