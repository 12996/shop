<template>
  <section class="page-card">
    <div class="page-header">
      <div>
        <h2>推荐位管理</h2>
        <p>维护首页推荐商品，并控制展示顺序。</p>
      </div>
      <button class="primary-button" @click="startCreate">新增推荐</button>
    </div>

    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

    <section class="form-card">
      <div class="form-grid">
        <label class="field">
          <span>推荐商品</span>
          <select v-model.number="form.product">
            <option :value="0">请选择商品</option>
            <option v-for="product in productOptions" :key="product.id" :value="product.id">
              {{ product.name }}
            </option>
          </select>
        </label>
        <label class="field">
          <span>展示顺序</span>
          <input v-model.number="form.sort_order" type="number" min="0" />
        </label>
        <label class="field">
          <span>状态</span>
          <select v-model="form.status">
            <option value="enabled">启用</option>
            <option value="disabled">停用</option>
          </select>
        </label>
      </div>

      <div class="form-actions">
        <button class="primary-button" :disabled="submitting" @click="submitForm">
          {{ submitting ? "处理中..." : editingId ? "保存修改" : "创建推荐" }}
        </button>
        <button v-if="editingId" class="ghost-button" @click="startCreate">取消编辑</button>
      </div>
    </section>

    <section class="table-card">
      <div v-if="loading" class="state-text">加载中...</div>
      <div v-else-if="items.length === 0" class="state-text">暂无推荐商品</div>

      <table v-else class="table">
        <thead>
          <tr>
            <th>商品</th>
            <th>排序</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.product_name ?? productNameMap[item.product] ?? `商品 #${item.product}` }}</td>
            <td>{{ item.sort_order }}</td>
            <td>{{ item.status === "enabled" ? "启用" : "停用" }}</td>
            <td class="actions">
              <button class="inline-button" @click="startEdit(item)">编辑</button>
              <button class="inline-button danger" @click="removeItem(item.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";

import {
  createRecommendation,
  deleteRecommendation,
  fetchRecommendations,
  updateRecommendation,
  type Recommendation,
  type RecommendationPayload,
} from "../../api/content";
import { fetchAdminProducts, type AdminProduct } from "../../api/products";
import { useWebAuthStore } from "../../stores/auth";

const authStore = useWebAuthStore();

const loading = ref(false);
const submitting = ref(false);
const editingId = ref<number | null>(null);
const errorMessage = ref("");
const items = ref<Recommendation[]>([]);
const products = ref<AdminProduct[]>([]);

const form = reactive<RecommendationPayload>({
  product: 0,
  sort_order: 0,
  status: "enabled",
});

const productOptions = computed(() => products.value.filter((item) => item.status === "on_shelf"));
const productNameMap = computed(() =>
  Object.fromEntries(products.value.map((item) => [item.id, item.name])),
);

onMounted(async () => {
  await authStore.ensureRoleSession("merchant");
  await loadInitialData();
});

async function loadInitialData() {
  loading.value = true;
  errorMessage.value = "";

  try {
    const [recommendationList, productList] = await Promise.all([
      fetchRecommendations(),
      fetchAdminProducts(),
    ]);
    items.value = recommendationList;
    products.value = productList;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载失败";
  } finally {
    loading.value = false;
  }
}

function startCreate() {
  editingId.value = null;
  Object.assign(form, {
    product: productOptions.value[0]?.id ?? 0,
    sort_order: 0,
    status: "enabled",
  });
}

function startEdit(item: Recommendation) {
  editingId.value = item.id;
  Object.assign(form, {
    product: item.product,
    sort_order: item.sort_order,
    status: item.status,
  });
}

async function submitForm() {
  submitting.value = true;
  errorMessage.value = "";

  try {
    if (editingId.value) {
      await updateRecommendation(editingId.value, form);
    } else {
      await createRecommendation(form);
    }
    await loadInitialData();
    startCreate();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "提交失败";
  } finally {
    submitting.value = false;
  }
}

async function removeItem(id: number) {
  try {
    await deleteRecommendation(id);
    await loadInitialData();
    if (editingId.value === id) {
      startCreate();
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "删除失败";
  }
}
</script>

<style scoped>
.page-card,
.form-card,
.table-card {
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

.page-header h2 {
  margin: 0;
}

.page-header p {
  margin: 8px 0 0;
  color: #6b7280;
}

.form-card,
.table-card {
  margin-top: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field input,
.field select {
  min-height: 40px;
  padding: 0 12px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font: inherit;
}

.form-actions,
.actions {
  display: flex;
  gap: 8px;
}

.form-actions {
  margin-top: 16px;
}

.primary-button,
.ghost-button,
.inline-button {
  min-height: 38px;
  padding: 0 14px;
  border: none;
  border-radius: 10px;
}

.primary-button,
.inline-button {
  background: #2563eb;
  color: #fff;
}

.ghost-button {
  background: #e5e7eb;
  color: #111827;
}

.inline-button.danger {
  background: #fee2e2;
  color: #b91c1c;
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
