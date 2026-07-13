<script setup>
/**
 * 部品名: SNSローディングスケルトン
 * 用途: post / story / profile 各画面の読み込み中プレースホルダー
 */
defineProps({
  variant: { type: String, default: 'post' }, // post | story | profile
  count: { type: Number, default: 1 },
})
</script>

<template>
  <div class="sns-skel" :class="`sns-skel--${variant}`" aria-hidden="true">
    <template v-if="variant === 'post'">
      <div v-for="i in count" :key="i" class="sns-skel__card">
        <div class="sns-skel__row">
          <span class="sns-skel__avatar sns-skel__shimmer" />
          <span class="sns-skel__line sns-skel__shimmer" style="width: 40%" />
        </div>
        <span class="sns-skel__block sns-skel__shimmer" />
        <span class="sns-skel__line sns-skel__shimmer" style="width: 80%" />
        <span class="sns-skel__line sns-skel__shimmer" style="width: 55%" />
      </div>
    </template>

    <template v-else-if="variant === 'story'">
      <span v-for="i in count" :key="i" class="sns-skel__story sns-skel__shimmer" />
    </template>

    <template v-else>
      <div class="sns-skel__profile-row">
        <span class="sns-skel__avatar sns-skel__avatar--lg sns-skel__shimmer" />
        <div class="sns-skel__profile-lines">
          <span class="sns-skel__line sns-skel__shimmer" style="width: 50%" />
          <span class="sns-skel__line sns-skel__shimmer" style="width: 70%" />
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.sns-skel__shimmer {
  background: linear-gradient(
    100deg,
    var(--sns-card) 30%,
    var(--sns-card-strong) 50%,
    var(--sns-card) 70%
  );
  background-size: 200% 100%;
  animation: sns-skel-shimmer 1.4s ease-in-out infinite;
  border-radius: 6px;
  display: block;
}
@keyframes sns-skel-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.sns-skel--post {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.sns-skel__card {
  padding: 14px;
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--sns-border);
  background: var(--sns-card);
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.sns-skel__row {
  display: flex;
  align-items: center;
  gap: 10px;
}
.sns-skel__avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  flex-shrink: 0;
}
.sns-skel__avatar--lg {
  width: 96px;
  height: 96px;
}
.sns-skel__line {
  height: 12px;
  border-radius: 4px;
}
.sns-skel__block {
  height: 160px;
  border-radius: var(--site-radius-md);
}

.sns-skel--story {
  display: flex;
  gap: 14px;
}
.sns-skel__story {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  flex-shrink: 0;
}

.sns-skel__profile-row {
  display: flex;
  gap: 16px;
  align-items: center;
}
.sns-skel__profile-lines {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
