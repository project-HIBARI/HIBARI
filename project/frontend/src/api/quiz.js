// client.js から apiRequest 関数を読み込む
import { apiRequest } from './client.js' 

// 各関数で apiRequest を呼び出すように変更
export const getQuizzes = () => {
  return apiRequest('/api/quizzes')
}

export const submitAnswer = (quizId, userAnswer) => {
  return apiRequest('/api/quizzes/answer', {
    method: 'POST',
    body: JSON.stringify({ quiz_id: quizId, user_answer: userAnswer })
  })
}

export const getRanking = () => {
  return apiRequest('/api/quizzes/ranking')
}

export const submitScore = (name, score) => {
  return apiRequest('/api/quizzes/ranking', {
    method: 'POST',
    body: JSON.stringify({ name: name, score: score })
  })
}