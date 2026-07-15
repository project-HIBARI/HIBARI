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
 *
 * creatorYears / creatorBio: Wikipedia日本語版等で確認した実在の経歴情報。
 * creatorImage: ライセンスを確認できた肖像写真がある場合のみ設定（Wikimedia Commonsより取得。
 * 秋元康・遠藤実はCC BY / CC BY-SA、永六輔・古賀政男・西條八十は日本国内パブリックドメイン）。
 * 確認できなかった人物は null とし、表示側で頭文字のフォールバックにする（存在しない画像を推測で使わないため）。
 */
function creatorImageUrl(filename) {
  return `/images/creators/${filename}`
}

export const CROSS_ARTIST_CONNECTIONS = [
  {
    id: 'tabibito',
    originSong: { artistId: 'hibari', title: '旅人', year: 1971, lyric: '阿久悠', music: '村井邦彦' },
    creator: '阿久悠',
    creatorRole: '作詞家',
    creatorYears: '1937–2007',
    creatorImage: null,
    featured: true,
    note: '昭和を代表する稀代の作詞家。ジャンルを問わず数多くのスターに詞を提供した。',
    creatorBio: '兵庫県淡路島出身。宣弘社のコピーライターを経て1966年頃から作詞家として本格活動し、生涯で5,000曲以上を手がけた。都はるみ「北の宿から」、石原裕次郎「いつも二人で」など多数のヒット曲を提供し、日本レコード大賞・大賞受賞曲は作詞家最多の5曲。紫綬褒章受章。',
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
    creatorYears: '1945–2009',
    creatorImage: null,
    featured: true,
    note: '阿久悠となかにし礼という二大作詞家の名曲を数多く手がけた作曲家。',
    creatorBio: '東京都出身。10代で美空ひばりに「さくらの唄」を提供し作曲家デビュー。石川さゆり「津軽海峡・冬景色」など幅広いヒット曲を手がけた。日本レコード大賞・中山晋平賞、古賀政男記念音楽大賞を受賞し、紫綬褒章を受章。歌手・黛ジュンは実妹。',
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
    creatorYears: '1938–2020',
    creatorImage: null,
    featured: true,
    note: '情感豊かな詞世界で知られる作詞家・作家。晩年まで数々の名曲を手がけた。',
    creatorBio: '旧満洲生まれ。石原裕次郎との出会いを機に作詞家へ転向し、美空ひばり「かもめと女」、藤圭子「女の人生」などを提供。黛ジュン「天使の誘惑」、細川たかし「北酒場」で日本レコード大賞を計3回受賞。小説家としても直木賞を受賞した。',
    targetSongs: [
      { artistId: 'yujiro', title: 'わが人生に悔いなし', year: 1987, lyric: 'なかにし礼', music: '加藤登紀子' },
    ],
  },
  {
    id: 'wakaretemo-arigatou',
    originSong: { artistId: 'hibari', title: '別れてもありがとう', year: 1969, lyric: '三浦康照', music: '猪俣公章' },
    creator: '猪俣公章',
    creatorRole: '作曲家',
    creatorYears: '1938–1993',
    creatorImage: null,
    featured: true,
    note: '演歌・歌謡曲の名曲を数多く手がけた昭和の作曲家。',
    creatorBio: '福島県会津坂下町出身。古賀政男に師事した作曲家・作詞家。藤圭子「女のブルース」はオリコン8週連続1位を記録し、五木ひろし「千曲川」で日本レコード大賞最優秀歌唱賞を受賞。森進一のデビュー曲「女のためいき」も手がけた。',
    targetSongs: [
      { artistId: 'keiko', title: '京都から博多まで', year: 1972, lyric: '阿久悠', music: '猪俣公章' },
    ],
  },
  {
    id: 'kawa-no-nagareno-yoni',
    originSong: { artistId: 'hibari', title: '川の流れのように', year: 1989, lyric: '秋元康', music: '見岳章' },
    creator: '秋元康',
    creatorRole: '作詞家',
    creatorYears: '1958年生',
    creatorImage: creatorImageUrl('akimoto-yasushi.jpg'),
    featured: false,
    note: '数多くのアイドル・歌手を手がけた作詞家。両曲とも本人の生前最後のシングルとなった。',
    creatorBio: '東京都出身。美空ひばりの遺作「川の流れのように」の作詞を担当し、作詞家としての地位を確立。おニャン子クラブ、AKB48、乃木坂46など数多くのアイドルグループを手がける放送作家・音楽プロデューサー。日本レコード大賞を複数年連続受賞し、紫綬褒章を受章。',
    targetSongs: [
      { artistId: 'takajin', title: 'その時の空', year: 2010, lyric: '秋元康', music: '小室哲哉' },
    ],
  },
  {
    id: 'ue-wo-muite-arukou',
    originSong: { artistId: 'hibari', title: '上を向いて歩こう(カバー)', year: 1975, lyric: '永六輔', music: '中村八大' },
    creator: '永六輔 & 中村八大',
    creatorRole: '作詞・作曲(同一楽曲のカバーで繋がる例)',
    creatorYears: '永六輔 1933–2016 ／ 中村八大 1931–1992',
    creatorImage: creatorImageUrl('ei-rokusuke.jpg'),
    featured: false,
    note: '坂本九のオリジナルを、美空ひばり・忌野清志郎(RCサクセション)がそれぞれカバーした一曲。同じ楽曲が世代を超えて歌い継がれた例。',
    creatorBio: '放送作家・作詞家の永六輔と、作曲家・ジャズピアニストの中村八大による黄金コンビ（坂本九を加え「六・八・九トリオ」）。「上を向いて歩こう」は "Sukiyaki" として米ビルボード1位を獲得した世界的ヒット曲で、「こんにちは赤ちゃん」など数々の名曲を残した。',
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
    creatorYears: '1920–2008',
    creatorImage: null,
    featured: false,
    note: '「おふくろさん」などで知られる作詞家。藤圭子の楽曲は内山田洋とクール・ファイブのオリジナルをカバーしたもの。',
    creatorBio: '北海道函館市出身。テレビドラマ『月光仮面』『愛の戦士レインボーマン』の原作・脚本で知られる作詞家・脚本家。「誰よりも君を愛す」「骨まで愛して」「おふくろさん」等を作詞。『まんが日本昔ばなし』の監修も担当し、日本作詩大賞を受賞。',
    targetSongs: [
      { artistId: 'keiko', title: '逢わずに愛して(カバー)', year: 1970, lyric: '川内康範', music: '彩木雅夫' },
    ],
  },
  {
    id: 'kitaguni-no-eki',
    originSong: { artistId: 'hibari', title: '北国の駅', year: 1973, lyric: '西沢爽', music: '鈴木邦彦' },
    creator: '鈴木邦彦',
    creatorRole: '作曲家',
    creatorYears: '1938年生',
    creatorImage: null,
    featured: false,
    note: '昭和歌謡・歌謡ポップスを支えた作曲家。',
    creatorBio: '東京府出身、慶應義塾大学卒。ジャズピアニストから中村八大の影響で作編曲家へ転身し、西城秀樹に「情熱の嵐」など多数の楽曲を提供。黛ジュン「天使の誘惑」で日本レコード大賞を受賞した。',
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
    creatorYears: '1947年生',
    creatorImage: null,
    featured: false,
    note: '演歌・歌謡曲を数多く手がけた作曲家。「北の旅人」は石原裕次郎が亡くなる直前にハワイで録音し、没後に追悼盤として発売された一曲。',
    creatorBio: '千葉県銚子市出身。歌手「田村しんじ」としてデビュー後、作曲家へ転向。石川さゆり「天城越え」で日本レコード大賞金賞を受賞した。日本作曲家協会会長・JASRAC会長を歴任し、銚子市名誉市民。',
    targetSongs: [
      { artistId: 'yujiro', title: '北の旅人', year: 1987, lyric: '山口洋子', music: '弦哲也' },
    ],
  },
  {
    id: 'hatsukoi-madorosu',
    originSong: { artistId: 'hibari', title: '初恋マドロス', year: 1960, lyric: '西沢爽', music: '遠藤実' },
    creator: '遠藤実',
    creatorRole: '作曲家',
    creatorYears: '1932–2008',
    creatorImage: creatorImageUrl('endo-minoru.jpg'),
    featured: false,
    note: '藤圭子には2曲、石原裕次郎には1曲を提供しており、ロースター内で最も多くのアーティストと繋がる作曲家。',
    creatorBio: '新潟県出身。戦後を代表する作曲家で生涯5,000曲以上を作曲した。舟木一夫「高校三年生」、千昌夫「北国の春」、森昌子「せんせい」など数々のヒットを生み出し、多くの新人歌手を見出した。1990年紫綬褒章、2003年文化功労者（大衆音楽分野で初）。',
    targetSongs: [
      { artistId: 'keiko', title: 'さすらい', year: 1975, lyric: 'よしかわかおり', music: '遠藤実' },
      { artistId: 'keiko', title: '北の港町', year: 1979, lyric: '遠藤実', music: '遠藤実' },
      { artistId: 'yujiro', title: '海鳴りの宿', year: 1975, lyric: '池田康生', music: '遠藤実' },
    ],
  },
  {
    id: 'midaregami',
    originSong: { artistId: 'hibari', title: 'みだれ髪', year: 1987, lyric: '星野哲郎', music: '船村徹' },
    creator: '船村徹',
    creatorRole: '作曲家',
    creatorYears: '1932–2017',
    creatorImage: null,
    featured: false,
    note: '「みだれ髪」は晩年の美空ひばりを代表する一曲。福島県いわき市の歌碑除幕式には本人も出席した。',
    creatorBio: '栃木県出身。生涯5,000曲以上を手がけた戦後演歌の巨匠。「別れの一本杉」「王将」「矢切の渡し」など多数のヒットを持ち、北島三郎・鳥羽一郎らを育てた。2016年、演歌の作曲家として初めて文化勲章を受章した。',
    targetSongs: [
      { artistId: 'keiko', title: '可愛い女', year: 1979, lyric: '中山大三郎', music: '船村徹' },
    ],
  },
  {
    id: 'kanashii-sake',
    originSong: { artistId: 'hibari', title: '悲しい酒', year: 1966, lyric: '石本美由起', music: '古賀政男' },
    creator: '古賀政男',
    creatorRole: '作曲家',
    creatorYears: '1904–1978',
    creatorImage: creatorImageUrl('koga-masao.jpg'),
    featured: false,
    note: '石原裕次郎の持ち歌としても知られる「誰か故郷を想わざる」（原曲は霧島昇、1940年）で作詞の西條八十と結ばれる。裕次郎による録音・発表時期は資料により確認できていない。',
    creatorBio: '福岡県出身。「古賀メロディー」で知られる昭和を代表する作曲家。生涯約5,000曲を作曲し、藤山一郎・美空ひばり・村田英雄らに数々のヒットを提供した。没後、国民栄誉賞を受賞。',
    targetSongs: [
      { artistId: 'yujiro', title: '誰か故郷を想わざる', year: '発表年不詳', lyric: '西條八十', music: '古賀政男' },
    ],
  },
  {
    id: 'echigo-jishi-no-uta',
    originSong: { artistId: 'hibari', title: '越後獅子の唄', year: 1950, lyric: '西條八十', music: '万城目正' },
    creator: '西條八十',
    creatorRole: '作詞家',
    creatorYears: '1892–1970',
    creatorImage: creatorImageUrl('saijo-yaso.jpg'),
    featured: false,
    note: '石原裕次郎の持ち歌としても知られる「誰か故郷を想わざる」（原曲は霧島昇、1940年）で作曲の古賀政男と結ばれる。裕次郎による録音・発表時期は資料により確認できていない。',
    creatorBio: '東京都出身。象徴詩人としても知られた作詞家で、「東京行進曲」「青い山脈」「王将」など多数の歌謡曲の詞を手がけた。日本藝術院会員、日本音楽著作権協会会長を歴任した。',
    targetSongs: [
      { artistId: 'yujiro', title: '誰か故郷を想わざる', year: '発表年不詳', lyric: '西條八十', music: '古賀政男' },
    ],
  },
]
