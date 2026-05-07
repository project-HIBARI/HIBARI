<script setup>
/**
 * 部品名: AI 美空ひばりモーダル（デモ応答）
 * 役割: チャット UI。実 API 未接続時は定型文で返す
 */
import { ref } from 'vue'
import ModalShell from './ModalShell.vue'
import TabBar from '../ui/TabBar.vue'
import { btnBeni, inputDark } from '../../utils/hibaru.js'

const emit = defineEmits(['close'])

const aiTab = ref('chat')
const messages = ref([
  { role: 'ai', text: 'こんにちは。私は美空ひばりの言葉・楽曲・生涯をもとにした応答AIです。どうぞ、お話しかけてください。' },
])
const input = ref('')
const loading = ref(false)
const lyricForm = ref({ theme: '', mood: '', scene: '' })
const lyricResult = ref('')
const lyricLoading = ref(false)

function send() {
  if (!input.value.trim() || loading.value) return
  const userMsg = input.value.trim()
  input.value = ''
  messages.value.push({ role: 'user', text: userMsg })
  loading.value = true
  window.setTimeout(() => {
    messages.value.push({
      role: 'ai',
      text: '（デモ）いつもひばりを想ってくださり、ありがとうございます。心温まるお言葉、大切に受け止めました。',
    })
    loading.value = false
  }, 600)
}

function generateLyric() {
  lyricLoading.value = true
  lyricResult.value = ''
  window.setTimeout(() => {
    lyricResult.value =
      '（デモ歌詞案）\n夕映えの港に　波の音ひとつ\n名も無き想いが　胸をよぎる\n別れはいつも　風の中\nそれでも明日を　信じて歩く'
    lyricLoading.value = false
  }, 800)
}
</script>

<template>
  <ModalShell title="✦ AI美空ひばり" @close="emit('close')">
    <div
      style="padding: 10px 14px; border: 1px solid rgba(201,169,97,0.4); margin-bottom: 20px; font-size: 11px; color: var(--paper-300); line-height: 1.7; background: rgba(201,169,97,0.04)"
    >
      ⚠ このAIは美空ひばりの言葉・歌・生涯をもとに生成された応答です。<strong>実際の美空ひばり本人の発言ではありません。</strong>
    </div>

    <TabBar
      :tabs="[
        { id: 'chat', label: '対話モード' },
        { id: 'lyric', label: '新曲制作支援', icon: 'disc' },
      ]"
      :active="aiTab"
      @update:active="(v) => (aiTab = v)"
    />

    <div v-if="aiTab === 'chat'" style="margin-top: 16px">
      <div style="max-height: 260px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; margin-bottom: 16px; padding: 4px 0">
        <div
          v-for="(m, i) in messages"
          :key="i"
          :style="{ display: 'flex', justifyContent: m.role === 'user' ? 'flex-end' : 'flex-start' }"
        >
          <div
            :style="{
              background: m.role === 'user' ? 'var(--beni-800)' : 'rgba(201,169,97,0.08)',
              border: `1px solid ${m.role === 'user' ? 'var(--beni-700)' : 'rgba(201,169,97,0.25)'}`,
              padding: '10px 14px',
              maxWidth: '80%',
              fontSize: '13px',
              lineHeight: 1.8,
              color: 'var(--paper-100)',
              fontFamily: 'var(--ff-serif)',
            }"
          >
            <div v-if="m.role === 'ai'" style="font-size: 10px; color: var(--kin-500); letter-spacing: 0.15em; margin-bottom: 4px">AI美空ひばり</div>
            {{ m.text }}
          </div>
        </div>
        <div v-if="loading" style="text-align: center; color: var(--kin-500); font-family: var(--ff-mincho); font-size: 13px">……</div>
      </div>
      <div style="display: flex; gap: 10px">
        <input
          v-model="input"
          placeholder="ひばりさんに話しかける…"
          :style="inputDark"
          aria-label="メッセージを入力"
          @keydown.enter.prevent="send"
        />
        <button type="button" :disabled="loading" :style="{ ...btnBeni, padding: '10px 20px', flexShrink: 0, fontSize: '12px' }" @click="send">
          送信
        </button>
      </div>
      <div style="margin-top: 10px; font-size: 11px; color: var(--paper-400)">一般会員: 月10回まで · プレミアム: 無制限</div>
    </div>

    <div v-if="aiTab === 'lyric'" style="margin-top: 16px">
      <div
        style="padding: 10px 14px; background: rgba(139,26,26,0.2); border: 1px solid var(--beni-700); margin-bottom: 20px; font-size: 12px; color: var(--paper-200); line-height: 1.7"
      >
        🔒 このモードはプレミアム会員限定です。
        <button type="button" style="background: transparent; border: 0; color: var(--kin-500); cursor: pointer; font-family: var(--ff-mincho); font-size: 12px">
          アップグレードする ›
        </button>
      </div>
      <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 16px">
        <input v-model="lyricForm.theme" placeholder="テーマ（例: 別れ・故郷・再会）" :style="inputDark" aria-label="テーマ" />
        <input v-model="lyricForm.mood" placeholder="ムード（例: 切ない・温かい・力強い）" :style="inputDark" aria-label="ムード" />
        <input v-model="lyricForm.scene" placeholder="情景（例: 港・夕暮れ・雪の夜）" :style="inputDark" aria-label="情景" />
      </div>
      <button type="button" :disabled="lyricLoading" :style="{ ...btnBeni, fontSize: '12px' }" @click="generateLyric">歌詞案を生成</button>
      <div
        v-if="lyricResult"
        style="margin-top: 20px; padding: 20px; background: rgba(201,169,97,0.05); border: 1px solid rgba(201,169,97,0.3); font-size: 14px; color: var(--paper-100); line-height: 2; font-family: var(--ff-mincho); white-space: pre-wrap"
      >
        {{ lyricResult }}
      </div>
    </div>
  </ModalShell>
</template>
