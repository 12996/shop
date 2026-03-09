<template>
  <nav class="tab-bar">
    <RouterLink
      v-for="item in items"
      :key="item.to"
      :to="item.to"
      class="tab-item"
      :class="{ active: route.path === item.to }"
    >
      <span class="tab-label">{{ item.label }}</span>
    </RouterLink>
  </nav>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";

const route = useRoute();

const items = [
  { label: "首页", to: "/" },
  { label: "商品", to: "/products" },
  { label: "购物车", to: "/cart" },
  { label: "订单", to: "/orders" },
];
</script>

<style scoped>
.tab-bar {
  position: sticky;
  bottom: 0;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  background: #fff;
  border-top: 1px solid #e5e7eb;
}

.tab-item {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 56px;
  color: #6b7280;
  text-decoration: none;
}

.tab-item.active {
  color: #2563eb;
  font-weight: 600;
}

.tab-label {
  font-size: 14px;
}
</style>
