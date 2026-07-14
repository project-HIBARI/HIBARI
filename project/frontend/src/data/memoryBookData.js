/**
 * Music Memory Book — デモ用データ
 */

export const MEMORY_BOOK_SUMMARY = {
  total: 86,
  startedAt: '2026.01.01',
  categories: {
    flowers: 24,
    posts: 18,
    songs: 32,
    aiChats: 12,
  },
}

export const MEMORY_BOOK_CATEGORIES = [
  {
    id: 'flowers',
    title: '献花の記録',
    count: 24,
    desc: 'あなたが捧げた献花の記録を振り返ります。',
    icon: 'flower',
    tone: 'pink',
  },
  {
    id: 'posts',
    title: '思い出の投稿',
    count: 18,
    desc: 'あなたが投稿した思い出のエピソードです。',
    icon: 'chat',
    tone: 'warm',
  },
  {
    id: 'songs',
    title: 'お気に入り楽曲',
    count: 32,
    desc: 'あなたが登録したお気に入りの楽曲一覧です。',
    icon: 'music',
    tone: 'purple',
  },
  {
    id: 'ai',
    title: 'AIとの会話',
    count: 12,
    desc: 'AI美空ひばりとの会話履歴を振り返ります。',
    icon: 'chat',
    tone: 'gold',
  },
  {
    id: 'albums',
    title: '年別アルバム',
    count: null,
    desc: '年ごとの思い出をアルバム形式で確認できます。',
    icon: 'calendar',
    tone: 'shelf',
  },
]

export const MEMORY_BOOK_YEARS = [
  { year: 2026, total: 86, tone: 'purple' },
  { year: 2025, total: 64, tone: 'blue' },
  { year: 2024, total: 48, tone: 'green' },
  { year: 2023, total: 32, tone: 'brown' },
]

export const MEMORY_BOOK_YEAR_2026 = {
  year: 2026,
  summary: {
    flowers: 24,
    posts: 18,
    songs: 32,
    aiChats: 12,
    total: 86,
  },
  timeline: [
    {
      id: 'mb-2026-01',
      month: 1,
      monthLabel: '1月',
      category: 'flowers',
      categoryLabel: '献花の記録',
      title: '白百合の花束を献花しました',
      date: '2026.01.01',
      dateDisplay: '2026.01.01（木）',
      description: '命日の日に、白百合の花束を献花しました。',
      icon: 'flower',
    },
    {
      id: 'mb-2026-03',
      month: 3,
      monthLabel: '3月',
      category: 'posts',
      categoryLabel: '思い出の投稿',
      title: '「東京キッド」の思い出を投稿しました',
      date: '2026.03.18',
      dateDisplay: '2026.03.18（水）',
      description: '初めて美空ひばりさんの歌を聴いた日のことを投稿しました。',
      icon: 'chat',
    },
    {
      id: 'mb-2026-06-song',
      month: 6,
      monthLabel: '6月',
      category: 'songs',
      categoryLabel: 'お気に入り楽曲',
      title: '「川の流れのように」をお気に入りに登録しました',
      date: '2026.06.15',
      dateDisplay: '2026.06.15（月）',
      description: '何度聴いても心に響く名曲です。',
      icon: 'music',
    },
    {
      id: 'mb-2026-08',
      month: 8,
      monthLabel: '8月',
      category: 'ai',
      categoryLabel: 'AIとの会話',
      title: 'AI美空ひばりと会話しました',
      date: '2026.08.12',
      dateDisplay: '2026.08.12（水）',
      description: 'AI美空ひばりさんと夏の思い出について語り合いました。',
      icon: 'chat',
    },
    {
      id: 'mb-2026-12',
      month: 12,
      monthLabel: '12月',
      category: 'posts',
      categoryLabel: '思い出の投稿',
      title: '紅白歌合戦の思い出を投稿しました',
      date: '2026.12.31',
      dateDisplay: '2026.12.31（木）',
      description: '毎年の紅白を見るのが楽しみです。',
      icon: 'chat',
    },
  ],
}

export const MEMORY_BOOK_DETAIL_SAMPLE = {
  id: 'mb-2026-06-flower',
  category: 'flowers',
  categoryLabel: '献花の記録',
  title: '白百合の花束を献花しました',
  date: '2026.06.20',
  dateDisplay: '2026.06.20（土）',
  location: '川のほとり記念館',
  visibility: '自分のみ',
  body: `命日の日に、美空ひばりさんに白百合の花束を献花しました。
今年もこうして想いを届けることができて、心が温かくなりました。
いつも歌声に励まされています。本当にありがとうございます。`,
  mainImage: '/images/flowers/yuri-white.png',
  photos: [
    { src: '/images/flowers/yuri-white.png', alt: '献花写真' },
    { src: '/images/page/misorahibari-chair.png', alt: '記念館周辺' },
    { src: '/images/page/kenka-image.png', alt: '花束のアップ' },
    { src: '/images/page/misorahibari-profile-hero.png', alt: '記念館外観' },
  ],
  aiMessage: `今年もひばりさんへ想いを届けられて素敵ですね。
白百合の花言葉は「純潔」「無垢」。
ひばりさんの歌声のように、これからもあなたの心に寄り添い続けます。`,
  memo: '命日に献花をしました。白百合の花がとてもきれいでした。',
  year: 2026,
  month: 6,
  monthLabel: '6月',
  indexInMonth: 1,
  totalInMonth: 4,
  prevId: null,
  nextId: 'mb-2026-06-song',
}
