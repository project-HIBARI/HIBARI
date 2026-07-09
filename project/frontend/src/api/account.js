import { apiRequest } from './client.js'

/** ログイン中のアカウント詳細を取得 */
export function fetchAccount() {
  return apiRequest('/api/account')
}

/**
 * プロフィール更新（氏名・メール・住所）
 * @param {{ name: string, email: string, address?: string }} payload
 */
export function updateAccount(payload) {
  return apiRequest('/api/account', {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}

/**
 * パスワード変更
 * @param {{ current_password: string, new_password: string }} payload
 */
export function changeAccountPassword(payload) {
  return apiRequest('/api/account/password', {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}

/**
 * 支払い方法の更新
 * @param {{ payment_method: string, payment_details?: object }} payload
 */
export function updateAccountPayment(payload) {
  return apiRequest('/api/account/payment', {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}

/**
 * 会員プラン変更
 * @param {{ is_premium: boolean }} payload
 */
export function updateAccountMembership(payload) {
  return apiRequest('/api/account/membership', {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}
