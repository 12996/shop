# PRD V2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 按 `docs/prd/unmanned-store-prd-v2.md` 落地 V2 需求，补齐注册入口、头像展示、首页商品发现、公告详情、商品详情评论、商家分类管理、商品图片文件上传和推荐轮播文案。

**Architecture:** 后端继续使用 `Django + DRF` 提供真实数据接口，通过新增迁移、模型字段、序列化器和 API 扩展来承载分类、公告详情、评论与图片上传。前端继续使用现有 `Vue 3 + Vite + Pinia + Vue Router` 双端结构，Web 端承担完整用户端/商家端能力，移动端补齐注册与用户首页/商品详情核心链路。

**Tech Stack:** `Django`, `Django REST Framework`, `pytest`, `Vue 3`, `Vite`, `Vue Router`, `Pinia`, `TypeScript`

---

### Task 1: 注册入口与头像展示

**Files:**
- Modify: `frontend/web/src/router/index.ts`
- Modify: `frontend/web/src/views/LoginView.vue`
- Modify: `frontend/web/src/views/user/UserProfileView.vue`
- Modify: `frontend/web/src/layouts/AdminLayout.vue`
- Modify: `frontend/web/src/stores/auth.ts`
- Modify: `frontend/web/src/api/auth.ts`
- Modify: `frontend/mobile/src/router/index.ts`
- Modify: `frontend/mobile/src/views/LoginView.vue`
- Create: `frontend/mobile/src/views/RegisterView.vue`
- Modify: `frontend/mobile/src/stores/auth.ts`
- Modify: `frontend/mobile/src/api/auth.ts`
- Modify: `backend/apps/users/tests/test_api_auth.py`
- Modify: `backend/apps/users/views.py`
- Modify: `backend/apps/users/serializers.py`

**Step 1: Write the failing backend auth API tests**

Add tests in `backend/apps/users/tests/test_api_auth.py` covering:

- Web/mobile registration payload with `username`, `phone`, `password`, `confirm_password`
- registration success returns authenticated payload
- avatar upload/profile response includes avatar path for layout rendering

**Step 2: Run the auth API tests to verify they fail**

Run:
```powershell
conda run -n shop python -m pytest .\backend\apps\users\tests\test_api_auth.py -v
```

Expected:
- FAIL on missing `confirm_password` validation and/or missing registration response behavior

**Step 3: Implement the minimal backend changes**

In `backend/apps/users/serializers.py` and `backend/apps/users/views.py`:

- validate `confirm_password`
- ensure register returns the same user payload shape needed by current auth store
- keep avatar/profile serialization stable for both top nav and sidebar

**Step 4: Add the front-end registration routes and views**

Implement:

- Web login page includes “去注册” entry and register form/page or mode
- Mobile login page includes “立即注册” entry
- Mobile router gets a register route
- both clients auto-login and redirect to home on successful registration

**Step 5: Add avatar rendering in the layout and profile flow**

Update `frontend/web/src/layouts/AdminLayout.vue` and auth/profile store logic to:

- show current user avatar in left sidebar user card
- show current user avatar in top right nav
- fallback to a default avatar when `avatar` is empty

**Step 6: Run focused verification**

Run:
```powershell
conda run -n shop python -m pytest .\backend\apps\users\tests\test_api_auth.py -v
```

Expected:
- PASS

**Step 7: Commit**

```powershell
git add backend/apps/users frontend/web/src frontend/mobile/src
git commit -m "feat: add registration entry points and avatar display"
```

### Task 2: 首页公告气泡、推荐轮播与全部商品列表

**Files:**
- Modify: `backend/apps/content/tests/test_content_api.py`
- Modify: `backend/apps/content/models.py`
- Modify: `backend/apps/content/serializers.py`
- Modify: `backend/apps/content/views.py`
- Modify: `backend/apps/content/urls.py`
- Modify: `frontend/web/src/views/user/UserHomeView.vue`
- Modify: `frontend/web/src/api/home.ts`
- Modify: `frontend/mobile/src/views/HomeView.vue`
- Modify: `frontend/mobile/src/api/home.ts`
- Create: `frontend/web/src/views/user/UserAnnouncementDetailView.vue`
- Create: `frontend/mobile/src/views/AnnouncementDetailView.vue`
- Modify: `frontend/web/src/router/index.ts`
- Modify: `frontend/mobile/src/router/index.ts`

**Step 1: Write the failing content API tests**

Add tests for:

- home endpoint returning current announcement + recommended items + full on-shelf product list
- announcement detail endpoint returning title and full content
- recommendation payload carrying merchant-maintained promo copy

**Step 2: Run the content tests to verify failure**

Run:
```powershell
conda run -n shop python -m pytest .\backend\apps\content\tests\test_content_api.py -v
```

Expected:
- FAIL because home payload and announcement detail route do not yet satisfy V2

**Step 3: Implement backend content changes**

Extend `backend/apps/content` to:

- add `promo_text` (or equivalent) to recommendation data model via migration
- expose announcement detail endpoint for front-end reading
- adjust home aggregation so it returns:
  - the current published announcement
  - enabled recommendations with product image + promo text
  - full on-shelf product list for “全部商品”

