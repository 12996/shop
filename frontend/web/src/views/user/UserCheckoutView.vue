<template>
  <section class="page-card">
    <div class="page-header">
      <div>
        <h2>确认订单</h2>
        <p>先生成待支付订单，再执行 mock 支付。</p>
      </div>
      <RouterLink class="ghost-button link-button" to="/user/cart">返回购物车</RouterLink>
    </div>

    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

    <section v-if="loading" class="state-card">加载中...</section>
    <section v-else-if="!preview || preview.items.length === 0" class="state-card">暂无可结算商品</section>
    <template v-else>
      <section class="section-card">
        <h3>结算商品</h3>
        <div v-for="item in preview.items" :key="item.id" class="checkout-row">
          <span>{{ item.product_name }}</span>
          <span>x{{ item.quantity }}</span>
          <span>￥{{ item.product_price }}</span>
        </div>
      </section>

      <section class="section-card">
        <h3>支付方式</h3>
        <label v-for="option in paymentOptions" :key="option.value" class="option-row">
          <input v-model="paymentMethod" type="radio" :value="option.value" />
          <span>{{ option.label }}</span>
        </label>
        <p class="tip-text">当前场景为店内自助购物，地址字段保留但不填写。</p>
      </section>

      <section class="section-card footer-row">
        <span>总金额：￥{{ preview.total_amount }}</span>
        <button class="primary-button" :disabled="submitting" @click="submitAndPay">
          {{ submitting ? "处理中..." : "提交订单并支付" }}
        </button>
      </section>
    </template>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { RouterLink, useRouter } from "vue-router";

import { fetchCheckoutPreview, type CheckoutPreview } from "../../api/cart";
import { createOrder, payOrder } from "../../api/orders";

const router = useRouter();

const loading = ref(false);
const submitting = ref(false);
const errorMessage = ref("");
const preview = ref<CheckoutPreview | null>(null);
const paymentMethod = ref("wechat");

const paymentOptions = [
  { label: "微信支付", value: "wechat" },
  { label: "支付宝", value: "alipay" },
  { label: "余额支付", value: "balance" },
];

onMounted(async () => {
  await loadPreview();
});

async function loadPreview() {
  loading.value = true;
  errorMessage.value = "";
  try {
    preview.value = await fetchCheckoutPreview();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载失败";
  } finally {
    loading.value = false;
  }
}

async function submitAndPay() {
  submitting.value = true;
  errorMessage.value = "";

  try {
    const order = await createOrder();
    await payOrder(order.id, paymentMethod.value);
    await router.push("/user/orders");
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "提交失败";
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.page-card,
.section-card,
.state-card {
  padding: 24px;
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
}

.section-card,
.state-card {
  margin-top: 20px;
}

.page-header,
.footer-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.page-header h2,
.section-card h3 {
  margin: 0;
}

.page-header p,
.tip-text {
  margin: 8px 0 0;
  color: #6b7280;
}

.checkout-row {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #e5e7eb;
}

.checkout-row:last-child {
  border-bottom: none;
}

.option-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
}

.primary-button,
.ghost-button {
  min-height: 40px;
  padding: 0 16px;
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

.link-button {
  text-decoration: none;
}

.error-text {
  margin-top: 16px;
  color: #dc2626;
}
</style>
