<template>
  <div class="page">
    <section v-if="!authStore.isAuthenticated" class="state-card">
      <p>请先登录后结算。</p>
      <RouterLink class="link-button" to="/login">去登录</RouterLink>
    </section>

    <template v-else>
      <section v-if="loading" class="state-card">加载中...</section>
      <section v-else-if="!preview || preview.items.length === 0" class="state-card">暂无可结算商品</section>

      <template v-else>
        <section class="summary-card">
          <div class="section-title">结算商品</div>
          <div v-for="item in preview.items" :key="item.id" class="checkout-item">
            <div>{{ item.product_name }}</div>
            <div>x{{ item.quantity }}</div>
            <div>￥{{ item.product_price }}</div>
          </div>
        </section>

        <section class="summary-card">
          <div class="section-title">支付方式</div>
          <label v-for="item in paymentOptions" :key="item.value" class="payment-option">
            <input v-model="paymentMethod" type="radio" :value="item.value" />
            <span>{{ item.label }}</span>
          </label>
        </section>

        <section class="summary-card">
          <div>总金额：￥{{ preview.total_amount }}</div>
          <div class="address-tip">店内自助购物，当前订单不填写地址。</div>
          <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
          <button class="primary-button" :disabled="submitting" @click="submitAndPay">
            {{ submitting ? "处理中..." : "提交订单并支付" }}
          </button>
        </section>
      </template>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { RouterLink, useRouter } from "vue-router";

import { createOrder, payOrder } from "../api/orders";
import { useAuthStore } from "../stores/auth";
import { useCartStore } from "../stores/cart";

const router = useRouter();
const authStore = useAuthStore();
const cartStore = useCartStore();

const loading = ref(false);
const submitting = ref(false);
const errorMessage = ref("");
const paymentMethod = ref("wechat");

const preview = computed(() => cartStore.checkoutPreview);
const paymentOptions = [
  { label: "微信支付", value: "wechat" },
  { label: "支付宝", value: "alipay" },
  { label: "余额支付", value: "balance" },
];

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    return;
  }
  loading.value = true;
  try {
    await cartStore.loadCheckoutPreview();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载失败";
  } finally {
    loading.value = false;
  }
});

async function submitAndPay() {
  errorMessage.value = "";
  submitting.value = true;
  try {
    const order = await createOrder();
    await payOrder(order.id, paymentMethod.value);
    await cartStore.loadCart();
    cartStore.clearCheckoutPreview();
    await router.push("/orders");
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "提交失败";
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.page {
  padding: 0 0 40px;
  box-sizing: border-box;
  font-family: sans-serif;
}

.summary-card,
.state-card {
  margin-top: 16px;
  padding: 16px;
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
}

.section-title {
  margin-bottom: 12px;
  color: #111827;
  font-weight: 600;
}

.checkout-item {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #f3f4f6;
}

.checkout-item:last-child {
  border-bottom: none;
}

.payment-option {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-top: 10px;
}

.address-tip {
  margin: 10px 0 0;
  color: #6b7280;
  font-size: 14px;
}

.error {
  color: #dc2626;
}

.link-button,
.primary-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
  padding: 0 16px;
  margin-top: 16px;
  border: none;
  border-radius: 10px;
  text-decoration: none;
}

.link-button {
  background: #e5e7eb;
  color: #111827;
}

.primary-button {
  width: 100%;
  background: #2563eb;
  color: #fff;
}
</style>
