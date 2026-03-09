import { computed, ref } from "vue";
import { defineStore } from "pinia";

import { fetchProfile, loginWithPassword, register, type WebAuthUser } from "../api/auth";
import { getWebToken, setWebToken } from "../api/http";

type WebRole = "user" | "merchant";

type WebUser = {
  id?: number;
  username: string;
  phone?: string | null;
  avatar?: string | null;
  role: WebRole;
  status?: string;
  email?: string;
};

const STORAGE_KEY = "web-auth-user";
const DEMO_PASSWORD = "Password123!";
const DEMO_ACCOUNTS: Record<WebRole, { username: string; phone: string; email: string }> = {
  user: {
    username: "web_demo_user",
    phone: "13700000001",
    email: "web-user@example.com",
  },
  merchant: {
    username: "web_demo_merchant",
    phone: "13700000002",
    email: "web-merchant@example.com",
  },
};

function loadStoredUser(): WebUser {
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return { username: "演示用户", role: "user" };
  }

  try {
    return JSON.parse(raw) as WebUser;
  } catch {
    return { username: "演示用户", role: "user" };
  }
}

export const useWebAuthStore = defineStore("web-auth", () => {
  const user = ref<WebUser>(loadStoredUser());
  const loading = ref(false);

  const role = computed(() => user.value.role);
  const isMerchant = computed(() => user.value.role === "merchant");
  const isAuthenticated = computed(() => Boolean(user.value.id && getWebToken()));

  function persist() {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(user.value));
  }

  function setUser(nextUser: WebAuthUser, token: string) {
    user.value = nextUser;
    persist();
    setWebToken(token);
  }

  async function ensureRoleSession(nextRole: WebRole) {
    loading.value = true;
    try {
      const account = DEMO_ACCOUNTS[nextRole];

      try {
        await register({
          username: account.username,
          password: DEMO_PASSWORD,
          phone: account.phone,
          email: account.email,
          role: nextRole,
        });
      } catch {
        // 账号已存在时继续登录
      }

      const payload = await loginWithPassword({
        username: account.username,
        password: DEMO_PASSWORD,
      });

      setUser(payload.user, payload.token);
      return payload.user;
    } finally {
      loading.value = false;
    }
  }

  async function setRole(nextRole: WebRole) {
    if (user.value.role === nextRole && user.value.id) {
      return user.value;
    }

    return ensureRoleSession(nextRole);
  }

  async function login(payload: { username: string; password: string }) {
    loading.value = true;
    try {
      const authPayload = await loginWithPassword(payload);
      setUser(authPayload.user, authPayload.token);
      return authPayload.user;
    } finally {
      loading.value = false;
    }
  }

  function setUsername(username: string) {
    user.value = {
      ...user.value,
      username,
    };
    persist();
  }

  function setUserProfile(nextUser: WebAuthUser) {
    user.value = nextUser;
    persist();
  }

  async function refreshProfile() {
    const profile = await fetchProfile();
    setUserProfile(profile);
    return profile;
  }

  function logout() {
    user.value = { username: "演示用户", role: "user" };
    window.localStorage.removeItem(STORAGE_KEY);
    setWebToken(null);
  }

  return {
    user,
    loading,
    role,
    isMerchant,
    isAuthenticated,
    login,
    setRole,
    ensureRoleSession,
    setUsername,
    setUserProfile,
    refreshProfile,
    logout,
  };
});
