<script setup>
/**
 * 部品名: ヘッダー内インライン検索（ポップアップなし）
 */
import { ref, computed, onMounted, onUnmounted } from 'vue'
import UiIco from '../ui/UiIco.vue'
import { buildSearchIndex, filterSearchResults } from '../../lib/siteSearch.js'

const emit = defineEmits(['navigate'])

const query = ref('')
const focused = ref(false)
const rootRef = ref(null)
const searchIndex = buildSearchIndex()

const results = computed(() => filterSearchResults(query.value, searchIndex))

const showDropdown = computed(
  () => focused.value && query.value.trim().length > 0,
)

function select(item) {
  emit('navigate', item.page)
  query.value = ''
  focused.value = false
}

function onDocumentClick(event) {
  if (!rootRef.value?.contains(event.target)) {
    focused.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', onDocumentClick)
})

onUnmounted(() => {
  document.removeEventListener('click', onDocumentClick)
})
</script>

<template>
  <div ref="rootRef" class="header-search">
    <UiIco name="search" :size="18" color="var(--site-text-muted)" class="header-search__icon" />
    <input
      v-model="query"
      type="search"
      class="header-search__input"
      placeholder="検索"
      aria-label="サイト内検索"
      @focus="focused = true"
    />
    <ul v-if="showDropdown" class="header-search__dropdown" role="listbox">
      <li v-if="!results.length" class="header-search__empty">該当なし</li>
      <li v-for="item in results" :key="item.key" role="option">
        <button type="button" class="header-search__item" @click="select(item)">
          <span class="header-search__type">{{ item.type }}</span>
          <span class="header-search__label">{{ item.label }}</span>
        </button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.header-search {
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
  min-width: 0;
  max-width: 200px;
  min-height: 44px;
  padding: 4px 10px;
  border: 1px solid var(--site-border);
  border-radius: 999px;
  background: #fff;
  box-sizing: border-box;
}
.header-search__icon {
  flex-shrink: 0;
}
.header-search__input {
  width: 100%;
  min-width: 0;
  border: 0;
  background: transparent;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-form-input);
  line-height: 1.4;
  color: var(--site-text);
  outline: none;
}
.header-search__input::placeholder {
  color: var(--site-text-light);
}
.header-search__dropdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  min-width: 260px;
  margin: 0;
  padding: 6px 0;
  list-style: none;
  background: #fff;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  box-shadow: var(--site-shadow-md);
  z-index: 70;
  max-height: 280px;
  overflow-y: auto;
}
.header-search__item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 14px;
  border: 0;
  background: transparent;
  text-align: left;
  cursor: pointer;
  font-family: var(--ff-sans-jp);
}
.header-search__item:hover {
  background: var(--murasaki-100);
}
.header-search__type {
  flex-shrink: 0;
  font-size: var(--font-size-badge);
  padding: 2px 8px;
  background: var(--murasaki-100);
  color: var(--murasaki-700);
  border-radius: 999px;
}
.header-search__label {
  font-size: var(--font-size-button);
  color: var(--site-text);
  overflow-wrap: anywhere;
}
.header-search__empty {
  padding: 12px 14px;
  font-size: var(--font-size-caption);
  color: var(--site-text-muted);
}

@media (max-width: 1099px) {
  .header-search {
    max-width: 140px;
  }
}
@media (max-width: 767px) {
  .header-search {
    display: none;
  }
}
</style>
