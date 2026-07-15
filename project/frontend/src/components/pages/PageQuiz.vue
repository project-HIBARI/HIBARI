<script setup>
import { computed, ref, onMounted } from 'vue'
import UiButton from '../ui/UiButton.vue'
import UiIco from '../ui/UiIco.vue'
import { getQuizzes, submitAnswer, getRanking, submitScore } from '../../api/quiz.js'
import { SITE_NAME } from '../../constants/site.js'

const gameState = ref('start')
const playerName = ref('')
const quizzes = ref([])
const currentIdx = ref(0)
const totalScore = ref(0)
const hasAnswered = ref(false)
const selectedAnswer = ref(null)
const correctAnswer = ref(null)
const explanation = ref('')
const isCorrect = ref(false)
const ranking = ref([])
const playerRank = ref(null)

const totalQuestions = computed(() => quizzes.value.length)
const progressPercent = computed(() => {
  if (!totalQuestions.value) return 0
  return Math.round(((currentIdx.value + 1) / totalQuestions.value) * 100)
})
const answerKeys = ['A', 'B', 'C', 'D']

onMounted(async () => {
  await fetchRanking()
})

async function fetchRanking() {
  try {
    ranking.value = await getRanking()
  } catch (err) {
    console.error('ランキング取得失敗:', err)
  }
}

async function startQuiz() {
  try {
    const data = await getQuizzes()
    if (!Array.isArray(data) || data.length === 0) {
      alert('クイズデータがありません')
      return
    }
    quizzes.value = data
    currentIdx.value = 0
    totalScore.value = 0
    hasAnswered.value = false
    selectedAnswer.value = null
    correctAnswer.value = null
    gameState.value = 'playing'
  } catch (err) {
    alert(err.message || 'クイズの読み込みに失敗しました')
  }
}

async function selectAnswer(key) {
  if (hasAnswered.value) return

  try {
    const result = await submitAnswer(quizzes.value[currentIdx.value].quiz_id, key)
    isCorrect.value = result.is_correct
    correctAnswer.value = result.correct_answer
    explanation.value = result.explanation

    if (isCorrect.value) totalScore.value += 100
    hasAnswered.value = true
    selectedAnswer.value = key
  } catch (err) {
    console.error('判定エラー:', err)
  }
}

function optionClass(key) {
  if (!hasAnswered.value) return {}
  const isSelected = selectedAnswer.value === key
  const isRight = correctAnswer.value === key
  return {
    'legend-quiz__option--selected': isSelected && isCorrect.value,
    'legend-quiz__option--wrong': isSelected && !isCorrect.value,
    'legend-quiz__option--correct': !isSelected && isRight,
  }
}

function next() {
  if (currentIdx.value < quizzes.value.length - 1) {
    currentIdx.value++
    hasAnswered.value = false
    selectedAnswer.value = null
    correctAnswer.value = null
  } else {
    finish()
  }
}

async function finish() {
  await submitScore(playerName.value || '名無しさん', totalScore.value)
  await fetchRanking()

  const nameToFind = playerName.value || '名無しさん'
  const myRecord = [...ranking.value]
    .reverse()
    .find((r) => r.name === nameToFind && r.score === totalScore.value)

  playerRank.value = myRecord ? myRecord.rank : null
  gameState.value = 'result'
}

function backToStart() {
  playerName.value = ''
  playerRank.value = null
  gameState.value = 'start'
}

function retryQuiz() {
  playerRank.value = null
  startQuiz()
}
</script>

