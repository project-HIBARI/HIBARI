<script setup>
/**
 * 部品名: 歩み — 下部関連ページ導線カード
 * 用途: ディスコグラフィー・ギャラリー等への誘導カード5枚を表示する
 */
const emit = defineEmits(['navigate', 'coming-soon'])

const cards = [
  {
    id: 'profile',
    title: '美空ひばりについて',
    desc: '彼女の人生と軌跡',
    deco: 'rose',
    action: 'navigate',
    target: 'profile',
  },
  {
    id: 'disco',
    title: 'ディスコグラフィー',
    desc: '楽曲・アルバム一覧',
    deco: 'record',
    action: 'navigate',
    target: 'disco',
  },
  {
    id: 'gallery',
    title: 'ギャラリー',
    desc: '写真でたどる軌跡',
    deco: 'gallery',
    action: 'coming-soon',
    target: 'gallery',
  },
  {
    id: 'events',
    title: 'イベント情報',
    desc: 'コンサート・企画展など',
    deco: 'stage',
    action: 'coming-soon',
    target: 'events',
  },
  {
    id: 'fanclub',
    title: 'ファンクラブ',
    desc: '入会・会員特典',
    deco: 'fanclub',
    action: 'coming-soon',
    target: 'fanclub',
  },
]

function onClick(card) {
  if (card.action === 'navigate') {
    emit('navigate', card.target)
  } else {
    emit('coming-soon', card.target)
  }
}
</script>

<template>
  <!-- 歩みページ下部の各セクションへの導線カード -->
  <section class="profile-related" aria-label="関連コンテンツ">
    <div class="profile-related__grid">
      <button
        v-for="c in cards"
        :key="c.id"
        type="button"
        class="profile-related__card"
        :class="`profile-related__card--${c.deco}`"
        :aria-label="c.title"
        @click="onClick(c)"
      >
        <div class="profile-related__visual" aria-hidden="true" />
        <div class="profile-related__body">
          <h3 class="profile-related__title">{{ c.title }}</h3>
          <p class="profile-related__desc">{{ c.desc }}</p>
          <span class="profile-related__arrow">›</span>
        </div>
      </button>
    </div>
  </section>
</template>

<style scoped>
.profile-related {
  margin-top: var(--sp-8);
  margin-bottom: var(--sp-6);
}
.profile-related__grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}
.profile-related__card {
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
  overflow: hidden;
  cursor: pointer;
  text-align: left;
  padding: 0;
  transition: transform 0.2s, box-shadow 0.2s;
}
.profile-related__card:hover {
  transform: translateY(-2px);
  box-shadow: var(--site-shadow-md);
}
.profile-related__visual {
  height: 100px;
  background: var(--site-surface-muted);
}
.profile-related__card--rose .profile-related__visual {
  background:
    radial-gradient(circle at 30% 60%, rgba(220, 120, 140, 0.35) 0%, transparent 50%),
    radial-gradient(circle at 70% 40%, rgba(240, 160, 180, 0.3) 0%, transparent 45%),
    linear-gradient(160deg, #fce8ec, #f5ebe0);
}
.profile-related__card--record .profile-related__visual {
  background:
    radial-gradient(circle at center, #2a201a 28%, transparent 29%),
    repeating-radial-gradient(circle at center, #333 0 1px, #222 1px 3px),
    linear-gradient(160deg, #3a2a1a, #1a1410);
  position: relative;
}
.profile-related__card--record .profile-related__visual::after {
  content: '';
  position: absolute;
  inset: 50% auto auto 50%;
  transform: translate(-50%, -50%);
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: 2px solid rgba(201, 169, 97, 0.4);
  background: radial-gradient(circle, var(--beni-700) 0%, #5e1111 100%);
}
.profile-related__card--gallery .profile-related__visual {
  background: linear-gradient(135deg, #d9c7a6 0%, #c4a882 100%);
}
.profile-related__card--stage .profile-related__visual {
  background:
    radial-gradient(ellipse at 50% 0%, rgba(255, 220, 100, 0.5) 0%, transparent 60%),
    linear-gradient(180deg, #4a1520 0%, #2a0810 100%);
}
.profile-related__card--fanclub .profile-related__visual {
  background: linear-gradient(135deg, var(--murasaki-700), var(--murasaki-900));
  position: relative;
}
.profile-related__card--fanclub .profile-related__visual::after {
  content: 'FC';
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--ff-latin);
  font-size: 28px;
  font-weight: 700;
  color: var(--kin-400);
  letter-spacing: 0.1em;
}
.profile-related__body {
  padding: 16px 18px 18px;
  position: relative;
}
.profile-related__title {
  margin: 0 0 6px;
  font-family: var(--ff-mincho);
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--site-text);
}
.profile-related__desc {
  margin: 0;
  font-size: 12px;
  line-height: 1.6;
  color: var(--site-text-muted);
}
.profile-related__arrow {
  position: absolute;
  right: 16px;
  bottom: 18px;
  font-size: 20px;
  color: var(--murasaki-500);
  line-height: 1;
}

@media (max-width: 1024px) {
  .profile-related__grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 767px) {
  .profile-related__grid {
    grid-template-columns: 1fr;
  }
}
</style>
