<template>
  <section class="page-card">
    <div class="page-header">
      <div>
        <h2>个人中心</h2>
        <p>支持资料更新、头像上传和密码修改。</p>
      </div>
    </div>

    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
    <p v-if="successMessage" class="success-text">{{ successMessage }}</p>

    <section class="form-card">
      <h3>基础资料</h3>
      <div class="form-grid">
        <label class="field">
          <span>用户名</span>
          <input v-model.trim="profileForm.username" type="text" />
        </label>
        <label class="field">
          <span>手机号</span>
          <input v-model.trim="profileForm.phone" type="text" />
        </label>
        <label class="field full-width">
          <span>邮箱</span>
          <input v-model.trim="profileForm.email" type="email" />
        </label>
      </div>
      <div class="action-row">
        <button class="primary-button" :disabled="profileSubmitting" @click="submitProfile">保存资料</button>
      </div>
    </section>

    <section class="form-card">
      <h3>头像上传</h3>
      <div class="meta-text">当前头像：{{ authStore.user.avatar || "未上传" }}</div>
      <input type="file" accept="image/*" @change="handleAvatarSelect" />
      <div class="action-row">
        <button class="primary-button" :disabled="avatarSubmitting || !avatarFile" @click="submitAvatar">上传头像</button>
      </div>
    </section>

    <section class="form-card">
      <h3>密码修改</h3>
      <div class="form-grid">
        <label class="field">
          <span>旧密码</span>
          <input v-model="passwordForm.old_password" type="password" />
        </label>
        <label class="field">
          <span>新密码</span>
          <input v-model="passwordForm.new_password" type="password" />
        </label>
      </div>
      <div class="action-row">
        <button class="primary-button" :disabled="passwordSubmitting" @click="submitPassword">修改密码</button>
      </div>
    </section>
  </section>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";

import { fetchProfile, updatePassword, updateProfile, uploadAvatar } from "../../api/auth";
import { useWebAuthStore } from "../../stores/auth";

const authStore = useWebAuthStore();

const errorMessage = ref("");
const successMessage = ref("");
const profileSubmitting = ref(false);
const avatarSubmitting = ref(false);
const passwordSubmitting = ref(false);
const avatarFile = ref<File | null>(null);

const profileForm = reactive({
  username: "",
  phone: "",
  email: "",
});

const passwordForm = reactive({
  old_password: "",
  new_password: "",
});

onMounted(async () => {
  await loadProfile();
});

async function loadProfile() {
  errorMessage.value = "";
  try {
    const profile = await fetchProfile();
    authStore.setUserProfile(profile);
    Object.assign(profileForm, {
      username: profile.username ?? "",
      phone: profile.phone ?? "",
      email: profile.email ?? "",
    });
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载失败";
  }
}

async function submitProfile() {
  profileSubmitting.value = true;
  errorMessage.value = "";
  successMessage.value = "";
  try {
    const profile = await updateProfile(profileForm);
    authStore.setUserProfile(profile);
    successMessage.value = "资料已更新";
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "保存失败";
  } finally {
    profileSubmitting.value = false;
  }
}

function handleAvatarSelect(event: Event) {
  const target = event.target as HTMLInputElement;
  avatarFile.value = target.files?.[0] ?? null;
}

async function submitAvatar() {
  if (!avatarFile.value) {
    return;
  }

  avatarSubmitting.value = true;
  errorMessage.value = "";
  successMessage.value = "";
  try {
    const profile = await uploadAvatar(avatarFile.value);
    authStore.setUserProfile(profile);
    successMessage.value = "头像已更新";
    avatarFile.value = null;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "上传失败";
  } finally {
    avatarSubmitting.value = false;
  }
}

async function submitPassword() {
  passwordSubmitting.value = true;
  errorMessage.value = "";
  successMessage.value = "";
  try {
    await updatePassword(passwordForm);
    Object.assign(passwordForm, { old_password: "", new_password: "" });
    successMessage.value = "密码已更新";
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "修改失败";
  } finally {
    passwordSubmitting.value = false;
  }
}
</script>

<style scoped>
.page-card,
.form-card {
  padding: 24px;
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
}

.form-card {
  margin-top: 20px;
}

.page-header h2,
.form-card h3 {
  margin: 0;
}

.page-header p,
.meta-text {
  margin: 8px 0 0;
  color: #6b7280;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  margin-top: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field.full-width {
  grid-column: 1 / -1;
}

.field input {
  min-height: 40px;
  padding: 0 12px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
}

.action-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.primary-button {
  min-height: 40px;
  padding: 0 16px;
  border: none;
  border-radius: 10px;
  background: #2563eb;
  color: #fff;
}

.error-text {
  margin-top: 16px;
  color: #dc2626;
}

.success-text {
  margin-top: 16px;
  color: #059669;
}
</style>
