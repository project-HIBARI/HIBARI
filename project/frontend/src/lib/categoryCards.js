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
    id: 'map',
    title: 'ゆかりの地',
    desc: '各地に残る足跡をたどる',
    image: PAGE_IMAGES.events,
    alt: 'ゆかりの地',
    action: 'navigate',
    target: 'map',
  },
  {
    id: 'memories',
    title: '思い出',
    desc: 'ファンが綴る記憶と記録',
    image: PAGE_IMAGES.gallery,
    alt: '思い出',
    action: 'navigate',
    target: 'memories',
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