<template>
  <div class="legend-quiz">
    <main id="main-content" class="legend-quiz__main">
      <!-- スタート画面 -->
      <section
        v-if="gameState === 'start'"
        class="legend-quiz__panel legend-quiz__intro"
        aria-labelledby="quiz-intro-title"
      >
        <p class="legend-quiz__eyebrow">LEGEND QUIZ</p>
        <h1 id="quiz-intro-title" class="legend-quiz__title">レジェンドアーティストクイズ</h1>
        <p class="legend-quiz__lead">
          昭和の歌謡界を彩ったレジェンドたちのエピソードに挑戦。<br />
          正解するたびに100点加算。ハイスコアを目指して検定に挑もう。
        </p>
        <p class="legend-quiz__meta">全10問・1問正解で100点</p>

        <label class="legend-quiz__name-label" for="quiz-player-name">プレイヤー名</label>
        <input
          id="quiz-player-name"
          v-model="playerName"
          type="text"
          maxlength="15"
          placeholder="お名前（空欄は匿名）"
          class="legend-quiz__name-input"
        />

        <UiButton variant="gold" size="lg" @click="startQuiz">
          クイズを開始する
        </UiButton>

        <div v-if="ranking.length" class="legend-quiz__ranking">
          <div class="legend-quiz__ranking-head">
            <UiIco name="crown" :size="16" color="var(--kin-400)" />
            <h2 class="legend-quiz__ranking-title">ランキング TOP10</h2>
          </div>
          <ol class="legend-quiz__ranking-list">
            <li
              v-for="(r, i) in ranking"
              :key="i"
              class="legend-quiz__ranking-item"
              :class="{ 'legend-quiz__ranking-item--top': r.rank <= 3 }"
            >
              <span class="legend-quiz__ranking-rank">{{ r.rank }}</span>
              <span class="legend-quiz__ranking-name">{{ r.name }}</span>
              <span class="legend-quiz__ranking-score">{{ r.score }}点</span>
            </li>
          </ol>
        </div>
      </section>

      <!-- プレイ画面 -->
      <section
        v-else-if="gameState === 'playing' && quizzes.length > 0"
        class="legend-quiz__panel legend-quiz__playing"
        :aria-labelledby="'quiz-q-' + currentIdx"
      >
        <div class="legend-quiz__progress-head">
          <p class="legend-quiz__progress-label">
            QUESTION {{ currentIdx + 1 }} / {{ totalQuestions }}
          </p>
          <p class="legend-quiz__progress-pct">{{ progressPercent }}%</p>
        </div>
        <div
          class="legend-quiz__progress-track"
          role="progressbar"
          :aria-valuenow="progressPercent"
          aria-valuemin="0"
          aria-valuemax="100"
          :aria-label="'進捗 ' + progressPercent + '%'"
        >
          <span class="legend-quiz__progress-fill" :style="{ width: progressPercent + '%' }" />
        </div>

        <p class="legend-quiz__score-chip">
          <UiIco name="spark" :size="14" color="var(--kin-400)" />
          現在のスコア {{ totalScore }} 点
        </p>

        <h2 :id="'quiz-q-' + currentIdx" class="legend-quiz__question">
          {{ quizzes[currentIdx].question }}
        </h2>

        <div class="legend-quiz__options" role="group" :aria-label="quizzes[currentIdx].question">
          <button
            v-for="key in answerKeys"
            :key="key"
            type="button"
            class="legend-quiz__option"
            :class="optionClass(key)"
            :disabled="hasAnswered"
            @click="selectAnswer(key)"
          >
            <span class="legend-quiz__option-key">{{ key }}</span>
            <span class="legend-quiz__option-text">
              {{ quizzes[currentIdx]['option_' + key.toLowerCase()] }}
            </span>
          </button>
        </div>

        <div
          v-if="hasAnswered"
          class="legend-quiz__feedback"
          :class="isCorrect ? 'legend-quiz__feedback--correct' : 'legend-quiz__feedback--wrong'"
        >
          <p class="legend-quiz__feedback-label">
            {{ isCorrect ? '正解！' : '残念…' }}
          </p>
          <p class="legend-quiz__feedback-text">{{ explanation }}</p>
          <UiButton variant="gold" size="md" @click="next">
            {{ currentIdx < quizzes.length - 1 ? '次の問題へ' : '結果を見る' }}
          </UiButton>
        </div>
      </section>

      <!-- 結果画面 -->
      <section
        v-else-if="gameState === 'result'"
        class="legend-quiz__panel legend-quiz__result"
        aria-labelledby="quiz-result-title"
      >
        <p class="legend-quiz__eyebrow">QUIZ COMPLETE</p>
        <h1 id="quiz-result-title" class="legend-quiz__title">検定終了</h1>

        <div class="legend-quiz__result-card">
          <p class="legend-quiz__result-score">{{ totalScore }}</p>
          <p class="legend-quiz__result-score-label">最終スコア</p>
          <p v-if="playerRank" class="legend-quiz__result-rank">
            あなたの記録は全体の <strong>{{ playerRank }} 位</strong> にランクインしました
          </p>
        </div>

        <div class="legend-quiz__result-actions">
          <UiButton variant="gold" size="md" @click="retryQuiz">もう一度挑戦</UiButton>
          <UiButton variant="outline" size="md" @click="backToStart">クイズTOPに戻る</UiButton>
        </div>
      </section>
    </main>

    <footer class="legend-quiz__footer" role="contentinfo">
      <p class="legend-quiz__copyright">© {{ SITE_NAME }}</p>
    </footer>
  </div>
