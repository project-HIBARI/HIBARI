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
    if (!auth.isFanclubMember.value) {
      return {
        allowed: false,
        reason: 'fanclub',
        message: 'この機能はファンクラブ有料会員のみご利用いただけます。',
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

  const GUEST_TRIAL_PERMISSIONS = new Set([PERMISSION.BOARD_POST, PERMISSION.AI_CHAT])

  function hasGuestTrial(permission) {
    return !auth.isFanclubMember.value && GUEST_TRIAL_PERMISSIONS.has(permission)
  }

  function getPerkState({ permission, premium = false, guestTrial = false }) {
    if (guestTrial && hasGuestTrial(permission)) {
      return { unlocked: false, trial: true, lockLabel: '10回まで' }
    }
    if (canUse(permission)) {
      return { unlocked: true, trial: false, lockLabel: '' }
    }
    if (!auth.isFanclubMember.value) {
      return { unlocked: false, trial: false, lockLabel: '有料会員限定' }
    }
    if (premium) {
      return { unlocked: false, trial: false, lockLabel: 'プレミアム' }
    }
    return { unlocked: false, trial: false, lockLabel: '有料会員限定' }
  }

  function canUse(permission) {
    return getAccessState(permission).allowed
  }

  return {
    ...auth,
    getAccessState,
    canUse,
    hasGuestTrial,
    getPerkState,
    PERMISSION,
  }
}
