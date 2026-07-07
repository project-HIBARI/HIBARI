/**
 * 公式SNSリンク（URLはここで一元管理）
 */
export const socialLinks = [
  {
    id: 'instagram',
    label: 'Instagram',
    href: '#',
    icon: 'icons8-instagram.png',
  },
  {
    id: 'x',
    label: 'X',
    href: '#',
    icon: 'icons8-x.png',
  },
  {
    id: 'youtube',
    label: 'YouTube',
    href: '#',
    icon: 'icons8-youtube.png',
  },
  {
    id: 'facebook',
    label: 'Facebook',
    href: '#',
    icon: 'icons8-facebook.png',
  },
  {
    id: 'line',
    label: 'LINE',
    href: '#',
    icon: 'icons8-line.png',
  },
]

/** @param {string} filename */
export function socialIconUrl(filename) {
  return `/images/social/${filename}`
}
