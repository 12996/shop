<template>
  <section class="page-card">
    <div class="page-header">
      <div>
        <h2>公告管理</h2>
        <p>维护首页公告内容，支持新增、编辑和删除。</p>
      </div>
      <button class="primary-button" @click="startCreate">新增公告</button>
    </div>

    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

    <section class="form-card">
      <div class="form-grid">
        <label class="field full-width">
          <span>公告标题</span>
          <input v-model.trim="form.title" type="text" />
        </label>
        <label class="field">
          <span>状态</span>
          <select v-model="form.status">
            <option value="draft">草稿</option>
            <option value="published">已发布</option>
          </select>
        </label>
        <label class="field full-width">
          <span>公告内容</span>
          <textarea v-model.trim="form.content" rows="4" />
        </label>
      </div>

      <div class="form-actions">
        <button class="primary-button" :disabled="submitting" @click="submitForm">
          {{ submitting ? "处理中..." : editingId ? "保存修改" : "创建公告" }}
        </button>
        <button v-if="editingId" class="ghost-button" @click="startCreate">取消编辑</button>
      </div>
    </section>

    <section class="table-card">
      <div v-if="loading" class="state-text">加载中...</div>
      <div v-else-if="items.length === 0" class="state-text">暂无公告</div>

      <table v-else class="table">
        <thead>
          <tr>
            <th>标题</th>
            <th>状态</th>
            <th>发布时间</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.title }}</td>
            <td>{{ item.status === "published" ? "已发布" : "草稿" }}</td>
            <td>{{ item.published_at ? formatDate(item.published_at) : "-" }}</td>
            <td>{{ formatDate(item.created_at) }}</td>
            <td class="actions">
              <button class="inline-button" @click="startEdit(item)">编辑</button>
              <button class="inline-button danger" @click="removeItem(item.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </section>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";

import {
  createAnnouncement,
  deleteAnnouncement,
  fetchAnnouncements,
  updateAnnouncement,
  type Announcement,
  type AnnouncementPayload,
} from "../../api/content";
import { useWebAuthStore } from "../../stores/auth";

const authStore = useWebAuthStore();

const loading = ref(false);
const submitting = ref(false);
const editingId = ref<number | null>(null);
const errorMessage = ref("");
const items = ref<Announcement[]>([]);

const form = reactive<AnnouncementPayload>({
  title: "",
  content: "",
  status: "draft",
});

onMounted(async () => {
  await authStore.ensureRoleSession("merchant");
  await loadItems();
});

async function loadItems() {
  loading.value = true;
  errorMessage.value = "";

  try {
    items.value = await fetchAnnouncements();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "加载失败";
  } finally {
    loading.value = false;
  }
}

function startCreate() {
  editingId.value = null;
  Object.assign(form, {
    title: "",
    content: "",
    status: "draft",
  });
}

function startEdit(item: Announcement) {
  editingId.value = item.id;
  Object.assign(form, {
    title: item.title,
    content: item.content,
    status: item.status,
  });
}

async function submitForm() {
  submitting.value = true;
  errorMessage.value = "";

  try {
    if (editingId.value) {
      await updateAnnouncement(editingId.value, form);
    } else {
      await createAnnouncement(form);
    }
    await loadItems();
    startCreate();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "提交失败";
  } finally {
    submitting.value = false;
  }
}

async function removeItem(id: number) {
  try {
    await deleteAnnouncement(id);
    await loadItems();
    if (editingId.value === id) {
      startCreate();
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "删除失败";
  }
}

function formatDate(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleString("zh-CN", { hour12: false });
}
</script>

<style scoped>
.page-card,
.form-card,
.table-card {
  padding: 24px;
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.page-header h2 {
  margin: 0;
}

.page-header p {
  margin: 8px 0 0;
  color: #6b7280;
}

.form-card,
.table-card {
  margin-top: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field.full-width {
  grid-column: 1 / -1;
}

.field input,
.field select,
.field textarea {
  min-height: 40px;
  padding: 0 12px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font: inherit;
}

.field textarea {
  min-height: 100px;
  padding: 12px;
}

.form-actions,
.actions {
  display: flex;
  gap: 8px;
}

.form-actions {
  margin-top: 16px;
}

.primary-button,
.ghost-button,
.inline-button {
  min-height: 38px;
  padding: 0 14px;
  border: none;
  border-radius: 10px;
}

.primary-button,
.inline-button {
  background: #2563eb;
  color: #fff;
}

.ghost-button {
  background: #e5e7eb;
  color: #111827;
}

.inline-button.danger {
  background: #fee2e2;
  color: #b91c1c;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 12px 8px;
  border-bottom: 1px solid #e5e7eb;
  text-align: left;
}

.error-text,
.state-text {
  margin-top: 16px;
}

.error-text {
  color: #dc2626;
}

.state-text {
  color: #6b7280;
}
</style>
