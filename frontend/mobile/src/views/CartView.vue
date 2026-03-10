<template>
  <div class="page">
    <section v-if="!authStore.isAuthenticated" class="state-card">
      <p>请先登录后查看购物车。</p>
      <RouterLink class="link-button" to="/login">去登录</RouterLink>
    </section>

    <template v-else>
      <section v-if="loading" class="state-card">加载中...</section>
      <section v-else-if="items.length === 0" class="state-card">购物车为空</section>

      <section v-else class="cart-list">
        <article v-for="item in items" :key="item.id" class="cart-card">
          <label class="selector">
            <input :checked="item.selected" type="checkbox" @change="toggleSelected(item.id, item.quantity, !item.selected)" />
            <span>{{ item.product_name }}</span>
          </label>
          <div class="meta">单价：￥{{ item.product_price }}</div>
          <div class="actions">
            <div class="quantity">
              <button :disabled="item.quantity <= 1" @click="changeQuantity(item.id, item.quantity - 1, item.selected)">-</button>
              <span>{{ item.quantity }}</span>
              <button @click="changeQuantity(item.id, item.quantity + 1, item.selected)">+</button>
            </div>
            <button class="danger" @click="removeItem(item.id)">删除</button>
          </div>
        </article>
      </section>

      <section v-if="items.length > 0" class="summary-card">
        <div>已选金额：￥{{ cartStore.selectedTotal.toFixed(2) }}</div>
        <button class="primary-button" @click="goToCheckout">去结算</button>
      </section>
    </template>

  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { RouterLink, useRouter } from "vue-router";

import { useAuthStore } from "../stores/auth";
import { useCartStore } from "../stores/cart";

const authStore = useAuthStore();
const cartStore = useCartStore();
const router = useRouter();

const loading = ref(false);
const items = computed(() => cartStore.cart?.items ?? []);

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    return;
  }
  loading.value = true;
  try {
    await cartStore.loadCart();
  } finally {
    loading.value = false;
  }
});

async function changeQuantity(itemId: number, quantity: number, selected: boolean) {
  await cartStore.changeItem(itemId, { quantity, selected });
}

async function toggleSelected(itemId: number, quantity: number, selected: boolean) {
  await cartStore.changeItem(itemId, { quantity, selected });
}

async function removeItem(itemId: number) {
  await cartStore.removeItem(itemId);
}

async function goToCheckout() {
  await cartStore.loadCheckoutPreview();
  await router.push("/checkout");
}
</script>

<style scoped>
.page {
  padding: 0 0 88px;
  box-sizing: border-box;
  font-family: sans-serif;
}

.state-card,
.cart-card,
.summary-card {
  padding: 16px;
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
}

.cart-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.selector {
  display: flex;
  gap: 8px;
  align-items: center;
  color: #111827;
  font-weight: 600;
}

.meta {
  margin-top: 8px;
  color: #6b7280;
}

.actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 12px;
}

.quantity {
  display: flex;
  gap: 12px;
  align-items: center;
}

.quantity button,
.danger,
.link-button,
.primary-button {
  min-height: 36px;
  padding: 0 14px;
  border: none;
  border-radius: 10px;
}

.quantity button,
.link-button {
  background: #e5e7eb;
  color: #111827;
  text-decoration: none;
}

.danger {
  background: #fee2e2;
  color: #b91c1c;
}

.summary-card {
  position: sticky;
  bottom: 72px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
}

.primary-button {
  background: #2563eb;
  color: #fff;
}
</style>
