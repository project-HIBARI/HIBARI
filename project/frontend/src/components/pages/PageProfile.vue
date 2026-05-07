<script setup>
/**
 * ページ: 歩み（プロフィール＋年表）
 */
import PageHead from '../ui/PageHead.vue'
import Photo from '../ui/Photo.vue'
import UiIco from '../ui/UiIco.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'

const p = HIBARU_DATA.profile
const rows = [
  ['芸名', '美空ひばり'],
  ['本名', '加藤和枝'],
  ['生誕', p.born],
  ['出生地', '横浜市磯子区滝頭'],
  ['逝去', p.died],
  ['享年', '五十二歳'],
  ['所属', p.label],
  ['生涯録音', p.totalSongs + '曲以上'],
  ['オリジナル', p.originalSongs + '曲'],
]
</script>

<template>
  <div>
    <PageHead kanji="歴" title="歩み" sub="Profile · MISORA HIBARI · 五十二年の軌跡" />
    <div style="display: grid; grid-template-columns: 360px 1fr; gap: 56px" class="prof-grid">
      <div style="position: sticky; top: 120px; align-self: start">
        <Photo :w="360" :h="460" caption="studio portrait · 日本コロムビア" variant="dark" />
        <div style="margin-top: 20px; padding: 20px; border: 1px solid rgba(201,169,97,0.3)">
          <dl style="margin: 0; display: grid; grid-template-columns: auto 1fr; gap: 10px 16px; font-size: 13px">
            <template v-for="[k, v] in rows" :key="k">
              <dt style="color: var(--kin-500); font-family: var(--ff-mincho); font-weight: 700">{{ k }}</dt>
              <dd style="margin: 0">{{ v }}</dd>
            </template>
          </dl>
        </div>
        <div style="margin-top: 16px; padding: 16px; border: 1px solid var(--beni-700); background: rgba(139,26,26,0.1)">
          <div style="font-family: var(--ff-mincho); font-size: 13px; font-weight: 700; margin-bottom: 8px; color: var(--kin-500)">主な受賞歴</div>
          <div
            v-for="(a, i) in p.awards"
            :key="i"
            style="font-size: 12px; color: var(--paper-200); line-height: 1.7; padding-left: 8px; border-left: 2px solid var(--beni-500); margin-bottom: 6px"
          >
            {{ a }}
          </div>
        </div>
      </div>
      <div>
        <article
          v-for="(t, i) in HIBARU_DATA.timeline"
          :key="i"
          style="display: grid; grid-template-columns: 110px 1fr; gap: 24px; padding: 26px 0; border-bottom: 1px solid rgba(201,169,97,0.2)"
        >
          <div>
            <div style="font-family: var(--ff-latin); font-size: 28px; font-weight: 700; color: var(--kin-500); line-height: 1">{{ t.year }}</div>
            <div style="font-family: var(--ff-mincho); font-size: 10px; color: var(--paper-300); margin-top: 5px; letter-spacing: 0.1em">{{ t.era }}</div>
            <div style="font-family: var(--ff-mincho); font-size: 11px; color: var(--beni-500); margin-top: 3px">{{ t.age }}歳</div>
          </div>
          <div>
            <h3 style="font-family: var(--ff-mincho); font-size: 18px; margin: 0 0 10px; letter-spacing: 0.06em">{{ t.title }}</h3>
            <p style="font-size: 14px; line-height: 2; color: var(--paper-200); margin: 0">{{ t.body }}</p>
            <button
              type="button"
              style="margin-top: 10px; background: transparent; border: 1px solid rgba(201,169,97,0.3); color: var(--paper-300); padding: 5px 12px; cursor: pointer; font-family: var(--ff-mincho); font-size: 11px; letter-spacing: 0.15em; display: flex; align-items: center; gap: 6px"
              aria-label="写真を見る（プレースホルダー）"
            >
              <UiIco name="search" :size="12" color="var(--paper-300)" /> 写真を見る
            </button>
          </div>
        </article>
      </div>
    </div>
  </div>
</template>