**Step 4: Implement Web user home view**

In `frontend/web/src/views/user/UserHomeView.vue`:

- render single rolling bubble announcement
- render recommendation carousel
- place category filter above full product list
- clicking announcement goes to announcement detail page
- clicking recommendation or product card goes to product detail

**Step 5: Implement mobile home parity**

In `frontend/mobile/src/views/HomeView.vue`:

- expose the same logical order:
  - bubble announcement
  - recommendation carousel
  - category filter
  - all products

**Step 6: Run focused verification**

Run:
```powershell
conda run -n shop python -m pytest .\backend\apps\content\tests\test_content_api.py -v
```

Expected:
- PASS

**Step 7: Commit**

```powershell
git add backend/apps/content frontend/web/src/views/user frontend/mobile/src/views
git commit -m "feat: add announcement detail and home merchandising flow"
```

### Task 3: 商品详情页、评论与点赞

**Files:**
- Create: `backend/apps/reviews/__init__.py`
- Create: `backend/apps/reviews/apps.py`
- Create: `backend/apps/reviews/models.py`
- Create: `backend/apps/reviews/serializers.py`
- Create: `backend/apps/reviews/views.py`
- Create: `backend/apps/reviews/urls.py`
- Create: `backend/apps/reviews/tests/test_review_api.py`
- Modify: `backend/config/settings.py`
- Modify: `backend/config/urls.py`
- Modify: `backend/apps/orders/models.py`
- Modify: `frontend/web/src/api/products.ts`
- Modify: `frontend/mobile/src/api/products.ts`
- Modify: `frontend/web/src/views/user/UserProductView.vue`
- Create: `frontend/web/src/views/user/UserProductDetailView.vue`
- Modify: `frontend/web/src/router/index.ts`
- Modify: `frontend/mobile/src/views/ProductListView.vue`
- Create: `frontend/mobile/src/views/ProductDetailView.vue`
- Modify: `frontend/mobile/src/router/index.ts`

**Step 1: Write the failing review API tests**

Create `backend/apps/reviews/tests/test_review_api.py` covering:

- purchased user can create a review
- non-purchased user cannot create a review
- same user can create multiple reviews for the same product
- review list is ordered by like count desc, then created time desc
- authenticated user can like a review

**Step 2: Run the review API tests to verify failure**

Run:
```powershell
conda run -n shop python -m pytest .\backend\apps\reviews\tests\test_review_api.py -v
```

Expected:
- FAIL because the review app and endpoints do not exist yet

**Step 3: Implement minimal review backend**

Add `reviews` app with:

- review model linked to user and product
- like-count support
- purchased-user eligibility check based on paid/completed orders
- list/create/like endpoints

**Step 4: Expose product detail endpoints to include review data**

Update product APIs so product detail can drive:

- gallery/main image
- pricing/description/inventory
- review list and comment entry state

**Step 5: Implement Web product detail UI**

Create `frontend/web/src/views/user/UserProductDetailView.vue` and route it from home/list pages.

Include:

- product core info
- add-to-cart
- review composer gated by purchase eligibility
- review list sorted by backend order
- like button

**Step 6: Implement mobile product detail UI**

Create `frontend/mobile/src/views/ProductDetailView.vue` with the same essential behaviors.

**Step 7: Run focused verification**

Run:
```powershell
conda run -n shop python -m pytest .\backend\apps\reviews\tests\test_review_api.py -v
```

Expected:
- PASS

**Step 8: Commit**

```powershell
git add backend/apps/reviews backend/config frontend/web/src frontend/mobile/src
git commit -m "feat: add product detail reviews and likes"
```

### Task 4: 商家分类管理

**Files:**
- Modify: `backend/apps/products/tests/test_admin_product_api.py`
- Create: `backend/apps/products/tests/test_category_admin_api.py`
- Modify: `backend/apps/products/serializers.py`
- Modify: `backend/apps/products/views.py`
- Modify: `backend/apps/products/urls.py`
- Modify: `frontend/web/src/views/admin/CategoryManageView.vue`
- Modify: `frontend/web/src/api/products.ts`

**Step 1: Write the failing category admin tests**

Cover:

- merchant can list categories
- merchant can create category
- merchant can update category
- merchant can enable/disable category
- merchant can reorder categories

**Step 2: Run the category tests to verify failure**

Run:
```powershell
conda run -n shop python -m pytest .\backend\apps\products\tests\test_category_admin_api.py -v
```

Expected:
- FAIL because admin category APIs are incomplete or missing

**Step 3: Implement backend category admin endpoints**

Add endpoints under `backend/apps/products/urls.py` and `views.py` for:

- admin category list/create
- admin category update
- admin category enable/disable
- admin category reorder

**Step 4: Implement Web category management UI**

Update `frontend/web/src/views/admin/CategoryManageView.vue` to include:

- category table
- create/edit form
- enable/disable actions
- ordering actions

**Step 5: Wire product form to existing enabled categories only**

Ensure product management page consumes only enabled categories and blocks creation when category list is empty.

