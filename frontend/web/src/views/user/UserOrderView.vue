<template>
  <section class="page-card">
    <div class="page-header">
      <div>
        <h2>我的订单</h2>
        <p>支持状态筛选、继续支付、取消订单和查看详情。</p>
      </div>
    </div>

    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

    <section class="tabs">
      <button
        v-for="tab in statusTabs"
        :key="tab.value"
        class="ghost-button"
        :class="{ active: activeStatus === tab.value }"
        @click="activeStatus = tab.value"
      >
        {{ tab.label }}
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
        <div class="meta-text">金额：￥{{ order.total_amount }}</div>
        <div class="meta-text">时间：{{ formatTime(order.created_at) }}</div>
        <div class="meta-text">商品：{{ order.items.map((item) => item.product_name).join("、") }}</div>
        <div class="action-row">
          <button
            v-if="order.status === 'pending_payment'"
            class="primary-button"
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
          <button class="ghost-button" @click="loadOrderDetail(order.id)">查看详情</button>
        </div>
      </article>
    </section>

    <section v-if="currentOrder" class="detail-card">
      <h3>订单详情</h3>
      <div class="meta-text">订单号：{{ currentOrder.order_number }}</div>
      <div class="meta-text">状态：{{ statusText(currentOrder.status) }}</div>
      <div class="meta-text">
        地址：{{ currentOrder.address_snapshot ? JSON.stringify(currentOrder.address_snapshot) : "店内自助购物，无收货地址" }}
      </div>
      <div v-for="item in currentOrder.items" :key="item.id" class="detail-row">
        <span>{{ item.product_name }}</span>
        <span>x{{ item.quantity }}</span>
        <span>￥{{ item.subtotal }}</span>
      </div>
    </section>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import { cancelOrder, fetchOrderDetail, fetchOrders, payOrder, type Order } from "../../api/orders";

const loading = ref(false);
const errorMessage = ref("");
const orders = ref<Order[]>([]);
const currentOrder = ref<Order | null>(null);
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
  await loadOrders();
});

async function loadOrders() {
  loading.value = true;
  errorMessage.value = "";
  try {
    orders.value = await fetchOrders();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载失败";
  } finally {
    loading.value = false;
  }
}

async function retryPay(orderId: number) {
  try {
    await payOrder(orderId, "wechat");
    await loadOrders();
    await loadOrderDetail(orderId);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "支付失败";
  }
}

async function cancelCurrentOrder(orderId: number) {
  try {
    await cancelOrder(orderId);
    await loadOrders();
    await loadOrderDetail(orderId);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "取消失败";
  }
}

async function loadOrderDetail(orderId: number) {
  try {
    currentOrder.value = await fetchOrderDetail(orderId);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载详情失败";
  }
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
.page-card,
.state-card,
.order-card,
.detail-card {
  padding: 24px;
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
}

.tabs,
.order-list,
.detail-card,
.state-card {
  margin-top: 20px;
}

.tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.page-header h2,
.detail-card h3 {
  margin: 0;
}

.page-header p,
.meta-text {
  margin: 8px 0 0;
  color: #6b7280;
}

.order-header,
.action-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}

.order-header {
  font-weight: 600;
}

.status {
  color: #2563eb;
}

.detail-row {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #e5e7eb;
}

.detail-row:last-child {
  border-bottom: none;
}

.primary-button,
.ghost-button,
.danger-button {
  min-height: 38px;
  padding: 0 14px;
  border: none;
  border-radius: 10px;
}

.primary-button {
  background: #2563eb;
  color: #fff;
}

.ghost-button {
  background: #e5e7eb;
  color: #111827;
}

.ghost-button.active {
  background: #2563eb;
  color: #fff;
}

.danger-button {
  background: #fee2e2;
  color: #b91c1c;
}

.error-text {
  margin-top: 16px;
  color: #dc2626;
}
</style>
