/**
 * アーティスト間の曲の繋がり (Cross-Artist Connections) データ
 * 同じ作詞家・作曲家が Music Memories ロースター内の複数アーティストに
 * 楽曲提供している実例。作詞・作曲者名は Wikipedia 日本語版・歌ネット等で確認済み。
 *
 * サイトのテーマは「既に亡くなったアーティスト」を扱うことであり、これは
 * ロースターに掲載するアーティスト本人（MUSIC_MEMORIES_ARTISTS）にのみ適用される。
 * 楽曲の作詞家・作曲家（脇役のクレジット）は存命でも構わない。
 *
 * 各エントリは「美空ひばりの楽曲（起点 = originSong）」を起点に、同じクリエイターが
 * 手がけた他アーティストの楽曲（targetSongs）へ辿る構造になっている。
 * artistId は musicMemoriesData.js の MUSIC_MEMORIES_ARTISTS の id と対応させ、
 * アーティスト名・画像はそちらから解決する（データの重複を避けるため）。
 *
 * 同じクリエイターでも起点となるひばりの楽曲が異なれば、別エントリ（別id）として
 * 追加できる（例: 同じ作詞家でも「旅人」起点と別の曲起点でタブを分けられる）。
 *
 * featured: true の項目はホーム(PageMusicMemories)にも代表例として表示される。
 * 「曲の繋がり」専用ページ(PageMusicConnections)では featured の有無に関わらず全件を表示する。
 */
export const CROSS_ARTIST_CONNECTIONS = [
  {
    id: 'tabibito',
    originSong: { artistId: 'hibari', title: '旅人', year: 1971, lyric: '阿久悠', music: '村井邦彦' },
    creator: '阿久悠',
    creatorRole: '作詞家',
    featured: true,
    note: '昭和を代表する稀代の作詞家。ジャンルを問わず数多くのスターに詞を提供した。',
    targetSongs: [
      { artistId: 'yujiro', title: '黎明', year: 1984, lyric: '阿久悠', music: '三木たかし' },
      { artistId: 'hideki', title: '若き獅子たち', year: 1976, lyric: '阿久悠', music: '三木たかし' },
      { artistId: 'keiko', title: '京都から博多まで', year: 1972, lyric: '阿久悠', music: '猪俣公章' },
    ],
  },
  {
    id: 'sakura-no-uta-miki',
    originSong: { artistId: 'hibari', title: 'さくらの唄', year: 1976, lyric: 'なかにし礼', music: '三木たかし' },
    creator: '三木たかし',
    creatorRole: '作曲家',
    featured: true,
    note: '阿久悠となかにし礼という二大作詞家の名曲を数多く手がけた作曲家。',
    targetSongs: [
      { artistId: 'yujiro', title: '黎明', year: 1984, lyric: '阿久悠', music: '三木たかし' },
      { artistId: 'hideki', title: '若き獅子たち', year: 1976, lyric: '阿久悠', music: '三木たかし' },
    ],
  },
  {
    id: 'sakura-no-uta-nakanishi',
    originSong: { artistId: 'hibari', title: 'さくらの唄', year: 1976, lyric: 'なかにし礼', music: '三木たかし' },
    creator: 'なかにし礼',
    creatorRole: '作詞家',
    featured: true,
    note: '情感豊かな詞世界で知られる作詞家・作家。晩年まで数々の名曲を手がけた。',
    targetSongs: [
      { artistId: 'yujiro', title: 'わが人生に悔いなし', year: 1987, lyric: 'なかにし礼', music: '加藤登紀子' },
    ],
  },
  {
    id: 'wakaretemo-arigatou',
    originSong: { artistId: 'hibari', title: '別れてもありがとう', year: 1969, lyric: '三浦康照', music: '猪俣公章' },
    creator: '猪俣公章',
    creatorRole: '作曲家',
    featured: true,
    note: '演歌・歌謡曲の名曲を数多く手がけた昭和の作曲家。',
    targetSongs: [
      { artistId: 'keiko', title: '京都から博多まで', year: 1972, lyric: '阿久悠', music: '猪俣公章' },
    ],
  },
  {
    id: 'kawa-no-nagareno-yoni',
    originSong: { artistId: 'hibari', title: '川の流れのように', year: 1989, lyric: '秋元康', music: '見岳章' },
    creator: '秋元康',
    creatorRole: '作詞家',
    featured: false,
    note: '数多くのアイドル・歌手を手がけた作詞家。両曲とも本人の生前最後のシングルとなった。',
    targetSongs: [
      { artistId: 'takajin', title: 'その時の空', year: 2010, lyric: '秋元康', music: '小室哲哉' },
    ],
  },
  {
    id: 'ue-wo-muite-arukou',
    originSong: { artistId: 'hibari', title: '上を向いて歩こう(カバー)', year: 1975, lyric: '永六輔', music: '中村八大' },
    creator: '永六輔 & 中村八大',
    creatorRole: '作詞・作曲(同一楽曲のカバーで繋がる例)',
    featured: false,
    note: '坂本九のオリジナルを、美空ひばり・忌野清志郎(RCサクセション)がそれぞれカバーした一曲。同じ楽曲が世代を超えて歌い継がれた例。',
    targetSongs: [
      { artistId: 'kyu', title: '上を向いて歩こう', year: 1961, lyric: '永六輔', music: '中村八大' },
      { artistId: 'kiyoshiro', title: '上を向いて歩こう(カバー)', year: 1979, lyric: '永六輔', music: '中村八大' },
    ],
  },
  {
    id: 'inori',
    originSong: { artistId: 'hibari', title: '熱祷(いのり)', year: 1968, lyric: '川内康範', music: '小野透' },
    creator: '川内康範',
    creatorRole: '作詞家',
    featured: false,
    note: '「おふくろさん」などで知られる作詞家。藤圭子の楽曲は内山田洋とクール・ファイブのオリジナルをカバーしたもの。',
    targetSongs: [
      { artistId: 'keiko', title: '逢わずに愛して(カバー)', year: 1970, lyric: '川内康範', music: '彩木雅夫' },
    ],
  },
  {
    id: 'kitaguni-no-eki',
    originSong: { artistId: 'hibari', title: '北国の駅', year: 1973, lyric: '西沢爽', music: '鈴木邦彦' },
    creator: '鈴木邦彦',
    creatorRole: '作曲家',
    featured: false,
    note: '昭和歌謡・歌謡ポップスを支えた作曲家。',
    targetSongs: [
      { artistId: 'hideki', title: '情熱の嵐', year: 1973, lyric: 'たかたかし', music: '鈴木邦彦' },
      { artistId: 'keiko', title: '花は流れて', year: 1972, lyric: '石坂まさを', music: '鈴木邦彦' },
    ],
  },
  {
    id: 'urimado',
    originSong: { artistId: 'hibari', title: '裏窓', year: 1988, lyric: 'たかたかし', music: '弦哲也' },
    creator: '弦哲也',
    creatorRole: '作曲家',
    featured: false,
    note: '演歌・歌謡曲を数多く手がけた作曲家。「北の旅人」は石原裕次郎が亡くなる直前にハワイで録音し、没後に追悼盤として発売された一曲。',
    targetSongs: [
      { artistId: 'yujiro', title: '北の旅人', year: 1987, lyric: '山口洋子', music: '弦哲也' },
    ],
  },
]
