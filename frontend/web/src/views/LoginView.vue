<template>
  <section class="login-shell">
    <div class="login-card">
      <div class="brand-tag">无人超市</div>
      <h1>Web 登录</h1>
      <p class="subtitle">未登录访问受保护页面时，会先跳到这里。</p>

      <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

      <label class="field">
        <span>用户名</span>
        <input v-model.trim="username" type="text" placeholder="请输入用户名" />
      </label>

      <label class="field">
        <span>密码</span>
        <input v-model="password" type="password" placeholder="请输入密码" />
      </label>

      <div class="action-row">
        <button class="primary-button" :disabled="submitting" @click="submitLogin">
          {{ submitting ? "登录中..." : "登录" }}
        </button>
      </div>

      <div class="demo-block">
        <span>示例账号</span>
        <div class="demo-actions">
          <button class="ghost-button" :disabled="submitting" @click="loginAsRole('user')">示例用户</button>
          <button class="ghost-button" :disabled="submitting" @click="loginAsRole('merchant')">示例商家</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { useWebAuthStore } from "../stores/auth";

const route = useRoute();
const router = useRouter();
const authStore = useWebAuthStore();

const username = ref("");
const password = ref("");
const submitting = ref(false);
const errorMessage = ref("");

function resolveTarget() {
  const redirect = route.query.redirect;
  return typeof redirect === "string" && redirect.startsWith("/") ? redirect : "/user/home";
}

async function submitLogin() {
  submitting.value = true;
  errorMessage.value = "";
  try {
    const user = await authStore.login({
      username: username.value,
      password: password.value,
    });
    await router.replace(user.role === "merchant" ? "/admin/dashboard" : resolveTarget());
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "登录失败";
  } finally {
    submitting.value = false;
  }
}

async function loginAsRole(role: "user" | "merchant") {
  submitting.value = true;
  errorMessage.value = "";
  try {
    const user = await authStore.ensureRoleSession(role);
    await router.replace(user.role === "merchant" ? "/admin/dashboard" : resolveTarget());
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "登录失败";
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.login-shell {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #f8fafc;
}

.login-card {
  width: 420px;
  padding: 32px;
  border-radius: 24px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
}

.brand-tag {
  color: #2563eb;
  font-size: 13px;
  font-weight: 600;
}

h1 {
  margin: 12px 0 0;
}

.subtitle {
  margin: 10px 0 0;
  color: #6b7280;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 16px;
}

.field input {
  min-height: 42px;
  padding: 0 12px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
}

.action-row {
  margin-top: 20px;
}

.primary-button,
.ghost-button {
  min-height: 42px;
  padding: 0 16px;
  border: none;
  border-radius: 10px;
}

.primary-button {
  width: 100%;
  background: #2563eb;
  color: #fff;
}

.demo-block {
  margin-top: 20px;
}

.demo-actions {
  display: flex;
  gap: 12px;
  margin-top: 10px;
}

.ghost-button {
  background: #e5e7eb;
  color: #111827;
}

.error-text {
  margin-top: 16px;
  color: #dc2626;
}
</style>
