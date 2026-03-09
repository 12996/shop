<template>
  <section class="page-card">
    <div class="page-header">
      <div>
        <h2>购物车</h2>
        <p>支持勾选、改数量、删除，以及进入结算。</p>
      </div>
      <RouterLink class="ghost-button link-button" to="/user/products">继续购物</RouterLink>
    </div>

    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

    <section v-if="loading" class="state-card">加载中...</section>
    <section v-else-if="items.length === 0" class="state-card">购物车为空</section>
    <template v-else>
      <section class="cart-list">
        <article v-for="item in items" :key="item.id" class="cart-card">
          <label class="selector">
            <input :checked="item.selected" type="checkbox" @change="toggleSelected(item)" />
            <span>{{ item.product_name }}</span>
          </label>
          <div class="meta-text">单价：￥{{ item.product_price }}</div>
          <div class="action-row">
            <div class="quantity-row">
              <button class="ghost-button" :disabled="item.quantity <= 1" @click="changeQuantity(item, item.quantity - 1)">-</button>
              <span>{{ item.quantity }}</span>
              <button class="ghost-button" @click="changeQuantity(item, item.quantity + 1)">+</button>
            </div>
            <button class="danger-button" @click="removeItem(item.id)">删除</button>
          </div>
        </article>
      </section>

      <section class="summary-card">
        <span>已选金额：￥{{ selectedTotal.toFixed(2) }}</span>
        <button class="primary-button" @click="goToCheckout">去结算</button>
      </section>
    </template>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { RouterLink, useRouter } from "vue-router";

import {
  deleteCartItem,
  fetchCart,
  fetchCheckoutPreview,
  updateCartItem,
  type CartItem,
} from "../../api/cart";

const router = useRouter();

const loading = ref(false);
const errorMessage = ref("");
const items = ref<CartItem[]>([]);

const selectedTotal = computed(() =>
  items.value
    .filter((item) => item.selected)
    .reduce((total, item) => total + Number(item.product_price) * item.quantity, 0),
);

onMounted(async () => {
  await loadCart();
});

async function loadCart() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const payload = await fetchCart();
    items.value = payload.items;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载失败";
  } finally {
    loading.value = false;
  }
}

async function changeQuantity(item: CartItem, quantity: number) {
  try {
    await updateCartItem(item.id, { quantity, selected: item.selected });
    await loadCart();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "更新失败";
  }
}

async function toggleSelected(item: CartItem) {
  try {
    await updateCartItem(item.id, { quantity: item.quantity, selected: !item.selected });
    await loadCart();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "更新失败";
  }
}

async function removeItem(itemId: number) {
  try {
    await deleteCartItem(itemId);
    await loadCart();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "删除失败";
  }
}

async function goToCheckout() {
  try {
    const preview = await fetchCheckoutPreview();
    if (preview.items.length === 0) {
      errorMessage.value = "请先勾选要结算的商品";
      return;
    }
    await router.push("/user/checkout");
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "结算失败";
  }
}
</script>

<style scoped>
.page-card,
.cart-card,
.summary-card,
.state-card {
  padding: 24px;
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
}

.cart-list,
.summary-card,
.state-card {
  margin-top: 20px;
}

.cart-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.page-header,
.action-row,
.summary-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.page-header h2 {
  margin: 0;
}

.page-header p,
.meta-text,
.state-card {
  margin: 8px 0 0;
  color: #6b7280;
}

.selector {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.quantity-row {
  display: flex;
  align-items: center;
  gap: 12px;
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

.danger-button {
  background: #fee2e2;
  color: #b91c1c;
}

.link-button {
  text-decoration: none;
}

.error-text {
  margin-top: 16px;
  color: #dc2626;
}
</style>
