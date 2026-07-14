/**
 * オープンチャットのメディア URL 解決
 */
const IMAGE_EXT = /\.(jpe?g|png|gif|webp)(\?.*)?$/i
const VIDEO_EXT = /\.(mp4|webm|mov)(\?.*)?$/i

export function resolveOpenChatMediaUrl(message) {
  if (!message) return ''

  const direct = message.media_url || message.media_path || ''
  if (!direct) return ''

  if (direct.startsWith('/api/open-chats/media/')) {
    return direct
  }

  if (direct.startsWith('/uploads/open-chat/')) {
    const filename = direct.split('/').pop()
    return filename ? `/api/open-chats/media/${filename}` : ''
  }

  return direct
}

export function isOpenChatImageMessage(message) {
  const url = resolveOpenChatMediaUrl(message)
  if (!url) return false

  const type = String(message?.message_type || '').toLowerCase()
  if (type === 'image') return true
  if (type === 'video') return false
  return IMAGE_EXT.test(url)
}

export function isOpenChatVideoMessage(message) {
  const url = resolveOpenChatMediaUrl(message)
  if (!url) return false

  const type = String(message?.message_type || '').toLowerCase()
  if (type === 'video') return true
  if (type === 'image') return false
  return VIDEO_EXT.test(url)
}
