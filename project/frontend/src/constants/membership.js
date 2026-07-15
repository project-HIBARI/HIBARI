/**
 * 会員区分・権限定義
 */

export const MEMBERSHIP = {
  GENERAL: 'general',
  PREMIUM: 'premium',
}

export const MEMBERSHIP_LABELS = {
  [MEMBERSHIP.GENERAL]: '一般会員',
  [MEMBERSHIP.PREMIUM]: 'プレミアム会員',
}

/** 権限キー */
export const PERMISSION = {
  NEWSLETTER: 'newsletter',
  TICKET_PREORDER: 'ticket_preorder',
  BOARD_POST: 'board_post',
  AI_CHAT: 'ai_chat',
  PREMIUM_VIDEO: 'premium_video',
  EXCLUSIVE_CONTENT: 'exclusive_content',
  AI_CHAT_UNLIMITED: 'ai_chat_unlimited',
  BOARD_POST_UNLIMITED: 'board_post_unlimited',
  PRIORITY_DISCOUNT: 'priority_discount',
  OPEN_CHAT: 'open_chat',
  AUDIO_DOWNLOAD: 'audio_download',
}

/** プラン別の利用可能権限 */
export const MEMBERSHIP_PERMISSIONS = {
  [MEMBERSHIP.GENERAL]: [
    PERMISSION.NEWSLETTER,
    PERMISSION.TICKET_PREORDER,
    PERMISSION.BOARD_POST,
    PERMISSION.AI_CHAT,
    PERMISSION.OPEN_CHAT,
  ],
  [MEMBERSHIP.PREMIUM]: [
    PERMISSION.NEWSLETTER,
    PERMISSION.TICKET_PREORDER,
    PERMISSION.BOARD_POST,
    PERMISSION.AI_CHAT,
    PERMISSION.OPEN_CHAT,
    PERMISSION.PREMIUM_VIDEO,
    PERMISSION.EXCLUSIVE_CONTENT,
    PERMISSION.AI_CHAT_UNLIMITED,
    PERMISSION.BOARD_POST_UNLIMITED,
    PERMISSION.PRIORITY_DISCOUNT,
    PERMISSION.AUDIO_DOWNLOAD,
  ],
}

export const MEMBERSHIP_PLANS = [
  {
    id: MEMBERSHIP.GENERAL,
    name: MEMBERSHIP_LABELS[MEMBERSHIP.GENERAL],
    price: '¥500',
    unit: '/ 月',
    features: [
      '月刊ニュースレター',
      'チケット先行予約',
      '掲示板投稿（月10回）',
      '月10回 AIひばり対話',
      'オープンチャット',
    ],
    locked: ['プレミアム限定映像', '限定コンテンツ', '優先申込＋会員割引', '高音質音声ダウンロード'],
  },
  {
    id: MEMBERSHIP.PREMIUM,
    name: MEMBERSHIP_LABELS[MEMBERSHIP.PREMIUM],
    price: '¥1,500',
    unit: '/ 月',
    features: [
      '一般会員特典すべて',
      'プレミアム限定映像',
      '限定コンテンツ',
      'AIひばり対話 無制限',
      '掲示板投稿 無制限',
      '優先申込＋会員割引',
      '高音質音声ダウンロード',
    ],
    locked: [],
    recommended: true,
  },
]

export const GENERAL_AI_CHAT_MONTHLY_LIMIT = 10
export const GENERAL_BOARD_POST_MONTHLY_LIMIT = 10
/** 非会員: 上限到達から解除までの日数 */
export const GUEST_USAGE_RESET_DAYS = 7
export const GUEST_AI_CHAT_LIMIT = 10
export const GUEST_BOARD_POST_LIMIT = 10

export function normalizeMembership(value) {
  return value === MEMBERSHIP.PREMIUM ? MEMBERSHIP.PREMIUM : MEMBERSHIP.GENERAL
}

export function hasPermission(membership, permission) {
  const tier = normalizeMembership(membership)
  return MEMBERSHIP_PERMISSIONS[tier]?.includes(permission) ?? false
}

export function isPremiumMember(membership) {
  return normalizeMembership(membership) === MEMBERSHIP.PREMIUM
}

export function getAiChatLimit(membership) {
  return isPremiumMember(membership) ? null : GENERAL_AI_CHAT_MONTHLY_LIMIT
}

export function getBoardPostLimit(membership) {
  return isPremiumMember(membership) ? null : GENERAL_BOARD_POST_MONTHLY_LIMIT
}
