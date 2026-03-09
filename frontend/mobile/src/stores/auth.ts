import { computed, ref } from "vue";
import { defineStore } from "pinia";

import { fetchProfile, loginWithCode, loginWithPassword, type AuthUser } from "../api/auth";

const TOKEN_KEY = "mobile-auth-token";
const USER_KEY = "mobile-auth-user";

function loadStoredUser(): AuthUser | null {
  const raw = window.localStorage.getItem(USER_KEY);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw) as AuthUser;
  } catch {
    window.localStorage.removeItem(USER_KEY);
    return null;
  }
}

export const useAuthStore = defineStore("mobile-auth", () => {
  const token = ref<string | null>(window.localStorage.getItem(TOKEN_KEY));
  const user = ref<AuthUser | null>(loadStoredUser());
  const loading = ref(false);

  const isAuthenticated = computed(() => Boolean(token.value && user.value));

  function persistSession(nextToken: string | null, nextUser: AuthUser | null) {
    token.value = nextToken;
    user.value = nextUser;

    if (nextToken) {
      window.localStorage.setItem(TOKEN_KEY, nextToken);
    } else {
      window.localStorage.removeItem(TOKEN_KEY);
    }

    if (nextUser) {
      window.localStorage.setItem(USER_KEY, JSON.stringify(nextUser));
    } else {
      window.localStorage.removeItem(USER_KEY);
    }
  }

  async function loginByPassword(username: string, password: string) {
    loading.value = true;
    try {
      const payload = await loginWithPassword({ username, password });
      persistSession(payload.token, payload.user);
      return payload.user;
    } finally {
      loading.value = false;
    }
  }

  async function loginByCode(phone: string, code: string) {
    loading.value = true;
    try {
      const payload = await loginWithCode({ phone, code });
      persistSession(payload.token, payload.user);
      return payload.user;
    } finally {
      loading.value = false;
    }
  }

  async function refreshProfile() {
    if (!token.value) {
      return null;
    }

    try {
      const profile = await fetchProfile();
      persistSession(token.value, profile);
      return profile;
    } catch {
      persistSession(null, null);
      return null;
    }
  }

  function logout() {
    persistSession(null, null);
  }

  return {
    token,
    user,
    loading,
    isAuthenticated,
    loginByPassword,
    loginByCode,
    refreshProfile,
    logout,
  };
});
