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
        message: 'この特典は Music Memories でログイン後にご利用いただけます。',
      }
    }
    if (!auth.isFanclubMember.value) {
      return {
        allowed: false,
        reason: 'fanclub',
        message: 'この特典は Music Memories でファンクラブ有料会員に加入するとご利用いただけます。',
      }
    }
    if (!auth.can(permission)) {
      return {
        allowed: false,
        reason: 'upgrade',
        message: `この特典は Music Memories で${MEMBERSHIP_LABELS.premium}に登録するとご利用いただけます。`,
      }
    }
    return { allowed: true, reason: null, message: '' }
  }

  function getPerkState({ permission, premium = false }) {
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
    getPerkState,
    PERMISSION,
  }
}
