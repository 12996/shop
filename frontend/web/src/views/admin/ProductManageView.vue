<template>
  <section class="page-card">
    <div class="page-header">
      <div>
        <h2>商品管理</h2>
        <p>支持商品列表、创建、编辑以及上下架。</p>
      </div>
      <button class="primary-button" @click="startCreate">新增商品</button>
    </div>

    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

    <section class="form-card">
      <div class="form-grid">
        <label class="field">
          <span>分类</span>
          <select v-model.number="form.category">
            <option :value="0">请选择分类</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </label>
        <label class="field">
          <span>商品名称</span>
          <input v-model.trim="form.name" type="text" />
        </label>
        <label class="field">
          <span>价格</span>
          <input v-model.trim="form.price" type="text" />
        </label>
        <label class="field">
          <span>状态</span>
          <select v-model="form.status">
            <option value="on_shelf">上架</option>
            <option value="off_shelf">下架</option>
          </select>
        </label>
        <label class="field">
          <span>库存数量</span>
          <input v-model.number="form.quantity" type="number" min="0" />
        </label>
        <label class="field">
          <span>预警阈值</span>
          <input v-model.number="form.alert_threshold" type="number" min="0" />
        </label>
        <label class="field full-width">
          <span>主图</span>
          <input v-model.trim="form.main_image" type="text" />
        </label>
        <label class="field full-width">
          <span>描述</span>
          <textarea v-model.trim="form.description" rows="3" />
        </label>
      </div>

      <div class="form-actions">
        <button class="primary-button" :disabled="submitting" @click="submitForm">
          {{ submitting ? "处理中..." : editingId ? "保存修改" : "创建商品" }}
        </button>
        <button v-if="editingId" class="ghost-button" @click="startCreate">取消编辑</button>
      </div>
    </section>

    <section class="table-card">
      <div v-if="loading" class="state-text">加载中...</div>
      <div v-else-if="products.length === 0" class="state-text">暂无商品</div>

      <table v-else class="table">
        <thead>
          <tr>
            <th>名称</th>
            <th>分类</th>
            <th>价格</th>
            <th>库存</th>
            <th>阈值</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in products" :key="item.id">
            <td>{{ item.name }}</td>
            <td>{{ item.category_name }}</td>
            <td>￥{{ item.price }}</td>
            <td>{{ item.quantity }}</td>
            <td>{{ item.alert_threshold }}</td>
            <td>{{ item.status === "on_shelf" ? "上架" : "下架" }}</td>
            <td class="actions">
              <button class="inline-button" @click="startEdit(item)">编辑</button>
              <button
                v-if="item.status === 'off_shelf'"
                class="inline-button"
                @click="toggleShelf(item.id, 'on')"
              >
                上架
              </button>
              <button
                v-else
                class="inline-button danger"
                @click="toggleShelf(item.id, 'off')"
              >
                下架
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </section>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";

import {
  createAdminProduct,
  fetchAdminProducts,
  fetchCategories,
  offShelfProduct,
  onShelfProduct,
  updateAdminProduct,
  type AdminProduct,
  type AdminProductPayload,
  type Category,
} from "../../api/products";
import { useWebAuthStore } from "../../stores/auth";

const authStore = useWebAuthStore();

const loading = ref(false);
const submitting = ref(false);
const editingId = ref<number | null>(null);
const errorMessage = ref("");
const categories = ref<Category[]>([]);
const products = ref<AdminProduct[]>([]);

const form = reactive<AdminProductPayload>({
  category: 0,
  name: "",
  main_image: "",
  description: "",
  price: "",
  status: "off_shelf",
  quantity: 0,
  alert_threshold: 0,
});

onMounted(async () => {
  await authStore.ensureRoleSession("merchant");
  await loadInitialData();
});

async function loadInitialData() {
  loading.value = true;
  errorMessage.value = "";

  try {
    const [categoryList, productList] = await Promise.all([fetchCategories(), fetchAdminProducts()]);
    categories.value = categoryList;
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
    category: categories.value[0]?.id ?? 0,
    name: "",
    main_image: "",
    description: "",
    price: "",
    status: "off_shelf",
    quantity: 0,
    alert_threshold: 0,
  });
}

function startEdit(product: AdminProduct) {
  editingId.value = product.id;
  Object.assign(form, {
    category: product.category,
    name: product.name,
    main_image: product.main_image ?? "",
    description: product.description ?? "",
    price: product.price,
    status: product.status,
    quantity: product.quantity,
    alert_threshold: product.alert_threshold,
  });
}

async function submitForm() {
  submitting.value = true;
  errorMessage.value = "";

  try {
    if (editingId.value) {
      await updateAdminProduct(editingId.value, form);
    } else {
      await createAdminProduct(form);
    }
    await loadInitialData();
    startCreate();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "提交失败";
  } finally {
    submitting.value = false;
  }
}

async function toggleShelf(productId: number, action: "on" | "off") {
  try {
    if (action === "on") {
      await onShelfProduct(productId);
    } else {
      await offShelfProduct(productId);
    }
    await loadInitialData();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "状态更新失败";
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
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field.full-width {
  grid-column: 1 / -1;
}

.field input,
.field select,
.field textarea {
  min-height: 40px;
  padding: 0 12px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font: inherit;
}

.field textarea {
  min-height: 88px;
  padding: 12px;
}

.form-actions {
  display: flex;
  gap: 12px;
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

.error-text,
.state-text {
  margin-top: 16px;
  color: #dc2626;
}

.state-text {
  color: #6b7280;
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
</style>
