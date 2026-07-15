<script setup>
/**
 * 部品名: Music Memory Book — アルバム表紙ビジュアル
 * 表紙デザイン（透明PNG）をモックアップの表紙面に重ねて表示
 */
import { computed } from 'vue'
import { getCoverDesignImage, normalizeCoverDesignId } from '../../../lib/memoryBookCoverDesigns.js'

const props = defineProps({
  year: { type: [Number, String], default: 2026 },
  subtitle: { type: String, default: 'Music Memories' },
  /** purple | blue | green | brown — designId 未指定時のフォールバック */
  tone: { type: String, default: 'purple' },
  size: { type: String, default: 'lg' },
  /** 1〜9: hyousi-design 透明PNG */
  designId: { type: Number, default: 1 },
})

const normalizedDesignId = computed(() => normalizeCoverDesignId(props.designId))
const coverImage = computed(() => getCoverDesignImage(normalizedDesignId.value))
const useDesignOverlay = computed(() => normalizedDesignId.value >= 1)
</script>

<template>
  <div
    class="mmb-cover"
    :class="[
      `mmb-cover--${size}`,
      useDesignOverlay ? 'mmb-cover--with-design' : `mmb-cover--${tone}`,
    ]"
    aria-hidden="true"
  >
    <div class="mmb-cover__spine" />
    <div class="mmb-cover__face">
      <img
        v-if="useDesignOverlay"
        :src="coverImage"
        alt=""
        class="mmb-cover__design"
        decoding="async"
      />

      <template v-else>
        <div class="mmb-cover__ornament mmb-cover__ornament--top">♪</div>
        <p class="mmb-cover__subtitle">{{ subtitle }}</p>
        <p class="mmb-cover__year">{{ year }}</p>
        <div class="mmb-cover__flowers">
          <span>✿</span>
          <span class="mmb-cover__note">♫</span>
          <span>✿</span>
        </div>
        <div class="mmb-cover__line" />
        <p class="mmb-cover__brand">MISORA HIBARI</p>
      </template>
    </div>
  </div>
</template>

<style scoped>
.mmb-cover {
  position: relative;
  perspective: 800px;
  max-width: 100%;
  box-sizing: border-box;
  flex-shrink: 1;
}

.mmb-cover:not(.mmb-cover--with-design) {
  filter: drop-shadow(0 18px 40px rgba(61, 36, 80, 0.28));
}

.mmb-cover--lg {
  width: min(220px, 100%);
  aspect-ratio: 11 / 15;
  height: auto;
}

.mmb-cover--md {
  width: min(168px, 100%);
  aspect-ratio: 168 / 228;
  height: auto;
}

.mmb-cover--sm {
  width: min(120px, 100%);
  aspect-ratio: 120 / 164;
  height: auto;
}

.mmb-cover__spine {
  position: absolute;
  left: 0;
  top: 8px;
  bottom: 8px;
  width: 14px;
  border-radius: 4px 0 0 4px;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.15), rgba(255, 255, 255, 0.08));
}

.mmb-cover__face {
  position: absolute;
  inset: 0 0 0 10px;
  border-radius: 4px 12px 12px 4px;
  border: 1px solid rgba(201, 169, 97, 0.45);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px 16px;
  text-align: center;
  overflow: hidden;
}

.mmb-cover--with-design .mmb-cover__face {
  padding: 0;
  border: 0;
  background: transparent;
  overflow: hidden;
}

.mmb-cover__design {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  border-radius: 4px 12px 12px 4px;
}

.mmb-cover__face::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 15%, rgba(255, 255, 255, 0.12) 0%, transparent 45%),
    radial-gradient(circle at 80% 85%, rgba(0, 0, 0, 0.12) 0%, transparent 50%);
  pointer-events: none;
}

.mmb-cover--with-design .mmb-cover__face::before {
  display: none;
}

.mmb-cover--purple .mmb-cover__face {
  background: linear-gradient(145deg, #5d3a6b 0%, #4a2d5e 45%, #3d2450 100%);
}

.mmb-cover--blue .mmb-cover__face {
  background: linear-gradient(145deg, #4a5a7a 0%, #3d4d68 45%, #2f3d55 100%);
}

.mmb-cover--green .mmb-cover__face {
  background: linear-gradient(145deg, #4a6a58 0%, #3d5748 45%, #2f4538 100%);
}

.mmb-cover--brown .mmb-cover__face {
  background: linear-gradient(145deg, #6a5248 0%, #574238 45%, #45342c 100%);
}

.mmb-cover__ornament {
  position: relative;
  z-index: 1;
  font-size: var(--font-size-small);
  color: var(--kin-400);
  letter-spacing: 0.3em;
  margin-bottom: 12px;
}

.mmb-cover__subtitle {
  position: relative;
  z-index: 1;
  margin: 0 0 8px;
  font-family: var(--ff-latin);
  font-size: var(--font-size-caption);
  letter-spacing: 0.28em;
  color: rgba(255, 255, 255, 0.85);
}

.mmb-cover__year {
  position: relative;
  z-index: 1;
  margin: 0;
  font-family: var(--ff-latin);
  font-size: 2.625rem;
  font-weight: 700;
  line-height: 1;
  color: var(--kin-400);
  letter-spacing: 0.06em;
}

.mmb-cover--sm .mmb-cover__year {
  font-size: var(--font-size-heading);
}

.mmb-cover__flowers {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 16px 0 12px;
  font-size: var(--font-size-caption);
  color: rgba(255, 255, 255, 0.55);
}

.mmb-cover__note {
  font-size: var(--font-size-body);
  color: var(--kin-500);
}

.mmb-cover__line {
  position: relative;
  z-index: 1;
  width: 48px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--kin-500), transparent);
  margin-bottom: 10px;
}

.mmb-cover__brand {
  position: relative;
  z-index: 1;
  margin: 0;
  font-family: var(--ff-latin);
  font-size: var(--font-size-badge);
  letter-spacing: 0.35em;
  color: rgba(255, 255, 255, 0.5);
}
</style>
