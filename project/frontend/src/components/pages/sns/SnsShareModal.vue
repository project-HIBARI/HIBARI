<script setup>
/**
 * 部品名: 投稿をDMで共有するモーダル
 */
import { ref, onMounted } from 'vue'
import ModalShell from '../../modals/ModalShell.vue'
import { fetchDmThreads, sendDm, searchDmUsers } from '../../../api/sns.js'

const props = defineProps({
  post: { type: Object, required: true },
})

const emit = defineEmits(['close'])

const recents = ref([])
const loading = ref(true)
const searchQuery = ref('')
const searchResults = ref([])
const searching = ref(false)
const sendingTo = ref(null)
const sentTo = ref(new Set())
const errorMessage = ref('')

async function load() {
  loading.value = true
  try {
    const data = await fetchDmThreads('inbox')
    recents.value = data.threads.map((t) => t.other)
  } catch {
    recents.value = []
  } finally {
    loading.value = false
  }
}

let searchDebounce = null
function onSearchInput() {
  clearTimeout(searchDebounce)
  const q = searchQuery.value.trim()
  if (!q) {
    searchResults.value = []
    return
  }
  searchDebounce = setTimeout(async () => {
    searching.value = true
    try {
      const data = await searchDmUsers(q)
      searchResults.value = data.users
    } catch {
      searchResults.value = []
    } finally {
      searching.value = false
    }
  }, 300)
}

async function sendTo(userItem) {
  if (sendingTo.value) return
  sendingTo.value = userItem.account_id
  errorMessage.value = ''
  try {
    await sendDm({
      recipient_id: userItem.account_id,
      message_type: 'post_share',
      shared_post_id: props.post.post_id,
    })
    sentTo.value = new Set([...sentTo.value, userItem.account_id])
  } catch (err) {
    errorMessage.value = err?.message || '共有に失敗しました'
  } finally {
    sendingTo.value = null
  }
}

onMounted(load)
</script>

<template>
  <ModalShell title="投稿を共有" @close="emit('close')">
    <div class="sns-share">
      <input
        v-model="searchQuery"
        type="text"
        class="sns-share__search"
        placeholder="ユーザー名で検索"
        @input="onSearchInput"
      />

      <p v-if="errorMessage" class="sns-share__error">{{ errorMessage }}</p>

      <p v-if="loading" class="sns-share__state">読み込み中…</p>
      <ul v-else class="sns-share__list">
        <li v-for="u in (searchQuery.trim() ? searchResults : recents)" :key="u.account_id">
          <div class="sns-share__user">
            <span class="sns-share__avatar">
              <img v-if="u.avatar_path" :src="u.avatar_path" :alt="u.name" />
              <span v-else>{{ (u.name || '?').charAt(0) }}</span>
            </span>
            <span class="sns-share__name">{{ u.name }}</span>
            <button
              type="button"
              class="sns-share__send-btn"
              :disabled="sendingTo === u.account_id || sentTo.has(u.account_id)"
              @click="sendTo(u)"
            >
              {{ sentTo.has(u.account_id) ? '送信済み' : '送信' }}
            </button>
          </div>
        </li>
      </ul>
      <p v-if="!loading && searchQuery.trim() && !searching && !searchResults.length" class="sns-share__state">
        該当するユーザーが見つかりません
      </p>
    </div>
  </ModalShell>
</template>

<style scoped>
.sns-share {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.sns-share__search {
  border: 1px solid var(--site-border);
  border-radius: 999px;
  padding: 9px 16px;
  font-size: 13px;
  color: var(--site-text);
}
.sns-share__state {
  margin: 0;
  padding: 16px 0;
  text-align: center;
  font-size: 12px;
  color: var(--site-text-muted);
}
.sns-share__error {
  margin: 0;
  color: var(--beni-600);
  font-size: 12px;
}
.sns-share__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: 360px;
  overflow-y: auto;
}
.sns-share__user {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 2px;
}
.sns-share__avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--murasaki-600);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}
.sns-share__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sns-share__name {
  flex: 1;
  font-size: 13px;
  color: var(--site-text);
}
.sns-share__send-btn {
  background: var(--murasaki-700);
  color: #fff;
  border: 0;
  border-radius: 999px;
  padding: 6px 14px;
  font-size: 12px;
  cursor: pointer;
}
.sns-share__send-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
