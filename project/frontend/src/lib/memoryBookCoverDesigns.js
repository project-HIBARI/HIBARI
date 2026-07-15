/**
 * Music Memory Book — アルバム表紙デザイン定義
 */
export const COVER_DESIGN_COUNT = 9

export const COVER_DESIGNS = Array.from({ length: COVER_DESIGN_COUNT }, (_, i) => {
  const id = i + 1
  return {
    id,
    label: `デザイン ${id}`,
    image: `/images/memorybook/covers/hyousi-design-${id}.png`,
  }
})

export function getCoverDesignImage(designId) {
  const id = Number(designId)
  if (!Number.isFinite(id) || id < 1 || id > COVER_DESIGN_COUNT) {
    return COVER_DESIGNS[0].image
  }
  return COVER_DESIGNS[id - 1].image
}

export function normalizeCoverDesignId(designId) {
  const id = Number(designId)
  if (!Number.isFinite(id) || id < 1 || id > COVER_DESIGN_COUNT) return 1
  return id
}
