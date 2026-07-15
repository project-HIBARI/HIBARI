<script setup>
/**
 * ページ: Music Memories アーティスト診断
 * 役割: 5問の回答タグとアーティスト特徴タグを照合し、1人をおすすめする
 */
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import UiButton from '../ui/UiButton.vue'
import UiIco from '../ui/UiIco.vue'
import SnsUsageCard from './sns/SnsUsageCard.vue'
import { MUSIC_MEMORIES_ARTISTS } from '../../data/musicMemoriesData.js'
import { DIAGNOSIS_QUESTIONS } from '../../data/artistDiagnosisData.js'
import { getRecommendedArtist } from '../../lib/artistDiagnosis.js'
import { consumeUsage, fetchUsage } from '../../api/usage.js'
import { SITE_NAME } from '../../constants/site.js'

const USAGE_FEATURE = 'artist-diagnosis'

const emit = defineEmits(['enter-site', 'open-encyclopedia'])

/** @type {import('vue').Ref<'intro' | 'question' | 'loading' | 'result' | 'error'>} */
const step = ref('intro')
const questionIndex = ref(0)
/** @type {import('vue').Ref<Record<number, string>>} */
const selectedAnswerIds = ref({})
const result = ref(null)
const usageStatus = ref(null)
const usageLoading = ref(true)
let loadingTimer = null

const totalQuestions = DIAGNOSIS_QUESTIONS.length
const currentQuestion = computed(() => DIAGNOSIS_QUESTIONS[questionIndex.value] || null)
const progressPercent = computed(() => Math.round(((questionIndex.value + 1) / totalQuestions) * 100))
const currentAnswerId = computed(() => selectedAnswerIds.value[questionIndex.value] || null)
const isLastQuestion = computed(() => questionIndex.value >= totalQuestions - 1)
const canGoNext = computed(() => Boolean(currentAnswerId.value))

const isUnlimited = computed(() => usageStatus.value != null && usageStatus.value.limit === null)
const canUse = computed(() => {
  if (usageLoading.value) return false
  if (usageStatus.value == null) return true
  return Boolean(usageStatus.value.can_use)
})
const remainingMessage = computed(() => {
  if (usageLoading.value || usageStatus.value == null) return '利用状況を確認しています…'
  if (isUnlimited.value) return '無制限に診断できます'
  if ((usageStatus.value.remaining ?? 0) > 0) return `残り${usageStatus.value.remaining}回`
  return '制限に達しました'
})
const nextResetLabel = computed(() => {
  if (isUnlimited.value) return ''
  if ((usageStatus.value?.remaining ?? 0) > 0) return ''
  return usageStatus.value?.reset_label || ''
})

async function refreshUsage() {
  usageLoading.value = true
  try {
    usageStatus.value = await fetchUsage(USAGE_FEATURE)
  } catch {
    usageStatus.value = null
  } finally {
    usageLoading.value = false
  }
}

function startDiagnosis() {
  if (!canUse.value) return
  selectedAnswerIds.value = {}
  questionIndex.value = 0
  result.value = null
  step.value = 'question'
}

function selectAnswer(answerId) {
  selectedAnswerIds.value = {
    ...selectedAnswerIds.value,
    [questionIndex.value]: answerId,
  }
}

function goBack() {
  if (questionIndex.value <= 0) return
  questionIndex.value -= 1
}

function goNext() {
  if (!canGoNext.value) return
  if (isLastQuestion.value) {
    runDiagnosis()
    return
  }
  questionIndex.value += 1
}

function buildSelectedAnswers() {
  return DIAGNOSIS_QUESTIONS.map((q, i) => {
    const answerId = selectedAnswerIds.value[i]
    return q.answers.find((a) => a.id === answerId) || null
  }).filter(Boolean)
}