**Step 6: Run focused verification**

Run:
```powershell
conda run -n shop python -m pytest .\backend\apps\products\tests\test_category_admin_api.py -v
conda run -n shop python -m pytest .\backend\apps\products\tests\test_admin_product_api.py -v
```

Expected:
- PASS

**Step 7: Commit**

```powershell
git add backend/apps/products frontend/web/src/views/admin
git commit -m "feat: add merchant category management"
```

### Task 5: 商品主图文件上传替代图片链接

**Files:**
- Modify: `backend/apps/products/tests/test_admin_product_api.py`
- Modify: `backend/apps/products/models.py`
- Create: `backend/apps/products/migrations/0003_product_image_uploads.py`
- Modify: `backend/apps/products/serializers.py`
- Modify: `backend/apps/products/views.py`
- Modify: `backend/config/settings.py`
- Modify: `frontend/web/src/views/admin/ProductManageView.vue`
- Modify: `frontend/web/src/api/products.ts`

**Step 1: Write the failing admin product upload tests**

Extend admin product tests to cover:

- create product with uploaded image file
- reject plain image URL text input path at UI/API contract level

**Step 2: Run the admin product tests to verify failure**

Run:
```powershell
conda run -n shop python -m pytest .\backend\apps\products\tests\test_admin_product_api.py -v
```

Expected:
- FAIL because product create/update currently expects string URLs

**Step 3: Implement backend image upload support**

Update product persistence to use a real upload field or managed file-path flow.

Requirements:

- API accepts multipart upload for product image
- product response still returns a usable image URL/path
- image-recognition flow, if still present later, must consume uploaded file input

**Step 4: Replace Web merchant product form input**

In `frontend/web/src/views/admin/ProductManageView.vue`:

- remove text input for image URL
- add file picker/upload control
- show uploaded preview

**Step 5: Run focused verification**

Run:
```powershell
conda run -n shop python -m pytest .\backend\apps\products\tests\test_admin_product_api.py -v
```

Expected:
- PASS

**Step 6: Commit**

```powershell
git add backend/apps/products backend/config frontend/web/src/views/admin/ProductManageView.vue
git commit -m "feat: support merchant product image uploads"
```

### Task 6: 推荐轮播文案与公告详情前台联动

**Files:**
- Modify: `backend/apps/content/tests/test_content_api.py`
- Modify: `backend/apps/content/serializers.py`
- Modify: `backend/apps/content/views.py`
- Modify: `frontend/web/src/views/admin/RecommendationView.vue`
- Modify: `frontend/web/src/api/content.ts`
- Modify: `frontend/web/src/views/user/UserHomeView.vue`

**Step 1: Write the failing recommendation copy tests**

Add tests for:

- merchant can create/update recommendation promo text
- home payload includes promo text for carousel rendering

**Step 2: Run tests to verify failure**

Run:
```powershell
conda run -n shop python -m pytest .\backend\apps\content\tests\test_content_api.py -v
```

Expected:
- FAIL on missing promo text persistence/serialization

**Step 3: Implement backend promo text support**

Extend `Recommendation` model/serializer/view logic to persist promo copy and expose it in home/admin payloads.

**Step 4: Implement admin recommendation form changes**

Update `frontend/web/src/views/admin/RecommendationView.vue` to:

- edit promo text
- keep using product image as banner image source

**Step 5: Run focused verification**

Run:
```powershell
conda run -n shop python -m pytest .\backend\apps\content\tests\test_content_api.py -v
```

Expected:
- PASS

**Step 6: Commit**

```powershell
git add backend/apps/content frontend/web/src/views/admin/RecommendationView.vue frontend/web/src/views/user/UserHomeView.vue
git commit -m "feat: add recommendation promo copy"
```

### Task 7: Cross-page polish, docs, and regression verification

**Files:**
- Modify: `README.md`
- Modify: `docs/demo/demo-script.md`
- Modify: `docs/design/api-design.md`
- Modify: `docs/prd/unmanned-store-prd-v2.md` (if implementation clarifies any accepted wording)

**Step 1: Update user-facing docs**

Reflect:

- register entry in both user clients
- announcement detail page
- product detail + review flow
- category admin support
- product image upload

**Step 2: Run Django validation**

Run:
```powershell
conda run -n shop python .\backend\manage.py check
```

Expected:
- PASS

**Step 3: Run the full targeted backend regression suite**

Run:
```powershell
conda run -n shop python -m pytest .\backend\apps\users\tests\test_api_auth.py .\backend\apps\content\tests\test_content_api.py .\backend\apps\products\tests\test_admin_product_api.py .\backend\apps\products\tests\test_product_api.py .\backend\apps\inventory\tests\test_inventory_api.py .\backend\apps\reviews\tests\test_review_api.py -v
```

Expected:
- PASS

**Step 4: Optional front-end build verification**

Run:
```powershell
cd frontend/web
npm run build
cd ..\mobile
npm run build
```

Expected:
- PASS

**Step 5: Commit**

```powershell
git add README.md docs
git commit -m "docs: update v2 implementation and demo guidance"
```
