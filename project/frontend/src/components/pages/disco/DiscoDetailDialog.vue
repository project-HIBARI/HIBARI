<script setup>
/**
 * 部品名: ディスコグラフィ — 楽曲詳細ダイアログ
 * 用途: 選択した楽曲のメタデータと「同じ曲で泣いた人マッチング」を表示する（ライトテーマ）
 */
import { ref, computed, watch } from 'vue'
import ModalShell from '../../modals/ModalShell.vue'
import RecordChip from '../../ui/RecordChip.vue'
import UiIco from '../../ui/UiIco.vue'
import { useMemberAccess } from '../../../composables/useMemberAccess.js'
import {
  fetchSongMemories,
  fetchSongMemorySummary,
  createSongMemory,
  fetchSongChatRoom,
} from '../../../api/songMemories.js'
import { MEMORY_TYPES, VISIBILITY_OPTIONS, memoryTypeMeta } from '../../../constants/songMemory.js'

const MAX_COMMENT_LENGTH = 20

const props = defineProps({
  detail: { type: Object, default: null },
})

const emit = defineEmits(['close', 'need-auth', 'open-song-chat', 'search-song-fans'])

const { isLoggedIn, canUse, PERMISSION } = useMemberAccess()

const memoriesLoading = ref(false)
const memoriesError = ref('')
const memories = ref([])
const summaryCount = ref(0)

const selectedType = ref('')
const comment = ref('')
const visibility = ref('public')
const submitting = ref(false)
const submitError = ref('')
const submitted = ref(false)

const chatLoading = ref(false)

async function loadMemories(songId) {
  memoriesLoading.value = true
  memoriesError.value = ''
  try {
    const [summaryRes, listRes] = await Promise.all([
      fetchSongMemorySummary(songId),
      fetchSongMemories(songId),
    ])
    summaryCount.value = summaryRes?.count || 0
    memories.value = listRes?.memories || []
  } catch (err) {
    memoriesError.value = err.message || '思い出の取得に失敗しました'
  } finally {
    memoriesLoading.value = false
  }
}

watch(
  () => props.detail,
  (song) => {
    selectedType.value = ''
    comment.value = ''
    visibility.value = 'public'
    submitError.value = ''
    submitted.value = false
    memories.value = []
    summaryCount.value = 0
    if (song?.songId) {
      loadMemories(song.songId)
    }
  },
)

const commentLength = computed(() => comment.value.length)

async function onSubmit() {
  if (!props.detail?.songId || !selectedType.value) return

  if (!isLoggedIn.value) {
    emit('need-auth', 'login')
    return
  }

  submitting.value = true
  submitError.value = ''
  try {
    await createSongMemory(props.detail.songId, {
      memoryType: selectedType.value,
      comment: comment.value.trim(),
      visibility: visibility.value,
    })
    submitted.value = true
    await loadMemories(props.detail.songId)
  } catch (err) {
    submitError.value = err.message || '登録に失敗しました'
  } finally {
    submitting.value = false
  }
}

async function onJoinChat() {
  if (!props.detail?.songId) return

  if (!canUse(PERMISSION.OPEN_CHAT)) {
    emit('need-auth', isLoggedIn.value ? 'register' : 'login')
    return
  }

  chatLoading.value = true
  try {
    const res = await fetchSongChatRoom(props.detail.songId)
    if (res?.room_id) {
      emit('open-song-chat', res.room_id)
      emit('close')
    }
  } catch (err) {
    submitError.value = err.message || 'チャットルームの取得に失敗しました'
  } finally {
    chatLoading.value = false
  }
}
</script>

