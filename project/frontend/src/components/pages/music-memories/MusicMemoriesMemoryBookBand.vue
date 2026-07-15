<script setup>
/**
 * 部品名: Music Memories — Music Memory Book 紹介帯
 * 用途: プラットフォームTOPで複数アーティスト対応の思い出帳機能を訴求
 */
import UiButton from '../../ui/UiButton.vue'
import { MEMORY_BOOK_SHOWCASE_ARTISTS } from '../../../data/musicMemoriesData.js'

const emit = defineEmits(['open-memory-book'])

const features = [
  { label: '献花の記録', icon: '✿' },
  { label: '思い出投稿', icon: '♪' },
  { label: 'お気に入り楽曲', icon: '♫' },
  { label: 'AIとの会話', icon: '✦' },
]
</script>

<template>
  <section class="mm-mbook" aria-labelledby="mm-mbook-title">
    <div class="mm-mbook__card">
      <div class="mm-mbook__visual" aria-hidden="true">
        <div class="mm-mbook__collage">
          <div
            v-for="(artist, index) in MEMORY_BOOK_SHOWCASE_ARTISTS"
            :key="artist.id"
            class="mm-mbook__thumb"
            :class="{
              'mm-mbook__thumb--open': artist.status === 'open',
              'mm-mbook__thumb--soon': artist.status === 'soon',
            }"
            :style="{ '--i': index }"
          >
            <img
              :src="artist.image"
              :alt="artist.name"
              class="mm-mbook__thumb-img"
              loading="lazy"
              decoding="async"
            />
            <span v-if="artist.status === 'soon'" class="mm-mbook__thumb-badge">準備中</span>
          </div>
        </div>
        <p class="mm-mbook__visual-caption">All Artists</p>
      </div>

      <div class="mm-mbook__body">
        <p class="mm-mbook__eyebrow">Music Memory Book</p>
        <h2 id="mm-mbook-title" class="mm-mbook__title">音楽の思い出帳</h2>
        <p class="mm-mbook__lead">
          献花・思い出・お気に入り楽曲・AIとの会話——あなたの音楽体験を、年ごとのアルバムに自動でまとめます。
          美空ひばりをはじめ、<strong>すべてのアーティスト</strong>のファンクラブで使える共通機能です。
        </p>

        <ul class="mm-mbook__features" aria-label="記録できる内容">
          <li v-for="item in features" :key="item.label" class="mm-mbook__feature">
            <span class="mm-mbook__feature-icon" aria-hidden="true">{{ item.icon }}</span>
            {{ item.label }}
          </li>
        </ul>

        <div class="mm-mbook__artists" aria-label="対応アーティスト">
          <span
            v-for="artist in MEMORY_BOOK_SHOWCASE_ARTISTS"
            :key="artist.id"
            class="mm-mbook__artist-chip"
            :class="{ 'mm-mbook__artist-chip--open': artist.status === 'open' }"
          >
            {{ artist.name }}
            <small v-if="artist.status === 'open'">利用可</small>
            <small v-else>順次対応</small>
          </span>
        </div>

        <UiButton variant="gold" size="md" class="mm-mbook__cta" @click="emit('open-memory-book')">
          思い出帳をみる
        </UiButton>
      </div>
    </div>
  </section>
</template>

<style scoped>
.mm-mbook {
  margin-bottom: clamp(40px, 7vw, 64px);
}

.mm-mbook__card {
  display: grid;
  grid-template-columns: minmax(340px, 1.05fr) minmax(0, 0.95fr);
  gap: 0;
  overflow: hidden;
  border: 1px solid rgba(201, 169, 97, 0.35);
  border-radius: var(--site-radius-lg);
  background: linear-gradient(125deg, rgba(26, 20, 24, 0.62), rgba(90, 58, 107, 0.22));
}

.mm-mbook__visual {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 18px;
  min-height: 420px;
  padding: clamp(32px, 5vw, 48px);
  background: linear-gradient(160deg, rgba(122, 80, 136, 0.28), rgba(26, 20, 24, 0.75));
  border-right: 1px solid rgba(201, 169, 97, 0.12);
}

.mm-mbook__collage {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: clamp(12px, 2vw, 16px);
  width: 100%;
  max-width: min(100%, 480px);
}

.mm-mbook__thumb {
  position: relative;
  aspect-ratio: 1;
  min-height: 120px;
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid rgba(201, 169, 97, 0.25);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.38);
}

.mm-mbook__thumb--open {
  border-color: rgba(201, 169, 97, 0.55);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.42);
}

.mm-mbook__thumb--soon {
  opacity: 0.78;
}

.mm-mbook__thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
  display: block;
  filter: grayscale(12%);
}

.mm-mbook__thumb--open .mm-mbook__thumb-img {
  filter: none;
}

.mm-mbook__thumb-badge {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 7px 8px;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  letter-spacing: 0.06em;
  text-align: center;
  color: rgba(248, 244, 239, 0.92);
  background: rgba(18, 13, 22, 0.78);
}

.mm-mbook__visual-caption {
  margin: 0;
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: rgba(201, 169, 97, 0.75);
}

.mm-mbook__body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: clamp(24px, 4vw, 36px) clamp(22px, 4vw, 36px);
}

.mm-mbook__eyebrow {
  margin: 0 0 8px;
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: var(--kin-400);
}

.mm-mbook__title {
  margin: 0 0 14px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.35rem, 2.5vw, 1.65rem);
  letter-spacing: 0.08em;
}

.mm-mbook__lead {
  margin: 0 0 18px;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.9;
  color: rgba(248, 244, 239, 0.72);
}

.mm-mbook__lead strong {
  color: rgba(201, 169, 97, 0.95);
  font-weight: 600;
}

.mm-mbook__features {
  list-style: none;
  margin: 0 0 16px;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px 14px;
}

.mm-mbook__feature {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  color: rgba(248, 244, 239, 0.82);
}

.mm-mbook__feature-icon {
  width: 22px;
  height: 22px;
  border-radius: 999px;
  border: 1px solid rgba(201, 169, 97, 0.35);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  color: var(--kin-400);
  flex-shrink: 0;
}

.mm-mbook__artists {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
}

.mm-mbook__artist-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.04);
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  color: rgba(248, 244, 239, 0.62);
}

.mm-mbook__artist-chip small {
  font-size: 9px;
  letter-spacing: 0.04em;
  color: rgba(248, 244, 239, 0.45);
}

.mm-mbook__artist-chip--open {
  border-color: rgba(201, 169, 97, 0.45);
  color: rgba(248, 244, 239, 0.88);
}

.mm-mbook__artist-chip--open small {
  color: var(--kin-400);
}

.mm-mbook__cta {
  align-self: flex-start;
}

@media (max-width: 720px) {
  .mm-mbook__card {
    grid-template-columns: 1fr;
  }

  .mm-mbook__visual {
    min-height: 0;
    border-right: none;
    border-bottom: 1px solid rgba(201, 169, 97, 0.12);
    padding: 28px 20px 32px;
  }

  .mm-mbook__collage {
    max-width: 100%;
    gap: 10px;
  }

  .mm-mbook__thumb {
    min-height: 96px;
  }

  .mm-mbook__features {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 960px) {
  .mm-mbook__collage {
    max-width: 520px;
  }

  .mm-mbook__thumb {
    min-height: 140px;
  }
}
</style>
