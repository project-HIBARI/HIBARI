import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { exec } from 'node:child_process'

/**
 * プラグイン: 開発サーバー起動後に Chrome で URL を開く
 * - Cursor 内の簡易プレビューではなく、実ブラウザで確認したい場合向け
 */
function openChromeDev() {
  return {
    name: 'open-chrome-dev',
    configureServer(server) {
      server.httpServer?.once('listening', () => {
        const addr = server.httpServer.address()
        const port =
          typeof addr === 'object' && addr && 'port' in addr
            ? addr.port
            : (server.config.server?.port ?? 5173)
        const url = `http://127.0.0.1:${port}/`

        if (process.platform === 'win32') {
          exec(`start chrome "${url}"`, { shell: 'cmd.exe' })
        } else if (process.platform === 'darwin') {
          exec(`open -a "Google Chrome" "${url}"`)
        } else {
          exec(`xdg-open "${url}"`, () => {})
        }
      })
    },
  }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), openChromeDev()],
  server: {
    /** Windows で localhost(IPv6) と 127.0.0.1(IPv4) の食い違いで ERR_CONNECTION_REFUSED になるのを防ぐ */
    host: '127.0.0.1',
    port: 5173,
    strictPort: true,
    /** Vite 標準の --open は既定ブラウザになるため明示的に false */
    open: false,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
    },
  },
})
