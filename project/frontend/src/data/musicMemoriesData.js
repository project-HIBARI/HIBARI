/** @param {string} filename */
function artistImageUrl(filename) {
  return `/images/artists/${filename}`
}

/**
 * Music Memories プラットフォーム上のアーティスト一覧（ファンクラブ入口 / 図鑑 / 診断の共通データ）
 * status: 'open' = 公開中 / 'soon' = 準備中
 * gender: 'male' | 'female' | 'group'
 * activeDecades: 活動が重なる年代の開始年配列（例: 1980 → 1980年代）
 */
export const MUSIC_MEMORIES_ARTISTS = [
  {
    id: 'kyu',
    name: '坂本九',
    nameEn: 'Sakamoto Kyu',
    tagline: '上を向いて歩こう、世界へ届けた歌',
    image: artistImageUrl('kyu.png'),
    status: 'soon',
    gender: 'male',
    activeDecades: [1950, 1960, 1970, 1980],
    activeStartYear: 1959,
    genres: ['ポップス', '歌謡曲'],
    featuredOrder: 1,
    recommendationTags: [
      'hope', 'uplifting', 'entertainment', 'classic', 'timeless', 'emotional',
      'kayokyoku', '1950s', '1960s', '1970s', '1980s', 'warm', 'gentle',
    ],
    resultCatchphrase: '世界へ届いた希望の歌を、いま聴きなおす',
    recommendationText:
      '明るい響きと希望のメッセージが、背中をやさしく押してくれます。',
  },
  {
    id: 'ozaki',
    name: '尾崎豊',
    nameEn: 'Ozaki Yutaka',
    tagline: '十五の夜から続く、魂の叫び',
    image: artistImageUrl('ozaki.png'),
    status: 'soon',
    gender: 'male',
    activeDecades: [1980, 1990],
    activeStartYear: 1983,
    genres: ['ロック', 'フォーク'],
    featuredOrder: 2,
    recommendationTags: [
      'youth', 'passionate', 'rebellious', 'emotional', 'powerful', 'hope',
      'ballad', 'dramatic', '1980s', '1990s', 'nostalgic',
    ],
    resultCatchphrase: '心の叫びをまっすぐ届ける、青春のカリスマ',
    recommendationText:
      '鮮烈な青春のメッセージが、いまの気持ちにまっすぐ響くはずです。',
  },
  {
    id: 'yujiro',
    name: '石原裕次郎',
    nameEn: 'Ishihara Yujiro',
    tagline: '太陽の男、昭和スターの記憶',
    image: artistImageUrl('yujiro.png'),
    status: 'soon',
    gender: 'male',
    activeDecades: [1950, 1960, 1970, 1980],
    activeStartYear: 1956,
    genres: ['歌謡曲', 'ムード歌謡'],
    featuredOrder: 3,
    recommendationTags: [
      'classic', 'cool', 'deep', 'entertainment', 'actor', 'elegant',
      'kayokyoku', '1950s', '1960s', '1970s', '1980s', 'stylish',
    ],
    resultCatchphrase: '大人の哀愁と華やかさをまとった、昭和のスター',
    recommendationText:
      '歌とスクリーンで輝いたスターの世界が、大人の気分に寄り添います。',
  },
  {
    id: 'hibari',
    name: '美空ひばり',
    nameEn: 'Misora Hibari',
    tagline: '昭和の歌姫、その声と軌跡をたどる',
    image: artistImageUrl('hibari.png'),
    status: 'open',
    siteId: 'hibari',
    gender: 'female',
    activeDecades: [1950, 1960, 1970, 1980],
    activeStartYear: 1949,
    genres: ['歌謡曲', '演歌'],
    featuredOrder: 4,
    recommendationTags: [
      'healing', 'warm', 'powerful', 'hope', 'emotional', 'gentle',
      'traditional', 'enka', 'kayokyoku', 'legend', 'timeless',
      '1940s', '1950s', '1960s', '1970s', '1980s', 'classic', 'elegant', 'entertainment',
    ],
    resultCatchphrase: '時代を越えて心を照らす、永遠の歌声',
    recommendationText:
      '温かさと力強さをあわせ持つ歌声が、あなたの心に寄り添ってくれるでしょう。',
  },
  {
    id: 'kiyoshiro',
    name: '忌野清志郎',
    nameEn: 'Imawano Kiyoshiro',
    tagline: 'RCから続く、ロックの不滅の魂',
    image: artistImageUrl('kiyoshiro.png'),
    status: 'soon',
    gender: 'male',
    activeDecades: [1970, 1980, 1990, 2000],
    activeStartYear: 1970,
    genres: ['ロック'],
    featuredOrder: 5,
    recommendationTags: [
      'rebellious', 'powerful', 'passionate', 'cool', 'urban', 'stylish',
      '1970s', '1980s', '1990s', 'versatile', 'dramatic',
    ],
    resultCatchphrase: '不滅のロック魂が、いまの気分を揺らす',
    recommendationText:
      '自由で力強い表現が、都会的でクールな音楽志向に合います。',
  },
  {
    id: 'hideki',
    name: '西城秀樹',
    nameEn: 'Saijo Hideki',
    tagline: 'ヤングマンの熱狂、永遠のアイドル',
    image: artistImageUrl('hideki.png'),
    status: 'soon',
    gender: 'male',
    activeDecades: [1970, 1980, 1990, 2000],
    activeStartYear: 1972,
    genres: ['ポップス', 'アイドル'],
    featuredOrder: 6,
    recommendationTags: [
      'entertainment', 'elegant', 'uplifting', 'youth', 'passionate',
      '1970s', '1980s', '1990s', 'stylish', 'hope',
    ],
    resultCatchphrase: '熱狂と華やかさをいまに残す、永遠のアイドル',
    recommendationText:
      '明るく華やかなエンターテインメントの魅力が、気分を高めてくれます。',
  },
  {
    id: 'keiko',
    name: '藤圭子',
    nameEn: 'Fuji Keiko',
    tagline: '圭子の夢は夜開ける、演歌の金字塔',
    image: artistImageUrl('keiko.png'),
    status: 'soon',
    gender: 'female',
    activeDecades: [1960, 1970, 1980],
    activeStartYear: 1969,
    genres: ['演歌'],
    featuredOrder: 7,
    recommendationTags: [
      'enka', 'traditional', 'emotional', 'delicate', 'dramatic', 'ballad',
      '1960s', '1970s', '1980s', 'healing', 'nostalgic',
    ],
    resultCatchphrase: '切なさと強さが交差する、演歌の金字塔',
    recommendationText:
      '繊細で情感豊かな演歌の世界が、いまの気持ちに深く響くでしょう。',
  },
  {
    id: 'hide',
    name: 'hide',
    nameEn: 'hide',
    tagline: 'X JAPAN、ヴィジュアルの革命児',
    image: artistImageUrl('hide.png'),
    status: 'soon',
    gender: 'male',
    activeDecades: [1980, 1990],
    activeStartYear: 1987,
    genres: ['ロック', 'ヴィジュアル系'],
    featuredOrder: 8,
    recommendationTags: [
      'passionate', 'rebellious', 'youth', 'powerful', 'dramatic', 'stylish',
      '1980s', '1990s', 'urban', 'cool',
    ],
    resultCatchphrase: 'ヴィジュアルの革命が残した、鮮烈な響き',
    recommendationText:
      '情熱と個性あふれる表現が、新しい出会いへのきっかけになります。',
  },
  {
    id: 'takajin',
    name: 'やしきたかじん',
    nameEn: 'Yashiki Takajin',
    tagline: '大阪の男、魂のバラードを紡ぐ',
    image: artistImageUrl('takajin.png'),
    status: 'soon',
    gender: 'male',
    activeDecades: [1970, 1980, 1990, 2000],
    activeStartYear: 1976,
    genres: ['歌謡曲', 'バラード'],
    featuredOrder: 9,
    recommendationTags: [
      'ballad', 'emotional', 'deep', 'classic', 'cool', 'warm',
      '1970s', '1980s', '1990s', 'kayokyoku', 'dramatic',
    ],
    resultCatchphrase: '魂のバラードが、静かに心へ染みる',
    recommendationText:
      '深い響きとバラードの情感が、落ち着いた音楽時間にぴったりです。',
  },
]