</template>

<style scoped>
.legend-quiz {
  min-height: calc(100vh - 72px);
  display: flex;
  flex-direction: column;
  background:
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(122, 80, 136, 0.14), transparent 55%),
    linear-gradient(180deg, #1a1418 0%, #231b22 42%, #2a2228 100%);
  color: #f8f4ef;
}

.legend-quiz__main {
  flex: 1;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: clamp(32px, 6vw, 56px) 24px 64px;
  box-sizing: border-box;
}

.legend-quiz__panel {
  max-width: 760px;
  margin: 0 auto;
  padding: clamp(28px, 5vw, 40px) clamp(20px, 4vw, 36px);
  border: 1px solid rgba(201, 169, 97, 0.28);
  border-radius: var(--site-radius-lg);
  background: linear-gradient(135deg, rgba(122, 80, 136, 0.14), rgba(26, 20, 24, 0.5));
}

.legend-quiz__intro,
.legend-quiz__result {
  text-align: center;
}

.legend-quiz__eyebrow {
  margin: 0 0 14px;
  font-family: var(--ff-latin);
  font-size: var(--font-size-caption);
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: var(--kin-400);
}

.legend-quiz__title {
  margin: 0 0 16px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.55rem, 4vw, 2.2rem);
  font-weight: 600;
  letter-spacing: 0.06em;
  line-height: 1.45;
}

.legend-quiz__lead {
  margin: 0 auto 18px;
  max-width: 520px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-small);
  line-height: 1.9;
  color: rgba(248, 244, 239, 0.72);
}

.legend-quiz__meta {
  margin: 0 0 28px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  letter-spacing: 0.08em;
  color: rgba(201, 169, 97, 0.9);
}

.legend-quiz__name-label {
  display: block;
  margin: 0 0 8px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  letter-spacing: 0.08em;
  color: rgba(248, 244, 239, 0.65);
  text-align: left;
}

.legend-quiz__name-input {
  width: 100%;
  margin-bottom: 24px;
  padding: 14px 16px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: var(--site-radius-md);
  background: rgba(122, 80, 136, 0.16);
  color: #f8f4ef;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-small);
  box-sizing: border-box;
  transition: border-color 0.2s, background 0.2s;
}

.legend-quiz__name-input::placeholder {
  color: rgba(248, 244, 239, 0.4);
}

.legend-quiz__name-input:focus {
  outline: none;
  border-color: rgba(201, 169, 97, 0.55);
  background: rgba(122, 80, 136, 0.28);
}

.legend-quiz__ranking {
  margin-top: 36px;
  padding-top: 28px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: left;
}

.legend-quiz__ranking-head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.legend-quiz__ranking-title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 1.05rem;
  letter-spacing: 0.06em;
  color: var(--kin-400);
}

.legend-quiz__ranking-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.legend-quiz__ranking-item {
  display: grid;
  grid-template-columns: 36px 1fr auto;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--site-radius-md);
  background: rgba(0, 0, 0, 0.18);
}

.legend-quiz__ranking-item--top {
  border-color: rgba(201, 169, 97, 0.35);
  background: rgba(201, 169, 97, 0.08);
}

.legend-quiz__ranking-rank {
  font-family: var(--ff-mono);
  font-size: var(--font-size-button);
  color: var(--kin-400);
  text-align: center;
}

.legend-quiz__ranking-name {
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-small);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.legend-quiz__ranking-score {
  font-family: var(--ff-mono);
  font-size: var(--font-size-button);
  color: rgba(248, 244, 239, 0.75);
}

.legend-quiz__progress-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 10px;
}

.legend-quiz__progress-label {
  margin: 0;
  font-family: var(--ff-latin);
  font-size: var(--font-size-caption);
  letter-spacing: 0.2em;
  color: var(--kin-400);
}

.legend-quiz__progress-pct {
  margin: 0;
  font-family: var(--ff-mono);
  font-size: var(--font-size-caption);
  color: rgba(248, 244, 239, 0.65);
}

