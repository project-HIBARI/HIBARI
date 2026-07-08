import { apiRequest } from './client.js'

export function createPost(payload) {
  return apiRequest('/api/posts', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function fetchPosts() {
  return apiRequest('/api/posts')
}

/**
 * 掲示板用メディア（画像・動画）をアップロード
 * @returns {Promise<{ path: string, media_type: 'image'|'video' }>}
 */
export async function uploadPostMedia(file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch('/api/posts/upload', {
    method: 'POST',
    credentials: 'include',
    body: formData,
  })

  let data = null
  const contentType = response.headers.get('content-type') || ''
  if (contentType.includes('application/json')) {
    data = await response.json()
  }

  if (!response.ok) {
    const message = data?.error || `アップロードに失敗しました（${response.status}）`
    const error = new Error(message)
    error.status = response.status
    error.data = data
    throw error
  }

  return data
}

/**
 * メディア付き投稿を作成（ファイルがある場合は先にアップロード）
 */
export async function createPostWithMedia(payload, mediaFile) {
  let image_path = payload.image_path ?? null
  let video_path = payload.video_path ?? null

  if (mediaFile) {
    const uploaded = await uploadPostMedia(mediaFile)
    if (uploaded.media_type === 'image') {
      image_path = uploaded.path
    } else {
      video_path = uploaded.path
    }
  }

  const result = await createPost({
    ...payload,
    image_path,
    video_path,
  })

  return { ...result, image_path, video_path }
}
