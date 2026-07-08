/**
 * 金融機関マスタ（疑似データ）
 * 主要行 + 検索用の追加金融機関
 */
export const BANKS = [
  { value: 'mizuho', label: 'みずほ銀行', icon: 'mizuho', kana: 'ミズホ' },
  { value: 'mufg', label: '三菱UFJ銀行', icon: 'mufg', kana: 'ミツビシユーエフジェイ' },
  { value: 'smbc', label: '三井住友銀行', icon: 'smbc', kana: 'ミツイスミトモ' },
  { value: 'yucho', label: 'ゆうちょ銀行', icon: 'yucho', kana: 'ユウチョ' },
  { value: 'resona', label: 'りそな銀行', icon: 'resona', kana: 'リソナ' },
  { value: 'saitama_resona', label: '埼玉りそな銀行', icon: 'resona', kana: 'サイタマリソナ' },
  { value: 'shinsei', label: '新生銀行', icon: 'shinsei', kana: 'シンセイ' },
  { value: 'aozora', label: 'あおぞら銀行', icon: 'bank', kana: 'アオゾラ' },
  { value: 'rakuten', label: '楽天銀行', icon: 'bank', kana: 'ラクテン' },
  { value: 'paypay', label: 'PayPay銀行', icon: 'bank', kana: 'ペイペイ' },
  { value: 'sbi', label: '住信SBIネット銀行', icon: 'bank', kana: 'スミシンエスビーアイ' },
  { value: 'seven_bank', label: 'セブン銀行', icon: 'seven', kana: 'セブン' },
  { value: 'hokkaido', label: '北海道銀行', icon: 'bank', kana: 'ホッカイドウ' },
  { value: 'higo', label: '肥後銀行', icon: 'bank', kana: 'ヒゴ' },
  { value: 'chiba', label: '千葉銀行', icon: 'bank', kana: 'チバ' },
  { value: 'yokohama', label: '横浜銀行', icon: 'bank', kana: 'ヨコハマ' },
  { value: 'chugoku', label: '中国銀行', icon: 'bank', kana: 'チュウゴク' },
  { value: 'hiroshima', label: '広島銀行', icon: 'bank', kana: 'ヒロシマ' },
  { value: 'fukuoka', label: '福岡銀行', icon: 'bank', kana: 'フクオカ' },
  { value: 'okinawa', label: '沖縄銀行', icon: 'bank', kana: 'オキナワ' },
]

export function findBank(value) {
  return BANKS.find((b) => b.value === value) || null
}

export function searchBanks(query) {
  const q = query.trim().toLowerCase()
  if (!q) return BANKS
  return BANKS.filter(
    (b) =>
      b.label.toLowerCase().includes(q) ||
      b.kana.toLowerCase().includes(q) ||
      b.value.includes(q),
  )
}
