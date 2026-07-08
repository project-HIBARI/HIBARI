/**
 * エントリポイント — Vue アプリ起動
 */
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { useTextSize } from './composables/useTextSize.js'

useTextSize()

createApp(App).mount('#app')
