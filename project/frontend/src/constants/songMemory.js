/**
 * 楽曲の思い出（同じ曲で泣いた人マッチング）の種類・公開範囲
 */
export const MEMORY_TYPES = [
  { value: 'tears', icon: 'tear', label: '涙した' },
  { value: 'nostalgic', icon: 'nostalgic', label: '懐かしい' },
  { value: 'loved_one', icon: 'loved-one', label: '大切な人を想う' },
  { value: 'energized', icon: 'energized', label: '元気をもらった' },
  { value: 'special_moment', icon: 'special-moment', label: '特別な瞬間' },
]

export const VISIBILITY_OPTIONS = [
  { value: 'public', label: '公開' },
  { value: 'members', label: '会員のみ' },
  { value: 'private', label: '自分のみ' },
]

export function memoryTypeMeta(type) {
  return MEMORY_TYPES.find((m) => m.value === type) || null
}
