// Real data — 美空ひばり公式サイト参照（事実情報のみ）
export const HIBARU_DATA = {

  profile: {
    stageName: '美空ひばり',
    realName: '加藤和枝',
    born: '1937年5月29日',
    bornPlace: '横浜市磯子区滝頭二丁目',
    died: '1989年6月24日 午後0時28分',
    cause: '間質性肺炎による呼吸不全',
    age: 52,
    debut: '1945年12月（杉田劇場・芸名:美空和枝）',
    label: '日本コロムビア',
    totalSongs: 1500,
    originalSongs: 517,
    awards: ['第7回日本レコード大賞（柔・1965年）', '紺綬褒章（1969年）', '国民栄誉賞（女性初・1989年7月4日）'],
  },

  news: [
    { date: '2026.05.29', title: '【お知らせ】美空ひばり公式ファンサイト リニューアルオープン', type: 'info', label: 'お知らせ' },
    { date: '2026.04.20', title: '【テレビ放映情報】4月29日（祝）NHK BSプレミアム「美空ひばり不死鳥コンサート」放映', type: 'tv', label: 'テレビ' },
    { date: '2026.04.15', title: '【イベント】5月29日（誕生日）記念館フィルムコンサート開催決定', type: 'event', label: 'イベント' },
    { date: '2026.04.10', title: '【テレビ放映情報】4月17日（金）テレビ朝日系「ザ・ベストテン名場面集」に美空ひばり出演映像', type: 'tv', label: 'テレビ' },
    { date: '2026.03.28', title: '【グッズ】「川の流れのように」発売37周年記念 特別限定盤CD発売', type: 'goods', label: 'グッズ' },
  ],

  discography: [
    { year: 1949, title: '悲しき口笛',          romaji: 'Kanashiki Kuchibue',      lyric: '菊田一夫',   music: '万城目正',   label: '日本コロムビア', type: 'シングル', genre: '歌謡曲', no: 'A-1001', note: 'デビュー作・同名映画主題歌' },
    { year: 1950, title: '東京キッド',           romaji: 'Tokyo Kid',               lyric: '東條寿三郎', music: '万城目正',   label: '日本コロムビア', type: 'シングル', genre: 'ポップス', no: 'A-1040', note: 'ハワイ・米国巡業帰国第一作' },
    { year: 1952, title: 'お祭りマンボ',         romaji: 'Omatsuri Mambo',          lyric: '原六朗',     music: '原六朗',     label: '日本コロムビア', type: 'シングル', genre: '歌謡曲', no: 'A-1250', note: '' },
    { year: 1952, title: 'リンゴ追分',           romaji: 'Ringo Oiwake',            lyric: '小沢不二夫', music: '米山正夫',   label: '日本コロムビア', type: 'シングル', genre: '民謡',   no: 'A-1228', note: '70万枚・戦後最大のヒット記録' },
    { year: 1957, title: '港町十三番地',         romaji: 'Minatochō Jūsanbanchi',   lyric: '石本美由起', music: '上原げんと', label: '日本コロムビア', type: 'シングル', genre: '演歌',   no: 'A-2100', note: '' },
    { year: 1960, title: '哀愁波止場',           romaji: 'Aishū Hatoba',            lyric: '石本美由起', music: '船村徹',     label: '日本コロムビア', type: 'シングル', genre: '演歌',   no: 'A-2800', note: '第2回日本レコード大賞歌唱賞' },
    { year: 1965, title: '柔',                   romaji: 'Yawara',                  lyric: '関沢新一',   music: '古賀政男',   label: '日本コロムビア', type: 'シングル', genre: '歌謡曲', no: 'A-5010', note: '第7回日本レコード大賞グランプリ・180万枚' },
    { year: 1966, title: '悲しい酒',             romaji: 'Kanashii Sake',           lyric: '石本美由起', music: '古賀政男',   label: '日本コロムビア', type: 'シングル', genre: '演歌',   no: 'A-5200', note: '' },
    { year: 1970, title: '人生将棋',             romaji: 'Jinsei Shōgi',            lyric: '西沢爽',     music: '船村徹',     label: '日本コロムビア', type: 'シングル', genre: '演歌',   no: 'A-7000', note: '第21回NHK紅白歌合戦で披露' },
    { year: 1972, title: 'ある女の詩',           romaji: 'Aru Onna no Uta',         lyric: '山上路夫',   music: '平尾昌晃',   label: '日本コロムビア', type: 'シングル', genre: '歌謡曲', no: 'A-7500', note: '' },
    { year: 1986, title: '愛燦燦',               romaji: 'Ai Sansan',               lyric: '小椋桂',     music: '小椋桂',     label: '日本コロムビア', type: 'シングル', genre: '歌謡曲', no: 'CK-450', note: '晩年の代表作' },
    { year: 1987, title: 'みだれ髪',             romaji: 'Midare-gami',             lyric: '吉岡治',     music: '市川昭介',   label: '日本コロムビア', type: 'シングル', genre: '演歌',   no: 'CK-500', note: '病後の再起第一作' },
    { year: 1989, title: '川の流れのように',     romaji: 'Kawa no Nagare no Yō ni', lyric: '秋元康',     music: '見岳章',     label: '日本コロムビア', type: 'シングル', genre: '歌謡曲', no: 'CK-600', note: '遺作・不朽の名曲' },
  ],

  timeline: [
    { year: 1937, era: '昭和十二年', age: 0,  title: '横浜・磯子に生まれる',          body: '加藤和枝として横浜市磯子区滝頭に誕生。魚屋「加藤商店」の長女。' },
    { year: 1945, era: '昭和二十年', age: 8,  title: '杉田劇場で初舞台',              body: '12月、横浜・磯子の杉田劇場で初舞台を踏む。芸名は「美空和枝」。' },
    { year: 1947, era: '昭和二十二年', age: 10, title: '芸名「美空ひばり」誕生',     body: '10月、伴淳三郎一座の公演に参加。この時に「美空ひばり」と命名される。' },
    { year: 1949, era: '昭和二十四年', age: 12, title: '「悲しき口笛」大ヒット',    body: '8月に発売した「悲しき口笛」が空前の大ヒット。10月に日本コロムビアと専属契約。' },
    { year: 1952, era: '昭和二十七年', age: 15, title: '「リンゴ追分」70万枚',      body: '4月にラジオ東京「リンゴ園の少女」主題歌として発売。戦後最大の売上記録を達成。' },
    { year: 1954, era: '昭和二十九年', age: 17, title: 'NHK紅白歌合戦初出場',       body: '12月31日、第5回NHK紅白歌合戦に「ひばりのマドロスさん」で初出場。' },
    { year: 1962, era: '昭和三十七年', age: 25, title: '小林旭と結婚',               body: '11月5日、俳優の小林旭と結婚。1964年6月に離婚。' },
    { year: 1965, era: '昭和四十年', age: 28, title: '「柔」でレコード大賞受賞',      body: '12月、第7回日本レコード大賞グランプリを「柔」（作詞:関沢新一／作曲:古賀政男）で受賞。' },
    { year: 1969, era: '昭和四十四年', age: 32, title: '紺綬褒章受章',               body: '日本赤十字社への奉仕活動の功績により受章。皇后陛下より直接授与。' },
    { year: 1981, era: '昭和五十六年', age: 44, title: '母・喜美枝逝去',             body: '7月29日、最大の理解者であった母・加藤喜美枝が68歳で逝去。しばし休養に入る。' },
    { year: 1987, era: '昭和六十二年', age: 50, title: '両側大腿骨骨頭壊死と診断', body: '4月に福岡で入院。両側大腿骨骨頭壊死・慢性肝炎と診断される。しかし復帰を誓う。' },
    { year: 1988, era: '昭和六十三年', age: 51, title: '東京ドーム 不死鳥コンサート', body: '4月11日、東京ドームで「不死鳥コンサート」。5万人の観客の前で39曲を熱唱した伝説の一夜。' },
    { year: 1989, era: '平成元年',    age: 52, title: '逝去・国民栄誉賞受賞',         body: '6月24日 午後0時28分、間質性肺炎による呼吸不全で逝去。享年52歳。7月4日、女性初の国民栄誉賞を受賞。' },
  ],

  places: [
    { id: 'isogo',      name: '生誕地（横浜市磯子区）',   area: '神奈川県横浜市磯子区滝頭',          type: 'birthplace', lat: 35.39, lng: 139.63, visitable: false,
      note: '美空ひばりが1937年5月29日に生まれた場所。現在は当時の面影はないが、ゆかりの地として語り継がれる。' },
    { id: 'sugita',     name: '杉田劇場跡（初舞台）',     area: '神奈川県横浜市磯子区杉田',          type: 'landmark',   lat: 35.35, lng: 139.60, visitable: false,
      note: '1945年12月、8歳の美空ひばり（当時:美空和枝）が初舞台を踏んだ劇場。現在は商業施設に。' },
    { id: 'noge',       name: '横浜野毛 美空ひばり像',    area: '神奈川県横浜市中区野毛',            type: 'monument',   lat: 35.44, lng: 139.63, visitable: true,
      note: '1993年12月、野毛商店街により建立。横浜国際劇場ゆかりの地に立つブロンズ像。' },
    { id: 'kinenkan',   name: '東京目黒 美空ひばり記念館', area: '東京都目黒区青葉台1丁目4番12号',   type: 'memorial',   lat: 35.65, lng: 139.70, visitable: true,
      note: '長男・加藤和也氏が公開する青葉台の自邸。TEL 03-5422-3358。開館10:00〜15:00（毎日）。' },
    { id: 'dome',       name: '東京ドーム（不死鳥コンサート）', area: '東京都文京区後楽1丁目',     type: 'stage',      lat: 35.71, lng: 139.75, visitable: true,
      note: '1988年4月11日、5万人の観客を前に39曲を歌った伝説の不死鳥コンサートの舞台。' },
    { id: 'shioya',     name: 'いわき市塩屋崎 みだれ髪の碑', area: '福島県いわき市小名浜岬',        type: 'monument',   lat: 36.98, lng: 140.97, visitable: true,
      note: '1988年10月2日除幕。美空ひばり本人が出席した「みだれ髪」の歌碑。塩屋崎灯台下に立つ。' },
    { id: 'hirosaki',   name: '弘前りんご公園 リンゴ追分碑', area: '青森県弘前市清水富田',          type: 'monument',   lat: 40.62, lng: 140.40, visitable: true,
      note: '2002年5月18日建立。「リンゴ追分」にちなみ、弘前市りんご公園内に建てられた歌碑。' },
    { id: 'osugi',      name: '高知・大杉 川の流れのように碑', area: '高知県長岡郡大豊町大杉',      type: 'monument',   lat: 33.72, lng: 133.65, visitable: true,
      note: '1993年5月22日建立。日本一の大杉のそばに立つ「川の流れのように」の歌碑。' },
  ],

  memories: [
    { id: 1, author: '佐藤 貞夫', age: 78, location: '東京都 葛飾区', date: '2026.04.20', title: '昭和三十年 日劇の楽屋口で', body: '学校帰り、友達と日劇の楽屋口で何時間も待ちました。赤い傘を差して出てこられた時、私たちに笑顔で手を振ってくださった。あの微笑みを今でも覚えています。', song: 'リンゴ追分', likes: 48, comments: 12 },
    { id: 2, author: '田中 美枝子', age: 72, location: '大阪府 堺市', date: '2026.04.15', title: '母と一緒に聴いた「悲しい酒」', body: '嫁いだばかりの頃、寂しさで泣いていた私に、母が「悲しい酒」のレコードを送ってくれました。それから五十年、この歌を聴くたびに母の顔を思い出します。', song: '悲しい酒', likes: 62, comments: 8 },
    { id: 3, author: '山田 征一', age: 81, location: '神奈川県 横浜市', date: '2026.04.10', title: '野毛の銅像の前で', body: '同じ横浜で育った者として、ひばりさんは誇りです。野毛の銅像を訪ねるたびに、「川の流れのように」を口ずさみます。', song: '川の流れのように', likes: 35, comments: 5 },
    { id: 4, author: '鈴木 きよ子', age: 69, location: '福岡県 北九州市', date: '2026.04.02', title: '昭和六十三年 東京ドーム', body: '不死鳥コンサートを観に夜行バスで上京しました。病を押しての舞台で、立ち上がって歌われた時の会場のどよめきは今も耳を離れません。', song: '愛燦燦', likes: 94, comments: 21 },
    { id: 5, author: '高橋 清', age: 85, location: '京都府 京都市', date: '2026.03.28', title: '目黒の記念館を訪ねて', body: '先日、青葉台の記念館を訪ねました。ひばりさんが愛したそのままのお部屋に、思わず涙がこぼれました。スタッフの方々の温かさが素晴らしかった。', song: '柔', likes: 41, comments: 9 },
    { id: 6, author: '伊藤 まり', age: 58, location: '宮城県 仙台市', date: '2026.03.20', title: '祖母から受け継いだレコード', body: '祖母が大切にしていたLPを形見として受け継ぎました。針を落とすと、祖母の台所の匂いがしてくるようです。世代を超えて、歌が時代をつなぐのだと思います。', song: '川の流れのように', likes: 57, comments: 14 },
  ],

  events: [
    { id: 1, title: 'みだれ髪ゆかりの地ツアー', type: 'tour', date: '2026.05.17（日）', time: '10:00〜', place: '福島県いわき市 塩屋崎灯台', fee: '¥8,800（会員割引 ¥7,500）', capacity: '定員30名', partner: 'いわき市観光協会 協力' },
    { id: 2, title: '第18回 ひばりをうたうのど自慢大会', type: 'nodojiman', date: '2026.05.24（日）', time: '13:00〜', place: '横浜市磯子公会堂', fee: '参加無料（観覧 ¥500）', capacity: '定員200名', partner: '横浜市磯子区 協力' },
    { id: 3, title: '横浜・野毛 銅像前ファン交流会', type: 'tour', date: '2026.05.29（誕生日）', time: '14:00〜', place: '横浜市野毛 美空ひばり像前', fee: '無料', capacity: '自由参加', partner: '野毛商店街振興組合 協力' },
    { id: 4, title: '春のカラオケ大会 〜ひばりを歌う夕べ〜', type: 'karaoke', date: '2026.06.07（土）', time: '18:00〜', place: '東京都内（会場調整中）', fee: '¥2,000（飲食別）', capacity: '定員50名', partner: '' },
    { id: 5, title: '不死鳥忌フォトコンテスト 2026', type: 'photo', date: '〆切:2026.06.15', time: '', place: 'オンライン＋表彰式:東京', fee: '参加無料', capacity: '一般公開', partner: '' },
  ],

  /** ホームページ「今後の放送・イベント」表示用（テレビ放映 + イベント） */
  homeSchedule: [
    { id: 'b1', date: '6/13 土', time: '19:00〜', title: 'NHK 総合 Eテレ「美空ひばり 世界の歌講座」', note: '再放送 · 第3回「川の流れのように」特集' },
    { id: 'b2', date: '6/18 水', time: '20:30〜', title: 'NHK BS プレミアム「美空ひばり 不死鳥コンサート」', note: '1988年 東京ドーム公演より' },
    { id: 'b3', date: '5/17 日', time: '10:00〜', title: 'みだれ髪ゆかりの地ツアー', note: '福島県いわき市 塩屋崎灯台 · 定員30名' },
    { id: 'b4', date: '5/29 木', time: '14:00〜', title: '横浜・野毛 銅像前ファン交流会', note: '誕生日記念 · 自由参加' },
  ],

  messages: [
    { name: '匿名のファン', location: '北海道', date: '2026.04.22', flower: '白百合',  body: 'お誕生日まであと37日。今年も「川の流れのように」を聴きながら、一年を振り返りました。' },
    { name: '悦子',         location: '千葉県', date: '2026.04.20', flower: '紅薔薇',  body: '89回目のお誕生日が近づきました。今でも毎朝、あなたの歌で目覚めます。' },
    { name: 'H.K.',          location: '大阪府', date: '2026.04.18', flower: '白菊',    body: '父の形見のレコード、今日も針を落としました。「柔」が流れると、父の笑顔が浮かびます。' },
    { name: '美智子',        location: '山形県', date: '2026.04.15', flower: 'かすみ草', body: '主人と出会った頃、二人で「愛燦燦」を歌いました。もうすぐ、あちらで会えますね。' },
    { name: '若いファン 21歳', location: '東京都', date: '2026.04.10', flower: '白百合', body: '祖母のラジカセから流れていた歌を、今は私が聴いています。世代を超えて届く歌声をありがとうございます。' },
  ],
};
