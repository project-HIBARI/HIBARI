import { PAGE_IMAGES } from './pageImages.js'

/** ホーム・歩み・ディスコグラフィ・献花・思い出ページ下部の共通導線カード */
export const HOME_CATEGORY_CARDS = [
  {
    id: 'profile',
    title: '美空ひばりについて',
    desc: '彼女の人生と軌跡',
    image: PAGE_IMAGES.about,
    alt: '美空ひばりについて',
    action: 'navigate',
    target: 'profile',
  },
  {
    id: 'disco',
    title: 'ディスコグラフィー',
    desc: '楽曲・アルバム一覧',
    image: PAGE_IMAGES.disco,
    alt: 'ディスコグラフィー',
    action: 'navigate',
    target: 'disco',
  },
  {
    id: 'gallery',
    title: 'ギャラリー',
    desc: '写真でたどる軌跡',
    image: PAGE_IMAGES.gallery,
    alt: 'ギャラリー',
    action: 'coming-soon',
    target: 'gallery',
  },
  {
    id: 'events',
    title: 'イベント情報',
    desc: 'コンサート・企画展など',
    image: PAGE_IMAGES.events,
    alt: 'イベント情報',
    action: 'coming-soon',
    target: 'events',
  },
  {
    id: 'fanclub',
    title: 'ファンクラブ',
    desc: '入会・会員特典',
    image: PAGE_IMAGES.fanclub,
    alt: 'ファンクラブ',
    action: 'coming-soon',
    target: 'fanclub',
  },
]
