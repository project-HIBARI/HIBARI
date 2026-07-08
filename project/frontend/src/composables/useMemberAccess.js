/**
 * 会員権限チェック（useAuth のラッパー）
 */
import { useAuth } from './useAuth.js'
import { PERMISSION, MEMBERSHIP_LABELS } from '../constants/membership.js'

export function useMemberAccess() {
  const auth = useAuth()

  function getAccessState(permission) {
    if (!auth.isLoggedIn.value) {
      return {
        allowed: false,
        reason: 'login',
        message: 'この機能は会員登録・ログイン後にご利用いただけます。',
      }
    }
    if (!auth.can(permission)) {
      return {
        allowed: false,
        reason: 'upgrade',
        message: `この機能は${MEMBERSHIP_LABELS.premium}限定です。`,
      }
    }
    return { allowed: true, reason: null, message: '' }
  }

  function canUse(permission) {
    return getAccessState(permission).allowed
  }

  return {
    ...auth,
    getAccessState,
    canUse,
    PERMISSION,
  }
}
