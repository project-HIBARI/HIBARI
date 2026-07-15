/**
 * Music Memories — アーティスト診断の質問・タグ表示ラベル
 */

export const DIAGNOSIS_QUESTIONS = [
  {
    id: 'music-purpose',
    question: '今、音楽に求めているものは？',
    answers: [
      {
        id: 'purpose-healing',
        label: '心を落ち着かせてくれる歌',
        tags: ['healing', 'gentle', 'emotional'],
      },
      {
        id: 'purpose-push',
        label: '背中を押してくれる歌',
        tags: ['powerful', 'hope', 'passionate'],
      },
      {
        id: 'purpose-youth',
        label: '青春を思い出す歌',
        tags: ['youth', 'nostalgic', 'emotional'],
      },
      {
        id: 'purpose-show',
        label: '華やかな世界へ連れていく歌',
        tags: ['elegant', 'entertainment', 'classic'],
      },
    ],
  },
  {
    id: 'voice-type',
    question: '惹かれる歌声は？',
    answers: [
      {
        id: 'voice-warm',
        label: '包み込むような温かい歌声',
        tags: ['warm', 'gentle', 'healing'],
      },
      {
        id: 'voice-power',
        label: '魂を揺さぶる力強い歌声',
        tags: ['powerful', 'passionate', 'dramatic'],
      },
      {
        id: 'voice-delicate',
        label: '繊細で切ない歌声',
        tags: ['delicate', 'youth', 'emotional'],
      },
      {
        id: 'voice-deep',
        label: '大人の余裕を感じる低い歌声',
        tags: ['deep', 'cool', 'classic'],
      },
    ],
  },
  {
    id: 'era',
    question: '聴いてみたい音楽の時代は？',
    answers: [
      {
        id: 'era-early',
        label: '昭和前期から1950年代',
        tags: ['1940s', '1950s', 'traditional'],
      },
      {
        id: 'era-mid',
        label: '1960年代から1970年代',
        tags: ['1960s', '1970s', 'classic'],
      },
      {
        id: 'era-late',
        label: '1980年代から1990年代',
        tags: ['1980s', '1990s', 'youth'],
      },
      {
        id: 'era-any',
        label: '年代にはこだわらない',
        tags: ['timeless', 'versatile'],
      },
    ],
  },
  {
    id: 'mood',
    question: '好きな音楽の雰囲気は？',
    answers: [
      {
        id: 'mood-enka',
        label: '演歌・歌謡曲の情緒',
        tags: ['enka', 'kayokyoku', 'traditional'],
      },
      {
        id: 'mood-ballad',
        label: '心に刺さるバラード',
        tags: ['ballad', 'emotional', 'dramatic'],
      },
      {
        id: 'mood-cool',
        label: '都会的でクールな音楽',
        tags: ['cool', 'urban', 'stylish'],
      },
      {
        id: 'mood-show',
        label: '明るく華やかなエンターテインメント',
        tags: ['entertainment', 'elegant', 'uplifting'],
      },
    ],
  },
  {
    id: 'story',
    question: 'アーティストの物語で惹かれるのは？',
    answers: [
      {
        id: 'story-legend',
        label: '長い時代を歌い続けた国民的スター',
        tags: ['legend', 'timeless', 'traditional'],
      },
      {
        id: 'story-youth',
        label: '短くも鮮烈な青春の生き方',
        tags: ['youth', 'passionate', 'rebellious'],
      },
      {
        id: 'story-actor',
        label: '歌だけでなく映画や俳優としても活躍',
        tags: ['actor', 'entertainment', 'classic'],
      },
      {
        id: 'story-hope',
        label: '逆境を越え、多くの人に希望を届けた人生',
        tags: ['hope', 'powerful', 'legend'],
      },
    ],
  },
]

/** 内部タグ → 結果画面用の日本語ラベル */
export const DIAGNOSIS_TAG_LABELS = {
  healing: '心に寄り添う歌声',
  gentle: 'やさしい響き',
  emotional: '情感あふれる表現',
  powerful: '力強い表現',
  hope: '希望を届ける歌',
  passionate: '情熱的な世界観',
  youth: '青春を感じる世界観',
  nostalgic: '懐かしさを誘う響き',
  elegant: '華やかで洗練された魅力',
  entertainment: '華やかなエンターテインメント',
  classic: '時代を越える魅力',
  warm: '温かく包み込む歌声',
  dramatic: 'ドラマチックな情感',
  delicate: '繊細で切ない歌声',
  deep: '深い響きの声',
  cool: 'クールな佇まい',
  '1940s': '昭和前期の時代感',
  '1950s': '1950年代の空気感',
  '1960s': '1960年代の魅力',
  '1970s': '1970年代の魅力',
  '1980s': '1980年代の世界観',
  '1990s': '1990年代の空気感',
  traditional: '昭和歌謡の情緒',
  timeless: '時代を超える普遍性',
  versatile: '幅広い音楽性',
  enka: '演歌の情緒',
  kayokyoku: '歌謡曲の味わい',
  ballad: '心に刺さるバラード',
  urban: '都会的な雰囲気',
  stylish: 'スタイリッシュな魅力',
  uplifting: '明るく前向きな響き',
  legend: '国民的レジェンド',
  rebellious: '鮮烈で自由な生き方',
  actor: 'スクリーンでも輝く存在',
}