function runDiagnosis() {
  step.value = 'loading'
  result.value = null
  if (loadingTimer) clearTimeout(loadingTimer)
  loadingTimer = setTimeout(async () => {
    try {
      if (!MUSIC_MEMORIES_ARTISTS.length) {
        step.value = 'error'
        return
      }
      const selected = buildSelectedAnswers()
      if (selected.length < totalQuestions) {
        step.value = 'error'
        return
      }
      const recommended = getRecommendedArtist(MUSIC_MEMORIES_ARTISTS, selected)
      if (!recommended.artist) {
        step.value = 'error'
        return
      }

      try {
        usageStatus.value = await consumeUsage(USAGE_FEATURE)
      } catch (err) {
        if (err?.status === 429 && err.data) {
          usageStatus.value = err.data
          step.value = 'intro'
          return
        }
        // サーバー未接続時などは結果表示を優先しつつ、次回は再確認
      }

      result.value = recommended
      step.value = 'result'
    } catch {
      step.value = 'error'
    }
  }, 700)
}

function resetAll() {
  if (loadingTimer) {
    clearTimeout(loadingTimer)
    loadingTimer = null
  }
  step.value = 'intro'
  questionIndex.value = 0
  selectedAnswerIds.value = {}
  result.value = null
  refreshUsage()
}

function onFanclub() {
  const artist = result.value?.artist
  if (!artist || artist.status !== 'open' || !artist.siteId) return
  emit('enter-site', artist.siteId)
}

onMounted(() => {
  refreshUsage()
})

onBeforeUnmount(() => {
  if (loadingTimer) clearTimeout(loadingTimer)
})
</script>