<template>
  <ModalShell v-if="detail" :title="detail.title" @close="emit('close')">
    <div class="disco-detail">
      <div class="disco-detail__header">
        <RecordChip :no="detail.no" color="var(--beni-700)" />
        <div class="disco-detail__intro">
          <span class="disco-detail__year">{{ detail.year }} · {{ detail.label }}</span>
          <p class="disco-detail__romaji">{{ detail.romaji }}</p>
        </div>
      </div>

      <dl class="disco-detail__dl">
        <dt>発売年</dt>
        <dd>{{ detail.year }}年</dd>
        <dt>形態</dt>
        <dd>{{ detail.type }}</dd>
        <dt>ジャンル</dt>
        <dd>{{ detail.genre }}</dd>
        <dt>作詞</dt>
        <dd>{{ detail.lyric }}</dd>
        <dt>作曲</dt>
        <dd>{{ detail.music }}</dd>
        <dt>品番</dt>
        <dd class="disco-detail__mono">{{ detail.no }}</dd>
        <dt>レーベル</dt>
        <dd>{{ detail.label }}</dd>
      </dl>

      <div v-if="detail.note" class="disco-detail__note">
        {{ detail.note }}
      </div>

      <div v-if="detail.songId" class="disco-memory">
        <hr class="hr-gold disco-memory__rule" />
        <div class="disco-memory__head">
          <h3 class="disco-memory__title">思い出の曲マッチング</h3>
          <p class="disco-memory__count">
            {{ summaryCount }}人がこの曲に思い出を寄せています
          </p>
        </div>

        <fieldset class="disco-memory__types">
          <legend class="sr-only">思い出の種類</legend>
          <button
            v-for="type in MEMORY_TYPES"
            :key="type.value"
            type="button"
            class="disco-memory__type"
            :class="{ 'disco-memory__type--on': selectedType === type.value }"
            @click="selectedType = type.value"
          >
            <UiIco
              :name="type.icon"
              :size="20"
              :color="selectedType === type.value ? 'var(--murasaki-700)' : 'var(--site-text-muted)'"
            />
            <span>{{ type.label }}</span>
          </button>
        </fieldset>

        <div class="disco-memory__form">
          <label class="disco-memory__comment-label" for="disco-memory-comment">
            ひとことコメント（任意・{{ MAX_COMMENT_LENGTH }}文字以内）
          </label>
          <input
            id="disco-memory-comment"
            v-model="comment"
            type="text"
            class="disco-memory__comment-input"
            :maxlength="MAX_COMMENT_LENGTH"
            placeholder="この曲の思い出を一言で…"
          />
          <span class="disco-memory__comment-count">{{ commentLength }}/{{ MAX_COMMENT_LENGTH }}</span>

          <fieldset class="disco-memory__visibility">
            <legend class="sr-only">公開範囲</legend>
            <button
              v-for="opt in VISIBILITY_OPTIONS"
              :key="opt.value"
              type="button"
              class="disco-memory__visibility-opt"
              :class="{ 'disco-memory__visibility-opt--on': visibility === opt.value }"
              @click="visibility = opt.value"
            >
              {{ opt.label }}
            </button>
          </fieldset>

          <p v-if="submitError" class="disco-memory__error">{{ submitError }}</p>
          <p v-if="submitted" class="disco-memory__success">思い出を登録しました</p>

          <button
            type="button"
            class="disco-memory__submit motion-button"
            :disabled="!selectedType || submitting"
            @click="onSubmit"
          >
            {{ submitting ? '登録中…' : '思い出を登録する' }}
          </button>

          <button
            type="button"
            class="disco-memory__chat motion-button"
            :disabled="chatLoading"
            @click="onJoinChat"
          >
            <UiIco name="chat" :size="15" color="var(--murasaki-700)" />
            この曲について語り合う
          </button>

          <button
            type="button"
            class="disco-memory__chat motion-button"
            @click="emit('search-song-fans', detail)"
          >
            <UiIco name="search" :size="15" color="var(--murasaki-700)" />
            同じ曲が好きな人を探す
          </button>
        </div>

        <div class="disco-memory__list">
          <p v-if="memoriesLoading" class="disco-memory__list-hint">読み込み中…</p>
          <p v-else-if="memoriesError" class="disco-memory__list-hint">{{ memoriesError }}</p>
          <p v-else-if="!memories.length" class="disco-memory__list-hint">まだ思い出が登録されていません</p>
          <ul v-else class="disco-memory__items">
            <li v-for="m in memories" :key="`${m.account_id}-${m.created_at}`" class="disco-memory__item">
              <UiIco
                v-if="memoryTypeMeta(m.memory_type)"
                :name="memoryTypeMeta(m.memory_type).icon"
                :size="16"
                color="var(--murasaki-700)"
              />
              <span class="disco-memory__item-name">{{ m.name }}</span>
              <span v-if="m.comment" class="disco-memory__item-comment">「{{ m.comment }}」</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </ModalShell>
</template>

