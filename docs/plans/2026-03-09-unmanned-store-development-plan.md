# 无人超市管理系统 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 基于已确认的 PRD、数据库设计、接口设计和系统架构，完成无人超市管理系统的前后端落地，实现移动端 H5 用户购物、Web 用户端、Web 商家端、订单库存闭环和图像识别辅助录入。

**Architecture:** 采用单体后端加双形态前端。后端使用 `Django + DRF + MySQL` 统一承载用户、商品、库存、购物车、订单、公告推荐和 YOLO 识别接口；前端统一使用 `Vue 3`，分为移动端 H5 UI 和 Web 后台式 UI。支付使用 mock，图像识别仅做辅助录入。

**Tech Stack:** `Vue 3`, `Vite`, `Vue Router`, `Pinia`, `Axios`, `Element Plus`, `Django`, `Django REST Framework`, `MySQL`, `Pytest`, `YOLO`, `ECharts`

---

### Task 1: 初始化项目骨架

**Files:**
- Create: `backend/manage.py`
- Create: `backend/config/settings.py`
- Create: `backend/config/urls.py`
- Create: `backend/requirements.txt`
- Create: `frontend/mobile/package.json`
- Create: `frontend/web/package.json`
- Create: `README.md`

**Step 1: 初始化后端项目结构**

Create:
- `backend/config/__init__.py`
- `backend/config/settings.py`
- `backend/config/urls.py`
- `backend/config/wsgi.py`

Expected minimal settings include:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
]
```

**Step 2: 初始化前端双项目结构**

Create:
- `frontend/mobile/src/main.ts`
- `frontend/web/src/main.ts`
- `frontend/mobile/src/router/index.ts`
- `frontend/web/src/router/index.ts`

**Step 3: 记录启动方式**

Create `README.md` with:

```md
- backend: `python manage.py runserver`
- frontend mobile: `npm run dev`
- frontend web: `npm run dev`
```

**Step 4: 验证骨架可启动**

Run:
- `cd backend && python manage.py check`
- `cd frontend/mobile && npm run dev`
- `cd frontend/web && npm run dev`

Expected:
- Django check 通过
- 两个前端项目可启动

### Task 2: 实现用户与认证模块

**Files:**
- Create: `backend/apps/users/models.py`
- Create: `backend/apps/users/serializers.py`
- Create: `backend/apps/users/views.py`
- Create: `backend/apps/users/urls.py`
- Create: `backend/apps/users/tests/test_auth.py`
- Modify: `backend/config/settings.py`
- Modify: `backend/config/urls.py`

**Step 1: 写用户模型测试**

Create `backend/apps/users/tests/test_auth.py`:

```python
from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
    def test_create_user_with_role(self):
        user = get_user_model().objects.create_user(
            username="zhangsan",
            password="123456",
            phone="13800000000",
            role="user",
        )
        assert user.username == "zhangsan"
        assert user.role == "user"
```

**Step 2: 运行测试确认失败**

Run:
- `cd backend && pytest apps/users/tests/test_auth.py -v`

Expected:
- FAIL，提示用户模型或 app 未定义

**Step 3: 实现最小用户模型**

Create `backend/apps/users/models.py`:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (("user", "普通用户"), ("merchant", "商家"))
    STATUS_CHOICES = (("enabled", "启用"), ("disabled", "禁用"))

    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="enabled")
    updated_at = models.DateTimeField(auto_now=True)
```

**Step 4: 实现注册、登录、资料接口**

Create:
- `backend/apps/users/serializers.py`
- `backend/apps/users/views.py`

Include endpoints:
- register
- login by password
- login by code
- profile
- avatar upload
- password update

**Step 5: 运行测试确认通过**

Run:
- `cd backend && pytest apps/users/tests/test_auth.py -v`

Expected:
- PASS

### Task 3: 实现分类、商品、库存模型

