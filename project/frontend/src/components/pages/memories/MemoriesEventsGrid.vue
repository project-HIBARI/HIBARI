<script setup>
/**
 * 部品名: 思い出ページ — 交流イベントカード群
 * 用途: 思い出ページのイベントタブで交流イベント一覧を表示する（会員先行・プレミアム割引）
 */
import UiButton from '../../ui/UiButton.vue'
import MemberGate from '../../common/MemberGate.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'
import { useMemberAccess } from '../../../composables/useMemberAccess.js'

const emit = defineEmits(['need-auth'])

const { canUse, isLoggedIn, isPremium, PERMISSION } = useMemberAccess()

const eventTypes = {
  nodojiman: { label: 'のど自慢', color: 'var(--murasaki-700)' },
  karaoke: { label: 'カラオケ', color: '#5a7a9a' },
  tour: { label: 'ゆかりの地ツアー', color: '#6a8a5a' },
  photo: { label: 'フォトコンテスト', color: '#7a5a9a' },
}

/** ツアー系の料金デモ（id: 1 = みだれ髪ゆかりの地ツアー） */
const tourPricing = {
  1: { regular: '¥8,800', member: '¥7,500', premium: '¥6,600' },
}

function isTourWithPreorder(ev) {
  return ev.type === 'tour' && ev.id === 1
}

function displayFee(ev) {
  const p = tourPricing[ev.id]
  if (!p) return ev.fee
  if (!isLoggedIn.value) return `${p.regular}（会員 ${p.member}）`
  if (isPremium.value && canUse(PERMISSION.PRIORITY_DISCOUNT)) {
    return `${p.premium}（プレミアム会員価格 · 一般 ${p.regular}）`
  }
  if (canUse(PERMISSION.TICKET_PREORDER)) {
    return `${p.member}（一般会員価格 · 一般 ${p.regular}）`
  }
  return ev.fee
}

function canApply(ev) {
  return isTourWithPreorder(ev) && canUse(PERMISSION.TICKET_PREORDER)
}
</script>

<template>
  <div class="mem-events">
    <article v-for="ev in HIBARU_DATA.events" :key="ev.id" class="mem-events__card">
      <div class="mem-events__tags">
        <span
          class="mem-events__type"
          :style="{ background: (eventTypes[ev.type] || { color: 'var(--site-text-muted)' }).color }"
        >
          {{ (eventTypes[ev.type] || { label: ev.type }).label }}
        </span>
        <span v-if="ev.partner" class="mem-events__partner">{{ ev.partner }}</span>
        <span v-if="isTourWithPreorder(ev)" class="mem-events__preorder">先行予約対象</span>
      </div>
      <h3 class="mem-events__title">{{ ev.title }}</h3>
      <dl class="mem-events__dl">
        <dt>日時</dt><dd>{{ ev.date }}</dd>
        <dt>会場</dt><dd>{{ ev.place }}</dd>
        <dt>定員</dt><dd>{{ ev.capacity }}</dd>
        <dt>料金</dt>
        <dd>
          {{ displayFee(ev) }}
          <span
            v-if="isTourWithPreorder(ev) && isPremium && canUse(PERMISSION.PRIORITY_DISCOUNT)"
            class="mem-events__priority"
          >優先枠あり</span>
        </dd>
      </dl>
      <div class="mem-events__actions">
        <template v-if="isTourWithPreorder(ev)">
          <UiButton v-if="canApply(ev)" variant="primary" size="sm">申し込む</UiButton>
          <MemberGate
            v-else
            :permission="PERMISSION.TICKET_PREORDER"
            feature="チケット先行予約"
            compact
            @login="emit('need-auth', 'login')"
            @register="emit('need-auth', 'register')"
            @upgrade="emit('need-auth', 'register')"
          />
        </template>
        <UiButton v-else variant="primary" size="sm">申し込む</UiButton>
        <UiButton variant="outline" size="sm">縁ページへ ›</UiButton>
      </div>
    </article>
  </div>
</template>

<style scoped>
.mem-events {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--sp-5);
  margin-top: var(--sp-5);
}
.mem-events__card {
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  padding: var(--sp-5);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
}
.mem-events__tags {
  display: flex;
  gap: 8px;
  margin-bottom: 14px;
  flex-wrap: wrap;
  align-items: center;
}
.mem-events__type {
  font-size: 10px;
  color: #fff;
  padding: 3px 10px;
  letter-spacing: 0.15em;
  font-family: var(--ff-mincho);
  border-radius: var(--site-radius-sm);
}
.mem-events__partner {
  font-size: 10px;
  border: 1px solid var(--kin-500);
  color: var(--kin-600);
  padding: 3px 8px;
  letter-spacing: 0.1em;
  font-family: var(--ff-mincho);
  border-radius: var(--site-radius-sm);
}
.mem-events__preorder {
  font-size: 9px;
  padding: 3px 8px;
  background: var(--murasaki-100);
  color: var(--murasaki-700);
  border: 1px solid var(--murasaki-400);
  border-radius: var(--site-radius-sm);
  letter-spacing: 0.08em;
}
.mem-events__title {
  font-family: var(--ff-mincho);
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 12px;
  color: var(--site-text);
}
.mem-events__dl {
  display: grid;
  grid-template-columns: 60px 1fr;
  gap: 6px 12px;
  font-size: 13px;
  color: var(--site-text-muted);
  margin: 0;
}
.mem-events__dl dt {
  color: var(--kin-600);
  font-family: var(--ff-mincho);
  font-weight: 700;
}
.mem-events__dl dd {
  margin: 0;
}
.mem-events__priority {
  display: inline-block;
  margin-left: 8px;
  font-size: 10px;
  font-weight: 700;
  color: var(--murasaki-700);
}
.mem-events__actions {
  display: flex;
  gap: 10px;
  margin-top: var(--sp-5);
  flex-wrap: wrap;
  align-items: center;
}

@media (max-width: 767px) {
  .mem-events {
    grid-template-columns: 1fr;
  }
}
</style>
