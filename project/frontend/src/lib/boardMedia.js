/**
 * 掲示板メディアのクライアント側バリデーション
 */
const IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
const VIDEO_TYPES = ['video/mp4', 'video/webm', 'video/quicktime']
const MAX_IMAGE_BYTES = 10 * 1024 * 1024
const MAX_VIDEO_BYTES = 50 * 1024 * 1024

export function getMediaKind(file) {
  if (!file) return null
  if (IMAGE_TYPES.includes(file.type) || file.type.startsWith('image/')) return 'image'
  if (VIDEO_TYPES.includes(file.type) || file.type.startsWith('video/')) return 'video'
  return null
}

export function validateBoardMediaFile(file) {
  if (!file) return null

  const kind = getMediaKind(file)
  if (!kind) {
    return '画像（JPG/PNG/GIF/WebP）または動画（MP4/WebM/MOV）を選択してください'
  }

  const max = kind === 'image' ? MAX_IMAGE_BYTES : MAX_VIDEO_BYTES
  if (file.size > max) {
    const limitMb = max / (1024 * 1024)
    return `ファイルサイズは${limitMb}MB以下にしてください`
  }

  return null
}

export function revokeMediaPreview(url) {
  if (url?.startsWith('blob:')) {
    URL.revokeObjectURL(url)
  }
}