<template>
  <div class="artist-match">
    <main id="main-content" class="artist-match__main">
      <!-- 開始 -->
      <section v-if="step === 'intro'" class="artist-match__panel artist-match__intro" aria-labelledby="match-intro-title">
        <p class="artist-match__eyebrow">ARTIST MATCH</p>
        <h1 id="match-intro-title" class="artist-match__title">あなたに響くアーティストは？</h1>
        <p class="artist-match__lead">
          5つの質問から、あなたの気分や音楽の好みに合うアーティストをご紹介します。<br />
          深く考えず、今の気持ちに近いものを選んでください。
        </p>
        <p class="artist-match__meta">全5問・所要時間約1分</p>

        <SnsUsageCard
          class="artist-match__usage"
          :message="remainingMessage"
          :next-reset-label="nextResetLabel"
          :unlimited="isUnlimited"
        />

        <UiButton
          variant="gold"
          size="lg"
          :disabled="!canUse"
          @click="startDiagnosis"
        >
          {{ canUse ? '診断をはじめる' : '制限に達しました' }}
        </UiButton>
      </section>

      <!-- 質問 -->
      <section
        v-else-if="step === 'question' && currentQuestion"
        class="artist-match__panel artist-match__question"
        :aria-labelledby="'match-q-' + currentQuestion.id"
      >
        <div class="artist-match__progress-head">
          <p class="artist-match__progress-label">
            QUESTION {{ questionIndex + 1 }} / {{ totalQuestions }}
          </p>
          <p class="artist-match__progress-pct">{{ progressPercent }}%</p>
        </div>
        <div
          class="artist-match__progress-track"
          role="progressbar"
          :aria-valuenow="progressPercent"
          aria-valuemin="0"
          aria-valuemax="100"
          :aria-label="'進捗 ' + progressPercent + '%'"
        >
          <span class="artist-match__progress-fill" :style="{ width: progressPercent + '%' }" />
        </div>

        <h2 :id="'match-q-' + currentQuestion.id" class="artist-match__q-text">
          {{ currentQuestion.question }}
        </h2>

        <div class="artist-match__answers" role="group" :aria-label="currentQuestion.question">
          <button
            v-for="answer in currentQuestion.answers"
            :key="answer.id"
            type="button"
            class="artist-match__answer"
            :class="{ 'artist-match__answer--selected': currentAnswerId === answer.id }"
            :aria-pressed="currentAnswerId === answer.id"
            @click="selectAnswer(answer.id)"
          >
            <span class="artist-match__answer-label">{{ answer.label }}</span>
            <span v-if="currentAnswerId === answer.id" class="artist-match__answer-check" aria-hidden="true">✓</span>
            <span v-if="currentAnswerId === answer.id" class="artist-match__sr">選択中</span>
          </button>
        </div>

        <div class="artist-match__nav-actions">
          <UiButton
            v-if="questionIndex > 0"
            variant="outline"
            size="md"
            @click="goBack"
          >
            戻る
          </UiButton>
          <span v-else class="artist-match__nav-spacer" aria-hidden="true" />
          <UiButton
            variant="gold"
            size="md"
            :disabled="!canGoNext"
            @click="goNext"
          >
            {{ isLastQuestion ? '診断結果を見る' : '次へ' }}
          </UiButton>
        </div>
      </section>

      <!-- 診断中 -->
      <section v-else-if="step === 'loading'" class="artist-match__panel artist-match__loading" aria-live="polite">
        <div class="artist-match__loading-note" aria-hidden="true">♪</div>
        <p class="artist-match__loading-text">あなたに響く歌声を探しています…</p>
      </section>

      <!-- 結果 -->
      <section
        v-else-if="step === 'result' && result?.artist"
        class="artist-match__panel artist-match__result"
        aria-labelledby="match-result-title"
      >
        <p class="artist-match__eyebrow">YOUR ARTIST</p>
        <h1 id="match-result-title" class="artist-match__title artist-match__title--result">
          あなたにおすすめのアーティストは…
        </h1>

        <div class="artist-match__result-card">
          <div class="artist-match__result-visual">
            <img
              v-if="result.artist.image"
              :src="result.artist.image"
              :alt="result.artist.name"
              class="artist-match__result-image"
            />
            <div v-else class="artist-match__result-placeholder" aria-hidden="true">♪</div>
            <span class="artist-match__best">BEST MATCH</span>
          </div>

          <div class="artist-match__result-body">
            <p class="artist-match__result-en">{{ result.artist.nameEn }}</p>
            <h2 class="artist-match__result-name">{{ result.artist.name }}</h2>
            <p class="artist-match__result-catch">{{ result.artist.resultCatchphrase }}</p>
            <p class="artist-match__result-reason">{{ result.artist.recommendationText }}</p>

            <div v-if="result.matchedLabels.length" class="artist-match__traits">
              <p class="artist-match__traits-label">一致した特徴</p>
              <ul class="artist-match__traits-list">
                <li v-for="label in result.matchedLabels" :key="label">{{ label }}</li>
              </ul>
            </div>

            <p v-if="result.artist.status === 'soon'" class="artist-match__soon-note">
              ファンクラブ準備中
            </p>

            <div class="artist-match__result-actions">
              <UiButton
                v-if="result.artist.status === 'open'"
                variant="gold"
                size="md"
                @click="onFanclub"
              >
                ファンクラブを見る
              </UiButton>
              <UiButton
                v-else
                variant="gold"
                size="md"
                @click="emit('open-encyclopedia')"
              >
                アーティスト図鑑で見る
              </UiButton>

              <UiButton variant="outline" size="md" @click="emit('open-encyclopedia')">
                アーティスト図鑑へ戻る
              </UiButton>

              <SnsUsageCard
                class="artist-match__usage artist-match__usage--result"
                :message="remainingMessage"
                :next-reset-label="nextResetLabel"
                :unlimited="isUnlimited"
              />

              <button
                type="button"
                class="artist-match__retry"
                :disabled="!canUse"
                @click="resetAll"
              >
                {{ canUse ? 'もう一度診断する' : '制限に達しました' }}
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- エラー -->
      <section v-else-if="step === 'error'" class="artist-match__panel artist-match__error" aria-labelledby="match-error-title">
        <h1 id="match-error-title" class="artist-match__title">診断結果を表示できませんでした</h1>
        <p class="artist-match__lead">アーティスト情報を確認して、もう一度お試しください。</p>
        <UiButton variant="gold" size="md" @click="resetAll">もう一度診断する</UiButton>
      </section>
    </main>

    <footer class="artist-match__footer" role="contentinfo">
      <p class="artist-match__copyright">© {{ SITE_NAME }}</p>
    </footer>
  </div>
</template>

<style scoped>
.artist-match {
  min-height: calc(100vh - 72px);
  display: flex;
  flex-direction: column;
  background:
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(122, 80, 136, 0.14), transparent 55%),
    linear-gradient(180deg, #1a1418 0%, #231b22 42%, #2a2228 100%);
  color: #f8f4ef;
}

.artist-match__main {
  flex: 1;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: clamp(32px, 6vw, 56px) 24px 64px;
  box-sizing: border-box;
}

