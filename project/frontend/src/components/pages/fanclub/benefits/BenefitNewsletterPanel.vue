<script setup>
/**
 * 会員特典: 月刊ニュースレター
 */
import MemberGate from '../../../common/MemberGate.vue'
import { HIBARU_DATA } from '../../../../data/hibaruData.js'
import { MEMBERSHIP_LABELS } from '../../../../constants/membership.js'
import { PERMISSION } from '../../../../constants/membership.js'
import { useMemberAccess } from '../../../../composables/useMemberAccess.js'

const emit = defineEmits(['need-auth'])

const { membership } = useMemberAccess()
</script>

<template>
  <MemberGate
    :permission="PERMISSION.NEWSLETTER"
    feature="月刊ニュースレター"
    @login="emit('need-auth', 'login')"
    @register="emit('need-auth', 'register')"
  >
    <p class="benefit-panel__badge">{{ MEMBERSHIP_LABELS[membership] }}向けコンテンツ</p>
    <p class="benefit-panel__lead">会員向けの最新情報・コラムを毎月お届けします。</p>
    <ul class="benefit-panel__list">
      <li v-for="(n, i) in HIBARU_DATA.news" :key="i" class="benefit-panel__item">
        <time class="benefit-panel__date">{{ n.date }}</time>
        <span v-if="n.label" class="benefit-panel__label">{{ n.label }}</span>
        <h3 class="benefit-panel__title">{{ n.title }}</h3>
      </li>
    </ul>
  </MemberGate>
</template>

<style scoped>
.benefit-panel__badge {
  display: inline-block;
  margin: 0 0 12px;
  padding: 4px 12px;
  font-size: 11px;
  color: var(--murasaki-700);
  background: var(--murasaki-100);
  border: 1px solid var(--murasaki-400);
  border-radius: 999px;
}
.benefit-panel__lead {
  margin: 0 0 16px;
  font-size: 13px;
  line-height: 1.7;
  color: var(--site-text-muted);
}
.benefit-panel__list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.benefit-panel__item {
  padding: 14px 0;
  border-bottom: 1px solid var(--site-border);
}
.benefit-panel__date {
  font-family: var(--ff-mono);
  font-size: 12px;
  color: var(--site-text-light);
}
.benefit-panel__label {
  display: inline-block;
  margin-left: 8px;
  padding: 2px 8px;
  font-size: 10px;
  color: var(--murasaki-700);
  background: var(--murasaki-100);
  border-radius: 4px;
}
.benefit-panel__title {
  margin: 6px 0 0;
  font-family: var(--ff-mincho);
  font-size: 15px;
  color: var(--site-text);
}
</style>
