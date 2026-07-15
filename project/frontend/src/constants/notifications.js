/**
 * SNS通知の種別定義（バックエンド notification_service.py の定数と一致させる）
 */

export const NOTIFICATION_TYPE = {
  POST_LIKE: 'post_like',
  POST_COMMENT: 'post_comment',
  FOLLOW: 'follow',
  DM_MESSAGE: 'dm_message',
  DM_REQUEST: 'dm_request',
  STORY_REACTION: 'story_reaction',
  STORY_REPLY: 'story_reply',
}

/** 通知アイコン（UiIco の name） */
export const NOTIFICATION_ICON = {
  [NOTIFICATION_TYPE.POST_LIKE]: 'heart',
  [NOTIFICATION_TYPE.POST_COMMENT]: 'chat',
  [NOTIFICATION_TYPE.FOLLOW]: 'user',
  [NOTIFICATION_TYPE.DM_MESSAGE]: 'mail',
  [NOTIFICATION_TYPE.DM_REQUEST]: 'mail',
  [NOTIFICATION_TYPE.STORY_REACTION]: 'heart',
  [NOTIFICATION_TYPE.STORY_REPLY]: 'send',
}

/**
 * 通知1件をタップしたときの遷移先を解決する。
 * 戻り値: { view, params } または null（遷移不要）
 */
export function resolveNotificationTarget(notification) {
  switch (notification.notification_type) {
    case NOTIFICATION_TYPE.POST_LIKE:
    case NOTIFICATION_TYPE.POST_COMMENT:
      return notification.target_deleted || !notification.post_id
        ? null
        : { view: 'post', postId: notification.post_id, commentId: notification.comment_id }
    case NOTIFICATION_TYPE.FOLLOW:
      return { view: 'profile', accountId: notification.actor_account_id }
    case NOTIFICATION_TYPE.DM_MESSAGE:
    case NOTIFICATION_TYPE.DM_REQUEST:
    case NOTIFICATION_TYPE.STORY_REACTION:
    case NOTIFICATION_TYPE.STORY_REPLY:
      return notification.thread_id ? { view: 'dm', threadId: notification.thread_id } : null
    default:
      return null
  }
}
