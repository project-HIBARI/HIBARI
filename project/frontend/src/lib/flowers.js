/**
 * 献花 — 花の種類定義（画像・表示名を一元管理）
 */
export const FLOWER_TYPES = [
  { id: 'yuri', name: '白百合', image: '/images/flowers/yuri-white.png', emoji: '🌸' },
  { id: 'bara', name: '紅薔薇', image: '/images/flowers/bara-red.png', emoji: '🌹' },
  { id: 'kiku', name: '白菊', image: '/images/flowers/kiku-white.png', emoji: '🌼' },
  { id: 'kasumisou', name: 'かすみ草', image: '/images/flowers/kasumisou.png', emoji: '🌿' },
  { id: 'kikyo', name: '桔梗', image: '/images/flowers/kikyo.png', emoji: '🔔' },
  { id: 'kotemari', name: '小手毬', image: '/images/flowers/kotemari.png', emoji: '🍃' },
]

export function flowerByName(name) {
  return FLOWER_TYPES.find((f) => f.name === name) ?? FLOWER_TYPES[0]
}

export function flowerEmoji(name) {
  return flowerByName(name).emoji
}

export function flowerImage(name) {
  return flowerByName(name).image
}

export function formatOfferingDate(isoOrStr) {
  if (!isoOrStr) return ''
  const d = new Date(isoOrStr)
  if (Number.isNaN(d.getTime())) return String(isoOrStr)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}.${m}.${day}`
}

export function mapOfferingToCard(row) {
  return {
    id: row.flower_offering_id,
    name: row.name || '匿名のファン',
    location: row.location || '',
    date: formatOfferingDate(row.offered_at),
    flower: row.flower_type,
    body: row.content,
  }
}
