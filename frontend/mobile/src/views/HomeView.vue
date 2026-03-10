<template>
  <div class="page">
    <section class="search-box">
      <input v-model.trim="keyword" type="text" placeholder="搜索商品或分类" @keyup.enter="goToProducts" />
    </section>

    <section class="notice-card">
      <div class="section-header">
        <span>公告</span>
        <RouterLink to="/orders">我的订单</RouterLink>
      </div>
      <p v-if="announcement">{{ announcement.content }}</p>
      <p v-else>暂无公告</p>
    </section>

    <section class="recommend-section">
      <div class="section-header">
        <span>推荐商品</span>
        <RouterLink to="/products">查看全部</RouterLink>
      </div>

      <div v-if="loading" class="state-card">加载中...</div>
      <div v-else-if="recommendations.length === 0" class="state-card">暂无推荐商品</div>

      <div v-else class="carousel-wrap">
        <button class="nav-btn" type="button" @click="prevSlide">&lt;</button>
        <div class="carousel-window">
          <div class="carousel-track" :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
            <article v-for="item in recommendations" :key="item.id" class="product-card">
              <div class="product-image">{{ item.product_image || item.product_name.slice(0, 2) }}</div>
              <div class="product-name">{{ item.product_name }}</div>
              <div class="product-price">￥{{ item.product_price }}</div>
              <button class="add-button" @click="handleAddToCart(item.product, $event)">加入购物车</button>
            </article>
          </div>
        </div>
        <button class="nav-btn" type="button" @click="nextSlide">&gt;</button>
      </div>

      <div v-if="recommendations.length > 1" class="dots">
        <button
          v-for="(_, index) in recommendations"
          :key="index"
          class="dot"
          :class="{ active: index === currentSlide }"
          type="button"
          @click="goSlide(index)"
        />
      </div>
    </section>

    <HomeProductSection />

    <div
      v-if="feedbackMessage"
      class="feedback-bubble"
      :class="feedbackType"
      :style="{ left: `${feedbackX}px`, top: `${feedbackY}px` }"
    >
      {{ feedbackMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import { RouterLink, useRouter } from "vue-router";

import HomeProductSection from "../components/HomeProductSection.vue";
import { fetchHomeData, type Announcement, type Recommendation } from "../api/home";
import { useAuthStore } from "../stores/auth";
import { useCartStore } from "../stores/cart";

const router = useRouter();
const authStore = useAuthStore();
const cartStore = useCartStore();

const loading = ref(false);
const keyword = ref("");
const announcement = ref<Announcement | null>(null);
const recommendations = ref<Recommendation[]>([]);
const currentSlide = ref(0);
const feedbackMessage = ref("");
const feedbackType = ref<"success" | "error">("success");
const feedbackX = ref(0);
const feedbackY = ref(0);

let timer: ReturnType<typeof setInterval> | null = null;
let feedbackTimer: ReturnType<typeof setTimeout> | null = null;
type FeedbackAnchor = { x: number; y: number };

onMounted(async () => {
  loading.value = true;
  try {
    const homePayload = await fetchHomeData();
    announcement.value = homePayload.announcement;
    recommendations.value = homePayload.recommendations;
    startAutoPlay();
  } finally {
    loading.value = false;
  }
});

onBeforeUnmount(() => {
  stopAutoPlay();
  if (feedbackTimer) {
    clearTimeout(feedbackTimer);
    feedbackTimer = null;
  }
});

function startAutoPlay() {
  stopAutoPlay();
  if (recommendations.value.length <= 1) {
    return;
  }
  timer = setInterval(() => {
    nextSlide();
  }, 3000);
}

function stopAutoPlay() {
  if (!timer) {
    return;
  }
  clearInterval(timer);
  timer = null;
}

function goSlide(index: number) {
  currentSlide.value = index;
}

function prevSlide() {
  const total = recommendations.value.length;
  if (!total) {
    return;
  }
  currentSlide.value = (currentSlide.value - 1 + total) % total;
}

function nextSlide() {
  const total = recommendations.value.length;
  if (!total) {
    return;
  }
  currentSlide.value = (currentSlide.value + 1) % total;
}

async function goToProducts() {
  await router.push({
    path: "/products",
    query: {
      ...(keyword.value ? { keyword: keyword.value } : {}),
    },
  });
}

async function handleAddToCart(productId: number, event: MouseEvent) {
  const anchor = resolveFeedbackAnchor(event);
  if (!authStore.isAuthenticated) {
    showFeedback("请先登录", "error", anchor);
    await router.push("/login");
    return;
  }
  try {
    await cartStore.addItem(productId, 1);
    showFeedback("已加入购物车", "success", anchor);
  } catch {
    showFeedback("加入购物车失败", "error", anchor);
  }
}

function resolveFeedbackAnchor(event?: MouseEvent): FeedbackAnchor {
  if (event?.currentTarget instanceof HTMLElement) {
    const rect = event.currentTarget.getBoundingClientRect();
    return {
      x: rect.left + rect.width / 2,
      y: Math.max(rect.top - 12, 64),
    };
  }
  return { x: window.innerWidth / 2, y: Math.max(window.innerHeight * 0.72, 120) };
}

function showFeedback(message: string, type: "success" | "error", anchor?: FeedbackAnchor) {
  feedbackMessage.value = message;
  feedbackType.value = type;
  const target = anchor ?? resolveFeedbackAnchor();
  feedbackX.value = target.x;
  feedbackY.value = target.y;

  if (feedbackTimer) {
    clearTimeout(feedbackTimer);
  }
  feedbackTimer = setTimeout(() => {
    feedbackMessage.value = "";
    feedbackTimer = null;
  }, 1200);
}
</script>

<style scoped>
.page {
  padding: 0 0 88px;
  box-sizing: border-box;
  font-family: sans-serif;
}

.search-box input {
  width: 100%;
  min-height: 44px;
  border: 1px solid #d1d5db;
  border-radius: 14px;
  padding: 0 14px;
  box-sizing: border-box;
}

.notice-card,
.recommend-section {
  margin-top: 16px;
  padding: 16px;
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  color: #111827;
  font-weight: 600;
}

.section-header a {
  color: #2563eb;
  text-decoration: none;
  font-size: 14px;
}

.notice-card p {
  margin: 0;
  color: #4b5563;
  line-height: 1.5;
}

.state-card {
  padding: 12px;
  border-radius: 14px;
  background: #f8fafc;
}

.carousel-wrap {
  display: grid;
  grid-template-columns: 32px 1fr 32px;
  gap: 8px;
  align-items: center;
}

.carousel-window {
  overflow: hidden;
}

.carousel-track {
  display: flex;
  transition: transform 0.35s ease;
}

.product-card {
  width: 100%;
  flex: 0 0 100%;
  padding: 12px;
  border-radius: 14px;
  background: #f8fafc;
  box-sizing: border-box;
}

.product-image {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 120px;
  border-radius: 12px;
  background: #dbeafe;
  color: #1d4ed8;
  font-weight: 600;
  text-align: center;
}

.product-name {
  margin-top: 10px;
  color: #111827;
  font-size: 14px;
}

.product-price {
  margin-top: 6px;
  color: #dc2626;
  font-weight: 600;
}

.add-button {
  width: 100%;
  min-height: 38px;
  margin-top: 10px;
  border: none;
  border-radius: 10px;
  background: #2563eb;
  color: #fff;
}

.nav-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 999px;
  background: #e2e8f0;
  color: #334155;
}

.dots {
  margin-top: 10px;
  display: flex;
  justify-content: center;
  gap: 8px;
}

.dot {
  width: 8px;
  height: 8px;
  border: none;
  border-radius: 999px;
  background: #cbd5e1;
}

.dot.active {
  background: #2563eb;
}

.feedback-bubble {
  position: fixed;
  transform: translate(-50%, -100%);
  padding: 6px 10px;
  border-radius: 999px;
  color: #fff;
  font-size: 12px;
  z-index: 40;
  pointer-events: none;
  animation: bubble-up 1.2s ease forwards;
}

.feedback-bubble.success {
  background: rgba(15, 23, 42, 0.88);
}

.feedback-bubble.error {
  background: rgba(220, 38, 38, 0.92);
}

@keyframes bubble-up {
  0% {
    opacity: 0;
    transform: translate(-50%, -90%);
  }
  20% {
    opacity: 1;
    transform: translate(-50%, -100%);
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -125%);
  }
}
</style>
