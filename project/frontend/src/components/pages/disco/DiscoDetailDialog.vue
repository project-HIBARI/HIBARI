<script setup>
/**
 * 部品名: ディスコグラフィ — 楽曲詳細ダイアログ
 * 用途: 選択した楽曲のメタデータをモーダルで表示する（ライトテーマ）
 */
import ModalShell from '../../modals/ModalShell.vue'
import RecordChip from '../../ui/RecordChip.vue'

defineProps({
  detail: { type: Object, default: null },
})

const emit = defineEmits(['close'])
</script>

<template>
  <ModalShell v-if="detail" :title="detail.title" @close="emit('close')">
    <div class="disco-detail">
      <div class="disco-detail__header">
        <RecordChip :no="detail.no" color="var(--beni-700)" />
        <div class="disco-detail__intro">
          <span class="disco-detail__year">{{ detail.year }} · {{ detail.label }}</span>
          <p class="disco-detail__romaji">{{ detail.romaji }}</p>
        </div>
      </div>

      <dl class="disco-detail__dl">
        <dt>発売年</dt>
        <dd>{{ detail.year }}年</dd>
        <dt>形態</dt>
        <dd>{{ detail.type }}</dd>
        <dt>ジャンル</dt>
        <dd>{{ detail.genre }}</dd>
        <dt>作詞</dt>
        <dd>{{ detail.lyric }}</dd>
        <dt>作曲</dt>
        <dd>{{ detail.music }}</dd>
        <dt>品番</dt>
        <dd class="disco-detail__mono">{{ detail.no }}</dd>
        <dt>レーベル</dt>
        <dd>{{ detail.label }}</dd>
      </dl>

      <div v-if="detail.note" class="disco-detail__note">
        {{ detail.note }}
      </div>
    </div>
  </ModalShell>
</template>

<style scoped>
.disco-detail__header {
  display: flex;
  gap: var(--sp-5);
  align-items: center;
  margin-bottom: var(--sp-5);
}
.disco-detail__year {
  display: block;
  font-family: var(--ff-mono);
  font-size: 10px;
  letter-spacing: 0.15em;
  color: var(--kin-600);
  margin-bottom: 4px;
}
.disco-detail__romaji {
  margin: 0;
  font-family: var(--ff-latin);
  font-style: italic;
  font-size: 14px;
  color: var(--site-text-muted);
}
.disco-detail__dl {
  display: grid;
  grid-template-columns: 80px 1fr;
  gap: 10px 16px;
  font-size: 14px;
  margin: 0;
}
.disco-detail__dl dt {
  color: var(--kin-600);
  font-family: var(--ff-mincho);
  letter-spacing: 0.06em;
}
.disco-detail__dl dd {
  margin: 0;
  color: var(--site-text);
}
.disco-detail__mono {
  font-family: var(--ff-mono);
  font-size: 12px;
}
.disco-detail__note {
  margin-top: var(--sp-5);
  padding: var(--sp-4);
  background: var(--site-surface-muted);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
  font-size: 13px;
  line-height: 1.8;
  color: var(--site-text);
}

@media (max-width: 480px) {
  .disco-detail__header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--sp-3);
  }
  .disco-detail__dl {
    grid-template-columns: 1fr;
    gap: 4px 0;
  }
  .disco-detail__dl dt {
    margin-top: 8px;
    font-size: 11px;
  }
  .disco-detail__dl dd {
    font-size: 13px;
  }
}
</style>
