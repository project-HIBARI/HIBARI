<script setup>
/**
 * 部品名: 支払い詳細 — 銀行振込
 * 入力: 金融機関の選択（一覧＋検索）/ 支店名 / 口座種別 / 口座番号 / 口座名義
 */
import { ref, computed } from 'vue'
import RegisterField from '../RegisterField.vue'
import RegisterOptionGroup from '../RegisterOptionGroup.vue'
import PaymentBrandIcon from './PaymentBrandIcon.vue'
import { BANKS, searchBanks, findBank } from './bankData.js'

const props = defineProps({
  form: { type: Object, required: true },
  errors: { type: Object, required: true },
})

const bankSearch = ref('')
const showSearchResults = ref(false)

const popularBanks = BANKS.slice(0, 4).map((b) => ({
  value: b.value,
  label: b.label,
  icon: b.icon,
}))

const searchResults = computed(() => searchBanks(bankSearch.value))

const selectedBank = computed(() => findBank(props.form.bankName))

function selectBank(value) {
  props.form.bankName = value
  bankSearch.value = findBank(value)?.label || ''
  showSearchResults.value = false
}

function onSearchInput() {
  showSearchResults.value = true
  if (!bankSearch.value.trim()) {
    props.form.bankName = ''
  }
}

const accountTypeOptions = [
  { value: 'ordinary', label: '普通' },
  { value: 'current', label: '当座' },
]
</script>

<template>
  <div class="pay-bank">
    <RegisterOptionGroup
      :model-value="form.bankName"
      name="pay-bank-popular"
      label="よく使われる金融機関"
      :options="popularBanks"
      :columns="2"
      @update:model-value="selectBank"
    />

    <div class="pay-bank__search">
      <label class="pay-bank__search-label" for="pay-bank-search">金融機関を検索</label>
      <input
        id="pay-bank-search"
        v-model="bankSearch"
        type="search"
        class="pay-bank__search-input"
        placeholder="銀行名・カナで検索（例: みずほ、ラクテン）"
        autocomplete="off"
        @input="onSearchInput"
        @focus="showSearchResults = true"
      />
      <ul v-if="showSearchResults && bankSearch.trim()" class="pay-bank__results">
        <li v-if="searchResults.length === 0" class="pay-bank__no-result">該当する金融機関がありません</li>
        <li v-for="bank in searchResults" :key="bank.value">
          <button
            type="button"
            class="pay-bank__result-btn"
            :class="{ 'pay-bank__result-btn--active': form.bankName === bank.value }"
            @click="selectBank(bank.value)"
          >
            <PaymentBrandIcon :brand="bank.icon" :size="28" />
            <span>{{ bank.label }}</span>
          </button>
        </li>
      </ul>
      <p v-if="errors.bankName" class="pay-bank__error">{{ errors.bankName }}</p>
      <p v-else-if="selectedBank" class="pay-bank__selected">
        選択中: <strong>{{ selectedBank.label }}</strong>
      </p>
    </div>

    <div class="pay-bank__account">
      <h3 class="pay-bank__account-title">振込元口座情報</h3>
      <RegisterField
        id="pay-bank-branch"
        v-model="form.bankBranch"
        label="支店名"
        placeholder="例）東京営業部"
        :error="errors.bankBranch"
        required
      />
      <RegisterOptionGroup
        v-model="form.bankAccountType"
        name="pay-bank-type"
        label="口座種別"
        :options="accountTypeOptions"
        :columns="2"
        :error="errors.bankAccountType"
        required
      />
      <RegisterField
        id="pay-bank-number"
        :model-value="form.bankAccountNumber"
        label="口座番号"
        inputmode="numeric"
        placeholder="7桁の口座番号"
        :maxlength="7"
        :error="errors.bankAccountNumber"
        required
        @update:model-value="(v) => (form.bankAccountNumber = v.replace(/\D/g, '').slice(0, 7))"
      />
      <RegisterField
        id="pay-bank-holder"
        v-model="form.bankAccountHolder"
        label="口座名義（カナ）"
        placeholder="例）ヤマダ タロウ"
        hint="全角カタカナでご入力ください。"
        :error="errors.bankAccountHolder"
        required
      />
    </div>

    <p class="pay-bank__note">
      毎月末締め・翌月払い。お申し込み後、振込先口座番号をメールでご案内します。
    </p>
  </div>
</template>

<style scoped>
.pay-bank {
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.pay-bank__search {
  position: relative;
}
.pay-bank__search-label {
  display: block;
  margin-bottom: 8px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  font-weight: 500;
  color: var(--site-text) !important;
}
.pay-bank__search-input {
  width: 100%;
  padding: 14px 16px;
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  color: var(--site-text) !important;
  background: #fffdf9 !important;
  border: 1px solid var(--site-border) !important;
  border-radius: var(--site-radius-sm);
  box-sizing: border-box;
}
.pay-bank__search-input::placeholder {
  color: var(--site-text-light) !important;
}
.pay-bank__search-input:focus {
  outline: none;
  border-color: var(--murasaki-400);
  box-shadow: 0 0 0 3px rgba(122, 80, 136, 0.12);
}
.pay-bank__results {
  position: absolute;
  z-index: 20;
  left: 0;
  right: 0;
  top: calc(100% + 4px);
  margin: 0;
  padding: 6px;
  list-style: none;
  max-height: 200px;
  overflow-y: auto;
  background: #fff;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
  box-shadow: var(--site-shadow-md);
}
.pay-bank__result-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 12px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  text-align: left;
  color: var(--site-text);
  background: transparent;
  border: 0;
  border-radius: var(--site-radius-sm);
  cursor: pointer;
}
.pay-bank__result-btn:hover,
.pay-bank__result-btn--active {
  background: var(--murasaki-100);
}
.pay-bank__no-result {
  padding: 12px;
  font-size: 12px;
  color: var(--site-text-light);
  text-align: center;
}
.pay-bank__error {
  margin: 6px 0 0;
  font-size: 11px;
  color: #c0453b;
}
.pay-bank__selected {
  margin: 8px 0 0;
  font-size: 12px;
  color: var(--site-text) !important;
}
.pay-bank__account {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding-top: 8px;
  border-top: 1px solid var(--site-border);
}
.pay-bank__account-title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 14px;
  font-weight: 700;
  color: var(--site-text) !important;
}
.pay-bank__note {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  line-height: 1.7;
  color: var(--site-text) !important;
}
</style>
