<script setup>
/**
 * 部品名: ホーム — 今後の放送・イベント一覧
 */
import { computed } from 'vue'
import UiCard from '../../ui/UiCard.vue'
import SectionTitle from '../../ui/SectionTitle.vue'
import MemberGate from '../../common/MemberGate.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'
import { useMemberAccess } from '../../../composables/useMemberAccess.js'

const emit = defineEmits(['open-all', 'need-auth'])

const { canUse, isPremium, PERMISSION } = useMemberAccess()

const items = HIBARU_DATA.homeSchedule.slice(0, 4)
const canPreorder = computed(() => canUse(PERMISSION.TICKET_PREORDER))

function onOpenAll() {
  if (canPreorder.value) {
    emit('open-all')
  } else {
    emit('need-auth', 'events')
  }
}

function isTour(ev) {
  return ev.id === 'b3'
}
</script>

<template>
  <UiCard tone="white" padding="md" class="top-events">
    <SectionTitle
      title="今後の放送・イベント"
      size="md"
      link-label="一覧を見る ›"
      @link-click="onOpenAll"
    />

    <ul class="top-events__list">
      <li v-for="ev in items" :key="ev.id" class="top-events__item">
        <div class="top-events__date-col">
          <span class="top-events__date">{{ ev.date }}</span>
          <span v-if="ev.time" class="top-events__time">{{ ev.time }}</span>
        </div>
        <div class="top-events__body">
          <p class="top-events__title">{{ ev.title }}</p>
          <p v-if="ev.note" class="top-events__note">{{ ev.note }}</p>
          <p v-if="isTour(ev) && canPreorder" class="top-events__badge">
            チケット先行予約 受付中
            <span v-if="isPremium" class="top-events__badge-sub">（優先枠・会員割引）</span>
          </p>
        </div>
      </li>
    </ul>

    <MemberGate
      v-if="!canPreorder"
      :permission="PERMISSION.TICKET_PREORDER"
      feature="チケット先行予約"
      compact
      class="top-events__gate"
      @login="emit('need-auth', 'login')"
      @register="emit('need-auth', 'register')"
      @upgrade="emit('need-auth', 'register')"
    />
  </UiCard>
</template>

<style scoped>
.top-events {
  height: 100%;
  min-height: 380px;
  display: flex;
  flex-direction: column;
}
.top-events__list {
  list-style: none;
  margin: 0;
  padding: 0;
  flex: 1;
}
.top-events__item {
  display: flex;
  gap: 16px;
  padding: 14px 0;
  border-bottom: 1px solid var(--site-border);
  align-items: flex-start;
}
.top-events__item:last-child {
  border-bottom: 0;
}
.top-events__date-col {
  flex-shrink: 0;
  width: 72px;
  text-align: center;
}
.top-events__date {
  display: block;
  font-family: var(--ff-mincho);
  font-size: 18px;
  font-weight: 800;
  line-height: 1.25;
  color: var(--murasaki-700);
  letter-spacing: 0.02em;
}
.top-events__time {
  display: block;
  margin-top: 4px;
  font-family: var(--ff-mono);
  font-size: 11px;
  color: var(--site-text-muted);
}
.top-events__body {
  flex: 1;
  min-width: 0;
}
.top-events__title {
  margin: 0 0 4px;
  font-size: 13px;
  line-height: 1.6;
  font-weight: 500;
  color: var(--site-text);
}
.top-events__note {
  margin: 0;
  font-size: 11px;
  line-height: 1.5;
  color: var(--site-text-light);
}
.top-events__badge {
  margin: 8px 0 0;
  font-size: 11px;
  font-weight: 700;
  color: var(--murasaki-700);
}
.top-events__badge-sub {
  font-weight: 500;
  color: var(--kin-600);
}
.top-events__gate {
  margin-top: 12px;
}

@media (max-width: 767px) {
  .top-events {
    min-height: auto;
  }
  .top-events__date {
    font-size: 16px;
  }
}
</style>
