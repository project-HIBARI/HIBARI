import { isPremiumMember } from '../constants/membership.js'

/**
 * Music Memory Book — 会員区分ごとの利用可否
 */
export function getMemoryBookAccess(membership) {
  const isPremium = isPremiumMember(membership)

  return {
    isPremium,
    canExportPdf: isPremium,
    canShareAlbum: isPremium,
    canAiRecap: isPremium,
    canChangeCover: isPremium,
    canViewAllYearAlbums: isPremium,
    limitNotice:
      '一般会員は当年のアルバム閲覧と思い出の確認までご利用いただけます。PDF保存・シェア・AI振り返り・表紙変更はプレミアム会員限定です。',
    premiumFeatureNotice: 'この機能はプレミアム会員限定です。',
  }
}

export function canViewMemoryBookYear(access, year) {
  if (access.isPremium) return true
  return Number(year) === new Date().getFullYear()
}
