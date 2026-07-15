import { ref, computed } from 'vue'
import { fetchSnsStories } from '../api/sns.js'

const STORIES_CACHE_TTL_MS = 30_000

const groups = ref([])
const loading = ref(false)
const error = ref('')
const activeGroups = ref(null)
const activeStartIndex = ref(0)

let requestId = 0
let inFlight = null
let fetchedAt = 0

function syncViewedFlags() {
  for (const group of groups.value) {
    group.has_unviewed = group.stories.some((s) => !s.viewed_by_viewer)
  }
}

async function ensureLoaded({ force = false } = {}) {
  const now = Date.now()
  if (!force && fetchedAt && now - fetchedAt < STORIES_CACHE_TTL_MS && groups.value.length) {
    return
  }
  if (inFlight) return inFlight

  const id = ++requestId
  loading.value = true
  error.value = ''
  inFlight = (async () => {
    try {
      const data = await fetchSnsStories()
      if (id !== requestId) return
      groups.value = data.groups || []
      fetchedAt = Date.now()
    } catch {
      if (id !== requestId) return
      error.value = 'ストーリーズの取得に失敗しました'
    } finally {
      if (id === requestId) {
        loading.value = false
        inFlight = null
      }
    }
  })()
  return inFlight
}

function removeStory(storyId) {
  for (const group of groups.value) {
    group.stories = group.stories.filter((s) => s.story_id !== storyId)
  }
  groups.value = groups.value.filter((g) => g.stories.length > 0)
  syncViewedFlags()
  fetchedAt = 0
}

function presenceFor(accountId) {
  const group = groups.value.find((g) => g.account_id === accountId)
  if (!group) return { hasStory: false, hasUnviewed: false }
  return { hasStory: true, hasUnviewed: !!group.has_unviewed }
}

function openGroup(group) {
  const index = groups.value.findIndex((g) => g.account_id === group.account_id)
  activeGroups.value = groups.value
  activeStartIndex.value = index >= 0 ? index : 0
}

function openForAccount(accountId) {
  const group = groups.value.find((g) => g.account_id === accountId)
  if (!group) return false
  openGroup(group)
  return true
}

function closeViewer() {
  activeGroups.value = null
  syncViewedFlags()
}

export function useSnsStoryPresence() {
  return {
    groups,
    loading,
    error: computed(() => error.value),
    activeGroups,
    activeStartIndex,
    ensureLoaded,
    syncViewedFlags,
    removeStory,
    presenceFor,
    openGroup,
    openForAccount,
    closeViewer,
  }
}
