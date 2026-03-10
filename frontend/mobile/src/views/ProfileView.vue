<template>
  <div class="page">
    <section class="card">
      <h2>基本信息</h2>
      <label class="field">
        <span>用户名</span>
        <input v-model.trim="profileForm.username" type="text" />
      </label>
      <label class="field">
        <span>手机号</span>
        <input v-model.trim="profileForm.phone" type="text" />
      </label>
      <label class="field">
        <span>邮箱</span>
        <input v-model.trim="profileForm.email" type="email" />
      </label>
      <p v-if="profileError" class="error">{{ profileError }}</p>
      <p v-if="profileSuccess" class="success">{{ profileSuccess }}</p>
      <button class="primary" type="button" :disabled="savingProfile" @click="handleSaveProfile">
        {{ savingProfile ? "保存中..." : "保存基本信息" }}
      </button>
    </section>

    <section class="card">
      <h2>修改头像</h2>
      <div class="avatar-row">
        <div class="preview">{{ avatarPreviewText }}</div>
        <input type="file" accept="image/*" @change="onAvatarChange" />
      </div>
      <p v-if="avatarFileName" class="hint">已选择: {{ avatarFileName }}</p>
      <p v-if="avatarError" class="error">{{ avatarError }}</p>
      <p v-if="avatarSuccess" class="success">{{ avatarSuccess }}</p>
      <button class="primary" type="button" :disabled="savingAvatar || !avatarFile" @click="handleSaveAvatar">
        {{ savingAvatar ? "上传中..." : "保存头像" }}
      </button>
    </section>

    <section class="card">
      <h2>修改密码</h2>
      <label class="field">
        <span>旧密码</span>
        <input v-model="passwordForm.oldPassword" type="password" autocomplete="current-password" />
      </label>
      <label class="field">
        <span>新密码</span>
        <input v-model="passwordForm.newPassword" type="password" autocomplete="new-password" />
      </label>
      <label class="field">
        <span>确认密码</span>
        <input v-model="passwordForm.confirmPassword" type="password" autocomplete="new-password" />
      </label>
      <p v-if="passwordError" class="error">{{ passwordError }}</p>
      <p v-if="passwordSuccess" class="success">{{ passwordSuccess }}</p>
      <button class="primary" type="button" :disabled="savingPassword" @click="handleSavePassword">
        {{ savingPassword ? "更新中..." : "更新密码" }}
      </button>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";

import { updatePassword, updateProfile, uploadAvatar } from "../api/auth";
import { useAuthStore } from "../stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const savingProfile = ref(false);
const savingAvatar = ref(false);
const savingPassword = ref(false);

const profileError = ref("");
const profileSuccess = ref("");
const avatarError = ref("");
const avatarSuccess = ref("");
const passwordError = ref("");
const passwordSuccess = ref("");

const avatarFile = ref<File | null>(null);
const avatarFileName = ref("");

const profileForm = reactive({
  username: "",
  phone: "",
  email: "",
});

const passwordForm = reactive({
  oldPassword: "",
  newPassword: "",
  confirmPassword: "",
});

const avatarPreviewText = computed(() => {
  const userName = authStore.user?.username?.trim();
  return userName ? userName.slice(0, 1).toUpperCase() : "U";
});

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    await router.push("/login");
    return;
  }
  await authStore.refreshProfile();
  profileForm.username = authStore.user?.username ?? "";
  profileForm.phone = authStore.user?.phone ?? "";
  profileForm.email = authStore.user?.email ?? "";
});

function toOptional(value: string) {
  const normalized = value.trim();
  return normalized ? normalized : undefined;
}

function resetMessages() {
  profileError.value = "";
  profileSuccess.value = "";
  avatarError.value = "";
  avatarSuccess.value = "";
  passwordError.value = "";
  passwordSuccess.value = "";
}

async function handleSaveProfile() {
  resetMessages();
  savingProfile.value = true;
  try {
    const nextUser = await updateProfile({
      username: profileForm.username,
      phone: toOptional(profileForm.phone),
      email: toOptional(profileForm.email),
    });
    authStore.user = nextUser;
    window.localStorage.setItem("mobile-auth-user", JSON.stringify(nextUser));
    profileSuccess.value = "基本信息已更新";
  } catch (error) {
    profileError.value = error instanceof Error ? error.message : "保存失败";
  } finally {
    savingProfile.value = false;
  }
}

function onAvatarChange(event: Event) {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0] ?? null;
  avatarFile.value = file;
  avatarFileName.value = file?.name ?? "";
}

async function handleSaveAvatar() {
  if (!avatarFile.value) {
    avatarError.value = "请先选择头像文件";
    return;
  }
  resetMessages();
  savingAvatar.value = true;
  try {
    const nextUser = await uploadAvatar(avatarFile.value);
    authStore.user = nextUser;
    window.localStorage.setItem("mobile-auth-user", JSON.stringify(nextUser));
    avatarSuccess.value = "头像已更新";
    avatarFile.value = null;
    avatarFileName.value = "";
  } catch (error) {
    avatarError.value = error instanceof Error ? error.message : "头像上传失败";
  } finally {
    savingAvatar.value = false;
  }
}

async function handleSavePassword() {
  resetMessages();
  if (!passwordForm.oldPassword || !passwordForm.newPassword) {
    passwordError.value = "请填写旧密码和新密码";
    return;
  }
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    passwordError.value = "两次输入的新密码不一致";
    return;
  }
  savingPassword.value = true;
  try {
    await updatePassword({
      old_password: passwordForm.oldPassword,
      new_password: passwordForm.newPassword,
    });
    passwordSuccess.value = "密码已更新";
    passwordForm.oldPassword = "";
    passwordForm.newPassword = "";
    passwordForm.confirmPassword = "";
  } catch (error) {
    passwordError.value = error instanceof Error ? error.message : "密码更新失败";
  } finally {
    savingPassword.value = false;
  }
}
</script>

<style scoped>
.page {
  padding: 0 0 20px;
  box-sizing: border-box;
}

.card {
  margin-top: 14px;
  padding: 16px;
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}

.card h2 {
  margin: 0 0 14px;
  font-size: 18px;
  color: #0f172a;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
  color: #334155;
  font-size: 14px;
}

.field input {
  min-height: 42px;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  padding: 0 12px;
}

.avatar-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.preview {
  width: 56px;
  height: 56px;
  border-radius: 999px;
  background: #dbeafe;
  color: #1d4ed8;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  font-size: 22px;
  font-weight: 700;
}

.hint {
  margin: 10px 0 8px;
  font-size: 13px;
  color: #64748b;
}

.primary {
  width: 100%;
  min-height: 44px;
  border: none;
  border-radius: 10px;
  background: #2563eb;
  color: #fff;
  font-size: 15px;
  font-weight: 700;
}

.error {
  margin: 4px 0 10px;
  color: #dc2626;
  font-size: 13px;
}

.success {
  margin: 4px 0 10px;
  color: #059669;
  font-size: 13px;
}
</style>
