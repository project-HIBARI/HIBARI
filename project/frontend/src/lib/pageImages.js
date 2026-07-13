/**
 * ページメインビジュアル画像パス（差し替えはここを更新）
 * 透過PNGは scripts/process-transparent-images.py で背景のみ除去（サイズ維持）
 */
export const PAGE_IMAGES = {
  about: 'flower-image.png',
  disco: 'cd-image.png',
  gallery: 'misorahibari-image.png',
  events: 'misorahibari-chair.png',
  fanclub: 'fanlogo.png',
  /** 献花ページ — 花選択ボタン用ブーケ画像 */
  kenka: 'kenka-image.png',
  benefits: 'benefits-image.png',
}

/** ページヒーロー共通メインビジュアル */
export const PAGE_HERO_IMAGE = 'misorahibari-mike-image.png'

/** 歩みページヒーロー肖像 */
export const PROFILE_HERO_IMAGE = 'misorahibari-profile-hero.png'

/** 歩みページサイドバー肖像 */
export const PROFILE_SIDEBAR_IMAGE = 'misorahibari-profile-sidebar.png'

/** @param {string} filename */
export function pageImageUrl(filename) {
  return `/images/page/${filename}`
}
