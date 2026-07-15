/**
 * 年別アルバムの共有テキストを生成
 */
export function buildYearAlbumSharePayload({ year, summary, timeline }) {
  const total = summary?.total ?? timeline?.length ?? 0
  const title = `${year}年の Music Memories`
  const text = [
    `${year}年の美空ひばりとの思い出アルバム`,
    `献花 ${summary?.flowers ?? 0}件 / 思い出投稿 ${summary?.posts ?? 0}件 / 合計 ${total}件`,
    '',
    'Music Memory Book で思い出を振り返りましょう。',
  ].join('\n')
  const url = window.location.href

  return { title, text, url }
}

/**
 * Web Share API またはクリップボードでアルバムを共有
 */
export async function shareYearAlbum(payload) {
  if (navigator.share) {
    try {
      await navigator.share({
        title: payload.title,
        text: payload.text,
        url: payload.url,
      })
      return { method: 'share' }
    } catch (err) {
      if (err?.name === 'AbortError') {
        return { method: 'cancelled' }
      }
    }
  }

  const copyText = `${payload.text}\n${payload.url}`
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(copyText)
    return { method: 'clipboard' }
  }

  throw new Error('共有機能を利用できません。')
}
