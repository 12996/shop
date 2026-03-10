<template>
  <main class="page">
    <section class="hero">
      <div class="brand">无人超市</div>
      <h1 class="title">{{ pageTitle }}</h1>
      <p class="subtitle">{{ pageSubtitle }}</p>
    </section>

    <section class="card">
      <div v-if="mode !== 'register'" class="tabs">
        <button
          class="tab"
          :class="{ active: mode === 'password' }"
          type="button"
          @click="switchMode('password')"
        >
          密码登录
        </button>
        <button
          class="tab"
          :class="{ active: mode === 'code' }"
          type="button"
          @click="switchMode('code')"
        >
          验证码登录
        </button>
      </div>

      <form class="form" @submit.prevent="handleSubmit">
        <template v-if="mode === 'password'">
          <label class="field">
            <span>用户名</span>
            <input
              v-model.trim="passwordForm.username"
              type="text"
              autocomplete="username"
              placeholder="请输入用户名"
              required
            />
          </label>

          <label class="field">
            <span>密码</span>
            <input
              v-model="passwordForm.password"
              type="password"
              autocomplete="current-password"
              placeholder="请输入密码"
              required
            />
          </label>
        </template>

        <template v-else-if="mode === 'code'">
          <label class="field">
            <span>手机号</span>
            <input
              v-model.trim="codeForm.phone"
              type="text"
              autocomplete="tel"
              placeholder="请输入手机号"
              required
            />
          </label>

          <label class="field">
            <span>验证码</span>
            <input
              v-model.trim="codeForm.code"
              type="text"
              inputmode="numeric"
              placeholder="请输入验证码，默认 123456"
              required
            />
          </label>
        </template>

        <template v-else>
          <label class="field">
            <span>用户名</span>
            <input
              v-model.trim="registerForm.username"
              type="text"
              autocomplete="username"
              placeholder="请设置登录用户名"
              required
            />
          </label>

          <label class="field">
            <span>密码</span>
            <input
              v-model="registerForm.password"
              type="password"
              autocomplete="new-password"
              placeholder="请设置登录密码"
              required
            />
          </label>

          <label class="field">
            <span>确认密码</span>
            <input
              v-model="registerForm.confirmPassword"
              type="password"
              autocomplete="new-password"
              placeholder="请再次输入密码"
              required
            />
          </label>

          <label class="field">
            <span>手机号</span>
            <input
              v-model.trim="registerForm.phone"
              type="text"
              autocomplete="tel"
              placeholder="选填，便于验证码登录"
            />
          </label>

          <label class="field">
            <span>邮箱</span>
            <input
              v-model.trim="registerForm.email"
              type="email"
              autocomplete="email"
              placeholder="选填"
            />
          </label>

          <p class="hint">注册成功后会自动登录，并直接进入首页。</p>
        </template>

        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

        <div class="action-row">
          <button class="primary-button" type="submit" :disabled="authStore.loading">
            {{ authStore.loading ? loadingLabel : submitLabel }}
          </button>
          <button class="switch-button" type="button" :disabled="authStore.loading" @click="switchAuthMode">
            {{ switchButtonLabel }}
          </button>
        </div>
      </form>
    </section>
  </main>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";

import { useAuthStore } from "../stores/auth";

type AuthMode = "password" | "code" | "register";

const authStore = useAuthStore();
const router = useRouter();

const mode = ref<AuthMode>("password");
const errorMessage = ref("");

const passwordForm = reactive({
  username: "",
  password: "",
});

const codeForm = reactive({
  phone: "",
  code: "123456",
});

const registerForm = reactive({
  username: "",
  password: "",
  confirmPassword: "",
  phone: "",
  email: "",
});

const pageTitle = computed(() => (mode.value === "register" ? "用户注册" : "用户登录"));

const pageSubtitle = computed(() => {
  if (mode.value === "register") {
    return "新用户可直接创建账号，注册成功后自动登录。";
  }
  return "支持用户名密码登录，也支持手机号验证码登录。";
});

const submitLabel = computed(() => (mode.value === "register" ? "注册并进入首页" : "登录"));
const loadingLabel = computed(() => (mode.value === "register" ? "注册中..." : "登录中..."));
const switchButtonLabel = computed(() => (mode.value === "register" ? "去登录" : "注册"));

function switchMode(nextMode: AuthMode) {
  mode.value = nextMode;
  errorMessage.value = "";
}

function switchAuthMode() {
  switchMode(mode.value === "register" ? "password" : "register");
}

function toOptionalValue(value: string) {
  const normalized = value.trim();
  return normalized ? normalized : undefined;
}

async function handleSubmit() {
  errorMessage.value = "";

  try {
    if (mode.value === "password") {
      await authStore.loginByPassword(passwordForm.username, passwordForm.password);
    } else if (mode.value === "code") {
      await authStore.loginByCode(codeForm.phone, codeForm.code);
    } else {
      if (!registerForm.username || !registerForm.password) {
        throw new Error("请输入用户名和密码");
      }
      if (registerForm.password !== registerForm.confirmPassword) {
        throw new Error("两次输入的密码不一致");
      }

      await authStore.registerAndLogin({
        username: registerForm.username,
        password: registerForm.password,
        phone: toOptionalValue(registerForm.phone),
        email: toOptionalValue(registerForm.email),
      });
    }

    await router.push("/");
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : mode.value === "register" ? "注册失败" : "登录失败";
  }
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  padding: 32px 20px;
  box-sizing: border-box;
  background: linear-gradient(180deg, #eff6ff 0%, #f8fafc 100%);
  font-family: "Segoe UI", "PingFang SC", sans-serif;
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
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
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

.field input:focus {
  border-color: #2563eb;
  outline: 2px solid rgba(37, 99, 235, 0.12);
}

.hint {
  margin: -4px 0 0;
  padding: 10px 12px;
  border-radius: 12px;
  background: #eff6ff;
  color: #1d4ed8;
  font-size: 13px;
}

.primary-button {
  min-height: 46px;
  width: 100%;
  border: none;
  border-radius: 12px;
  background: #2563eb;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
}

.primary-button:disabled {
  opacity: 0.7;
}

.action-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.switch-button {
  min-height: 46px;
  width: 100%;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  background: #fff;
  color: #1e3a8a;
  font-size: 15px;
  font-weight: 600;
}

.switch-button:disabled {
  opacity: 0.7;
}

.error {
  margin: 0;
  color: #dc2626;
  font-size: 14px;
}
</style>
