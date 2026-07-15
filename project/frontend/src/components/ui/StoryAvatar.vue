<script setup>
/**
 * 部品名: ストーリー連動アバター
 * 役割: 有効なストーリーがあればリング表示＋クリックでビューア起動、無ければプロフィール遷移をemitする
 */
import { ref, computed } from 'vue'
import { useSnsStoryPresence } from '../../composables/useSnsStoryPresence.js'

const props = defineProps({
  accountId: { type: Number, required: true },
  name: { type: String, default: '' },
  avatarPath: { type: String, default: null },
  size: { type: Number, default: 40 },
  ring: { type: Boolean, default: true },
})

const emit = defineEmits(['open-profile'])

const { presenceFor, openForAccount } = useSnsStoryPresence()
const imgFailed = ref(false)

const presence = computed(() => (props.ring ? presenceFor(props.accountId) : { hasStory: false, hasUnviewed: false }))

const ringClass = computed(() => {
  if (!presence.value.hasStory) return ''
  return presence.value.hasUnviewed ? 'story-avatar--unviewed' : 'story-avatar--viewed'
})

const sizeStyle = computed(() => ({ width: `${props.size}px`, height: `${props.size}px` }))

function onClick() {
  if (presence.value.hasStory && openForAccount(props.accountId)) return
  emit('open-profile', props.accountId)
}
</script>

<template>
  <button
    type="button"
    class="story-avatar"
    :class="ringClass"
    :style="sizeStyle"
    :aria-label="name ? `${name}さんのプロフィール` : 'プロフィール'"
    @click="onClick"
  >
    <span class="story-avatar__inner">
      <img
        v-if="avatarPath && !imgFailed"
        :src="avatarPath"
        :alt="name"
        loading="lazy"
        @error="imgFailed = true"
      />
      <span v-else>{{ (name || '?').charAt(0) }}</span>
    </span>
  </button>
</template>

<style scoped>
.story-avatar {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  padding: 2px;
  border-radius: 50%;
  border: 2px solid transparent;
  background: transparent;
  cursor: pointer;
  min-width: 32px;
  min-height: 32px;
}

.story-avatar--unviewed {
  border-color: var(--sns-gold, var(--kin-500));
  background: linear-gradient(135deg, var(--sns-gold, var(--kin-500)), var(--sns-purple, var(--murasaki-600)));
}

.story-avatar--viewed {
  border-color: rgba(255, 255, 255, 0.3);
}

.story-avatar__inner {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  overflow: hidden;
  background: var(--sns-purple, var(--murasaki-700));
  color: #fff;
  font-size: 15px;
  font-family: var(--ff-sans-jp);
  border: 2px solid var(--sns-bg, #1a1418);
}

.story-avatar__inner img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
