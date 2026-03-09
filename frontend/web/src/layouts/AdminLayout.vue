<template>
  <div class="layout-shell">
    <aside class="sidebar">
      <div class="brand-block">
        <div class="brand-tag">无人超市</div>
        <div class="brand-title">Web 管理端</div>
      </div>

      <nav class="menu">
        <RouterLink
          v-for="item in visibleMenuItems"
          :key="item.to"
          :to="item.to"
          class="menu-item"
          :class="{ active: route.path === item.to }"
        >
          {{ item.label }}
        </RouterLink>
      </nav>
    </aside>

    <div class="main-shell">
      <header class="topbar">
        <div>
          <div class="page-tag">{{ currentSection }}</div>
          <h1 class="page-title">{{ currentTitle }}</h1>
        </div>

        <div class="toolbar">
          <select :value="authStore.role" class="role-switcher" @change="handleRoleChange">
            <option value="user">用户角色</option>
            <option value="merchant">商家角色</option>
          </select>
          <div class="user-card">
            <div class="user-name">{{ authStore.user.username }}</div>
            <div class="user-role">{{ authStore.role === "merchant" ? "商家" : "用户" }}</div>
          </div>
        </div>
      </header>

      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, watch } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";

import { useWebAuthStore } from "../stores/auth";

const route = useRoute();
const router = useRouter();
const authStore = useWebAuthStore();

const menuItems = [
  { label: "用户首页", to: "/user/home", section: "用户端", role: "user" },
  { label: "商品浏览", to: "/user/products", section: "用户端", role: "user" },
  { label: "购物车", to: "/user/cart", section: "用户端", role: "user" },
  { label: "确认订单", to: "/user/checkout", section: "用户端", role: "user", hidden: true },
  { label: "我的订单", to: "/user/orders", section: "用户端", role: "user" },
  { label: "个人中心", to: "/user/profile", section: "用户端", role: "user" },
  { label: "控制台", to: "/admin/dashboard", section: "商家端", role: "merchant" },
  { label: "商品管理", to: "/admin/products", section: "商家端", role: "merchant" },
  { label: "分类管理", to: "/admin/categories", section: "商家端", role: "merchant" },
  { label: "库存管理", to: "/admin/inventory", section: "商家端", role: "merchant" },
  { label: "订单管理", to: "/admin/orders", section: "商家端", role: "merchant" },
  { label: "公告管理", to: "/admin/announcements", section: "商家端", role: "merchant" },
  { label: "推荐位管理", to: "/admin/recommendations", section: "商家端", role: "merchant" },
  { label: "销售统计", to: "/admin/statistics", section: "商家端", role: "merchant" },
] as const;

const defaultPathByRole = {
  user: "/user/home",
  merchant: "/admin/dashboard",
} as const;

const visibleMenuItems = computed(() =>
  menuItems.filter((item) => item.role === authStore.role && !item.hidden),
);

const currentItem = computed(
  () => menuItems.find((item) => item.to === route.path) ?? { label: "页面", section: "系统" },
);

const currentTitle = computed(() => currentItem.value.label);
const currentSection = computed(() => currentItem.value.section);

async function handleRoleChange(event: Event) {
  const nextRole = (event.target as HTMLSelectElement).value as "user" | "merchant";
  await authStore.setRole(nextRole);
  router.push(defaultPathByRole[nextRole]);
}

watch(
  () => authStore.role,
  (role) => {
    const isCurrentPathAllowed = menuItems.some((item) => item.role === role && item.to === route.path);
    if (!isCurrentPathAllowed) {
      router.replace(defaultPathByRole[role]);
    }
  },
  { immediate: true },
);
</script>

<style scoped>
.layout-shell {
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: 100vh;
  background: #f8fafc;
  font-family: sans-serif;
}

.sidebar {
  padding: 24px 16px;
  background: #111827;
  color: #fff;
}

.brand-block {
  padding: 12px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.08);
}

.brand-tag {
  color: #93c5fd;
  font-size: 13px;
  font-weight: 600;
}

.brand-title {
  margin-top: 8px;
  font-size: 22px;
  font-weight: 700;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 24px;
}

.menu-item {
  display: flex;
  align-items: center;
  min-height: 42px;
  padding: 0 14px;
  border-radius: 12px;
  color: #d1d5db;
  text-decoration: none;
}

.menu-item.active {
  background: #2563eb;
  color: #fff;
}

.main-shell {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 28px;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
}

.page-tag {
  color: #2563eb;
  font-size: 13px;
  font-weight: 600;
}

.page-title {
  margin: 8px 0 0;
  color: #111827;
  font-size: 28px;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 16px;
}

.role-switcher {
  min-height: 40px;
  min-width: 120px;
  padding: 0 12px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  background: #fff;
}

.user-card {
  padding: 10px 14px;
  border-radius: 12px;
  background: #f3f4f6;
}

.user-name {
  color: #111827;
  font-weight: 600;
}

.user-role {
  margin-top: 4px;
  color: #6b7280;
  font-size: 13px;
}

.content {
  padding: 24px 28px;
}
</style>
