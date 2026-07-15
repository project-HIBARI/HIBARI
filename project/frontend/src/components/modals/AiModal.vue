<script setup>
/**
 * 部品名: AI 美空ひばりモーダル（デモ応答）
 * 用途: チャット UI。会員区分に応じた利用制限を適用
 */
import { ref, computed, onMounted } from 'vue'
import ModalShell from './ModalShell.vue'
import TabBar from '../ui/TabBar.vue'
import UiButton from '../ui/UiButton.vue'
import {
  isPremiumMember,
  PERMISSION,
  hasPermission,
} from '../../constants/membership.js'
import { bindAiUsageRef, refreshAiUsageStatus, consumeAiUsage } from '../../lib/aiUsage.js'
import { sendChatMessage } from '../../lib/chatApi.js'
import { HIBARI_AVATAR_SRC, HIBARI_AVATAR_ALT } from '../../lib/hibariAvatar.js'

const props = defineProps({
  membership: { type: String, default: 'general' },
  isLoggedIn: { type: Boolean, default: false },
  accountId: { type: [Number, String], default: null },
})

const emit = defineEmits(['close', 'open-auth'])

const aiTab = ref('chat')
const messages = ref([
  { role: 'ai', text: 'こんにちは。私は美空ひばりの言葉・楽曲・生涯をもとにした応答AIです。どうぞ、お話しかけてください。' },
])
const input = ref('')
const loading = ref(false)
const chatError = ref('')
const usageStatus = ref(null)
const lyricForm = ref({ theme: '', mood: '', scene: '' })
const lyricResult = ref('')
const lyricLoading = ref(false)
const currentRoomId = ref(null)

bindAiUsageRef(usageStatus)

const isPremium = computed(
  () => props.isLoggedIn && isPremiumMember(props.membership),
)
const remainingChats = computed(() => usageStatus.value?.remaining ?? null)
const canSendChat = computed(() => {
  if (usageStatus.value != null) return Boolean(usageStatus.value.can_use)
  return false
})
const guestResetLabel = computed(() => usageStatus.value?.reset_label ?? '')
const isGuestUsage = computed(() => usageStatus.value?.is_guest ?? !props.isLoggedIn)
const canUseLyric = computed(() => props.isLoggedIn && hasPermission(props.membership, PERMISSION.EXCLUSIVE_CONTENT))

onMounted(() => {
  refreshAiUsageStatus().catch(() => {
    chatError.value = '利用状況を取得できません。バックエンドの起動を確認してください。'
  })
})

function getDemoReply(userMsg) {
  const text = userMsg.trim()

  if (/こんにちは|こんばんは|おはよう|はじめまして/i.test(text)) {
    return 'こんにちは。いつも歌を聴いてくださって、ありがとうございます。今日はどんなお話をしましょうか。'
  }
  if (/歌|曲|うた|シングル|名曲/i.test(text)) {
    return '「川の流れのように」「いつでも夢を」… 皆さんに愛された曲がたくさんありますね。どの曲がお好きですか。'
  }
  if (/出身|九州|福岡|ゆかり|地元/i.test(text)) {
    return '博多生まれの私ですが、全国の皆さんの応援があってこそでした。故郷の風景も、今でも大切に思っています。'
  }
  if (/ありがとう|感謝|お礼/i.test(text)) {
    return 'こちらこそ、温かいお言葉をありがとうございます。あなたの想いが、とてもうれしいです。'
  }
  if (/さようなら|ばいばい|またね/i.test(text)) {
    return 'はい、またお話ししましょう。いつでも、ここでお待ちしていますね。'
  }

  return `「${text}」ですね。ありがとうございます。デモ版のため簡単なお返事になりますが、いつもひばりを想ってくださる心がとてもうれしいです。`
}

