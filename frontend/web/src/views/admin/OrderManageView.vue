<template>
  <section class="page-card">
    <div class="page-header">
      <div>
        <h2>订单管理</h2>
        <p>查看订单列表、筛选状态、查看详情并完成已支付订单。</p>
      </div>
      <label class="filter-field">
        <span>状态筛选</span>
        <select v-model="activeStatus" @change="loadOrders">
          <option value="all">全部</option>
          <option value="pending_payment">待支付</option>
          <option value="paid">已支付</option>
          <option value="completed">已完成</option>
          <option value="cancelled">已取消</option>
        </select>
      </label>
    </div>

    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

    <section class="table-card">
      <div v-if="loading" class="state-text">加载中...</div>
      <div v-else-if="orders.length === 0" class="state-text">暂无订单数据</div>

      <table v-else class="table">
        <thead>
          <tr>
            <th>订单号</th>
            <th>用户</th>
            <th>状态</th>
            <th>金额</th>
            <th>支付方式</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in orders" :key="item.id">
            <td>{{ item.order_number }}</td>
            <td>{{ item.username }}</td>
            <td>{{ statusLabelMap[item.status] ?? item.status }}</td>
            <td>￥{{ item.total_amount }}</td>
            <td>{{ paymentMethodLabelMap[item.payment_method ?? ""] ?? "-" }}</td>
            <td>{{ formatDate(item.created_at) }}</td>
            <td class="actions">
              <button class="inline-button" @click="selectOrder(item.id)">查看详情</button>
              <button
                v-if="item.status === 'paid'"
                class="inline-button success"
                @click="handleComplete(item.id)"
              >
                完成订单
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <section v-if="selectedOrder" class="detail-card">
      <div class="detail-header">
        <h3>订单详情</h3>
        <span class="detail-status">{{ statusLabelMap[selectedOrder.status] }}</span>
      </div>

      <div class="detail-grid">
        <div><strong>订单号：</strong>{{ selectedOrder.order_number }}</div>
        <div><strong>用户：</strong>{{ selectedOrder.username }}</div>
        <div><strong>订单金额：</strong>￥{{ selectedOrder.total_amount }}</div>
        <div>
          <strong>支付方式：</strong>
          {{ paymentMethodLabelMap[selectedOrder.payment_method ?? ""] ?? "-" }}
        </div>
        <div><strong>创建时间：</strong>{{ formatDate(selectedOrder.created_at) }}</div>
        <div>
          <strong>地址信息：</strong>
          {{ selectedOrder.address_snapshot ? "已预留地址信息" : "店内自助购物，无收货地址" }}
        </div>
      </div>

      <table class="table detail-table">
        <thead>
          <tr>
            <th>商品</th>
            <th>单价</th>
            <th>数量</th>
            <th>小计</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in selectedOrder.items" :key="item.id">
            <td>{{ item.product_name }}</td>
            <td>￥{{ item.product_price }}</td>
            <td>{{ item.quantity }}</td>
            <td>￥{{ item.subtotal }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

import {
  completeAdminOrder,
  fetchAdminOrderDetail,
  fetchAdminOrders,
  type AdminOrder,
} from "../../api/orders";
import { useWebAuthStore } from "../../stores/auth";

const authStore = useWebAuthStore();

const loading = ref(false);
const errorMessage = ref("");
const activeStatus = ref("all");
const orders = ref<AdminOrder[]>([]);
const selectedOrder = ref<AdminOrder | null>(null);

const statusLabelMap: Record<string, string> = {
  pending_payment: "待支付",
  paid: "已支付",
  completed: "已完成",
  cancelled: "已取消",
};

const paymentMethodLabelMap: Record<string, string> = {
  wechat: "微信支付",
  alipay: "支付宝",
  balance: "余额支付",
};

onMounted(async () => {
  await authStore.ensureRoleSession("merchant");
  await loadOrders();
});

async function loadOrders() {
  loading.value = true;
  errorMessage.value = "";

  try {
    const list = await fetchAdminOrders(activeStatus.value);
    orders.value = list;
    selectedOrder.value = list[0] ?? null;
    if (selectedOrder.value) {
      await selectOrder(selectedOrder.value.id);
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载失败";
  } finally {
    loading.value = false;
  }
}

async function selectOrder(orderId: number) {
  try {
    selectedOrder.value = await fetchAdminOrderDetail(orderId);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "详情加载失败";
  }
}

async function handleComplete(orderId: number) {
  try {
    await completeAdminOrder(orderId);
    await loadOrders();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "完成订单失败";
  }
}

function formatDate(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleString("zh-CN", { hour12: false });
}
</script>

<style scoped>
.page-card,
.table-card,
.detail-card {
  padding: 24px;
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.page-header h2,
.detail-header h3 {
  margin: 0;
}

.page-header p {
  margin: 8px 0 0;
  color: #6b7280;
}

.filter-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-field select {
  min-width: 140px;
  min-height: 40px;
  padding: 0 12px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font: inherit;
}

.table-card,
.detail-card {
  margin-top: 20px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 12px 8px;
  border-bottom: 1px solid #e5e7eb;
  text-align: left;
}

.actions {
  display: flex;
  gap: 8px;
}

.inline-button {
  min-height: 36px;
  padding: 0 12px;
  border: none;
  border-radius: 10px;
  background: #2563eb;
  color: #fff;
}

.inline-button.success {
  background: #16a34a;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}

.detail-status {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  background: #dbeafe;
  color: #1d4ed8;
  font-size: 13px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px 20px;
  margin-bottom: 16px;
}

.detail-table {
  margin-top: 16px;
}

.error-text,
.state-text {
  margin-top: 16px;
}

.error-text {
  color: #dc2626;
}

.state-text {
  color: #6b7280;
}
</style>
