/**
 * オープニング映像用の定数・補間関数
 * （元 React opening-film.jsx から移植）
 */

export const ASSETS = {
  stageBg: { type: 'svg', src: null },
  photoFrames: [
    { src: null, caption: 'デビュー 一九四九年', year: 1949 },
    { src: null, caption: 'リンゴ追分 一九五二年', year: 1952 },
    { src: null, caption: '柔 一九六五年', year: 1965 },
    { src: null, caption: '不死鳥コンサート 一九八八年', year: 1988 },
    { src: null, caption: '川の流れのように 一九八九年', year: 1989 },
  ],
  headlines: [
    { year: 1949, song: '悲しき口笛', title: '「悲しき口笛」空前の大ヒット', sub: '十二歳の天才少女、全国区へ' },
    { year: 1952, song: 'リンゴ追分', title: '「リンゴ追分」戦後最大記録', sub: '七十万枚、昭和の伝説となる' },
    { year: 1965, song: '柔', title: '第七回レコード大賞 グランプリ', sub: '「柔」——歌謡界の頂点に立つ' },
    { year: 1988, song: '不死鳥コンサート', title: '東京ドーム 五万人 熱狂', sub: '不死鳥コンサート、伝説の一夜' },
  ],
}

export const SCENES = [
  { id: 'curtain', in: 0.0, hold: 0.055, out: 0.2, end: 0.25 },
  { id: 'record', in: 0.21, hold: 0.26, out: 0.71, end: 0.75 },
  { id: 'signature', in: 0.71, hold: 0.755, out: 0.97, end: 1.0 },
]

export function sceneOpacity(t, scene) {
  if (t < scene.in || t > scene.end) return 0
  if (t < scene.hold) return (t - scene.in) / (scene.hold - scene.in)
  if (t < scene.out) return 1
  return 1 - (t - scene.out) / (scene.end - scene.out)
}

export function localT(t, scene) {
  return Math.max(0, Math.min(1, (t - scene.hold) / (scene.out - scene.hold)))
}

export function itemOpacity(lt, index, total, options = {}) {
  const stagger = options.stagger !== undefined ? options.stagger : 1 / total
  const window_ = options.window !== undefined ? options.window : stagger * 2
  const fadeDur = options.fadeDur !== undefined ? options.fadeDur : 0.07
  const start = index * stagger
  const end = Math.min(start + window_, 1.0)
  const fadeIn = start + fadeDur
  const fadeOut = end - fadeDur
  if (lt < start || lt > end) return 0
  if (lt < fadeIn) return (lt - start) / fadeDur
  if (lt < fadeOut) return 1
  return (end - lt) / fadeDur
}

export const PHOTO_OFFSETS_PC = [
  { left: '4%', top: '11%', rotate: 2, scale: 1.0, entryX: 30, entryY: -12, overlap: false, landscape: false },
  { right: '28%', top: '8%', rotate: -2, scale: 0.96, entryX: -20, entryY: -18, overlap: true, landscape: true },
  { left: '26%', top: '62%', rotate: -1, scale: 1.02, entryX: 18, entryY: 22, overlap: true, landscape: false },
  { right: '4%', top: '54%', rotate: 3, scale: 0.97, entryX: -28, entryY: 14, overlap: false, landscape: true },
  { left: '3%', top: '40%', rotate: 1, scale: 1.0, entryX: 24, entryY: 8, overlap: false, landscape: false },
]

export const PHOTO_OFFSETS_SP = [
  { bottom: '14%', left: '4%', rotate: 2, scale: 1.0, entryX: 18, entryY: 22 },
  { bottom: '14%', left: '50%', rotate: -2, scale: 0.95, entryX: -18, entryY: 22 },
  { bottom: '14%', left: '22%', rotate: 1, scale: 1.02, entryX: 0, entryY: 28 },
  { bottom: '14%', left: '64%', rotate: -3, scale: 0.98, entryX: -16, entryY: 22 },
  { bottom: '14%', left: '36%', rotate: 2, scale: 1.0, entryX: 10, entryY: 28 },
]

export const HEADLINE_OFFSETS_PC = [
  { right: '27%', top: '64%', rotate: -2, entryX: -22, entryY: 12, overlap: true },
  { left: '3%', top: '52%', rotate: 1, entryX: 28, entryY: 6, overlap: false },
  { left: '24%', top: '10%', rotate: -1, entryX: 16, entryY: -18, overlap: true },
  { right: '3%', top: '14%', rotate: 2, entryX: -26, entryY: -14, overlap: false },
]

export const HEADLINE_OFFSETS_SP = [
  { top: '8%', left: '4%', rotate: -2, entryX: 10, entryY: -18 },
  { top: '8%', left: '44%', rotate: 1, entryX: -10, entryY: -18 },
  { top: '8%', left: '16%', rotate: -1, entryX: 10, entryY: -18 },
  { top: '8%', left: '58%', rotate: 2, entryX: -10, entryY: -18 },
]

export const TOUCH_LT = 0.14