async function send() {
  if (!input.value.trim() || loading.value) return
  chatError.value = ''

  if (!canSendChat.value) {
    chatError.value = props.isLoggedIn
      ? '一般会員の今月の利用上限（10回）に達しました。プレミアム会員は無制限でご利用いただけます。'
      : `非会員の利用上限（10回）に達しました。${guestResetLabel.value} に解除されます。会員登録後は月10回までご利用いただけます（プレミアムは無制限）。`
    return
  }

  const userMsg = input.value.trim()
  input.value = ''
  messages.value.push({ role: 'user', text: userMsg })

  try {
    if (!isPremium.value) {
      await consumeAiUsage()
    }
  } catch (err) {
    messages.value.pop()
    input.value = userMsg
    chatError.value = err.message || '送信に失敗しました。'
    return
  }

  loading.value = true

    if (props.isLoggedIn) {
    try {
      const data = await sendChatMessage({
        message: userMsg,
        roomId: currentRoomId.value,
      })
      if (data.room_id) currentRoomId.value = Number(data.room_id)
      messages.value.push({
        role: 'ai',
        text: data.message,
      })
    } catch (err) {
      messages.value.push({
        role: 'ai',
        text: getDemoReply(userMsg),
      })
      if (err.status === 401) {
        chatError.value = 'ログインが必要です。簡易応答を表示しています。'
      } else {
        chatError.value = 'AIサーバーに接続できなかったため、簡易応答を表示しています。'
      }
    } finally {
      loading.value = false
    }
    return
  }

  window.setTimeout(() => {
    messages.value.push({
      role: 'ai',
      text: getDemoReply(userMsg),
    })
    loading.value = false
  }, 600)
}