**Files:**
- Create: `backend/apps/products/models.py`
- Create: `backend/apps/inventory/models.py`
- Create: `backend/apps/products/tests/test_product_models.py`
- Modify: `backend/config/settings.py`

**Step 1: 写商品与库存模型测试**

Create `backend/apps/products/tests/test_product_models.py`:

```python
from django.test import TestCase
from apps.products.models import Category, Product
from apps.inventory.models import Stock


class ProductStockModelTest(TestCase):
    def test_product_has_one_stock_record(self):
        category = Category.objects.create(name="饮料")
        product = Product.objects.create(category=category, name="可乐", price="3.50")
        stock = Stock.objects.create(product=product, quantity=10, alert_threshold=3)
        assert stock.product == product
        assert stock.quantity == 10
```

**Step 2: 运行测试确认失败**

Run:
- `cd backend && pytest apps/products/tests/test_product_models.py -v`

**Step 3: 实现分类、商品、库存、库存日志模型**

Create models matching the database design:
- `Category`
- `Product`
- `Stock`
- `StockLog`

**Step 4: 生成并执行迁移**

Run:
- `cd backend && python manage.py makemigrations`
- `cd backend && python manage.py migrate`

Expected:
- 迁移成功

**Step 5: 再次运行测试**

Run:
- `cd backend && pytest apps/products/tests/test_product_models.py -v`

Expected:
- PASS

### Task 4: 实现购物车模型与结算预览

**Files:**
- Create: `backend/apps/cart/models.py`
- Create: `backend/apps/cart/serializers.py`
- Create: `backend/apps/cart/views.py`
- Create: `backend/apps/cart/tests/test_cart_api.py`
- Modify: `backend/config/urls.py`

**Step 1: 写购物车“同商品数量累加”测试**

```python
def test_add_same_product_accumulates_quantity(api_client, user, product):
    api_client.force_authenticate(user=user)
    api_client.post("/api/cart/items", {"product_id": product.id, "quantity": 1}, format="json")
    response = api_client.post("/api/cart/items", {"product_id": product.id, "quantity": 2}, format="json")
    assert response.status_code == 200
```

**Step 2: 运行失败测试**

Run:
- `cd backend && pytest apps/cart/tests/test_cart_api.py -v`

**Step 3: 实现购物车和购物车项模型**

Implement:
- `Cart`
- `CartItem`

Rule:
- `(cart, product)` 唯一
- 再次加入时累加数量

**Step 4: 实现接口**

Implement endpoints:
- `GET /api/cart`
- `POST /api/cart/items`
- `PUT /api/cart/items/{id}`
- `DELETE /api/cart/items/{id}`
- `POST /api/cart/checkout`

**Step 5: 运行测试**

Run:
- `cd backend && pytest apps/cart/tests/test_cart_api.py -v`

### Task 5: 实现订单与状态流转

**Files:**
- Create: `backend/apps/orders/models.py`
- Create: `backend/apps/orders/services.py`
- Create: `backend/apps/orders/serializers.py`
- Create: `backend/apps/orders/views.py`
- Create: `backend/apps/orders/tests/test_order_flow.py`

**Step 1: 写“提交订单先生成待支付订单”测试**

```python
def test_submit_order_creates_pending_payment_order(api_client, user, cart_item):
    api_client.force_authenticate(user=user)
    response = api_client.post("/api/orders", {
        "item_ids": [cart_item.id],
        "payment_method": "wechat",
        "address_id": None,
    }, format="json")
    assert response.status_code == 200
    assert response.data["data"]["status"] == "pending_payment"
```

**Step 2: 写“取消订单回补库存”测试**

```python
def test_cancel_order_rolls_back_stock(api_client, pending_order, stock):
    original = stock.quantity
    response = api_client.post(f"/api/orders/{pending_order.id}/cancel")
    assert response.status_code == 200
```

**Step 3: 实现订单、订单项、订单服务**

