<script setup>
/**
 * 部品名: 思い出 — 投稿フォーム（サイド）
 */
import UiButton from '../../ui/UiButton.vue'
import MemberGate from '../../common/MemberGate.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'
import { useMemberAccess } from '../../../composables/useMemberAccess.js'

const songs = HIBARU_DATA.discography.map((d) => d.title)

const props = defineProps({
  submitted: { type: Boolean, default: false },
  postData: { type: Object, required: true },
  errors: { type: Object, default: () => ({}) },
})

const emit = defineEmits(['update:postData', 'submit', 'reset', 'need-auth'])

const { canUse, PERMISSION } = useMemberAccess()
const canPost = () => canUse(PERMISSION.BOARD_POST)

function patch(partial) {
  emit('update:postData', { ...props.postData, ...partial })
}

function onSubmit() {
  if (!canPost()) {
    emit('need-auth', 'login')
    return
  }
  emit('submit')
}
</script>

<template>
  <aside class="mem-post">
    <div class="mem-post__card">
      <MemberGate
        v-if="!canPost()"
        :permission="PERMISSION.BOARD_POST"
        feature="掲示板投稿"
        @login="emit('need-auth', 'login')"
        @register="emit('need-auth', 'register')"
        @upgrade="emit('need-auth', 'register-premium')"
      />
      <template v-else>
        <div v-if="submitted" class="mem-post__done">
          <div class="mem-post__done-icon">✦</div>
          <div class="mem-post__done-title">投稿ありがとうございます</div>
          <p class="mem-post__done-text">会員の皆さまの思い出が、ひばりの記憶を紡いでいます。</p>
          <UiButton variant="outline" size="md" class="mem-post__full" @click="emit('reset')">続けて投稿</UiButton>
        </div>
        <template v-else>
          <h2 class="mem-post__heading">思い出を寄せる</h2>
          <p class="mem-post__member-note">会員限定 · 掲示板投稿</p>
          <div class="mem-post__fields">
            <input
              :value="postData.name"
              class="mem-post__input"
              placeholder="お名前（匿名可）"
              aria-label="お名前"
              @input="patch({ name: $event.target.value })"
            />
            <input
              :value="postData.pref"
              class="mem-post__input"
              placeholder="都道府県"
              aria-label="都道府県"
              @input="patch({ pref: $event.target.value })"
            />
            <div>
              <input
                :value="postData.title"
                class="mem-post__input"
                :class="{ 'mem-post__input--error': errors.title }"
                placeholder="思い出の題 *"
                aria-label="タイトル"
                aria-required="true"
                @input="patch({ title: $event.target.value })"
              />
              <div v-if="errors.title" class="mem-post__error" role="alert">{{ errors.title }}</div>
            </div>
            <div>
              <textarea
                :value="postData.body"
                rows="5"
                class="mem-post__input mem-post__textarea"
                :class="{ 'mem-post__input--error': errors.body }"
                placeholder="本文 *"
                aria-label="本文"
                aria-required="true"
                @input="patch({ body: $event.target.value })"
              />
              <div v-if="errors.body" class="mem-post__error" role="alert">{{ errors.body }}</div>
            </div>
            <select
              :value="postData.song"
              class="mem-post__input"
              aria-label="心に残る一曲"
              @change="patch({ song: $event.target.value })"
            >
              <option value="">心に残る一曲を選ぶ</option>
              <option v-for="s in songs" :key="s" :value="s">{{ s }}</option>
            </select>
            <button type="button" class="mem-post__attach" aria-label="写真を添付（任意）">
              📷 写真を添付（任意）
            </button>
            <UiButton variant="primary" size="md" class="mem-post__full" @click="onSubmit">投稿する</UiButton>
          </div>
        </template>
      </template>
    </div>
  </aside>
</template>

<style scoped>
.mem-post__card {
  position: sticky;
  top: 120px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  padding: var(--sp-5);
  background: linear-gradient(135deg, var(--site-bg-pink) 0%, var(--site-surface) 100%);
  box-shadow: var(--site-shadow);
}
.mem-post__heading {
  font-family: var(--ff-mincho);
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 4px;
  color: var(--murasaki-700);
}
.mem-post__member-note {
  margin: 0 0 var(--sp-4);
  font-size: 11px;
  color: var(--site-text-muted);
}
.mem-post__fields {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.mem-post__input {
  width: 100%;
  background: var(--site-surface);
  border: 1px solid var(--site-border-strong);
  color: var(--site-text);
  padding: 10px 12px;
  font-family: var(--ff-serif);
  font-size: 13px;
  border-radius: var(--site-radius-sm);
  outline: none;
}
.mem-post__input:focus {
  border-color: var(--murasaki-400);
}
.mem-post__input--error {
  border-color: var(--beni-500);
}
.mem-post__textarea {
  resize: vertical;
}
.mem-post__error {
  font-size: 11px;
  color: var(--beni-600);
  margin-top: 3px;
}
.mem-post__attach {
  background: var(--site-surface-muted);
  border: 1px dashed var(--site-border-strong);
  color: var(--site-text-muted);
  padding: 10px 12px;
  cursor: pointer;
  text-align: left;
  font-size: 13px;
  border-radius: var(--site-radius-sm);
}
.mem-post__full {
  width: 100%;
  justify-content: center;
}
.mem-post__done {
  text-align: center;
  padding: var(--sp-4) 0;
}
.mem-post__done-icon {
  font-size: 36px;
  margin-bottom: 12px;
  color: var(--kin-600);
}
.mem-post__done-title {
  font-family: var(--ff-mincho);
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 12px;
  color: var(--site-text);
}
.mem-post__done-text {
  font-size: 13px;
  color: var(--site-text-muted);
  line-height: 1.8;
  margin: 0 0 var(--sp-4);
}

@media (max-width: 767px) {
  .mem-post__card {
    position: static;
  }
}
</style>