<style scoped>
.disco-detail__header {
  display: flex;
  gap: var(--sp-5);
  align-items: center;
  margin-bottom: var(--sp-5);
}
.disco-detail__year {
  display: block;
  font-family: var(--ff-mono);
  font-size: 10px;
  letter-spacing: 0.15em;
  color: var(--kin-600);
  margin-bottom: 4px;
}
.disco-detail__romaji {
  margin: 0;
  font-family: var(--ff-latin);
  font-style: italic;
  font-size: 14px;
  color: var(--site-text-muted);
}
.disco-detail__dl {
  display: grid;
  grid-template-columns: 80px 1fr;
  gap: 10px 16px;
  font-size: 14px;
  margin: 0;
}
.disco-detail__dl dt {
  color: var(--kin-600);
  font-family: var(--ff-mincho);
  letter-spacing: 0.06em;
}
.disco-detail__dl dd {
  margin: 0;
  color: var(--site-text);
}
.disco-detail__mono {
  font-family: var(--ff-mono);
  font-size: 12px;
}
.disco-detail__note {
  margin-top: var(--sp-5);
  padding: var(--sp-4);
  background: var(--site-surface-muted);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
  font-size: 13px;
  line-height: 1.8;
  color: var(--site-text);
}

.disco-memory__rule {
  margin: var(--sp-5) 0;
}
.disco-memory__head {
  margin-bottom: var(--sp-4);
}
.disco-memory__title {
  margin: 0 0 4px;
  font-family: var(--ff-mincho);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--site-text);
}
.disco-memory__count {
  margin: 0;
  font-size: 12px;
  color: var(--site-text-muted);
}
.disco-memory__types {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 0 0 var(--sp-4);
  padding: 0;
  border: 0;
}
.disco-memory__type {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  background: var(--site-surface);
  color: var(--site-text-muted);
  font-size: 12px;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s, color 0.2s;
}
.disco-memory__type:hover {
  border-color: var(--murasaki-400);
}
.disco-memory__type--on {
  border-color: var(--murasaki-500);
  background: rgba(232, 223, 240, 0.45);
  color: var(--site-text);
}
.disco-memory__form {
  margin-bottom: var(--sp-4);
}
.disco-memory__comment-label {
  display: block;
  margin-bottom: 6px;
  font-size: 12px;
  color: var(--site-text-muted);
}
.disco-memory__comment-input {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 12px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
  background: var(--site-surface);
  color: var(--site-text);
  font-size: 13px;
}
.disco-memory__comment-count {
  display: block;
  margin: 4px 0 10px;
  font-size: 11px;
  color: var(--site-text-muted);
  text-align: right;
}
.disco-memory__visibility {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 0 0 var(--sp-4);
  padding: 0;
  border: 0;
}
.disco-memory__visibility-opt {
  padding: 8px 14px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  background: var(--site-surface);
  color: var(--site-text-muted);
  font-size: 12px;
  white-space: nowrap;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s, color 0.2s;
}
.disco-memory__visibility-opt:hover {
  border-color: var(--murasaki-400);
}
.disco-memory__visibility-opt--on {
  border-color: var(--murasaki-500);
  background: rgba(232, 223, 240, 0.45);
  color: var(--site-text);
}
.disco-memory__error {
  margin: 0 0 10px;
  font-size: 12px;
  color: var(--beni-700);
}
.disco-memory__success {
  margin: 0 0 10px;
  font-size: 12px;
  color: var(--murasaki-700);
}
.disco-memory__submit {
  display: block;
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--murasaki-500);
  border-radius: var(--site-radius-lg);
  background: var(--murasaki-700);
  color: #fff;
  font-family: var(--ff-mincho);
  font-size: 14px;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
}
.disco-memory__submit:hover:not(:disabled) {
  background: var(--murasaki-800, #4a2f63);
  border-color: var(--murasaki-700);
}
.disco-memory__submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.disco-memory__chat {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 100%;
  margin-top: 8px;
  padding: 10px 16px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  background: var(--site-surface);
  color: var(--site-text);
  font-size: 13px;
  cursor: pointer;
  transition: border-color 0.2s;
}
.disco-memory__chat:hover:not(:disabled) {
  border-color: var(--murasaki-400);
}
.disco-memory__chat:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.disco-memory__list-hint {
  margin: 0;
  font-size: 12px;
  color: var(--site-text-muted);
}
.disco-memory__items {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 180px;
  overflow-y: auto;
}
.disco-memory__item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 10px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
  font-size: 12px;
  color: var(--site-text);
}
.disco-memory__item-name {
  font-weight: 700;
}
.disco-memory__item-comment {
  color: var(--site-text-muted);
}
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

@media (max-width: 480px) {
  .disco-detail__header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--sp-3);
  }
  .disco-detail__dl {
    grid-template-columns: 1fr;
    gap: 4px 0;
  }
  .disco-detail__dl dt {
    margin-top: 8px;
    font-size: 11px;
  }
  .disco-detail__dl dd {
    font-size: 13px;
  }
}
</style>
