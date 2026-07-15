function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

function buildPdfHtml({ year, summary, timeline, coverDesignLabel }) {
  const entries = (timeline || []).map((item) => `
    <article class="entry">
      <p class="entry-meta">${escapeHtml(item.dateDisplay || item.date)} · ${escapeHtml(item.categoryLabel)}</p>
      <h3>${escapeHtml(item.title)}</h3>
      <p>${escapeHtml(item.description || '')}</p>
    </article>
  `).join('')

  return `<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <title>${escapeHtml(year)}年 Music Memories</title>
  <style>
    body { font-family: "Hiragino Mincho ProN", "Yu Mincho", serif; color: #3d2450; margin: 32px; line-height: 1.8; }
    h1 { font-size: 28px; margin: 0 0 8px; letter-spacing: 0.08em; }
    .sub { color: #6b5b73; margin: 0 0 24px; font-size: 14px; }
    .hint {
      margin: 0 0 20px;
      padding: 12px 16px;
      border-radius: 8px;
      background: #f5eef8;
      border: 1px solid #dcc9e4;
      font-size: 13px;
      color: #5d3a6b;
    }
    .stats { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 28px; }
    .stat { border: 1px solid #ddd; border-radius: 8px; padding: 12px; text-align: center; }
    .stat strong { display: block; font-size: 22px; color: #5d3a6b; }
    .entry { border-top: 1px solid #e8e0ec; padding: 16px 0; page-break-inside: avoid; }
    .entry-meta { font-size: 12px; color: #8a7a92; margin: 0 0 6px; }
    .entry h3 { margin: 0 0 8px; font-size: 16px; }
    .entry p { margin: 0; font-size: 13px; color: #4a3f50; white-space: pre-line; }
    .footer { margin-top: 32px; font-size: 11px; color: #9a8aa2; text-align: center; }
    @page { size: A4; margin: 18mm; }
    @media print {
      body { margin: 0; }
      .hint { display: none !important; }
    }
  </style>
</head>
<body>
  <p class="hint">印刷ダイアログで「PDFに保存」または「Microsoft Print to PDF」を選ぶと、ファイルとして保存できます。</p>
  <h1>${escapeHtml(year)}年の Music Memories</h1>
  <p class="sub">Music Memory Book · 表紙: ${escapeHtml(coverDesignLabel || 'デザイン 1')}</p>
  <div class="stats">
    <div class="stat"><strong>${summary?.flowers ?? 0}</strong>献花</div>
    <div class="stat"><strong>${summary?.posts ?? 0}</strong>思い出投稿</div>
    <div class="stat"><strong>${summary?.songs ?? 0}</strong>お気に入り楽曲</div>
    <div class="stat"><strong>${summary?.aiChats ?? 0}</strong>AIとの会話</div>
    <div class="stat"><strong>${summary?.total ?? 0}</strong>合計</div>
  </div>
  ${entries || '<p>この年の思い出はまだありません。</p>'}
  <p class="footer">Music Memory Book — MISORA HIBARI</p>
  <script>
    window.addEventListener('load', function () {
      setTimeout(function () {
        window.focus();
        window.print();
      }, 250);
    });
  <\/script>
</body>
</html>`
}

function triggerPrint(targetWindow) {
  setTimeout(() => {
    try {
      targetWindow.focus()
      targetWindow.print()
    } catch {
      // ignore — user can still use browser print manually
    }
  }, 300)
}

function printViaIframe(html) {
  const iframe = document.createElement('iframe')
  iframe.setAttribute('title', 'Music Memory Book PDF')
  iframe.style.cssText = 'position:fixed;right:0;bottom:0;width:0;height:0;border:0;opacity:0;pointer-events:none'
  document.body.appendChild(iframe)

  const frameWindow = iframe.contentWindow
  const doc = frameWindow?.document
  if (!doc) {
    iframe.remove()
    throw new Error('PDFの準備に失敗しました。')
  }

  doc.open()
  doc.write(html)
  doc.close()
  triggerPrint(frameWindow)
  setTimeout(() => iframe.remove(), 60_000)
}

/**
 * 年別アルバムを印刷用ウィンドウで開き、PDF保存ダイアログを表示
 */
export function exportYearAlbumPdf({ year, summary, timeline, coverDesignLabel }) {
  const html = buildPdfHtml({ year, summary, timeline, coverDesignLabel })
  const blob = new Blob([html], { type: 'text/html;charset=utf-8' })
  const blobUrl = URL.createObjectURL(blob)

  const printWindow = window.open(blobUrl, '_blank')
  if (!printWindow) {
    URL.revokeObjectURL(blobUrl)
    printViaIframe(html)
    return
  }

  const cleanup = () => URL.revokeObjectURL(blobUrl)
  printWindow.addEventListener('load', () => {
    cleanup()
    triggerPrint(printWindow)
  }, { once: true })

  // load が発火しない環境向けフォールバック
  setTimeout(() => {
    cleanup()
    if (!printWindow.closed) triggerPrint(printWindow)
  }, 1200)
}