/**
 * 今日のアーティスト（紹介枠・新規集客用）
 * 公開中の美空ひばりファンクラブへ誘導するため、固定表示する。
 */
function pickTodaysArtist() {
  const artist = MUSIC_MEMORIES_ARTISTS.find((a) => a.id === 'hibari')
  return {
    ...artist,
    headline: artist.resultCatchphrase,
    blurb: artist.recommendationText,
  }
}

export const TODAYS_ARTIST = pickTodaysArtist()

/** Music Memory Book 紹介帯 — 複数アーティスト対応を見せるサムネイル */
export const MEMORY_BOOK_SHOWCASE_ARTISTS = MUSIC_MEMORIES_ARTISTS.slice(0, 6)

/** Music Memories オープンチャットのアーティストフィルタ */
export const PLATFORM_CHAT_ARTISTS = [
  { id: 'all', label: 'すべて' },
  { id: 'hibari', label: '美空ひばり' },
  { id: 'lounge', label: '広場' },
]

/** 図鑑 — 活動年代フィルタ選択肢 */
export const ARTIST_ENCYCLOPEDIA_DECADES = [
  { value: 'all', label: 'すべての年代' },
  { value: 1950, label: '1950年代' },
  { value: 1960, label: '1960年代' },
  { value: 1970, label: '1970年代' },
  { value: 1980, label: '1980年代' },
  { value: 1990, label: '1990年代' },
  { value: 2000, label: '2000年代以降' },
]

/** 図鑑 — 性別フィルタ */
export const ARTIST_ENCYCLOPEDIA_GENDERS = [
  { value: 'all', label: 'すべて' },
  { value: 'male', label: '男性' },
  { value: 'female', label: '女性' },
  { value: 'group', label: 'グループ' },
]

/** 図鑑 — 公開状態フィルタ */
export const ARTIST_ENCYCLOPEDIA_STATUSES = [
  { value: 'all', label: 'すべて' },
  { value: 'open', label: '公開中' },
  { value: 'soon', label: '準備中' },
]

/** 図鑑 — 並び順 */
export const ARTIST_ENCYCLOPEDIA_SORTS = [
  { value: 'featured', label: 'おすすめ順' },
  { value: 'name', label: '名前順' },
  { value: 'year-asc', label: '活動開始年が古い順' },
  { value: 'year-desc', label: '活動開始年が新しい順' },
]

export function decadeLabel(year) {
  if (year >= 2000) return '2000年代以降'
  return `${year}年代`
}

export function genderLabel(gender) {
  if (gender === 'male') return '男性'
  if (gender === 'female') return '女性'
  if (gender === 'group') return 'グループ'
  return ''
}

export function statusLabel(status) {
  if (status === 'open') return '公開中'
  if (status === 'soon') return '準備中'
  return ''
}
