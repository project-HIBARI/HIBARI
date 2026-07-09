<script setup>
/**
 * 放送・イベント一覧（会員向け・プレミアム割引表示）
 */
import { ref } from 'vue'
import ModalShell from './ModalShell.vue'
import UiButton from '../ui/UiButton.vue'
import EventApplyModal from './EventApplyModal.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'
import { useMemberAccess } from '../../composables/useMemberAccess.js'
import { PERMISSION } from '../../constants/membership.js'

const emit = defineEmits(['close', 'navigate'])

const { canUse, isPremium } = useMemberAccess()

const selectedEvent = ref(null)

const tourPricing = {
  b3: { regular: '¥8,800', member: '¥7,500', premium: '¥6,600' },
}

function getFee(id) {
  const p = tourPricing[id]
  if (!p) return null
  if (isPremium.value) return { label: 'プレミアム会員価格', value: p.premium }
  return { label: '一般会員価格', value: p.member }
}

function canPreorder(ev) {
  return ev.id === 'b3' && canUse(PERMISSION.TICKET_PREORDER)
}

function openApply(ev) {
  selectedEvent.value = {
    id: ev.id,
    title: ev.title,
    date: ev.date,
    time: ev.time,
    place: ev.note?.split('·')?.[0]?.trim() || '',
    note: ev.note,
    fee: getFee(ev.id)?.value || '',
    type: ev.id === 'b3' ? 'tour' : 'nodojiman',
  }
}
</script>

<template>
  <ModalShell title="✦ 放送・イベント" @close="emit('close')">
    <ul class="events-modal__list">
      <li v-for="ev in HIBARU_DATA.homeSchedule" :key="ev.id" class="events-modal__item">
        <div class="events-modal__head">
          <span class="events-modal__date">{{ ev.date }}</span>
          <span v-if="ev.time" class="events-modal__time">{{ ev.time }}</span>
        </div>
        <h3 class="events-modal__title">{{ ev.title }}</h3>
        <p class="events-modal__note">{{ ev.note }}</p>
        <p v-if="getFee(ev.id)" class="events-modal__fee">
          {{ getFee(ev.id).label }}: <strong>{{ getFee(ev.id).value }}</strong>
          <span class="events-modal__fee-regular">（一般 {{ tourPricing[ev.id].regular }}）</span>
        </p>
        <div class="events-modal__actions">
          <UiButton
            v-if="ev.id === 'b3' || ev.id === 'b4'"
            variant="primary"
            size="sm"
            @click="openApply(ev)"
          >
            {{ canPreorder(ev) ? '先行予約する' : '申し込む' }}
          </UiButton>
          <span v-if="canPreorder(ev) && isPremium" class="events-modal__priority">優先枠あり</span>
        </div>
      </li>
    </ul>
  </ModalShell>

  <EventApplyModal
    v-if="selectedEvent"
    :event="selectedEvent"
    @close="selectedEvent = null"
    @navigate="emit('navigate', $event); emit('close')"
  />
</template>

<style scoped>
.events-modal__list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.events-modal__item {
  padding: 16px 0;
  border-bottom: 1px solid var(--site-border);
}
.events-modal__head {
  display: flex;
  gap: 10px;
  align-items: baseline;
}
.events-modal__date {
  font-family: var(--ff-mincho);
  font-size: 18px;
  font-weight: 700;
  color: var(--murasaki-700);
}
.events-modal__time {
  font-size: 12px;
  color: var(--site-text-muted);
}
.events-modal__title {
  margin: 8px 0 4px;
  font-size: 15px;
  color: var(--site-text);
}
.events-modal__note {
  margin: 0;
  font-size: 12px;
  color: var(--site-text-muted);
}
.events-modal__fee {
  margin: 10px 0 0;
  font-size: 13px;
  color: var(--kin-600);
}
.events-modal__fee-regular {
  margin-left: 6px;
  font-size: 11px;
  color: var(--site-text-light);
}
.events-modal__actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 12px;
}
.events-modal__priority {
  font-size: 11px;
  color: var(--murasaki-700);
  font-weight: 700;
}
</style>