Implement:
- `Order`
- `OrderItem`
- service methods:
  - create_order_from_cart
  - pay_order
  - cancel_order
  - complete_order

**Step 4: 实现接口**

Implement:
- `POST /api/orders`
- `GET /api/orders`
- `GET /api/orders/{id}`
- `POST /api/orders/{id}/pay`
- `POST /api/orders/{id}/cancel`
- `POST /api/admin/orders/{id}/complete`

**Step 5: 运行订单测试**

Run:
- `cd backend && pytest apps/orders/tests/test_order_flow.py -v`

### Task 6: 实现公告与推荐位

**Files:**
- Create: `backend/apps/content/models.py`
- Create: `backend/apps/content/serializers.py`
- Create: `backend/apps/content/views.py`
- Create: `backend/apps/content/tests/test_content_api.py`

**Step 1: 写公告与推荐位测试**

```python
def test_home_returns_latest_announcement_and_recommendations(api_client):
    response = api_client.get("/api/home")
    assert response.status_code == 200
```

**Step 2: 实现模型**

Implement:
- `Announcement`
- `Recommendation`

Rules:
- 公告支持 draft/published
- 推荐位按 `sort_order` 排序
- 同一商品只保留一条推荐记录

**Step 3: 实现接口**

Implement:
- `GET /api/home`
- `GET /api/admin/announcements`
- `POST /api/admin/announcements`
- `PUT /api/admin/announcements/{id}`
- `DELETE /api/admin/announcements/{id}`
- `GET /api/admin/recommendations`
- `POST /api/admin/recommendations`
- `PUT /api/admin/recommendations/{id}`
- `DELETE /api/admin/recommendations/{id}`

**Step 4: 运行测试**

Run:
- `cd backend && pytest apps/content/tests/test_content_api.py -v`

### Task 7: 实现图像识别辅助录入接口

**Files:**
- Create: `backend/apps/vision/services.py`
- Create: `backend/apps/vision/views.py`
- Create: `backend/apps/vision/tests/test_recognize_api.py`

**Step 1: 写识别接口测试**

```python
def test_recognize_returns_candidate_fields(api_client, merchant_user, image_file):
    api_client.force_authenticate(user=merchant_user)
    response = api_client.post("/api/admin/vision/recognize", {"image": image_file})
    assert response.status_code == 200
```

**Step 2: 先写 mock 识别实现**

Implement service:

```python
def recognize_product(image_path):
    return {
        "recognized_name": "示例商品",
        "recommended_category_id": 1,
        "recommended_category_name": "饮料",
        "confidence": "0.90",
    }
```

**Step 3: 接入真实 YOLO 前保持接口稳定**

Requirement:
- 先保证后端接口和前端录入流程可联调
- 后续再替换识别服务内部实现

**Step 4: 运行测试**

Run:
- `cd backend && pytest apps/vision/tests/test_recognize_api.py -v`

### Task 8: 实现移动端 H5 用户端壳和核心页面

**Files:**
- Create: `frontend/mobile/src/views/LoginView.vue`
- Create: `frontend/mobile/src/views/HomeView.vue`
- Create: `frontend/mobile/src/views/ProductListView.vue`
- Create: `frontend/mobile/src/views/CartView.vue`
- Create: `frontend/mobile/src/views/CheckoutView.vue`
- Create: `frontend/mobile/src/views/OrderListView.vue`
- Create: `frontend/mobile/src/stores/auth.ts`
- Create: `frontend/mobile/src/stores/cart.ts`
- Create: `frontend/mobile/src/api/*.ts`

**Step 1: 搭页面路由**

Routes:
- `/login`
- `/`
- `/products`
- `/cart`
- `/checkout`
- `/orders`

**Step 2: 实现登录、首页、商品列表静态页面**

Use current PRD wireframes as baseline.

**Step 3: 接入真实接口**