.legend-quiz__progress-track {
  height: 6px;
  margin-bottom: 20px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.legend-quiz__progress-fill {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--kin-500), var(--kin-400));
  transition: width 0.3s ease;
}

.legend-quiz__score-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin: 0 0 20px;
  padding: 6px 12px;
  border: 1px solid rgba(201, 169, 97, 0.35);
  border-radius: 999px;
  background: rgba(201, 169, 97, 0.1);
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  letter-spacing: 0.06em;
  color: var(--kin-400);
}

.legend-quiz__question {
  margin: 0 0 24px;
  font-family: var(--ff-mincho);
  font-size: clamp(1.25rem, 3vw, 1.6rem);
  letter-spacing: 0.06em;
  line-height: 1.55;
  text-align: center;
}

.legend-quiz__options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 24px;
}

.legend-quiz__option {
  display: flex;
  align-items: flex-start;
  gap: 12px;
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

.legend-quiz__option:hover:not(:disabled) {
  border-color: rgba(201, 169, 97, 0.55);
  background: rgba(122, 80, 136, 0.28);
}

.legend-quiz__option:disabled {
  cursor: default;
}

.legend-quiz__option--selected {
  border-color: rgba(201, 169, 97, 0.75);
  background: rgba(201, 169, 97, 0.16);
}

.legend-quiz__option--wrong {
  border-color: rgba(200, 90, 90, 0.7);
  background: rgba(200, 90, 90, 0.12);
}

.legend-quiz__option--correct {
  border-color: rgba(120, 190, 120, 0.7);
  background: rgba(120, 190, 120, 0.12);
}

.legend-quiz__option-key {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 1px solid rgba(201, 169, 97, 0.5);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--ff-latin);
  font-size: var(--font-size-caption);
  font-weight: 600;
  color: var(--kin-400);
}

.legend-quiz__option-text {
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-small);
  line-height: 1.65;
  letter-spacing: 0.02em;
}

.legend-quiz__feedback {
  padding: 20px;
  border-radius: var(--site-radius-md);
  text-align: center;
}

.legend-quiz__feedback--correct {
  border: 1px solid rgba(201, 169, 97, 0.45);
  background: rgba(201, 169, 97, 0.1);
}

.legend-quiz__feedback--wrong {
  border: 1px solid rgba(200, 90, 90, 0.35);
  background: rgba(200, 90, 90, 0.08);
}

.legend-quiz__feedback-label {
  margin: 0 0 10px;
  font-family: var(--ff-mincho);
  font-size: 1.15rem;
  letter-spacing: 0.08em;
  color: var(--kin-400);
}

.legend-quiz__feedback--wrong .legend-quiz__feedback-label {
  color: rgba(230, 160, 160, 0.95);
}

.legend-quiz__feedback-text {
  margin: 0 0 18px;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-small);
  line-height: 1.8;
  color: rgba(248, 244, 239, 0.8);
  text-align: left;
}

.legend-quiz__result-card {
  margin: 0 auto 28px;
  max-width: 360px;
  padding: 28px 24px;
  border: 1px solid rgba(201, 169, 97, 0.35);
  border-radius: var(--site-radius-lg);
  background: rgba(0, 0, 0, 0.2);
}

.legend-quiz__result-score {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: clamp(2.8rem, 10vw, 4rem);
  line-height: 1;
  color: var(--kin-400);
}

.legend-quiz__result-score-label {
  margin: 8px 0 0;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-button);
  letter-spacing: 0.12em;
  color: rgba(248, 244, 239, 0.65);
}

.legend-quiz__result-rank {
  margin: 18px 0 0;
  padding-top: 18px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-small);
  line-height: 1.7;
  color: rgba(248, 244, 239, 0.8);
}

.legend-quiz__result-rank strong {
  color: var(--kin-400);
}

.legend-quiz__result-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
}

.legend-quiz__result-actions :deep(.ui-btn--outline) {
  border-color: rgba(201, 169, 97, 0.4);
  color: rgba(248, 244, 239, 0.85);
  background: transparent;
}

.legend-quiz__footer {
  padding: 24px;
  text-align: center;
}

.legend-quiz__copyright {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  letter-spacing: 0.08em;
  color: rgba(248, 244, 239, 0.35);
}

@media (max-width: 600px) {
  .legend-quiz__options {
    grid-template-columns: 1fr;
  }
}
</style>
