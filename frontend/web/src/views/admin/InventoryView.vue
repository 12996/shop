<template>
  <section class="page-card">
    <div class="page-header">
      <div>
        <h2>库存管理</h2>
        <p>支持库存列表查看、预警识别和手动库存调整。</p>
      </div>
    </div>

    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

    <section class="table-card">
      <div v-if="loading" class="state-text">加载中...</div>
      <div v-else-if="items.length === 0" class="state-text">暂无库存数据</div>

      <table v-else class="table">
        <thead>
          <tr>
            <th>商品</th>
            <th>分类</th>
            <th>状态</th>
            <th>库存</th>
            <th>阈值</th>
            <th>预警</th>
            <th>调整库存</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.product_id">
            <td>{{ item.product_name }}</td>
            <td>{{ item.category_name }}</td>
            <td>{{ item.product_status === "on_shelf" ? "上架" : "下架" }}</td>
            <td>{{ item.quantity }}</td>
            <td>{{ item.alert_threshold }}</td>
            <td>
              <span class="alert-badge" :class="{ active: item.is_alert }">
                {{ item.is_alert ? "库存预警" : "正常" }}
              </span>
            </td>
            <td>
              <div class="adjust-row">
                <input v-model.number="adjustMap[item.product_id]" type="number" min="0" />
                <button class="inline-button" @click="submitAdjust(item.product_id)">保存</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

import { adjustInventory, fetchInventory, type InventoryItem } from "../../api/products";
import { useWebAuthStore } from "../../stores/auth";

const authStore = useWebAuthStore();

const loading = ref(false);
const errorMessage = ref("");
const items = ref<InventoryItem[]>([]);
const adjustMap = ref<Record<number, number>>({});

onMounted(async () => {
  await authStore.ensureRoleSession("merchant");
  await loadInventory();
});

async function loadInventory() {
  loading.value = true;
  errorMessage.value = "";

  try {
    const inventory = await fetchInventory();
    items.value = inventory;
    adjustMap.value = Object.fromEntries(inventory.map((item) => [item.product_id, item.quantity]));
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载失败";
  } finally {
    loading.value = false;
  }
}

async function submitAdjust(productId: number) {
  try {
    await adjustInventory(productId, {
      quantity: Number(adjustMap.value[productId] ?? 0),
      remark: "Web 商家端手动调整",
    });
    await loadInventory();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "库存调整失败";
  }
}
</script>

<style scoped>
.page-card,
.table-card {
  padding: 24px;
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
}

.page-header h2 {
  margin: 0;
}

.page-header p {
  margin: 8px 0 0;
  color: #6b7280;
}

.table-card {
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

.alert-badge {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  background: #e5e7eb;
  color: #4b5563;
  font-size: 13px;
}

.alert-badge.active {
  background: #fee2e2;
  color: #b91c1c;
}

.adjust-row {
  display: flex;
  gap: 8px;
}

.adjust-row input {
  width: 88px;
  min-height: 36px;
  padding: 0 10px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
}

.inline-button {
  min-height: 36px;
  padding: 0 12px;
  border: none;
  border-radius: 10px;
  background: #2563eb;
  color: #fff;
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
