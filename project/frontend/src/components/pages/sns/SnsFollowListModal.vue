<script setup>
/**
 * 部品名: フォロー中 / フォロワー 一覧モーダル
 */
import { ref, onMounted } from 'vue'
import ModalShell from '../../modals/ModalShell.vue'
import { fetchSnsFollowing, fetchSnsFollowers } from '../../../api/sns.js'

const props = defineProps({
  accountId: { type: Number, required: true },
  mode: { type: String, required: true }, // following | followers
})

const emit = defineEmits(['close', 'open-profile'])

const users = ref([])
const loading = ref(true)
const errorMessage = ref('')

async function load() {
  loading.value = true
  errorMessage.value = ''
  try {
    const fetcher = props.mode === 'following' ? fetchSnsFollowing : fetchSnsFollowers
    const data = await fetcher(props.accountId)
    users.value = data.users
  } catch (err) {
    errorMessage.value = err?.message || '一覧の取得に失敗しました'
  } finally {
    loading.value = false
  }
}

function onOpenProfile(id) {
  emit('open-profile', id)
  emit('close')
}

onMounted(load)
</script>

<template>
  <ModalShell :title="mode === 'following' ? 'フォロー中' : 'フォロワー'" @close="emit('close')">
    <p v-if="loading" class="sns-follow-list__state">読み込み中…</p>
    <template v-else-if="errorMessage">
      <p class="sns-follow-list__state sns-follow-list__state--error">{{ errorMessage }}</p>
      <button type="button" class="sns-follow-list__retry" @click="load">再試行</button>
    </template>
    <p v-else-if="!users.length" class="sns-follow-list__state">まだ誰もいません</p>
    <ul v-else class="sns-follow-list">
      <li v-for="u in users" :key="u.account_id">
        <button type="button" class="sns-follow-list__user" @click="onOpenProfile(u.account_id)">
          <span class="sns-follow-list__avatar">
            <img v-if="u.avatar_path" :src="u.avatar_path" :alt="u.name" />
            <span v-else>{{ (u.name || '?').charAt(0) }}</span>
          </span>
          <span class="sns-follow-list__name">{{ u.name }}</span>
        </button>
      </li>
    </ul>
  </ModalShell>
</template>

<style scoped>
.sns-follow-list__state {
  margin: 0;
  padding: 20px 0;
  text-align: center;
  font-size: 13px;
  color: var(--site-text-muted);
}
.sns-follow-list__state--error {
  color: var(--beni-600);
}
.sns-follow-list__retry {
  display: block;
  margin: 0 auto;
  background: transparent;
  border: 1px solid var(--murasaki-400);
  color: var(--murasaki-700);
  border-radius: 999px;
  padding: 6px 16px;
  font-size: 12px;
  cursor: pointer;
}
.sns-follow-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: 420px;
  overflow-y: auto;
}
.sns-follow-list__user {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 8px 4px;
  background: transparent;
  border: 0;
  cursor: pointer;
  text-align: left;
}
.sns-follow-list__avatar {
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
.sns-follow-list__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sns-follow-list__name {
  font-size: 13px;
  color: var(--site-text);
}
</style>
