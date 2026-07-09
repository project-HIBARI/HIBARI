<script setup>
/**
 * 会員特典: チケット先行予約・優先申込
 */
import { ref } from 'vue'
import MemberGate from '../../../common/MemberGate.vue'
import UiButton from '../../../ui/UiButton.vue'
import EventApplyModal from '../../../modals/EventApplyModal.vue'
import { HIBARU_DATA } from '../../../../data/hibaruData.js'
import { useMemberAccess } from '../../../../composables/useMemberAccess.js'
import { PERMISSION } from '../../../../constants/membership.js'

const props = defineProps({
  premiumFocus: { type: Boolean, default: false },
})

const emit = defineEmits(['need-auth', 'navigate'])

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
  <MemberGate
    :permission="premiumFocus ? PERMISSION.PRIORITY_DISCOUNT : PERMISSION.TICKET_PREORDER"
    :feature="premiumFocus ? '優先申込＋会員割引' : 'チケット先行予約'"
    @login="emit('need-auth', 'login')"
    @register="emit('need-auth', premiumFocus ? 'register-premium' : 'register')"
    @upgrade="emit('need-auth', 'register-premium')"
  >
    <p v-if="premiumFocus" class="benefit-panel__lead benefit-panel__lead--premium">
      プレミアム会員向けの優先申込枠と会員割引価格がご利用いただけます。
    </p>
    <p v-else class="benefit-panel__lead">
      コンサートやイベントの先行予約にご利用いただけます。
    </p>
    <ul class="benefit-panel__list">
      <li v-for="ev in HIBARU_DATA.homeSchedule" :key="ev.id" class="benefit-panel__item">
        <div class="benefit-panel__head">
          <span class="benefit-panel__date">{{ ev.date }}</span>
          <span v-if="ev.time" class="benefit-panel__time">{{ ev.time }}</span>
        </div>
        <h3 class="benefit-panel__title">{{ ev.title }}</h3>
        <p class="benefit-panel__note">{{ ev.note }}</p>
        <p v-if="getFee(ev.id)" class="benefit-panel__fee">
          {{ getFee(ev.id).label }}: <strong>{{ getFee(ev.id).value }}</strong>
          <span class="benefit-panel__fee-regular">（一般 {{ tourPricing[ev.id].regular }}）</span>
        </p>
        <div class="benefit-panel__actions">
          <UiButton
            v-if="ev.id === 'b3' || ev.id === 'b4'"
            variant="primary"
            size="sm"
            @click="openApply(ev)"
          >
            {{ canPreorder(ev) ? '先行予約する' : '申し込む' }}
          </UiButton>
          <span v-if="canPreorder(ev) && isPremium" class="benefit-panel__priority">優先枠あり</span>
        </div>
      </li>
    </ul>
  </MemberGate>

  <EventApplyModal
    v-if="selectedEvent"
    :event="selectedEvent"
    @close="selectedEvent = null"
    @navigate="emit('navigate', $event)"
  />
</template>

<style scoped>
.benefit-panel__lead {
  margin: 0 0 16px;
  font-size: 13px;
  line-height: 1.7;
  color: var(--site-text-muted);
}
.benefit-panel__lead--premium {
  padding: 10px 14px;
  background: linear-gradient(135deg, #fff9f6 0%, var(--murasaki-100) 100%);
  border: 1px solid rgba(201, 169, 97, 0.45);
  border-radius: var(--site-radius-md);
  color: var(--murasaki-700);
}
.benefit-panel__list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.benefit-panel__item {
  padding: 16px 0;
  border-bottom: 1px solid var(--site-border);
}
.benefit-panel__head {
  display: flex;
  gap: 10px;
  align-items: baseline;
}
.benefit-panel__date {
  font-family: var(--ff-mincho);
  font-size: 18px;
  font-weight: 700;
  color: var(--murasaki-700);
}
.benefit-panel__time {
  font-size: 12px;
  color: var(--site-text-muted);
}
.benefit-panel__title {
  margin: 8px 0 4px;
  font-size: 15px;
  color: var(--site-text);
}
.benefit-panel__note {
  margin: 0;
  font-size: 12px;
  color: var(--site-text-muted);
}
.benefit-panel__fee {
  margin: 10px 0 0;
  font-size: 13px;
  color: var(--kin-600);
}
.benefit-panel__fee-regular {
  margin-left: 6px;
  font-size: 11px;
  color: var(--site-text-light);
}
.benefit-panel__actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 12px;
}
.benefit-panel__priority {
  font-size: 11px;
  color: var(--murasaki-700);
  font-weight: 700;
}
</style>
