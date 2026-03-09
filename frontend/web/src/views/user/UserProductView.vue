<template>
  <section class="page-card">
    <div class="page-header">
      <div>
        <h2>商品浏览</h2>
        <p>支持分类筛选、关键词搜索和直接加入购物车。</p>
      </div>
    </div>

    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

    <section class="toolbar-card">
      <input v-model.trim="keyword" type="text" placeholder="搜索商品名称" @keyup.enter="loadProducts" />
      <button class="ghost-button" :class="{ active: activeCategoryId === null }" @click="selectCategory(null)">全部</button>
      <button
        v-for="category in categories"
        :key="category.id"
        class="ghost-button"
        :class="{ active: activeCategoryId === category.id }"
        @click="selectCategory(category.id)"
      >
        {{ category.name }}
      </button>
      <button class="primary-button" @click="loadProducts">搜索</button>
    </section>

    <section v-if="loading" class="state-card">加载中...</section>
    <section v-else-if="products.length === 0" class="state-card">未找到相关商品</section>
    <section v-else class="product-grid">
      <article v-for="item in products" :key="item.id" class="product-card">
        <div class="image-box">{{ item.main_image || item.name.slice(0, 2) }}</div>
        <div class="product-name">{{ item.name }}</div>
        <div class="meta-text">{{ item.category_name }}</div>
        <div class="product-price">￥{{ item.price }}</div>
        <div class="stock" :class="stockClass(item.stock_quantity)">{{ stockText(item.stock_quantity) }}</div>
        <p class="description">{{ item.description || "暂无描述" }}</p>
        <button class="primary-button" :disabled="item.stock_quantity <= 0" @click="addToCart(item.id)">
          {{ item.stock_quantity <= 0 ? "已售罄" : "加入购物车" }}
        </button>
      </article>
    </section>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { addCartItem } from "../../api/cart";
import { fetchCategories, fetchProducts, type Category, type Product } from "../../api/products";

const route = useRoute();
const router = useRouter();

const loading = ref(false);
const errorMessage = ref("");
const keyword = ref(typeof route.query.keyword === "string" ? route.query.keyword : "");
const activeCategoryId = ref<number | null>(
  typeof route.query.categoryId === "string" ? Number(route.query.categoryId) : null,
);
const categories = ref<Category[]>([]);
const products = ref<Product[]>([]);

onMounted(async () => {
  categories.value = await fetchCategories();
  await loadProducts();
});

async function loadProducts() {
  loading.value = true;
  errorMessage.value = "";
  try {
    products.value = await fetchProducts({
      categoryId: activeCategoryId.value,
      keyword: keyword.value,
    });
    await syncQuery();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载失败";
  } finally {
    loading.value = false;
  }
}

async function selectCategory(categoryId: number | null) {
  activeCategoryId.value = categoryId;
  await loadProducts();
}

async function syncQuery() {
  await router.replace({
    path: "/user/products",
    query: {
      ...(activeCategoryId.value ? { categoryId: String(activeCategoryId.value) } : {}),
      ...(keyword.value ? { keyword: keyword.value } : {}),
    },
  });
}

async function addToCart(productId: number) {
  try {
    await addCartItem({ product_id: productId, quantity: 1 });
    await router.push("/user/cart");
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加入购物车失败";
  }
}

function stockText(stockQuantity: number) {
  if (stockQuantity <= 0) {
    return "已售罄";
  }
  if (stockQuantity <= 5) {
    return `剩余 ${stockQuantity} 件`;
  }
  return "库存充足";
}

function stockClass(stockQuantity: number) {
  if (stockQuantity <= 0) {
    return "soldout";
  }
  if (stockQuantity <= 5) {
    return "low";
  }
  return "normal";
}
</script>

<style scoped>
.page-card,
.toolbar-card,
.state-card {
  padding: 24px;
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
}

.toolbar-card,
.state-card,
.product-grid {
  margin-top: 20px;
}

.toolbar-card {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.toolbar-card input {
  min-width: 260px;
  min-height: 40px;
  padding: 0 12px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}

.product-card {
  padding: 20px;
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
}

.image-box {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 120px;
  border-radius: 12px;
  background: #dbeafe;
  color: #1d4ed8;
  font-weight: 700;
}

.product-name,
.meta-text,
.product-price,
.stock,
.description {
  margin-top: 10px;
}

.meta-text,
.description,
.state-card {
  color: #6b7280;
}

.product-price {
  color: #dc2626;
  font-weight: 700;
}

.stock.normal {
  color: #059669;
}

.stock.low {
  color: #d97706;
}

.stock.soldout {
  color: #6b7280;
}

.primary-button,
.ghost-button {
  min-height: 40px;
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

.error-text {
  margin-top: 16px;
  color: #dc2626;
}
</style>
