<script setup>
/**
 * 部品名: AI 美空ひばりモーダル（デモ応答）
 * 用途: チャット UI。実 API 未接続時は定型文で返す（ライトテーマ）
 */
import { ref } from 'vue'
import ModalShell from './ModalShell.vue'
import TabBar from '../ui/TabBar.vue'
import UiButton from '../ui/UiButton.vue'

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
    <div class="ai-modal__notice">
      ⚠ このAIは美空ひばりの言葉・歌・生涯をもとに生成された応答です。
      <strong>実際の美空ひばり本人の発言ではありません。</strong>
    </div>

    <TabBar
      :dark="false"
      :tabs="[
        { id: 'chat', label: '対話モード' },
        { id: 'lyric', label: '新曲制作支援', icon: 'disc' },
      ]"
      :active="aiTab"
      @update:active="(v) => (aiTab = v)"
    />

    <div v-if="aiTab === 'chat'" class="ai-modal__chat">
      <div class="ai-modal__messages">
        <div
          v-for="(m, i) in messages"
          :key="i"
          class="ai-modal__row"
          :class="m.role === 'user' ? 'ai-modal__row--user' : 'ai-modal__row--ai'"
        >
          <div class="ai-modal__bubble" :class="m.role === 'user' ? 'ai-modal__bubble--user' : 'ai-modal__bubble--ai'">
            <div v-if="m.role === 'ai'" class="ai-modal__bubble-label">AI美空ひばり</div>
            {{ m.text }}
          </div>
        </div>
        <div v-if="loading" class="ai-modal__loading">……</div>
      </div>
      <div class="ai-modal__input-row">
        <input
          v-model="input"
          class="ai-modal__input"
          placeholder="ひばりさんに話しかける…"
          aria-label="メッセージを入力"
          @keydown.enter.prevent="send"
        />
        <UiButton variant="primary" size="md" :disabled="loading" @click="send">送信</UiButton>
      </div>
      <p class="ai-modal__hint">一般会員: 月10回まで · プレミアム: 無制限</p>
    </div>

    <div v-if="aiTab === 'lyric'" class="ai-modal__lyric">
      <div class="ai-modal__premium">
        🔒 このモードはプレミアム会員限定です。
        <button type="button" class="ai-modal__premium-link">アップグレードする ›</button>
      </div>
      <div class="ai-modal__lyric-fields">
        <input v-model="lyricForm.theme" class="ai-modal__input" placeholder="テーマ（例: 別れ・故郷・再会）" aria-label="テーマ" />
        <input v-model="lyricForm.mood" class="ai-modal__input" placeholder="ムード（例: 切ない・温かい・力強い）" aria-label="ムード" />
        <input v-model="lyricForm.scene" class="ai-modal__input" placeholder="情景（例: 港・夕暮れ・雪の夜）" aria-label="情景" />
      </div>
      <UiButton variant="primary" size="md" :disabled="lyricLoading" @click="generateLyric">歌詞案を生成</UiButton>
      <div v-if="lyricResult" class="ai-modal__lyric-result">{{ lyricResult }}</div>
    </div>
  </ModalShell>
</template>

<style scoped>
.ai-modal__notice {
  padding: 10px 14px;
  margin-bottom: 20px;
  font-size: 11px;
  line-height: 1.7;
  color: var(--site-text-muted);
  background: var(--site-surface-muted);
  border: 1px solid var(--site-border);
  border-left: 3px solid var(--kin-500);
  border-radius: var(--site-radius-sm);
}
.ai-modal__chat {
  margin-top: 16px;
}
.ai-modal__messages {
  max-height: 260px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
  padding: 4px 0;
}
.ai-modal__row {
  display: flex;
}
.ai-modal__row--user {
  justify-content: flex-end;
}
.ai-modal__row--ai {
  justify-content: flex-start;
}
.ai-modal__bubble {
  padding: 10px 14px;
  max-width: 85%;
  font-size: 13px;
  line-height: 1.8;
  font-family: var(--ff-serif);
  border-radius: var(--site-radius-md);
}
.ai-modal__bubble--user {
  background: var(--murasaki-700);
  color: #fff;
  border: 1px solid var(--murasaki-800);
  border-radius: 12px 12px 4px 12px;
}
.ai-modal__bubble--ai {
  background: var(--site-surface-muted);
  color: var(--site-text);
  border: 1px solid var(--site-border);
  border-radius: 12px 12px 12px 4px;
}
.ai-modal__bubble-label {
  font-size: 10px;
  color: var(--kin-600);
  letter-spacing: 0.15em;
  margin-bottom: 4px;
  font-family: var(--ff-mincho);
}
.ai-modal__loading {
  text-align: center;
  color: var(--murasaki-600);
  font-family: var(--ff-mincho);
  font-size: 13px;
}
.ai-modal__input-row {
  display: flex;
  gap: 10px;
}
.ai-modal__input {
  flex: 1;
  min-width: 0;
  background: var(--site-surface);
  border: 1px solid var(--site-border-strong);
  color: var(--site-text);
  padding: 10px 12px;
  font-family: var(--ff-serif);
  font-size: 13px;
  border-radius: var(--site-radius-sm);
  outline: none;
}
.ai-modal__input:focus {
  border-color: var(--murasaki-400);
}
.ai-modal__hint {
  margin: 10px 0 0;
  font-size: 11px;
  color: var(--site-text-light);
}
.ai-modal__lyric {
  margin-top: 16px;
}
.ai-modal__premium {
  padding: 10px 14px;
  margin-bottom: 20px;
  font-size: 12px;
  line-height: 1.7;
  color: var(--site-text);
  background: var(--site-bg-pink);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
}
.ai-modal__premium-link {
  background: transparent;
  border: 0;
  color: var(--murasaki-700);
  cursor: pointer;
  font-family: var(--ff-mincho);
  font-size: 12px;
  padding: 0;
  margin-left: 4px;
}
.ai-modal__premium-link:hover {
  text-decoration: underline;
}
.ai-modal__lyric-fields {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}
.ai-modal__lyric-result {
  margin-top: 20px;
  padding: 20px;
  background: var(--site-surface-muted);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  font-size: 14px;
  color: var(--site-text);
  line-height: 2;
  font-family: var(--ff-mincho);
  white-space: pre-wrap;
}

@media (max-width: 480px) {
  .ai-modal__input-row {
    flex-direction: column;
  }
  .ai-modal__bubble {
    max-width: 92%;
  }
}
</style>
