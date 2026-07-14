/**
 * Music Memories / 美空ひばり ファンクラブ用ユーティリティ
 * - 日付計算・今日の一曲・共通スタイルオブジェクト
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

/** 紫ボタン（ライトテーマ主要 CTA） */
export const btnPrimary = {
  background: 'var(--murasaki-700)',
  color: '#fff',
  border: '1px solid var(--murasaki-800)',
  padding: '14px 28px',
  fontFamily: 'var(--ff-sans-jp)',
  fontSize: '13px',
  letterSpacing: '0.1em',
  cursor: 'pointer',
  display: 'inline-flex',
  alignItems: 'center',
  gap: '10px',
  borderRadius: 'var(--site-radius-sm)',
  boxShadow: '0 2px 8px rgba(93, 58, 107, 0.2)',
}

/** 線枠ボタン（ライトテーマ） */
export const btnOutline = {
  background: 'var(--site-surface)',
  color: 'var(--murasaki-700)',
  border: '1px solid var(--murasaki-400)',
  padding: '12px 24px',
  fontFamily: 'var(--ff-sans-jp)',
  fontSize: '13px',
  letterSpacing: '0.1em',
  cursor: 'pointer',
  borderRadius: 'var(--site-radius-sm)',
}

/** ゴースト（透明枠）ボタン — ライトテーマ */
export const btnGhost = {
  background: 'transparent',
  color: 'var(--site-text-muted)',
  border: '1px solid var(--site-border-strong)',
  padding: '12px 24px',
  fontFamily: 'var(--ff-sans-jp)',
  fontSize: '13px',
  letterSpacing: '0.1em',
  cursor: 'pointer',
  borderRadius: 'var(--site-radius-sm)',
}

/** 朱色ボタン — レガシー領域（思い出・献花等）向け */
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

/** ヘッダー内の小ボタン — ライトテーマ */
export const hdrBtn = {
  background: 'var(--site-surface)',
  border: '1px solid var(--site-border-strong)',
  color: 'var(--site-text-muted)',
  padding: '6px 14px',
  cursor: 'pointer',
  fontFamily: 'var(--ff-sans-jp)',
  fontSize: '12px',
  letterSpacing: '0.06em',
  minHeight: '36px',
  borderRadius: 'var(--site-radius-sm)',
}

/** ライト背景フォーム入力 */
export const inputLight = {
  background: 'var(--site-surface)',
  border: '1px solid var(--site-border-strong)',
  color: 'var(--site-text)',
  padding: '10px 12px',
  fontFamily: 'var(--ff-serif)',
  fontSize: '13px',
  outline: 'none',
  width: '100%',
  borderRadius: 'var(--site-radius-sm)',
}

/** 暗背景フォーム入力 — レガシー領域向け */
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
