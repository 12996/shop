<template>
  <header class="top-nav">
    <div>
      <div class="brand">无人超市</div>
      <h1 class="title">{{ resolvedTitle }}</h1>
    </div>

    <div class="menu-wrap">
      <button class="avatar-button" type="button" @click="toggleMenu">
        <span class="avatar">{{ avatarText }}</span>
      </button>

      <div v-if="menuOpen" class="menu-panel">
        <div class="user-meta">
          <div class="meta-name">{{ userName }}</div>
          <div class="meta-sub">{{ userSub }}</div>
        </div>
        <button class="menu-item" type="button" @click="goProfile">用户中心</button>
        <button class="menu-item danger" type="button" @click="handleLogout">退出登录</button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { useAuthStore } from "../stores/auth";

type Props = {
  title?: string;
};

const props = defineProps<Props>();
const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();
const menuOpen = ref(false);

const resolvedTitle = computed(() => {
  if (props.title) {
    return props.title;
  }
  const routeTitle = route.meta?.title;
  return typeof routeTitle === "string" && routeTitle.trim() ? routeTitle : "首页";
});

const userName = computed(() => authStore.user?.username || "未登录用户");
const userSub = computed(() => authStore.user?.phone || authStore.user?.email || "点击可进入用户中心");
const avatarText = computed(() => {
  const source = authStore.user?.username?.trim();
  return source ? source.slice(0, 1).toUpperCase() : "U";
});

watch(
  () => route.fullPath,
  () => {
    menuOpen.value = false;
  },
);

function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}

async function goProfile() {
  if (!authStore.isAuthenticated) {
    await router.push("/login");
    return;
  }
  await router.push("/profile");
}

async function handleLogout() {
  authStore.logout();
  await router.push("/login");
}
</script>

<style scoped>
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.brand {
  font-size: 13px;
  color: #2563eb;
  font-weight: 700;
}

.title {
  margin: 8px 0 0;
  font-size: 42px;
  line-height: 1;
  color: #0f172a;
}

.menu-wrap {
  position: relative;
}

.avatar-button {
  border: none;
  background: transparent;
  padding: 0;
}

.avatar {
  width: 42px;
  height: 42px;
  border-radius: 999px;
  background: #dbeafe;
  color: #1d4ed8;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.menu-panel {
  position: absolute;
  top: 50px;
  right: 0;
  width: 200px;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  background: #fff;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
  padding: 10px;
  z-index: 10;
}

.user-meta {
  padding: 6px 6px 10px;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 8px;
}

.meta-name {
  color: #0f172a;
  font-size: 14px;
  font-weight: 700;
}

.meta-sub {
  margin-top: 2px;
  color: #64748b;
  font-size: 12px;
  word-break: break-all;
}

.menu-item {
  width: 100%;
  border: none;
  background: #fff;
  text-align: left;
  font-size: 14px;
  color: #1e293b;
  padding: 8px 6px;
  border-radius: 8px;
}

.menu-item.danger {
  color: #dc2626;
}
</style>