.artist-match__usage {
  width: 100%;
  max-width: 420px;
  margin: 0 auto 20px;
  text-align: left;
}

.artist-match__usage--result {
  margin: 8px auto 4px;
}

.artist-match__retry:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.artist-match__panel {
  max-width: 760px;
  margin: 0 auto;
  padding: clamp(28px, 5vw, 40px) clamp(20px, 4vw, 36px);
  border: 1px solid rgba(201, 169, 97, 0.28);
  border-radius: var(--site-radius-lg);
  background: linear-gradient(135deg, rgba(122, 80, 136, 0.14), rgba(26, 20, 24, 0.5));
}

.artist-match__intro,
.artist-match__loading,
.artist-match__error {
  text-align: center;
}

.artist-match__eyebrow {
  margin: 0 0 14px;
  font-family: var(--ff-latin);
  font-size: var(--font-size-caption);
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: var(--kin-400);
}

.artist-match__title {
  margin: 0 0 16px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.55rem, 4vw, 2.2rem);
  font-weight: 600;
  letter-spacing: 0.06em;
  line-height: 1.45;
}

.artist-match__title--result {
  text-align: center;
  margin-bottom: 28px;
}

.artist-match__lead {
  margin: 0 auto 18px;
  max-width: 520px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-small);
  line-height: 1.9;
  color: rgba(248, 244, 239, 0.72);
}

.artist-match__meta {
  margin: 0 0 28px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  letter-spacing: 0.08em;
  color: rgba(201, 169, 97, 0.9);
}

.artist-match__progress-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 10px;
}

.artist-match__progress-label {
  margin: 0;
  font-family: var(--ff-latin);
  font-size: var(--font-size-caption);
  letter-spacing: 0.2em;
  color: var(--kin-400);
}

.artist-match__progress-pct {
  margin: 0;
  font-family: var(--ff-mono);
  font-size: var(--font-size-caption);
  color: rgba(248, 244, 239, 0.65);
}

.artist-match__progress-track {
  height: 6px;
  margin-bottom: 28px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.artist-match__progress-fill {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--kin-500), var(--kin-400));
  transition: width 0.3s ease;
}

.artist-match__q-text {
  margin: 0 0 24px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.25rem, 3vw, 1.6rem);
  letter-spacing: 0.06em;
  line-height: 1.55;
  text-align: center;
}

.artist-match__answers {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 28px;
}

.artist-match__answer {
  position: relative;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
  min-height: 88px;
  padding: 18px 16px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: var(--site-radius-md);
  background: rgba(122, 80, 136, 0.16);
  color: #f8f4ef;
  text-align: left;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s, color 0.2s;
}

.artist-match__answer:hover {
  border-color: rgba(201, 169, 97, 0.55);
  background: rgba(122, 80, 136, 0.28);
}

.artist-match__answer:focus-visible {
  outline: 2px solid rgba(201, 169, 97, 0.7);
  outline-offset: 2px;
}

.artist-match__answer--selected {
  border-color: rgba(201, 169, 97, 0.75);
  background: rgba(201, 169, 97, 0.16);
  color: #fffaf3;
}

.artist-match__answer-label {
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-small);
  line-height: 1.65;
  letter-spacing: 0.02em;
}

.artist-match__answer-check {
  flex-shrink: 0;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 1px solid rgba(201, 169, 97, 0.8);
  background: rgba(201, 169, 97, 0.25);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-caption);
  color: var(--kin-300, #e4c97a);
}

