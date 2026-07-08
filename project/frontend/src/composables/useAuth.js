import { ref, readonly } from 'vue'
import * as authApi from '../lib/authApi.js'

const user = ref(null)
const ready = ref(false)

/**
 * セッション認証状態（Flask session cookie 連携）
 */
export function useAuth() {
  async function refreshUser() {
    try {
      const result = await authApi.fetchMe()
      user.value = result.login ? result.user : null
    } catch {
      user.value = null
    } finally {
      ready.value = true
    }
  }

  async function login(email, password) {
    const result = await authApi.login(email, password)
    user.value = result.user
    return result
  }

  async function register(name, email, password) {
    return authApi.register(name, email, password)
  }

  async function logout() {
    await authApi.logout()
    user.value = null
  }

  return {
    user: readonly(user),
    ready: readonly(ready),
    refreshUser,
    login,
    register,
    logout,
  }
}
