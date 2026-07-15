<script setup>
/**
 * 部品名: ストーリーズ一覧（横スクロール）
 */
import { computed } from 'vue'
import UiIco from '../../ui/UiIco.vue'
import SnsSkeletonCard from './SnsSkeletonCard.vue'
import { useAuth } from '../../../composables/useAuth.js'

const props = defineProps({
  groups: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['open', 'create'])

const { user, isLoggedIn } = useAuth()

const selfGroup = computed(() => {
  if (!isLoggedIn.value) return null
  return props.groups.find((g) => g.account_id === user.value?.account_id) || null
})

const otherGroups = computed(() =>
  props.groups.filter((g) => !isLoggedIn.value || g.account_id !== user.value?.account_id),
)

function onSelfAvatarClick() {
  if (selfGroup.value) {
    emit('open', selfGroup.value)
  } else {
    emit('create')
  }
}
</script>

<template>
  <section class="sns-story-bar" aria-label="ストーリーズ">
    <div v-if="loading" class="sns-story-bar__loading" aria-busy="true">
      <SnsSkeletonCard variant="story" :count="6" />
    </div>

    <div v-else class="sns-story-bar__row">
      <div v-if="isLoggedIn" class="sns-story-bar__item">
        <button
          type="button"
          class="sns-story-bar__avatar-btn"
          :class="{ 'sns-story-bar__avatar-btn--unviewed': selfGroup?.has_unviewed }"
          @click="onSelfAvatarClick"
        >
          <span class="sns-story-bar__avatar">
            {{ (user?.name || '?').charAt(0) }}
          </span>
          <button
            type="button"
            class="sns-story-bar__plus"
            aria-label="ストーリーズを追加"
            @click.stop="emit('create')"
          >
            <UiIco name="plus" :size="12" color="#fff" />
          </button>
        </button>
        <span class="sns-story-bar__label">自分のストーリー</span>
      </div>

      <div v-for="g in otherGroups" :key="g.account_id" class="sns-story-bar__item">
        <button
          type="button"
          class="sns-story-bar__avatar-btn"
          :class="{ 'sns-story-bar__avatar-btn--unviewed': g.has_unviewed }"
          @click="emit('open', g)"
        >
          <span class="sns-story-bar__avatar">
            <img v-if="g.author_avatar_path" :src="g.author_avatar_path" :alt="g.author_name" />
            <span v-else>{{ (g.author_name || '?').charAt(0) }}</span>
          </span>
        </button>
        <span class="sns-story-bar__label">{{ g.author_name }}</span>
      </div>

      <p v-if="!loading && !groups.length" class="sns-story-bar__empty">
        まだストーリーズがありません
      </p>
    </div>
  </section>
</template>

<style scoped>
.sns-story-bar {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
.sns-story-bar::-webkit-scrollbar {
  display: none;
}
.sns-story-bar__row {
  display: flex;
  gap: 14px;
  padding: 4px 2px;
}
.sns-story-bar__loading {
  padding: 4px 2px;
}
.sns-story-bar__empty {
  margin: 0;
  padding: 14px 4px;
  font-size: 12px;
  color: var(--sns-text-muted, rgba(248, 244, 239, 0.5));
  white-space: nowrap;
}
.sns-story-bar__item {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  width: 64px;
}
.sns-story-bar__avatar-btn {
  position: relative;
  width: 56px;
  height: 56px;
  min-width: 44px;
  min-height: 44px;
  border-radius: 50%;
  padding: 2px;
  border: 2px solid var(--sns-border, rgba(255, 255, 255, 0.15));
  background: transparent;
  cursor: pointer;
}
.sns-story-bar__avatar-btn--unviewed {
  border-color: var(--sns-gold, var(--kin-500));
  background: linear-gradient(135deg, var(--sns-gold, var(--kin-500)), var(--sns-purple, var(--murasaki-600)));
}
.sns-story-bar__avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  overflow: hidden;
  background: var(--sns-purple, var(--murasaki-700));
  color: #fff;
  font-size: 18px;
  font-family: var(--ff-sans-jp);
  border: 2px solid var(--sns-bg, #1a1418);
}
.sns-story-bar__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sns-story-bar__plus {
  position: absolute;
  bottom: -2px;
  right: -2px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--sns-purple, var(--murasaki-600));
  border: 2px solid var(--sns-bg, #1a1418);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.sns-story-bar__label {
  font-size: 10px;
  color: var(--sns-text-muted, rgba(248, 244, 239, 0.7));
  max-width: 64px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
