/**
 * Music Memory Book — 既存APIデータを思い出帳形式へ変換
 */
import { fetchFlowerOfferings } from '../api/flowers.js'
import { fetchPosts } from '../api/posts.js'
import { flowerImage } from './flowers.js'

const WEEKDAY_LABELS = ['日', '月', '火', '水', '木', '金', '土']
const YEAR_THEME_COLORS = ['purple', 'blue', 'green', 'brown']

const CATEGORY_LABELS = {
  flowers: '献花の記録',
  posts: '思い出の投稿',
  songs: 'お気に入り楽曲',
  ai: 'AIとの会話',
}

const CATEGORY_ICONS = {
  flowers: 'flower',
  posts: 'chat',
  songs: 'music',
  ai: 'chat',
}

function parseDate(isoOrStr) {
  if (!isoOrStr) return null
  const normalized = String(isoOrStr).replace(' ', 'T')
  const d = new Date(normalized)
  return Number.isNaN(d.getTime()) ? null : d
}

export function formatDateDot(isoOrStr) {
  const d = parseDate(isoOrStr)
  if (!d) return '—'
  return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, '0')}.${String(d.getDate()).padStart(2, '0')}`
}

export function formatDateDisplay(isoOrStr) {
  const d = parseDate(isoOrStr)
  if (!d) return '—'
  const wd = WEEKDAY_LABELS[d.getDay()]
  return `${formatDateDot(isoOrStr)}（${wd}）`
}

function mapFlowerToItem(row) {
  const d = parseDate(row.offered_at)
  const flowerName = row.flower_type || '白百合'
  const month = d ? d.getMonth() + 1 : null
  return {
    id: `flower-${row.flower_offering_id}`,
    category: 'flowers',
    categoryLabel: CATEGORY_LABELS.flowers,
    icon: CATEGORY_ICONS.flowers,
    occurredAt: row.offered_at,
    year: d?.getFullYear() ?? null,
    month,
    monthLabel: month ? `${month}月` : '',
    title: `${flowerName}を献花`,
    date: formatDateDot(row.offered_at),
    dateDisplay: formatDateDisplay(row.offered_at),
    description: row.content || '',
    location: row.location || '—',
    visibility: '公開',
    body: row.content || '',
    mainImage: flowerImage(flowerName),
    photos: [{ src: flowerImage(flowerName), alt: `${flowerName}の献花` }],
    aiMessage: `${flowerName}への想いが、あなたの思い出帳に残りました。`,
    memo: flowerName,
    raw: row,
  }
}

function mapPostToItem(row) {
  const d = parseDate(row.created_at)
  const month = d ? d.getMonth() + 1 : null
  const title = row.title ? `「${row.title}」の思い出を投稿しました` : '思い出を投稿しました'
  const images = row.image_path ? [{ src: row.image_path, alt: row.title || '投稿画像' }] : []
  return {
    id: `post-${row.post_id}`,
    category: 'posts',
    categoryLabel: CATEGORY_LABELS.posts,
    icon: CATEGORY_ICONS.posts,
    occurredAt: row.created_at,
    year: d?.getFullYear() ?? null,
    month,
    monthLabel: month ? `${month}月` : '',
    title,
    date: formatDateDot(row.created_at),
    dateDisplay: formatDateDisplay(row.created_at),
    description: row.content || '',
    location: row.location || '—',
    visibility: '公開',
    body: row.content || '',
    mainImage: row.image_path || '/images/page/misorahibari-chair.png',
    photos: images,
    aiMessage: 'あなたの大切な思い出が、アルバムに残りました。',
    memo: row.title || '—',
    raw: row,
  }
}

function sortItemsNewestFirst(items) {
  return [...items].sort((a, b) => {
    const da = parseDate(a.occurredAt)?.getTime() ?? 0
    const db = parseDate(b.occurredAt)?.getTime() ?? 0
    return db - da
  })
}

function attachPrevNext(items) {
  const sorted = sortItemsNewestFirst(items)
  return sorted.map((item, i) => ({
    ...item,
    prevId: sorted[i + 1]?.id ?? null,
    nextId: sorted[i - 1]?.id ?? null,
  }))
}

function countByCategory(items) {
  return items.reduce(
    (acc, item) => {
      if (item.category === 'flowers') acc.flowers += 1
      if (item.category === 'posts') acc.posts += 1
      if (item.category === 'songs') acc.songs += 1
      if (item.category === 'ai') acc.aiChats += 1
      return acc
    },
    { flowers: 0, posts: 0, songs: 0, aiChats: 0 },
  )
}

function buildCategories(counts) {
  return [
    {
      id: 'flowers',
      title: '献花の記録',
      count: counts.flowers,
      desc: 'あなたが捧げた献花の記録を振り返ります。',
      icon: 'flower',
      tone: 'pink',
    },
    {
      id: 'posts',
      title: '思い出の投稿',
      count: counts.posts,
      desc: 'あなたが投稿した思い出のエピソードです。',
      icon: 'chat',
      tone: 'warm',
    },
    {
      id: 'songs',
      title: 'お気に入り楽曲',
      count: counts.songs,
      desc: 'あなたが登録したお気に入りの楽曲一覧です。',
      icon: 'music',
      tone: 'purple',
    },
    {
      id: 'ai',
      title: 'AIとの会話',
      count: counts.aiChats,
      desc: 'AI美空ひばりとの会話履歴を振り返ります。',
      icon: 'chat',
      tone: 'gold',
    },
    {
      id: 'albums',
      title: '年別アルバム',
      count: null,
      desc: '年ごとの思い出をアルバム形式で確認できます。',
      icon: 'calendar',
      tone: 'shelf',
    },
  ]
}

function buildYears(items) {
  const currentYear = new Date().getFullYear()
  const yearsWithData = new Set(items.map((i) => i.year).filter(Boolean))
  if (!yearsWithData.size) yearsWithData.add(currentYear)
  const minYear = Math.min(...yearsWithData, currentYear)
  const years = []
  for (let y = currentYear; y >= minYear; y -= 1) {
    const yearItems = items.filter((i) => i.year === y)
    const idx = currentYear - y
    years.push({
      year: y,
      total: yearItems.length,
      tone: YEAR_THEME_COLORS[idx % YEAR_THEME_COLORS.length],
    })
  }
  return years
}

function buildSummary(items) {
  const counts = countByCategory(items)
  const dates = items
    .map((i) => parseDate(i.occurredAt))
    .filter(Boolean)
    .sort((a, b) => a.getTime() - b.getTime())
  const startedAt = dates.length ? formatDateDot(dates[0]) : '—'
  const currentYear = new Date().getFullYear()
  const currentYearTotal = items.filter((i) => i.year === currentYear).length
  return {
    total: items.length,
    startedAt,
    categories: counts,
    currentYear: { year: currentYear, total: currentYearTotal },
  }
}

function buildYearDetail(items, year) {
  const yearItems = sortItemsNewestFirst(items.filter((i) => i.year === year))
  const counts = countByCategory(yearItems)
  return {
    year,
    summary: {
      flowers: counts.flowers,
      posts: counts.posts,
      songs: counts.songs,
      aiChats: counts.aiChats,
      total: yearItems.length,
    },
    timeline: yearItems.map((item) => ({
      id: item.id,
      month: item.month,
      monthLabel: item.monthLabel,
      category: item.category,
      categoryLabel: item.categoryLabel,
      title: item.title,
      date: item.date,
      dateDisplay: item.dateDisplay,
      description: item.description,
      icon: item.icon,
    })),
  }
}

function enrichMonthPosition(item, allItems) {
  const sameMonth = allItems.filter(
    (i) => i.year === item.year && i.month === item.month,
  )
  const indexInMonth = sameMonth.findIndex((i) => i.id === item.id) + 1
  return {
    ...item,
    indexInMonth: indexInMonth || 1,
    totalInMonth: sameMonth.length || 1,
  }
}

/**
 * 既存API（献花・思い出投稿）から思い出帳データを構築
 */
export async function loadMemoryBookFromApi() {
  const [flowersResult, postsResult] = await Promise.allSettled([
    fetchFlowerOfferings(),
    fetchPosts(),
  ])

  const flowers = flowersResult.status === 'fulfilled' && Array.isArray(flowersResult.value)
    ? flowersResult.value.map(mapFlowerToItem)
    : []

  const posts = postsResult.status === 'fulfilled' && Array.isArray(postsResult.value)
    ? postsResult.value.map(mapPostToItem)
    : []

  const items = attachPrevNext([...flowers, ...posts])
  const itemMap = Object.fromEntries(items.map((i) => [i.id, i]))

  return {
    items,
    itemMap,
    summary: buildSummary(items),
    categories: buildCategories(countByCategory(items)),
    years: buildYears(items),
    getYearDetail: (year) => buildYearDetail(items, year),
    getItemDetail: (id) => {
      const item = itemMap[id]
      if (!item) return null
      return enrichMonthPosition(item, items)
    },
    errors: {
      flowers: flowersResult.status === 'rejected' ? flowersResult.reason : null,
      posts: postsResult.status === 'rejected' ? postsResult.reason : null,
    },
  }
}
