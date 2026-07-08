/**
 * 認証・会員状態
 */
import { ref, computed, readonly } from 'vue'
import { fetchCurrentUser, login as loginApi, logout as logoutApi } from '../api/auth.js'
import { normalizeMembership, hasPermission, isPremiumMember, getAiChatLimit } from '../constants/membership.js'

const user = ref(null)
const loading = ref(false)
const initialized = ref(false)

export function useAuth() {
  const isLoggedIn = computed(() => Boolean(user.value))
  const membership = computed(() => normalizeMembership(user.value?.membership))
  const isPremium = computed(() => isPremiumMember(membership.value))

  async function refreshUser() {
    loading.value = true
    try {
      const data = await fetchCurrentUser()
      user.value = data.user
    } catch {
      user.value = null
    } finally {
      loading.value = false
      initialized.value = true
    }
  }

  async function login(email, password) {
    const result = await loginApi(email, password)
    user.value = result.user
    return result
  }

  async function logout() {
    try {
      await logoutApi()
    } finally {
      user.value = null
    }
  }

  function setUser(nextUser) {
    user.value = nextUser
  }

  function can(permission) {
    if (!user.value) return false
    return hasPermission(membership.value, permission)
  }

  return {
    user: readonly(user),
    loading: readonly(loading),
    initialized: readonly(initialized),
    isLoggedIn,
    membership,
    isPremium,
    refreshUser,
    login,
    logout,
    setUser,
    can,
    getAiChatLimit: () => getAiChatLimit(membership.value),
  }
}
