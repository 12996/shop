<template>
  <section class="page-card">
    <div class="page-header">
      <div>
        <h2>销售统计</h2>
        <p>查看订单总数、销售总额、已完成订单数和热销商品排行。</p>
      </div>
    </div>

    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

    <section class="stats-grid">
      <article class="stats-card">
        <span class="stats-label">订单总数</span>
        <strong class="stats-value">{{ overview?.order_count ?? 0 }}</strong>
      </article>
      <article class="stats-card">
        <span class="stats-label">销售总额</span>
        <strong class="stats-value">￥{{ overview?.sales_amount ?? "0.00" }}</strong>
      </article>
      <article class="stats-card">
        <span class="stats-label">已完成订单</span>
        <strong class="stats-value">{{ overview?.completed_order_count ?? 0 }}</strong>
      </article>
    </section>

    <section class="table-card">
      <div class="table-header">
        <h3>热销商品排行</h3>
      </div>

      <div v-if="loading" class="state-text">加载中...</div>
      <div v-else-if="hotProducts.length === 0" class="state-text">暂无统计数据</div>

      <table v-else class="table">
        <thead>
          <tr>
            <th>排名</th>
            <th>商品名称</th>
            <th>销量</th>
            <th>关联订单数</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in hotProducts" :key="item.product_id">
            <td>{{ index + 1 }}</td>
            <td>{{ item.product_name }}</td>
            <td>{{ item.sales_count }}</td>
            <td>{{ item.order_count }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

import {
  fetchHotProducts,
  fetchStatisticsOverview,
  type HotProduct,
  type StatisticsOverview,
} from "../../api/content";
import { useWebAuthStore } from "../../stores/auth";

const authStore = useWebAuthStore();

const loading = ref(false);
const errorMessage = ref("");
const overview = ref<StatisticsOverview | null>(null);
const hotProducts = ref<HotProduct[]>([]);

onMounted(async () => {
  await authStore.ensureRoleSession("merchant");
  await loadStatistics();
});

async function loadStatistics() {
  loading.value = true;
  errorMessage.value = "";

  try {
    const [overviewResponse, hotProductResponse] = await Promise.all([
      fetchStatisticsOverview(),
      fetchHotProducts(),
    ]);
    overview.value = overviewResponse;
    hotProducts.value = hotProductResponse;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载失败";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.page-card,
.stats-card,
.table-card {
  padding: 24px;
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
}

.page-header h2,
.table-header h3 {
  margin: 0;
}

.page-header p {
  margin: 8px 0 0;
  color: #6b7280;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 20px;
}

.stats-label {
  display: block;
  color: #6b7280;
  font-size: 14px;
}

.stats-value {
  display: block;
  margin-top: 12px;
  font-size: 28px;
  line-height: 1.2;
}

.table-card {
  margin-top: 20px;
}

.table-header {
  margin-bottom: 12px;
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