Connect:
- auth
- home
- products
- cart
- orders

**Step 4: 手动验证主流程**

Expected:
- 登录
- 浏览商品
- 加入购物车
- 下单
- mock 支付
- 查看订单

### Task 9: 实现 Web 后台式 UI 壳

**Files:**
- Create: `frontend/web/src/layouts/AdminLayout.vue`
- Create: `frontend/web/src/router/index.ts`
- Create: `frontend/web/src/stores/auth.ts`
- Create: `frontend/web/src/views/user/*.vue`
- Create: `frontend/web/src/views/admin/*.vue`

**Step 1: 建统一布局**

Layout includes:
- 左侧菜单
- 顶部栏
- 内容区

**Step 2: 实现角色菜单过滤**

Rules:
- `user` sees: 首页、商品浏览、购物车、我的订单、个人中心
- `merchant` sees: 控制台、商品管理、分类管理、库存管理、订单管理、公告推荐、销售统计

**Step 3: 验证角色切换**

Expected:
- 不同角色只看到对应菜单

### Task 10: 实现商家后台核心页面

**Files:**
- Create: `frontend/web/src/views/admin/ProductManageView.vue`
- Create: `frontend/web/src/views/admin/InventoryView.vue`
- Create: `frontend/web/src/views/admin/OrderManageView.vue`
- Create: `frontend/web/src/views/admin/AnnouncementView.vue`
- Create: `frontend/web/src/views/admin/RecommendationView.vue`
- Create: `frontend/web/src/views/admin/StatisticsView.vue`

**Step 1: 商品管理页**

Connect:
- product list
- create/edit
- on shelf/off shelf

**Step 2: 库存管理页**

Connect:
- inventory list
- alert flag
- stock adjust

**Step 3: 订单管理页**

Connect:
- order list
- order detail
- complete order

**Step 4: 公告与推荐位**

Connect:
- announcement CRUD
- recommendation add/sort/delete

**Step 5: 销售统计页**

Connect:
- overview
- hot products
- ECharts rendering

### Task 11: 权限、联调与回归测试

**Files:**
- Create: `backend/apps/common/permissions.py`
- Create: `backend/tests/test_permissions.py`
- Create: `frontend/web/src/router/guards.ts`
- Create: `frontend/mobile/src/router/guards.ts`

**Step 1: 写权限测试**

Test:
- 用户不能访问 `/api/admin/*`
- 商家不能查看他人私有用户数据
- 用户不能查看他人订单

**Step 2: 实现后端权限类**

Implement:
- `IsAuthenticated`
- `IsMerchant`
- `IsOrderOwner`

**Step 3: 实现前端路由守卫**

Rules:
- 未登录跳登录
- 非商家禁止进入商家页面

**Step 4: 跑回归测试**

Run:
- `cd backend && pytest -v`
- `cd frontend/web && npm run build`
- `cd frontend/mobile && npm run build`

Expected:
- 后端测试通过
- 前端构建通过

### Task 12: 文档收尾与答辩材料准备

**Files:**
- Modify: `docs/prd/unmanned-store-prd.md`
- Modify: `docs/design/database-design.md`
- Modify: `docs/design/api-design.md`
- Modify: `docs/design/system-architecture.md`
- Modify: `docs/design/tech-stack.md`
- Create: `docs/demo/demo-script.md`

**Step 1: 清理文档命名**

Rename final docs when implementation stabilizes.

**Step 2: 生成演示脚本**

Create demo flow:
- 用户注册/登录
- 商品浏览与加购
- 下单与支付
- 商家上架商品
- 图像识别辅助录入
- 库存预警
- 销售统计

**Step 3: 最终验证**

Checklist:
- 需求文档和实现一致
- 数据库设计和接口设计一致
- 页面流程可完整演示

**Step 4: 提交**

If git repo is initialized:

```bash
git add .
git commit -m "docs: add unmanned store implementation plan"
```