.artist-match__sr {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

.artist-match__nav-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.artist-match__nav-spacer {
  width: 1px;
  height: 1px;
}

.artist-match__nav-actions :deep(.ui-btn) {
  min-height: 44px;
  min-width: 120px;
}

.artist-match__nav-actions :deep(.ui-btn--outline) {
  border-color: rgba(201, 169, 97, 0.4);
  color: rgba(248, 244, 239, 0.85);
  background: transparent;
}

.artist-match__loading-note {
  margin: 0 auto 16px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 1px solid rgba(201, 169, 97, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-subtitle);
  color: var(--kin-400);
  animation: match-pulse 1.1s ease-in-out infinite;
}

.artist-match__loading-text {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 1.05rem;
  letter-spacing: 0.08em;
  color: rgba(248, 244, 239, 0.8);
}

@keyframes match-pulse {
  0%, 100% { opacity: 0.55; transform: scale(0.96); }
  50% { opacity: 1; transform: scale(1); }
}

.artist-match__result {
  max-width: 960px;
  animation: match-fade 0.45s ease;
}

@keyframes match-fade {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.artist-match__result-card {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
  gap: 28px;
  align-items: start;
}

.artist-match__result-visual {
  position: relative;
  overflow: hidden;
  border-radius: var(--site-radius-lg);
  border: 1px solid rgba(201, 169, 97, 0.28);
  aspect-ratio: 4 / 5;
  background: rgba(0, 0, 0, 0.25);
}

.artist-match__result-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
  display: block;
}

.artist-match__result-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: rgba(255, 255, 255, 0.2);
}

.artist-match__best {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 5px 10px;
  border-radius: 999px;
  border: 1px solid rgba(201, 169, 97, 0.7);
  background: rgba(26, 20, 24, 0.78);
  font-family: var(--ff-latin);
  font-size: var(--font-size-badge);
  letter-spacing: 0.16em;
  color: var(--kin-300, #e4c97a);
}

.artist-match__result-en {
  margin: 0 0 6px;
  font-family: var(--ff-latin);
  font-size: var(--font-size-caption);
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--kin-400);
}

.artist-match__result-name {
  margin: 0 0 12px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.6rem, 3vw, 2rem);
  letter-spacing: 0.06em;
}

.artist-match__result-catch {
  margin: 0 0 12px;
  font-family: var(--ff-mincho);
  font-size: 1.05rem;
  line-height: 1.7;
  letter-spacing: 0.04em;
  color: rgba(248, 244, 239, 0.92);
}

.artist-match__result-reason {
  margin: 0 0 20px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-small);
  line-height: 1.85;
  color: rgba(248, 244, 239, 0.7);
}

.artist-match__traits-label {
  margin: 0 0 10px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  letter-spacing: 0.12em;
  color: rgba(248, 244, 239, 0.55);
}

.artist-match__traits-list {
  list-style: none;
  margin: 0 0 20px;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.artist-match__traits-list li {
  padding: 5px 10px;
  border-radius: 999px;
  border: 1px solid rgba(201, 169, 97, 0.35);
  background: rgba(201, 169, 97, 0.1);
  font-size: var(--font-size-caption);
  color: rgba(248, 244, 239, 0.85);
}

.artist-match__soon-note {
  margin: 0 0 14px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  letter-spacing: 0.1em;
  color: rgba(201, 169, 97, 0.9);
}

.artist-match__result-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.artist-match__result-actions :deep(.ui-btn--outline) {
  border-color: rgba(201, 169, 97, 0.4);
  color: rgba(248, 244, 239, 0.85);
  background: transparent;
}

.artist-match__retry {
  border: 0;
  background: transparent;
  color: rgba(248, 244, 239, 0.65);
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-button);
  text-decoration: underline;
  text-underline-offset: 3px;
  cursor: pointer;
  padding: 8px 4px;
}

.artist-match__retry:hover {
  color: var(--kin-400);
}

.artist-match__footer {
  padding: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  text-align: center;
}

.artist-match__copyright {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  color: rgba(248, 244, 239, 0.4);
  letter-spacing: 0.08em;
}

@media (max-width: 900px) {
  .artist-match__result-card {
    grid-template-columns: 1fr;
  }

  .artist-match__result-visual {
    max-width: 420px;
    margin: 0 auto;
    width: 100%;
  }
}

@media (max-width: 640px) {
  .artist-match__main {
    padding: 28px 16px 48px;
  }

  .artist-match__panel {
    padding: 22px 16px;
  }

  .artist-match__answers {
    grid-template-columns: 1fr;
  }

  .artist-match__answer {
    min-height: 72px;
  }

  .artist-match__nav-actions {
    flex-direction: column-reverse;
    align-items: stretch;
  }

  .artist-match__nav-actions :deep(.ui-btn) {
    width: 100%;
  }

  .artist-match__result-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .artist-match__result-actions :deep(.ui-btn) {
    width: 100%;
  }

  .artist-match__retry {
    text-align: center;
  }
}
</style>
