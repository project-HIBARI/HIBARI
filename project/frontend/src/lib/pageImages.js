/**
 * ページメインビジュアル画像パス（差し替えはここを更新）
 * 透過PNGは scripts/process-transparent-images.py で背景のみ除去（サイズ維持）
 */
export const PAGE_IMAGES = {
  about: 'flower-image.png',
  disco: 'cd-image.png',
  gallery: 'misorahibari-image.png',
  events: 'misorahibari-chair.png',
  fanclub: 'fanclub-image.png',
  benefits: 'benefits-image.png',
}

/** ページヒーロー共通メインビジュアル */
export const PAGE_HERO_IMAGE = 'misorahibari-mike-image.png'

/** @param {string} filename */
export function pageImageUrl(filename) {
  return `/images/page/${filename}`
}
