import { pageImageUrl } from '../lib/pageImages.js'

/** @param {string} filename */
function artistImageUrl(filename) {
  return `/images/artists/${filename}`
}

/** Music Memories プラットフォーム上のファンクラブ一覧 */
export const MUSIC_MEMORIES_ARTISTS = [
  {
    id: 'hibari',
    name: '美空ひばり',
    nameEn: 'Misora Hibari',
    tagline: '昭和の歌姫、その声と軌跡をたどる',
    image: pageImageUrl('misorahibari-profile-hero.png'),
    status: 'open',
    siteId: 'hibari',
  },
  {
    id: 'ozaki',
    name: '尾崎豊',
    nameEn: 'Ozaki Yutaka',
    tagline: '十五の夜から続く、魂の叫び',
    image: artistImageUrl('ozaki.png'),
    status: 'soon',
  },
  {
    id: 'yujiro',
    name: '石原裕次郎',
    nameEn: 'Ishihara Yujiro',
    tagline: '太陽の男、昭和スターの記憶',
    image: artistImageUrl('yujiro.png'),
    status: 'soon',
  },
  {
    id: 'kyu',
    name: '坂本九',
    nameEn: 'Sakamoto Kyu',
    tagline: '上を向いて歩こう、世界へ届けた歌',
    image: artistImageUrl('kyu.png'),
    status: 'soon',
  },
  {
    id: 'kiyoshiro',
    name: '忌野清志郎',
    nameEn: 'Imawano Kiyoshiro',
    tagline: 'RCから続く、ロックの不滅の魂',
    image: artistImageUrl('kiyoshiro.png'),
    status: 'soon',
  },
  {
    id: 'hideki',
    name: '西城秀樹',
    nameEn: 'Saijo Hideki',
    tagline: 'ヤングマンの熱狂、永遠のアイドル',
    image: artistImageUrl('hideki.png'),
    status: 'soon',
  },
  {
    id: 'keiko',
    name: '藤圭子',
    nameEn: 'Fuji Keiko',
    tagline: '圭子の夢は夜開ける、演歌の金字塔',
    image: artistImageUrl('keiko.png'),
    status: 'soon',
  },
  {
    id: 'hide',
    name: 'hide',
    nameEn: 'hide',
    tagline: 'X JAPAN、ヴィジュアルの革命児',
    image: artistImageUrl('hide.png'),
    status: 'soon',
  },
  {
    id: 'takajin',
    name: 'やしきたかじん',
    nameEn: 'Yashiki Takajin',
    tagline: '大阪の男、魂のバラードを紡ぐ',
    image: artistImageUrl('takajin.png'),
    status: 'soon',
  },
]

/**
 * 今日のアーティスト（日替わり紹介枠・新規集客用）
 * 暫定: 美空ひばりを固定表示。後日ローテーションに差し替え予定。
 */
export const TODAYS_ARTIST = {
  ...MUSIC_MEMORIES_ARTISTS.find((a) => a.id === 'hibari'),
  headline: '昭和の歌姫を、いま改めて知る',
  blurb:
    '可憐さと力強さをあわせ持つ歌声で、時代を超えて愛され続ける美空ひばり。ファンクラブでは楽曲・映像・思い出の記録にふれられます。',
}

/** Music Memories オープンチャットのアーティストフィルタ */
export const PLATFORM_CHAT_ARTISTS = [
  { id: 'all', label: 'すべて' },
  { id: 'hibari', label: '美空ひばり' },
  { id: 'lounge', label: '広場' },
]