function generateLyric() {
  if (!canUseLyric.value) return
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
      <p v-if="!isLoggedIn" class="ai-modal__gate">
        非会員の方も AIひばりと10回までお話しいただけます（あと {{ remainingChats ?? '—' }} 回）。
        上限到達後は1週間で解除されます。
        <button type="button" class="ai-modal__gate-link" @click="emit('open-auth', 'login')">ログイン</button>
        /
        <button type="button" class="ai-modal__gate-link" @click="emit('open-auth', 'register')">会員登録</button>
        で特典をご確認ください。
      </p>
      <div class="ai-modal__messages">
        <div
          v-for="(m, i) in messages"
          :key="i"
          class="ai-modal__row"
          :class="m.role === 'user' ? 'ai-modal__row--user' : 'ai-modal__row--ai'"
        >
          <img
            v-if="m.role === 'ai'"
            :src="HIBARI_AVATAR_SRC"
            :alt="HIBARI_AVATAR_ALT"
            class="ai-modal__avatar"
            width="40"
            height="40"
            decoding="async"
          />
          <div class="ai-modal__bubble" :class="m.role === 'user' ? 'ai-modal__bubble--user' : 'ai-modal__bubble--ai'">
            <div v-if="m.role === 'ai'" class="ai-modal__bubble-label">AI美空ひばり</div>
            {{ m.text }}
          </div>
        </div>
        <div v-if="loading" class="ai-modal__row ai-modal__row--ai ai-modal__row--loading">
          <img
            :src="HIBARI_AVATAR_SRC"
            :alt="HIBARI_AVATAR_ALT"
            class="ai-modal__avatar"
            width="40"
            height="40"
            decoding="async"
          />
          <div class="ai-modal__bubble ai-modal__bubble--ai ai-modal__bubble--typing" aria-live="polite">
            <div class="ai-modal__bubble-label">AI美空ひばり</div>
            <span class="ai-modal__typing">……</span>
          </div>
        </div>
      </div>
      <div class="ai-modal__input-row">
        <input
          v-model="input"
          class="ai-modal__input"
          placeholder="ひばりさんに話しかける…"
          aria-label="メッセージを入力"
          :disabled="!canSendChat"
          @keydown.enter.prevent="send"
        />
        <UiButton
          variant="primary"
          size="md"
          :disabled="loading || !canSendChat"
          @click="send"
        >
          送信
        </UiButton>
      </div>
      <p v-if="chatError" class="ai-modal__error" role="alert">{{ chatError }}</p>
      <p class="ai-modal__hint">
        <template v-if="isPremium">プレミアム会員: AIひばり対話 無制限</template>
        <template v-else-if="isLoggedIn">一般会員: 今月あと {{ remainingChats ?? '—' }} 回（月10回まで）</template>
        <template v-else-if="!canSendChat && isGuestUsage">非会員: 上限到達。{{ guestResetLabel }} に解除されます</template>
        <template v-else>非会員: あと {{ remainingChats ?? '—' }} 回（10回まで・上限到達後1週間で解除）</template>
      </p>
    </div>

    <div v-if="aiTab === 'lyric'" class="ai-modal__lyric">
      <div v-if="!canUseLyric" class="ai-modal__premium">
        🔒 新曲制作支援はプレミアム会員限定の限定コンテンツです。
        <button type="button" class="ai-modal__premium-link" @click="emit('open-auth', 'register')">プレミアムに登録 ›</button>
      </div>
      <template v-else>
      <div class="ai-modal__lyric-fields">
        <input v-model="lyricForm.theme" class="ai-modal__input" placeholder="テーマ（例: 別れ・故郷・再会）" aria-label="テーマ" />
        <input v-model="lyricForm.mood" class="ai-modal__input" placeholder="ムード（例: 切ない・温かい・力強い）" aria-label="ムード" />
        <input v-model="lyricForm.scene" class="ai-modal__input" placeholder="情景（例: 港・夕暮れ・雪の夜）" aria-label="情景" />
      </div>
      <UiButton variant="primary" size="md" :disabled="lyricLoading" @click="generateLyric">歌詞案を生成</UiButton>
      <div v-if="lyricResult" class="ai-modal__lyric-result">{{ lyricResult }}</div>
      </template>
    </div>
  </ModalShell>
</template>

<style scoped>
.ai-modal__notice {
  padding: 10px 14px;
  margin-bottom: 20px;
  font-size: var(--font-size-caption);
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
  align-items: flex-end;
  gap: 10px;
}
.ai-modal__row--user {
  justify-content: flex-end;
}
.ai-modal__row--ai {
  justify-content: flex-start;
}
.ai-modal__avatar {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--kin-500);
  box-shadow: 0 2px 8px rgba(60, 40, 30, 0.12);
  background: var(--site-surface-muted);
}
.ai-modal__bubble {
  padding: 10px 14px;
  max-width: 85%;
  font-size: var(--font-size-button);
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
  font-size: var(--font-size-badge);
  color: var(--kin-600);
  letter-spacing: 0.15em;
  margin-bottom: 4px;
  font-family: var(--ff-mincho);
}
.ai-modal__typing {
  color: var(--murasaki-600);
  font-family: var(--ff-mincho);
  font-size: var(--font-size-button);
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
  font-size: var(--font-size-button);
  border-radius: var(--site-radius-sm);
  outline: none;
}
.ai-modal__input:focus {
  border-color: var(--murasaki-400);
}
.ai-modal__hint {
  margin: 10px 0 0;
  font-size: var(--font-size-caption);
  color: var(--site-text-light);
}
.ai-modal__gate {
  margin: 0 0 12px;
  padding: 10px 12px;
  font-size: var(--font-size-caption);
  line-height: 1.7;
  color: var(--site-text-muted);
  background: var(--site-surface-muted);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
}
.ai-modal__gate-link {
  background: transparent;
  border: 0;
  padding: 0;
  color: var(--murasaki-700);
  cursor: pointer;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-caption);
  text-decoration: underline;
}
.ai-modal__error {
  margin: 10px 0 0;
  font-size: var(--font-size-caption);
  line-height: 1.6;
  color: #9b2c2c;
}
.ai-modal__lyric {
  margin-top: 16px;
}
.ai-modal__premium {
  padding: 10px 14px;
  margin-bottom: 20px;
  font-size: var(--font-size-caption);
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
  font-size: var(--font-size-caption);
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
  font-size: var(--font-size-small);
  color: var(--site-text);
  line-height: 2;
  font-family: var(--ff-mincho);
  white-space: pre-wrap;
}

@media (max-width: 767px) {
  .ai-modal__input-row {
    flex-direction: column;
  }
  .ai-modal__input-row :deep(button) {
    width: 100%;
    justify-content: center;
  }
  .ai-modal__bubble {
    max-width: 92%;
  }
}
</style>
