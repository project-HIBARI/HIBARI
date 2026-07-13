/**
 * 軽量トースト通知 — シングルトンref配列で保持し、ToastHostが描画する
 */
import { ref } from 'vue'

const toasts = ref([])
let seq = 0

export function useToast() {
  function showToast(message, { tone = 'default', duration = 3000 } = {}) {
    const id = ++seq
    toasts.value = [...toasts.value, { id, message, tone }]
    if (duration > 0) {
      setTimeout(() => dismissToast(id), duration)
    }
    return id
  }

  function dismissToast(id) {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  return { toasts, showToast, dismissToast }
}
