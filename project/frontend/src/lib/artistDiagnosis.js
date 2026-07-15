/**
 * Music Memories — アーティスト診断のスコア計算
 * ランダムなし。同じ回答では常に同じ結果になる。
 */
import { DIAGNOSIS_TAG_LABELS } from '../data/artistDiagnosisData.js'

/**
 * @param {Array<{ tags?: string[] }>} selectedAnswers
 * @returns {string[]}
 */
export function collectSelectedTags(selectedAnswers) {
  const tags = []
  for (const answer of selectedAnswers || []) {
    if (!answer?.tags?.length) continue
    for (const tag of answer.tags) tags.push(tag)
  }
  return tags
}

/**
 * @param {object[]} artists
 * @param {Array<{ tags?: string[] }>} selectedAnswers
 * @returns {{ artist: object, score: number, matchedTags: string[] }[]}
 */
export function calculateArtistScores(artists, selectedAnswers) {
  const selectedTags = collectSelectedTags(selectedAnswers)
  if (!artists?.length) return []

  return artists.map((artist) => {
    const artistTags = new Set(artist.recommendationTags || [])
    let score = 0
    const matched = []
    for (const tag of selectedTags) {
      if (!artistTags.has(tag)) continue
      score += 1
      matched.push(tag)
    }
    return { artist, score, matchedTags: matched }
  })
}

/**
 * 同点時: 公開中(open) → featuredOrder 小 → 配列順
 * @param {object[]} artists
 * @param {Array<{ tags?: string[] }>} selectedAnswers
 * @returns {{ artist: object | null, score: number, matchedTags: string[], matchedLabels: string[] }}
 */
export function getRecommendedArtist(artists, selectedAnswers) {
  const scored = calculateArtistScores(artists, selectedAnswers)
  if (!scored.length) {
    return { artist: null, score: 0, matchedTags: [], matchedLabels: [] }
  }

  const withIndex = scored.map((entry, index) => ({ ...entry, index }))
  withIndex.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score
    const aOpen = a.artist.status === 'open' ? 1 : 0
    const bOpen = b.artist.status === 'open' ? 1 : 0
    if (bOpen !== aOpen) return bOpen - aOpen
    const aOrder = a.artist.featuredOrder ?? 999
    const bOrder = b.artist.featuredOrder ?? 999
    if (aOrder !== bOrder) return aOrder - bOrder
    return a.index - b.index
  })

  const best = withIndex[0]
  if (!best || best.score <= 0) {
    // タグ不足などでスコア0のみの場合でも、同点ルールで1人を返す
    const fallback = withIndex[0]
    return {
      artist: fallback?.artist || null,
      score: fallback?.score || 0,
      matchedTags: [],
      matchedLabels: [],
    }
  }

  const uniqueMatched = [...new Set(best.matchedTags)]
  const matchedLabels = uniqueMatched
    .map((tag) => DIAGNOSIS_TAG_LABELS[tag])
    .filter(Boolean)
    .slice(0, 3)

  return {
    artist: best.artist,
    score: best.score,
    matchedTags: uniqueMatched,
    matchedLabels,
  }
}
