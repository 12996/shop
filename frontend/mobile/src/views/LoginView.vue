<template>
  <main class="page">
    <section class="hero">
      <div class="brand">无人超市</div>
      <h1 class="title">用户登录</h1>
      <p class="subtitle">支持用户名密码登录，也支持手机号验证码登录。</p>
    </section>

    <section class="card">
      <div class="tabs">
        <button class="tab" :class="{ active: mode === 'password' }" @click="mode = 'password'">
          密码登录
        </button>
        <button class="tab" :class="{ active: mode === 'code' }" @click="mode = 'code'">
          验证码登录
        </button>
      </div>

      <form class="form" @submit.prevent="handleSubmit">
        <template v-if="mode === 'password'">
          <label class="field">
            <span>用户名</span>
            <input v-model.trim="passwordForm.username" type="text" placeholder="请输入用户名" />
          </label>

          <label class="field">
            <span>密码</span>
            <input v-model="passwordForm.password" type="password" placeholder="请输入密码" />
          </label>
        </template>

        <template v-else>
          <label class="field">
            <span>手机号</span>
            <input v-model.trim="codeForm.phone" type="text" placeholder="请输入手机号" />
          </label>

          <label class="field">
            <span>验证码</span>
            <input v-model.trim="codeForm.code" type="text" placeholder="请输入验证码，默认 123456" />
          </label>
        </template>

        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

        <button class="primary-button" type="submit" :disabled="authStore.loading">
          {{ authStore.loading ? "登录中..." : "登录" }}
        </button>
      </form>
    </section>
  </main>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";

import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();
const router = useRouter();

const mode = ref<"password" | "code">("password");
const errorMessage = ref("");

const passwordForm = reactive({
  username: "",
  password: "",
});

const codeForm = reactive({
  phone: "",
  code: "123456",
});

async function handleSubmit() {
  errorMessage.value = "";

  try {
    if (mode.value === "password") {
      await authStore.loginByPassword(passwordForm.username, passwordForm.password);
    } else {
      await authStore.loginByCode(codeForm.phone, codeForm.code);
    }
    await router.push("/");
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "登录失败";
  }
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  padding: 32px 20px;
  box-sizing: border-box;
  background: linear-gradient(180deg, #eff6ff 0%, #f8fafc 100%);
  font-family: sans-serif;
}

.hero {
  margin-bottom: 24px;
}

.brand {
  display: inline-flex;
  padding: 6px 12px;
  border-radius: 999px;
  background: #dbeafe;
  color: #1d4ed8;
  font-size: 13px;
  font-weight: 600;
}

.title {
  margin: 16px 0 8px;
  font-size: 28px;
  color: #111827;
}

.subtitle {
  margin: 0;
  color: #6b7280;
  line-height: 1.5;
}

.card {
  padding: 20px;
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
}

.tabs {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin-bottom: 20px;
}

.tab {
  min-height: 40px;
  border: none;
  border-radius: 10px;
  background: #f3f4f6;
  color: #6b7280;
}

.tab.active {
  background: #2563eb;
  color: #fff;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  color: #374151;
  font-size: 14px;
}

.field input {
  min-height: 44px;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  padding: 0 14px;
  font-size: 14px;
}

.primary-button {
  min-height: 46px;
  border: none;
  border-radius: 12px;
  background: #2563eb;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
}

.error {
  margin: 0;
  color: #dc2626;
  font-size: 14px;
}
</style>
