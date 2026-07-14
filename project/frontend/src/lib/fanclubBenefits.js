/**
 * 会員特典 feature キー → ファンクラブ会員サイト内セクション
 */
export const BENEFIT_SECTIONS = {
  news: 'newsletter',
  events: 'events',
  'priority-events': 'priority-events',
  board: 'board',
  ai: 'chat',
  disco: 'premium-video',
  pv: 'premium-video',
  gallery: 'exclusive-content',
  'open-chat': 'open-chat',
}

export function benefitToSection(feature) {
  return BENEFIT_SECTIONS[feature] || null
}
