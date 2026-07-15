/**
 * AI未使用時のフォールバック振り返り文を生成
 */
export function buildYearRecapFallback({ year, summary, timeline }) {
  const total = summary?.total ?? timeline?.length ?? 0
  if (!total) {
    return `${year}年の思い出はまだ記録されていません。\n\n献花や思い出投稿を送ると、ここに1年の振り返りが表示されます。美空ひばりとの大切な時間を、少しずつアルバムに残していきましょう。`
  }

  const months = [...new Set((timeline || []).map((t) => t.monthLabel).filter(Boolean))]
  const monthText = months.length ? `${months.join('、')}など` : '一年を通して'
  const highlights = (timeline || []).slice(0, 5).map((t) => `・${t.date} ${t.title}`).join('\n')

  return [
    `${year}年、あなたは美空ひばりとの思い出を${total}件、アルバムに残しました。`,
    '',
    `献花 ${summary?.flowers ?? 0}件、思い出投稿 ${summary?.posts ?? 0}件と、${monthText}にわたって想いが積み重なっています。`,
    '',
    '【この年のハイライト】',
    highlights || '・記録された思い出を大切に保管しています',
    '',
    '一つひとつの瞬間が、あなただけのMusic Memory Bookを彩っています。来年も、歌とともに温かい思い出を重ねていきましょう。',
  ].join('\n')
}
