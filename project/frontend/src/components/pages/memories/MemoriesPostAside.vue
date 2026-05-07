<script setup>
/**
 * 部品名: 思い出 — 投稿フォーム（サイド）
 */
import { btnBeni, btnGhost, inputDark } from '../../../utils/hibaru.js'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const songs = HIBARU_DATA.discography.map((d) => d.title)

const props = defineProps({
  submitted: { type: Boolean, default: false },
  postData: { type: Object, required: true },
  errors: { type: Object, default: () => ({}) },
})

const emit = defineEmits(['update:postData', 'submit', 'reset'])

function patch(partial) {
  emit('update:postData', { ...props.postData, ...partial })
}
</script>

<template>
  <aside>
    <div style="position: sticky; top: 120px; border: 1px solid var(--kin-500); padding: 24px; background: rgba(139,26,26,0.1)">
      <div v-if="submitted" style="text-align: center; padding: 20px 0">
        <div style="font-size: 36px; margin-bottom: 12px">✦</div>
        <div style="font-family: var(--ff-mincho); font-size: 18px; font-weight: 700; margin-bottom: 12px">投稿ありがとうございます</div>
        <p style="font-size: 13px; color: var(--paper-200); line-height: 1.8">会員登録で投稿への返信・いいねの通知が届きます。</p>
        <button type="button" :style="{ ...btnBeni, width: '100%', justifyContent: 'center', marginTop: '16px', fontSize: '12px' }">会員登録 ›</button>
        <button type="button" :style="{ ...btnGhost, width: '100%', justifyContent: 'center', marginTop: '10px', fontSize: '12px' }" @click="emit('reset')">
          続けて投稿
        </button>
      </div>
      <template v-else>
        <div style="font-family: var(--ff-mincho); font-size: 18px; font-weight: 700; margin-bottom: 16px">思い出を寄せる</div>
        <div style="display: flex; flex-direction: column; gap: 10px">
          <input
            :value="postData.name"
            placeholder="お名前（匿名可）"
            :style="inputDark"
            aria-label="お名前"
            @input="patch({ name: $event.target.value })"
          />
          <input
            :value="postData.pref"
            placeholder="都道府県"
            :style="inputDark"
            aria-label="都道府県"
            @input="patch({ pref: $event.target.value })"
          />
          <div>
            <input
              :value="postData.title"
              placeholder="思い出の題 *"
              :style="{ ...inputDark, border: errors.title ? '1px solid var(--beni-500)' : '1px solid rgba(201,169,97,0.3)' }"
              aria-label="タイトル"
              aria-required="true"
              @input="patch({ title: $event.target.value })"
            />
            <div v-if="errors.title" style="font-size: 11px; color: var(--beni-500); margin-top: 3px" role="alert">{{ errors.title }}</div>
          </div>
          <div>
            <textarea
              :value="postData.body"
              rows="5"
              placeholder="本文 *"
              :style="{ ...inputDark, resize: 'vertical' }"
              aria-label="本文"
              aria-required="true"
              @input="patch({ body: $event.target.value })"
            />
            <div v-if="errors.body" style="font-size: 11px; color: var(--beni-500); margin-top: 3px" role="alert">{{ errors.body }}</div>
          </div>
          <select
            :value="postData.song"
            :style="inputDark"
            aria-label="心に残る一曲"
            @change="patch({ song: $event.target.value })"
          >
            <option value="">心に残る一曲を選ぶ</option>
            <option v-for="s in songs" :key="s" :value="s">{{ s }}</option>
          </select>
          <button
            type="button"
            :style="{ ...inputDark, background: 'rgba(10,6,4,0.3)', cursor: 'pointer', textAlign: 'left', border: '1px dashed rgba(201,169,97,0.3)' }"
            aria-label="写真を添付（任意）"
          >
            📷 写真を添付（任意）
          </button>
          <button type="button" :style="{ ...btnBeni, width: '100%', justifyContent: 'center', marginTop: '4px' }" @click="emit('submit')">投稿する</button>
        </div>
      </template>
    </div>
  </aside>
</template>
