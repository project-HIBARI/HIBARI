/**
 * サイト内検索 — インデックス生成
 */
import { HIBARU_DATA } from '../data/hibaruData.js'

export function buildSearchIndex() {
  const items = []
  for (const n of HIBARU_DATA.news || []) {
    items.push({ type: 'ニュース', label: n.title, page: 'news', key: `news-${n.id}` })
  }
  for (const d of HIBARU_DATA.discography || []) {
    items.push({ type: '楽曲', label: d.title, page: 'disco', key: `disco-${d.title}` })
  }
  for (const p of HIBARU_DATA.places || []) {
    items.push({ type: 'ゆかりの地', label: p.name, page: 'map', key: `place-${p.id}` })
  }
  for (const e of HIBARU_DATA.events || []) {
    items.push({ type: 'イベント', label: e.title, page: 'memories', key: `event-${e.id}` })
  }
  items.push(
    { type: 'ページ', label: 'ファンクラブ', page: 'fanclub', key: 'page-fanclub' },
    { type: 'ページ', label: '献花', page: 'message', key: 'page-message' },
    { type: 'ページ', label: 'お問い合わせ', page: 'contact', key: 'page-contact' },
    { type: 'ページ', label: 'FAQ', page: 'faq', key: 'page-faq' },
  )
  return items
}

export function filterSearchResults(query, items, limit = 8) {
  const q = (query || '').trim().toLowerCase()
  if (!q) return []
  return items.filter((item) => item.label.toLowerCase().includes(q)).slice(0, limit)
}
