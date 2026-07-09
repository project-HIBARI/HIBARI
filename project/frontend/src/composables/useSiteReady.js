/**
 * サイトイントロ完了（.site-shell--ready）を待つユーティリティ
 */
export function prefersReducedMotion() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

export function whenSiteReady(callback) {
  const shell = document.querySelector('.site-shell')
  if (!shell || shell.classList.contains('site-shell--ready')) {
    callback()
    return () => {}
  }

  const observer = new MutationObserver(() => {
    if (shell.classList.contains('site-shell--ready')) {
      observer.disconnect()
      requestAnimationFrame(() => {
        requestAnimationFrame(callback)
      })
    }
  })
  observer.observe(shell, { attributes: true, attributeFilter: ['class'] })
  return () => observer.disconnect()
}
