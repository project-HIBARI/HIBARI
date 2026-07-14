/**
 * アーティスト間の曲の繋がり (Cross-Artist Connections) データ
 * 同じ作詞家・作曲家が Music Memories ロースター内の複数アーティストに
 * 楽曲提供している実例。作詞・作曲者名は Wikipedia 日本語版・歌ネット等で確認済み。
 *
 * サイトのテーマは「既に亡くなったアーティスト」を扱うことであり、これは
 * ロースターに掲載するアーティスト本人（MUSIC_MEMORIES_ARTISTS）にのみ適用される。
 * 楽曲の作詞家・作曲家（脇役のクレジット）は存命でも構わない。
 *
 * artistId は musicMemoriesData.js の MUSIC_MEMORIES_ARTISTS の id と対応させ、
 * アーティスト名・画像はそちらから解決する（データの重複を避けるため）。
 *
 * featured: true の項目はホーム(PageMusicMemories)にも代表例として表示される。
 * 「曲の繋がり」専用ページ(PageMusicConnections)では featured の有無に関わらず全件を表示する。
 */
export const CROSS_ARTIST_CONNECTIONS = [
  {
    id: 'aku-yu',
    creator: '阿久悠',
    role: '作詞家',
    featured: true,
    note: '昭和を代表する稀代の作詞家。ジャンルを問わず数多くのスターに詞を提供した。',
    songs: [
      { artistId: 'hibari', title: '旅人', year: 1971, lyric: '阿久悠', music: '村井邦彦' },
      { artistId: 'yujiro', title: '黎明', year: 1984, lyric: '阿久悠', music: '三木たかし' },
      { artistId: 'hideki', title: '若き獅子たち', year: 1976, lyric: '阿久悠', music: '三木たかし' },
      { artistId: 'keiko', title: '京都から博多まで', year: 1972, lyric: '阿久悠', music: '猪俣公章' },
    ],
  },
  {
    id: 'miki-takashi',
    creator: '三木たかし',
    role: '作曲家',
    featured: true,
    note: '阿久悠となかにし礼という二大作詞家の名曲を数多く手がけた作曲家。',
    songs: [
      { artistId: 'hibari', title: 'さくらの唄', year: 1976, lyric: 'なかにし礼', music: '三木たかし' },
      { artistId: 'yujiro', title: '黎明', year: 1984, lyric: '阿久悠', music: '三木たかし' },
      { artistId: 'hideki', title: '若き獅子たち', year: 1976, lyric: '阿久悠', music: '三木たかし' },
    ],
  },
  {
    id: 'nakanishi-rei',
    creator: 'なかにし礼',
    role: '作詞家',
    featured: true,
    note: '情感豊かな詞世界で知られる作詞家・作家。晩年まで数々の名曲を手がけた。',
    songs: [
      { artistId: 'hibari', title: 'さくらの唄', year: 1976, lyric: 'なかにし礼', music: '三木たかし' },
      { artistId: 'yujiro', title: 'わが人生に悔いなし', year: 1987, lyric: 'なかにし礼', music: '加藤登紀子' },
    ],
  },
  {
    id: 'inomata-koushou',
    creator: '猪俣公章',
    role: '作曲家',
    featured: true,
    note: '演歌・歌謡曲の名曲を数多く手がけた昭和の作曲家。',
    songs: [
      { artistId: 'hibari', title: '別れてもありがとう', year: 1969, lyric: '三浦康照', music: '猪俣公章' },
      { artistId: 'keiko', title: '京都から博多まで', year: 1972, lyric: '阿久悠', music: '猪俣公章' },
    ],
  },
  {
    id: 'akimoto-yasushi',
    creator: '秋元康',
    role: '作詞家',
    featured: false,
    note: '数多くのアイドル・歌手を手がけた作詞家。両曲とも本人の生前最後のシングルとなった。',
    songs: [
      { artistId: 'hibari', title: '川の流れのように', year: 1989, lyric: '秋元康', music: '見岳章' },
      { artistId: 'takajin', title: 'その時の空', year: 2010, lyric: '秋元康', music: '小室哲哉' },
    ],
  },
  {
    id: 'nagai-nakamura',
    creator: '永六輔 & 中村八大',
    role: '作詞・作曲(同一楽曲のカバーで繋がる例)',
    featured: false,
    note: '坂本九のオリジナルを、美空ひばり・忌野清志郎(RCサクセション)がそれぞれカバーした一曲。同じ楽曲が世代を超えて歌い継がれた例。',
    songs: [
      { artistId: 'kyu', title: '上を向いて歩こう', year: 1961, lyric: '永六輔', music: '中村八大' },
      { artistId: 'hibari', title: '上を向いて歩こう(カバー)', year: 1975, lyric: '永六輔', music: '中村八大' },
      { artistId: 'kiyoshiro', title: '上を向いて歩こう(カバー)', year: 1979, lyric: '永六輔', music: '中村八大' },
    ],
  },
  {
    id: 'kawachi-koban',
    creator: '川内康範',
    role: '作詞家',
    featured: false,
    note: '「おふくろさん」などで知られる作詞家。藤圭子の楽曲は内山田洋とクール・ファイブのオリジナルをカバーしたもの。',
    songs: [
      { artistId: 'hibari', title: '熱祷(いのり)', year: 1968, lyric: '川内康範', music: '小野透' },
      { artistId: 'keiko', title: '逢わずに愛して(カバー)', year: 1970, lyric: '川内康範', music: '彩木雅夫' },
    ],
  },
  {
    id: 'suzuki-kunihiko',
    creator: '鈴木邦彦',
    role: '作曲家',
    featured: false,
    note: '昭和歌謡・歌謡ポップスを支えた作曲家。',
    songs: [
      { artistId: 'hideki', title: '情熱の嵐', year: 1973, lyric: 'たかたかし', music: '鈴木邦彦' },
      { artistId: 'keiko', title: '花は流れて', year: 1972, lyric: '石坂まさを', music: '鈴木邦彦' },
      { artistId: 'hibari', title: '北国の駅', year: 1973, lyric: '西沢爽', music: '鈴木邦彦' },
    ],
  },
  {
    id: 'gen-tetsuya',
    creator: '弦哲也',
    role: '作曲家',
    featured: false,
    note: '演歌・歌謡曲を数多く手がけた作曲家。「北の旅人」は石原裕次郎が亡くなる直前にハワイで録音し、没後に追悼盤として発売された一曲。',
    songs: [
      { artistId: 'yujiro', title: '北の旅人', year: 1987, lyric: '山口洋子', music: '弦哲也' },
      { artistId: 'hibari', title: '裏窓', year: 1988, lyric: 'たかたかし', music: '弦哲也' },
    ],
  },
]
