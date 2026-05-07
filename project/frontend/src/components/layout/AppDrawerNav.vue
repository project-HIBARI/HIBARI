<script setup>
/**
 * 部品名: スマホ用ドロワーナビ
 */
defineProps({
  open: { type: Boolean, default: false },
  items: { type: Array, required: true },
  page: { type: String, required: true },
})

const emit = defineEmits(['close', 'navigate', 'open-modal', 'replay-film'])
</script>

<template>
  <div v-if="open" role="dialog" aria-modal="true" aria-label="ナビゲーション" style="position: fixed; inset: 0; z-index: 200">
    <div style="position: absolute; inset: 0; background: rgba(0,0,0,0.6)" @click="emit('close')" />
    <div
      style="position: absolute; top: 0; right: 0; bottom: 0; width: 280px; background: #0a0604; border-left: 1px solid rgba(201,169,97,0.3); display: flex; flex-direction: column"
    >
      <div style="display: flex; justify-content: flex-end; padding: 16px">
        <button
          type="button"
          style="background: transparent; border: 1px solid rgba(201,169,97,0.4); color: var(--paper-100); padding: 8px 14px; cursor: pointer; font-family: var(--ff-mincho); font-size: 12px; min-height: 44px"
          aria-label="閉じる"
          @click="emit('close')"
        >
          ✕ 閉じる
        </button>
      </div>
      <button
        v-for="n in items"
        :key="n.id"
        type="button"
        :style="{
          border: 0,
          background: page === n.id ? 'var(--beni-800)' : 'transparent',
          borderLeft: page === n.id ? '3px solid var(--kin-500)' : '3px solid transparent',
          color: page === n.id ? 'var(--paper-50)' : 'var(--paper-200)',
          padding: '0 20px',
          cursor: 'pointer',
          minHeight: '56px',
          display: 'flex',
          alignItems: 'center',
          gap: '16px',
          fontFamily: 'var(--ff-mincho)',
          borderBottom: '1px solid rgba(201,169,97,0.1)',
        }"
        :aria-current="page === n.id ? 'page' : undefined"
        @click="emit('navigate', n.id)"
      >
        <span
          :style="{
            fontSize: '24px',
            fontWeight: 700,
            color: page === n.id ? 'var(--kin-500)' : 'var(--beni-500)',
            width: '28px',
          }"
        >{{ n.kanji }}</span>
        <span style="font-size: 15px; letter-spacing: 0.1em">{{ n.label }}</span>
      </button>
      <div style="border-top: 1px solid rgba(201,169,97,0.3); margin: 8px 0" />
      <button
        type="button"
        style="border: 0; background: transparent; color: var(--kin-500); padding: 0 20px; cursor: pointer; min-height: 52px; text-align: left; font-family: var(--ff-mincho); font-size: 14px; letter-spacing: 0.15em; border-bottom: 1px solid rgba(201,169,97,0.1)"
        @click="emit('open-modal', 'fanclub')"
      >
        ✦ ファンクラブ
      </button>
      <button
        type="button"
        style="border: 0; background: transparent; color: var(--kin-500); padding: 0 20px; cursor: pointer; min-height: 52px; text-align: left; font-family: var(--ff-mincho); font-size: 14px; letter-spacing: 0.15em; border-bottom: 1px solid rgba(201,169,97,0.1)"
        @click="emit('open-modal', 'goods')"
      >
        ✦ グッズ
      </button>
      <button
        type="button"
        style="border: 0; background: transparent; color: var(--kin-500); padding: 0 20px; cursor: pointer; min-height: 52px; text-align: left; font-family: var(--ff-mincho); font-size: 14px; letter-spacing: 0.15em; border-bottom: 1px solid rgba(201,169,97,0.1)"
        @click="emit('open-modal', 'ai')"
      >
        ✦ AI美空ひばり
      </button>
      <button
        type="button"
        style="border: 0; background: transparent; color: var(--paper-300); padding: 0 20px; cursor: pointer; min-height: 48px; text-align: left; font-family: var(--ff-mincho); font-size: 13px; letter-spacing: 0.1em; margin-top: auto; border-top: 1px solid rgba(201,169,97,0.2)"
        @click="emit('replay-film')"
      >
        ▶ オープニング映像を再生
      </button>
    </div>
  </div>
</template>
