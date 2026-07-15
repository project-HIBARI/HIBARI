/**
 * Music Memory Book — 既存APIデータを思い出帳形式へ変換
 */
import { fetchMyFlowerOfferings } from '../api/flowers.js'
import { fetchMyPosts } from '../api/posts.js'
import { fetchRooms, fetchMessages } from '../lib/chatApi.js'
import { HIBARU_DATA } from '../data/hibaruData.js'
import { flowerImage } from './flowers.js'
import { getDiscoFavoriteAddedAt, loadDiscoFavoriteIds } from './discoFavorites.js'
import { HIBARI_AVATAR_SRC } from './hibariAvatar.js'

export function parseMemoryItemRef(id) {
  if (!id) return null
  const match = String(id).match(/^(flower|post)-(\d+)$/)
  if (!match) return null
  return {
    category: match[1] === 'flower' ? 'flowers' : 'posts',
    sourceId: Number(match[2]),
  }
}

export function isMemoryItemManageable(item) {
  return item?.category === 'flowers' || item?.category === 'posts'
}

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

function mapSongToItem(song) {
  const occurredAt = getDiscoFavoriteAddedAt(song.id)
  const d = parseDate(occurredAt)
  const month = d ? d.getMonth() + 1 : null
  const bodyLines = [
    song.note ? `解説：${song.note}` : '',
    `作詞：${song.lyric} / 作曲：${song.music}`,
    song.label ? `レーベル：${song.label}` : '',
    `リリース年：${song.year}年`,
  ].filter(Boolean)

  return {
    id: `song-${song.id}`,
    category: 'songs',
    categoryLabel: CATEGORY_LABELS.songs,
    icon: CATEGORY_ICONS.songs,
    occurredAt,
    year: d?.getFullYear() ?? null,
    month,
    monthLabel: month ? `${month}月` : '',
    title: `「${song.title}」をお気に入りに追加`,
    date: formatDateDot(occurredAt),
    dateDisplay: formatDateDisplay(occurredAt),
    description: song.note || `${song.year}年発売の${song.type || '楽曲'}`,
    location: song.label || '—',
    visibility: 'プライベート',
    body: bodyLines.join('\n'),
    mainImage: '/images/page/misorahibari-chair.png',
    photos: [],
    aiMessage: `「${song.title}」は、あなたのMusic Memory Bookに残された大切な一曲です。`,
    memo: song.title,
    raw: song,
  }
}

function formatChatSender(sender) {
  if (sender === 'user') return 'あなた'
  if (sender === 'assistant') return 'AI美空ひばり'
  return sender || '—'
}

function mapAiRoomToItem(room, messages) {
  const occurredAt = messages.length
    ? messages[messages.length - 1].created_at
    : room.created_at
  const d = parseDate(occurredAt)
  const month = d ? d.getMonth() + 1 : null
  const preview = messages
    .slice(-6)
    .map((m) => `${formatChatSender(m.sender)}：${m.content}`)
    .join('\n\n')
  const firstAi = messages.find((m) => m.sender === 'assistant')

  return {
    id: `ai-${room.ai_chat_room_id}`,
    category: 'ai',
    categoryLabel: CATEGORY_LABELS.ai,
    icon: CATEGORY_ICONS.ai,
    occurredAt,
    year: d?.getFullYear() ?? null,
    month,
    monthLabel: month ? `${month}月` : '',
    title: `AIとの会話「${room.room_name || '新しいチャット'}」`,
    date: formatDateDot(occurredAt),
    dateDisplay: formatDateDisplay(occurredAt),
    description: messages.length
      ? `${messages.length}件のメッセージ`
      : '会話を開始しました',
    location: 'オンライン',
    visibility: 'プライベート',
    body: preview || 'この会話の記録はまだありません。',
    mainImage: HIBARI_AVATAR_SRC,
    photos: [],
    aiMessage: firstAi?.content || 'AI美空ひばりとの会話が記録されています。',
    memo: room.room_name || '—',
    raw: { room, messages },
  }
}

function loadFavoriteSongItems() {
  const favoriteIds = new Set(loadDiscoFavoriteIds())
  if (!favoriteIds.size) return []

  return HIBARU_DATA.discography
    .filter((song) => favoriteIds.has(song.id))
    .map(mapSongToItem)
}

async function loadAiChatItems() {
  try {
    const rooms = await fetchRooms()
    if (!Array.isArray(rooms) || !rooms.length) return []

    const results = await Promise.all(
      rooms.map(async (room) => {
        try {
          const messages = await fetchMessages(room.ai_chat_room_id)
          return mapAiRoomToItem(room, Array.isArray(messages) ? messages : [])
        } catch {
          return mapAiRoomToItem(room, [])
        }
      }),
    )

    return results
  } catch {
    return []
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
  const yearCounts = new Map()

  for (const item of items) {
    if (!item.year) continue
    yearCounts.set(item.year, (yearCounts.get(item.year) || 0) + 1)
  }

  if (!yearCounts.size) {
    return [{ year: currentYear, total: 0, tone: 'purple' }]
  }

  return [...yearCounts.entries()]
    .sort((a, b) => b[0] - a[0])
    .map(([year, total]) => ({
      year,
      total,
      tone: YEAR_THEME_COLORS[(currentYear - year) % YEAR_THEME_COLORS.length],
    }))
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
    timeline: yearItems.map(itemToTimelineEntry),
  }
}

function itemToTimelineEntry(item) {
  return {
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
  }
}

