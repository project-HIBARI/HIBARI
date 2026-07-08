<script setup>
/**
 * 部品名: 支払いブランドアイコン
 * 用途: クレジット・銀行・コンビニ・キャリア各サービスのブランド表示
 */
defineProps({
  brand: { type: String, required: true },
  size: { type: Number, default: 32 },
})
</script>

<template>
  <span
    class="pay-icon"
    :class="`pay-icon--${brand}`"
    :style="{ width: `${size}px`, height: `${size}px`, fontSize: `${Math.round(size * 0.34)}px` }"
    aria-hidden="true"
  >
    <template v-if="brand === 'credit'">CARD</template>
    <template v-else-if="brand === 'bank'">銀</template>
    <template v-else-if="brand === 'conveni'">CV</template>
    <template v-else-if="brand === 'carrier'">📱</template>
    <template v-else-if="brand === 'mizuho'">みずほ</template>
    <template v-else-if="brand === 'mufg'">MUFG</template>
    <template v-else-if="brand === 'smbc'">SMBC</template>
    <template v-else-if="brand === 'yucho'">ゆうちょ</template>
    <template v-else-if="brand === 'resona'">りそな</template>
    <template v-else-if="brand === 'shinsei'">新生</template>
    <template v-else-if="brand === 'familymart'">FM</template>
    <template v-else-if="brand === 'seven'">7</template>
    <template v-else-if="brand === 'lawson'">L</template>
    <template v-else-if="brand === 'docomo'">d</template>
    <template v-else-if="brand === 'au'">au</template>
    <template v-else-if="brand === 'softbank'">SB</template>
    <template v-else>●</template>
  </span>
</template>

<style scoped>
.pay-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border-radius: 8px;
  font-family: var(--ff-sans-jp);
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1;
  color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
}
.pay-icon--credit { background: linear-gradient(135deg, #1a3a6e, #2d5aa0); }
.pay-icon--bank { background: linear-gradient(135deg, #2e6b4a, #3d8b5e); }
.pay-icon--conveni { background: linear-gradient(135deg, #c45c26, #e07830); }
.pay-icon--carrier { background: linear-gradient(135deg, #555, #777); font-size: 0.9em !important; }
.pay-icon--mizuho { background: #0066b3; font-size: 0.55em !important; }
.pay-icon--mufg { background: #d4002a; }
.pay-icon--smbc { background: #004831; font-size: 0.6em !important; }
.pay-icon--yucho { background: #00a040; font-size: 0.55em !important; }
.pay-icon--resona { background: #c41230; font-size: 0.55em !important; }
.pay-icon--shinsei { background: #003366; font-size: 0.55em !important; }
.pay-icon--familymart { background: #00a040; }
.pay-icon--seven { background: #e85d04; font-size: 0.75em !important; }
.pay-icon--lawson { background: #0068b7; font-size: 0.8em !important; }
.pay-icon--docomo { background: #cc0033; font-size: 0.85em !important; }
.pay-icon--au { background: #ea5504; text-transform: lowercase; }
.pay-icon--softbank { background: #a0a0a0; color: #fff; font-size: 0.55em !important; }
</style>
