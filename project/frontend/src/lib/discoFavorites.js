export const DISCO_FAV_KEY = 'hbr-disco-favorites'
export const DISCO_FAV_META_KEY = 'hbr-disco-favorites-meta'

export function loadDiscoFavoriteIds() {
  try {
    const raw = localStorage.getItem(DISCO_FAV_KEY)
    if (!raw) return []
    const ids = JSON.parse(raw)
    return Array.isArray(ids) ? ids : []
  } catch {
    return []
  }
}

export function loadDiscoFavoriteMeta() {
  try {
    const raw = localStorage.getItem(DISCO_FAV_META_KEY)
    const meta = raw ? JSON.parse(raw) : {}
    return meta && typeof meta === 'object' ? meta : {}
  } catch {
    return {}
  }
}

export function saveDiscoFavoriteIds(ids) {
  try {
    localStorage.setItem(DISCO_FAV_KEY, JSON.stringify(ids))
  } catch {
    /* ignore */
  }
}

export function saveDiscoFavoriteMeta(meta) {
  try {
    localStorage.setItem(DISCO_FAV_META_KEY, JSON.stringify(meta))
  } catch {
    /* ignore */
  }
}

export function getDiscoFavoriteAddedAt(id) {
  const meta = loadDiscoFavoriteMeta()
  if (meta[id]) return meta[id]
  return new Date().toISOString()
}

/**
 * @returns {{ ids: Set<string>, added: boolean }}
 */
export function toggleDiscoFavorite(id) {
  const ids = new Set(loadDiscoFavoriteIds())
  const meta = loadDiscoFavoriteMeta()

  if (ids.has(id)) {
    ids.delete(id)
    delete meta[id]
  } else {
    ids.add(id)
    meta[id] = new Date().toISOString()
  }

  saveDiscoFavoriteIds([...ids])
  saveDiscoFavoriteMeta(meta)
  return { ids, added: ids.has(id) }
}

export function loadDiscoFavoriteIdSet() {
  return new Set(loadDiscoFavoriteIds())
}