export const FILTER_MODES = {
  SAME_DAY: 'same-day',
  SAME_PLACE: 'same-place',
  SAME_CATEGORY: 'same-category',
}

function getRelatedItems(items, mode, memory) {
  if (!memory) return []

  if (mode === FILTER_MODES.SAME_DAY) {
    const key = formatDateDot(memory.occurredAt)
    if (key === '—') return []
    return sortItemsNewestFirst(items.filter((i) => formatDateDot(i.occurredAt) === key))
  }

  if (mode === FILTER_MODES.SAME_PLACE) {
    const loc = (memory.location || '').trim()
    if (!loc || loc === '—') return []
    return sortItemsNewestFirst(items.filter((i) => (i.location || '').trim() === loc))
  }

  if (mode === FILTER_MODES.SAME_CATEGORY) {
    return sortItemsNewestFirst(items.filter((i) => i.category === memory.category))
  }

  return []
}

export function buildFilterViewData(items, mode, memory) {
  if (!memory) return null

  const related = getRelatedItems(items, mode, memory)
  const titles = {
    [FILTER_MODES.SAME_DAY]: `${memory.dateDisplay}の思い出`,
    [FILTER_MODES.SAME_PLACE]: `${memory.location}の思い出`,
    [FILTER_MODES.SAME_CATEGORY]: `${memory.categoryLabel}の思い出`,
  }
  const leads = {
    [FILTER_MODES.SAME_DAY]: '同じ日に記録された思い出を一覧で確認できます。',
    [FILTER_MODES.SAME_PLACE]: '同じ場所に関連する思い出を一覧で確認できます。',
    [FILTER_MODES.SAME_CATEGORY]: '同じカテゴリの思い出を一覧で確認できます。',
  }
  const emptyMessages = {
    [FILTER_MODES.SAME_DAY]: '同じ日の思い出は見つかりませんでした。',
    [FILTER_MODES.SAME_PLACE]: '同じ場所の思い出は見つかりませんでした。',
    [FILTER_MODES.SAME_CATEGORY]: '同じカテゴリの思い出は見つかりませんでした。',
  }

  return {
    mode,
    title: titles[mode] || '関連する思い出',
    lead: leads[mode] || '',
    emptyMessage: emptyMessages[mode] || '思い出が見つかりませんでした。',
    timeline: related.map(itemToTimelineEntry),
    total: related.length,
  }
}

const CATEGORY_VIEW_CONFIG = {
  flowers: {
    lead: 'あなたが捧げた献花の記録を一覧で確認できます。',
    emptyMessage: '献花の記録はまだありません。',
    emptyActionLabel: '献花ページへ',
    emptyAction: 'message',
  },
  posts: {
    lead: 'あなたが投稿した思い出を一覧で確認できます。',
    emptyMessage: '思い出の投稿はまだありません。',
    emptyActionLabel: '思い出投稿ページへ',
    emptyAction: 'memories',
  },
  songs: {
    lead: 'お気に入りに登録した楽曲を一覧で確認できます。',
    emptyMessage: 'お気に入り楽曲はまだありません。ディスコグラフィでハートをタップして追加できます。',
    emptyActionLabel: 'ディスコグラフィへ',
    emptyAction: 'disco',
  },
  ai: {
    lead: 'AI美空ひばりとの会話履歴を一覧で確認できます。',
    emptyMessage: 'AIとの会話履歴はまだありません。ログインして会話を始めると、ここに記録されます。',
    emptyActionLabel: 'AIチャットを開く',
    emptyAction: 'ai',
  },
}

export function buildCategoryViewData(items, categoryId) {
  const config = CATEGORY_VIEW_CONFIG[categoryId]
  if (!config) return null

  const related = sortItemsNewestFirst(items.filter((item) => item.category === categoryId))

  return {
    mode: 'category',
    categoryId,
    title: CATEGORY_LABELS[categoryId] || 'カテゴリ',
    lead: config.lead,
    emptyMessage: config.emptyMessage,
    emptyActionLabel: config.emptyActionLabel,
    emptyAction: config.emptyAction,
    timeline: related.map(itemToTimelineEntry),
    total: related.length,
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
  const [flowersResult, postsResult, aiResult] = await Promise.allSettled([
    fetchMyFlowerOfferings(),
    fetchMyPosts(),
    loadAiChatItems(),
  ])

  const flowers = flowersResult.status === 'fulfilled' && Array.isArray(flowersResult.value)
    ? flowersResult.value.map(mapFlowerToItem)
    : []

  const posts = postsResult.status === 'fulfilled' && Array.isArray(postsResult.value)
    ? postsResult.value.map(mapPostToItem)
    : []

  const songs = loadFavoriteSongItems()

  const aiChats = aiResult.status === 'fulfilled' && Array.isArray(aiResult.value)
    ? aiResult.value
    : []

  const items = attachPrevNext([...flowers, ...posts, ...songs, ...aiChats])
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
    getFilterViewData: (mode, memoryId) => {
      const memory = itemMap[memoryId]
      if (!memory) return null
      return buildFilterViewData(items, mode, memory)
    },
    getCategoryViewData: (categoryId) => buildCategoryViewData(items, categoryId),
    errors: {
      flowers: flowersResult.status === 'rejected' ? flowersResult.reason : null,
      posts: postsResult.status === 'rejected' ? postsResult.reason : null,
      ai: aiResult.status === 'rejected' ? aiResult.reason : null,
    },
  }
}
