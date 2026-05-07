/**
 * 美空ひばりファンサイト用ユーティリティ
 * - 日付計算・今日の一曲など
 */
import { HIBARU_DATA } from '../data/hibaruData.js'

/** 指定月日までの日数（今年過ぎていれば翌年） */
export function daysUntil(month, day) {
  const now = new Date()
  let target = new Date(now.getFullYear(), month - 1, day)
  if (target <= now) target.setFullYear(now.getFullYear() + 1)
  return Math.ceil((target - now) / 86400000)
}

/** 日付シードでディスコグラフィから1曲選ぶ */
export function todaysSong() {
  const d = new Date()
  const seed = d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate()
  const list = HIBARU_DATA.discography
  return list[seed % list.length]
}

/** 朱色ボタン（主要 CTA） */
export const btnBeni = {
  background: 'var(--beni-700)',
  color: 'var(--paper-50)',
  border: '1px solid var(--kin-500)',
  padding: '14px 28px',
  fontFamily: 'var(--ff-mincho)',
  fontSize: '13px',
  letterSpacing: '0.2em',
  cursor: 'pointer',
  display: 'inline-flex',
  alignItems: 'center',
  gap: '10px',
}

/** ゴースト（線枠）ボタン */
export const btnGhost = {
  background: 'transparent',
  color: 'var(--paper-100)',
  border: '1px solid var(--paper-300)',
  padding: '12px 24px',
  fontFamily: 'var(--ff-mincho)',
  fontSize: '13px',
  letterSpacing: '0.2em',
  cursor: 'pointer',
}

/** ヘッダー内の小ボタン */
export const hdrBtn = {
  background: 'transparent',
  border: '1px solid rgba(201,169,97,0.4)',
  color: 'var(--paper-200)',
  padding: '6px 14px',
  cursor: 'pointer',
  fontFamily: 'var(--ff-mincho)',
  fontSize: '12px',
  letterSpacing: '0.15em',
  minHeight: '36px',
}

/** 暗背景フォーム入力 */
export const inputDark = {
  background: 'rgba(10,6,4,0.6)',
  border: '1px solid rgba(201,169,97,0.3)',
  color: 'var(--paper-100)',
  padding: '10px 12px',
  fontFamily: 'var(--ff-serif)',
  fontSize: '13px',
  outline: 'none',
  width: '100%',
}
