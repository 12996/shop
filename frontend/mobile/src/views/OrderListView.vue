<template>
  <div class="page-shell">
    <main class="page">
      <header class="topbar">
        <div>
          <div class="brand">无人超市</div>
          <h1 class="page-title">我的订单</h1>
        </div>
      </header>

      <section v-if="!authStore.isAuthenticated" class="state-card">
        <p>请先登录后查看订单。</p>
        <RouterLink class="link-button" to="/login">去登录</RouterLink>
      </section>

      <template v-else>
        <section class="tabs">
          <button
            v-for="item in statusTabs"
            :key="item.value"
            class="tab"
            :class="{ active: activeStatus === item.value }"
            @click="activeStatus = item.value"
          >
            {{ item.label }}
          </button>
        </section>

        <section v-if="loading" class="state-card">加载中...</section>
        <section v-else-if="filteredOrders.length === 0" class="state-card">暂无订单</section>

        <section v-else class="order-list">
          <article v-for="order in filteredOrders" :key="order.id" class="order-card">
            <div class="order-header">
              <span>{{ order.order_number }}</span>
              <span class="status">{{ statusText(order.status) }}</span>
            </div>
            <div class="order-meta">金额：￥{{ order.total_amount }}</div>
            <div class="order-meta">时间：{{ formatTime(order.created_at) }}</div>
            <div class="order-meta">商品：{{ order.items.map((item) => item.product_name).join("、") }}</div>
            <div class="actions">
              <button
                v-if="order.status === 'pending_payment'"
                class="secondary-button"
                @click="retryPay(order.id)"
              >
                继续支付
              </button>
              <button
                v-if="order.status === 'pending_payment'"
                class="danger-button"
                @click="cancelCurrentOrder(order.id)"
              >
                取消订单
              </button>
            </div>
          </article>
        </section>
      </template>
    </main>

    <MobileTabBar />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

import { cancelOrder, fetchOrders, payOrder, type Order } from "../api/orders";
import MobileTabBar from "../components/MobileTabBar.vue";
import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();
const loading = ref(false);
const orders = ref<Order[]>([]);
const activeStatus = ref("all");

const statusTabs = [
  { label: "全部", value: "all" },
  { label: "待支付", value: "pending_payment" },
  { label: "已支付", value: "paid" },
  { label: "已完成", value: "completed" },
  { label: "已取消", value: "cancelled" },
];

const filteredOrders = computed(() =>
  activeStatus.value === "all"
    ? orders.value
    : orders.value.filter((order) => order.status === activeStatus.value),
);

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    return;
  }

  loading.value = true;
  try {
    orders.value = await fetchOrders();
  } finally {
    loading.value = false;
  }
});

async function retryPay(orderId: number) {
  await payOrder(orderId, "wechat");
  orders.value = await fetchOrders();
}

async function cancelCurrentOrder(orderId: number) {
  await cancelOrder(orderId);
  orders.value = await fetchOrders();
}

function statusText(status: string) {
  const map: Record<string, string> = {
    pending_payment: "待支付",
    paid: "已支付",
    completed: "已完成",
    cancelled: "已取消",
  };
  return map[status] ?? status;
}

function formatTime(value: string) {
  return new Date(value).toLocaleString("zh-CN");
}
</script>

<style scoped>
.page-shell {
  min-height: 100vh;
  background: #f8fafc;
}

.page {
  padding: 20px 16px 88px;
  box-sizing: border-box;
  font-family: sans-serif;
}

.topbar {
  margin-bottom: 16px;
}

.brand {
  font-size: 13px;
  color: #2563eb;
  font-weight: 600;
}

.page-title {
  margin: 8px 0 0;
  font-size: 26px;
  color: #111827;
}

.tabs {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  margin-bottom: 16px;
}

.tab {
  min-height: 36px;
  padding: 0 14px;
  border: none;
  border-radius: 999px;
  background: #e5e7eb;
  color: #4b5563;
}

.tab.active {
  background: #2563eb;
  color: #fff;
}

.state-card,
.order-card {
  padding: 16px;
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  color: #111827;
  font-weight: 600;
}

.status {
  color: #2563eb;
}

.order-meta {
  margin-top: 8px;
  color: #6b7280;
  font-size: 14px;
}

.actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.secondary-button,
.danger-button,
.link-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 36px;
  padding: 0 14px;
  border: none;
  border-radius: 10px;
  text-decoration: none;
}

.secondary-button {
  background: #2563eb;
  color: #fff;
}

.danger-button {
  background: #fee2e2;
  color: #b91c1c;
}

.link-button {
  background: #e5e7eb;
  color: #111827;
}
</style>
