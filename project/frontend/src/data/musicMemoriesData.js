import { pageImageUrl } from '../lib/pageImages.js'

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
    id: 'placeholder-1',
    name: 'Coming Soon',
    nameEn: 'Artist',
    tagline: '新しいレジェンドのファンクラブを準備中',
    image: null,
    status: 'soon',
  },
  {
    id: 'placeholder-2',
    name: 'Coming Soon',
    nameEn: 'Artist',
    tagline: '音楽の記憶を、これからも紡いでいきます',
    image: null,
    status: 'soon',
  },
]

/** Music Memories オープンチャットのアーティストフィルタ */
export const PLATFORM_CHAT_ARTISTS = [
  { id: 'all', label: 'すべて' },
  { id: 'hibari', label: '美空ひばり' },
  { id: 'lounge', label: '広場' },
]
