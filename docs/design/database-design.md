# 无人超市管理系统：数据库与类设计文档

> 状态：当前实现版  
> 说明：该文档用于承载数据库设计、领域类定义和后端实现映射，不放入 PRD 正文。

## 1. 设计目标

- 将需求文档与实现设计解耦
- 为 `Django` 后端建模提供直接参考
- 为后续数据库表设计、类设计、接口设计提供统一基础

## 2. 设计范围

- 数据库核心表
- 主要领域对象 / 类定义
- 关键表关系
- 订单地址预留策略
- 推荐位排序策略
- 图像识别辅助录入的数据边界

## 3. 数据库设计

### 3.1 用户相关

#### `users_user`
- `id`
- `username`：用户名，登录用
- `password`：密码哈希
- `phone`：手机号
- `avatar`：头像路径
- `role`：角色，`user` / `merchant`
- `status`：启用 / 禁用
- `created_at`
- `updated_at`

说明：
- 用户和商家共用一张用户表，使用 `role` 区分身份
- 用户支持头像上传与密码修改
- `username` 唯一
- `phone` 可为空，但填写后必须唯一

#### `users_address`
- `id`
- `user_id`
- `receiver_name`
- `receiver_phone`
- `province`
- `city`
- `detail_address`
- `is_default`
- `created_at`
- `updated_at`

说明：
- 当前店内自助购物场景下地址允许为空
- 该表作为后续配送场景的预留能力

### 3.2 商品与分类

#### `products_category`
- `id`
- `name`
- `sort_order`
- `status`
- `created_at`
- `updated_at`

#### `products_product`
- `id`
- `category_id`
- `name`
- `main_image`
- `description`
- `price`
- `status`：上架 / 下架
- `created_at`
- `updated_at`

说明：
- 商品表只保存商品基础信息
- 不直接保存库存数量
- 商品名称不强制唯一
- 商品不建议物理删除，采用下架处理

### 3.3 库存相关

#### `inventory_stock`
- `id`
- `product_id`
- `quantity`
- `alert_threshold`
- `updated_at`

#### `inventory_stock_log`
- `id`
- `product_id`
- `change_type`：入库 / 出库 / 回补 / 人工调整
- `change_amount`
- `before_qty`
- `after_qty`
- `operator_id`
- `remark`
- `created_at`

说明：
- 库存独立成表，用于支撑库存校验、库存预警和库存变更追踪
- 库存日志用于追踪每次库存变化原因
- `product_id` 唯一，保证一个商品只对应一条当前库存记录
- `quantity >= 0`
- `alert_threshold >= 0`

### 3.4 购物车相关

#### `cart_cart`
- `id`
- `user_id`
- `created_at`
- `updated_at`

#### `cart_cart_item`
- `id`
- `cart_id`
- `product_id`
- `quantity`
- `selected`
- `created_at`
- `updated_at`

说明：
- 购物车与订单分离
- `selected` 用于支持部分商品结算
- 一个用户只保留一个购物车
- 同一商品在同一购物车中只保留一条记录
- 再次加入购物车时直接累加数量

### 3.5 订单相关

#### `orders_order`
- `id`
- `order_number`
- `user_id`
- `total_amount`
- `pay_amount`
- `status`：`待支付` / `已支付` / `已完成` / `已取消`
- `payment_method`
- `address_id`：可空
- `address_snapshot`：可空
- `created_at`
- `paid_at`
- `completed_at`
- `cancelled_at`

说明：
- 订单在用户点击“提交订单”时生成
- 当前场景下 `address_id` 可为空
- 建议保留 `address_snapshot`，避免用户后续修改地址影响历史订单
- `order_number` 唯一
- 已取消订单不可重新支付，用户需重新下单

#### `orders_order_item`
- `id`
- `order_id`
- `product_id`
- `product_name`
- `product_image`
- `product_price`
- `quantity`
- `subtotal`

说明：
- 订单项必须保存商品快照
- 避免商品后续修改影响历史订单展示

### 3.6 内容管理相关

#### `content_announcement`
- `id`
- `title`
- `content`
- `status`
- `publisher_id`
- `published_at`
- `created_at`
- `updated_at`

#### `content_recommendation`
- `id`
- `product_id`
- `sort_order`
- `status`
- `created_at`
- `updated_at`

说明：
- 推荐商品单独成表
- `sort_order` 用于控制商品在首页推荐区域的展示顺序
- 同一商品同一时间只保留一条有效推荐记录
- 取消推荐时直接删除推荐记录
- 首页默认展示最新 1 条公告，点击“更多”查看公告列表

### 3.7 图像识别相关

#### 可选表：`vision_recognition_record`
- `id`
- `image_path`
- `recognized_name`
- `recommended_category_id`
- `confidence`
- `raw_result`
- `operator_id`
- `created_at`

说明：
- 该表是可选扩展表
- 第一版实现可以不落库
- 若后续需要保留识别历史或追踪识别效果，可启用该表

## 4. 关键关系

- 一个 `User` 可拥有多个 `Order`
- 一个 `User` 可拥有多个 `Address`
- 一个 `User` 对应一个 `Cart`
- 一个 `Cart` 对应多个 `CartItem`
- 一个 `Category` 对应多个 `Product`
- 一个 `Product` 对应一个当前 `Stock`
- 一个 `Product` 对应多个 `StockLog`
- 一个 `Order` 对应多个 `OrderItem`
- 一个 `Product` 可对应多个 `Recommendation` 记录（按业务约束通常只保留有效的一条）

## 5. 领域类定义建议

### 5.1 用户域

#### `User`
- 属性：`id`, `username`, `phone`, `avatar`, `role`, `status`
- 行为：
  - `change_password()`
  - `update_profile()`
  - `upload_avatar()`

#### `Address`
- 属性：`receiver_name`, `receiver_phone`, `province`, `city`, `detail_address`, `is_default`
- 行为：
  - `set_default()`

### 5.2 商品域

#### `Category`
- 属性：`name`, `sort_order`, `status`

#### `Product`
- 属性：`name`, `category`, `main_image`, `description`, `price`, `status`
- 行为：
  - `on_shelf()`
  - `off_shelf()`
  - `update_info()`

#### `Stock`
- 属性：`product`, `quantity`, `alert_threshold`
- 行为：
  - `increase()`
  - `decrease()`
  - `rollback()`
  - `is_alerting()`
  - `is_available(quantity)`

### 5.3 购物车域

#### `Cart`
- 属性：`user`
- 行为：
  - `add_item(product, quantity)`
  - `remove_item(item_id)`
  - `update_item_quantity(item_id, quantity)`
  - `get_selected_items()`

#### `CartItem`
- 属性：`product`, `quantity`, `selected`

### 5.4 订单域

#### `Order`
- 属性：`order_no`, `user`, `total_amount`, `pay_amount`, `status`, `payment_method`, `address`
- 行为：
  - `create_from_cart()`
  - `pay()`
  - `cancel()`
  - `complete()`
  - `is_payable()`

#### `OrderItem`
- 属性：`product_id`, `product_name`, `product_image`, `product_price`, `quantity`, `subtotal`

### 5.5 内容域

#### `Announcement`
- 属性：`title`, `content`, `status`, `publisher`
- 行为：
  - `publish()`
  - `unpublish()`

#### `Recommendation`
- 属性：`product`, `sort_order`, `status`
- 行为：
  - `move_up()`
  - `move_down()`
  - `update_sort_order()`

### 5.6 图像识别域

#### `RecognitionService`
- 职责：
  - 接收商品图片
  - 调用 `YOLO` 模型识别
  - 返回商品名称候选、推荐分类、置信度

说明：
- 图像识别建议实现为服务对象，而不是核心业务实体
- 第一版重点是“辅助录入”，不直接自动上架

## 6. 关键设计决策

- 用户和商家共用用户表，降低实现复杂度
- 商品和库存拆表，便于库存预警与日志追踪
- 订单必须保存商品快照
- 地址信息保留但可空，兼容当前店内自助购物场景
- 推荐位使用排序字段控制首页展示位置
- 图像识别作为辅助服务，不作为核心实体依赖
- 分类采用单级分类
- 商品销量不直接存表，通过订单项统计得到

## 7. 约束、索引与删除策略

### 7.1 唯一约束
- `users_user.username`
- `users_user.phone`
- `products_category.name`
- `inventory_stock.product_id`
- `cart_cart.user_id`
- `cart_cart_item (cart_id, product_id)` 联合唯一
- `orders_order.order_number`
- `content_recommendation.product_id`

### 7.2 建议索引
- `orders_order.user_id`
- `orders_order.status`
- `orders_order.created_at`
- `orders_order_item.order_id`
- `products_product.category_id`
- `products_product.status`
- `inventory_stock.quantity`
- `content_announcement.status`
- `content_recommendation.sort_order`

### 7.3 删除策略
- 用户：一般不物理删除，采用禁用账号
- 地址：允许删除；历史订单依赖 `address_snapshot`
- 商品：不物理删除，采用下架
- 分类：不物理删除，采用禁用
- 公告：允许物理删除
- 推荐位：取消推荐时直接删除记录
- 订单：不物理删除
- 订单项：不物理删除
- 库存日志：不物理删除

## 8. 后续可继续补充

- 字段类型与长度约束
- 主键 / 外键 / 唯一索引设计
- Django `models.py` 草案
- 数据库 E-R 图
- 接口与模型映射关系

## 8. 数据库 E-R 图

```mermaid
erDiagram
    USERS_USER ||--o{ USERS_ADDRESS : has
    USERS_USER ||--|| CART_CART : owns
    USERS_USER ||--o{ ORDERS_ORDER : places
    USERS_USER ||--o{ INVENTORY_STOCK_LOG : operates
    USERS_USER ||--o{ CONTENT_ANNOUNCEMENT : publishes

    PRODUCTS_CATEGORY ||--o{ PRODUCTS_PRODUCT : contains
    PRODUCTS_PRODUCT ||--|| INVENTORY_STOCK : has
    PRODUCTS_PRODUCT ||--o{ INVENTORY_STOCK_LOG : records
    PRODUCTS_PRODUCT ||--o{ CART_CART_ITEM : selected_in
    PRODUCTS_PRODUCT ||--o{ CONTENT_RECOMMENDATION : recommended_as

    CART_CART ||--o{ CART_CART_ITEM : contains

    ORDERS_ORDER ||--o{ ORDERS_ORDER_ITEM : contains
    USERS_ADDRESS ||--o{ ORDERS_ORDER : referenced_by

    USERS_USER {
        bigint id PK
        varchar username UK
        varchar phone UK
        varchar password
        varchar avatar
        varchar role
        varchar status
        datetime created_at
        datetime updated_at
    }

    USERS_ADDRESS {
        bigint id PK
        bigint user_id FK
        varchar receiver_name
        varchar receiver_phone
        varchar province
        varchar city
        varchar detail_address
        boolean is_default
        datetime created_at
        datetime updated_at
    }

    PRODUCTS_CATEGORY {
        bigint id PK
        varchar name UK
        int sort_order
        varchar status
        datetime created_at
        datetime updated_at
    }

    PRODUCTS_PRODUCT {
        bigint id PK
        bigint category_id FK
        varchar name
        varchar main_image
        text description
        decimal price
        varchar status
        datetime created_at
        datetime updated_at
    }

    INVENTORY_STOCK {
        bigint id PK
        bigint product_id FK_UK
        int quantity
        int alert_threshold
        datetime updated_at
    }

    INVENTORY_STOCK_LOG {
        bigint id PK
        bigint product_id FK
        bigint operator_id FK
        varchar change_type
        int change_amount
        int before_qty
        int after_qty
        varchar remark
        datetime created_at
    }

    CART_CART {
        bigint id PK
        bigint user_id FK_UK
        datetime created_at
        datetime updated_at
    }

    CART_CART_ITEM {
        bigint id PK
        bigint cart_id FK
        bigint product_id FK
        int quantity
        boolean selected
        datetime created_at
        datetime updated_at
    }

    ORDERS_ORDER {
        bigint id PK
        varchar order_number UK
        bigint user_id FK
        bigint address_id FK
        decimal total_amount
        decimal pay_amount
        varchar status
        varchar payment_method
        json address_snapshot
        datetime created_at
        datetime paid_at
        datetime completed_at
        datetime cancelled_at
    }

    ORDERS_ORDER_ITEM {
        bigint id PK
        bigint order_id FK
        bigint product_id
        varchar product_name
        varchar product_image
        decimal product_price
        int quantity
        decimal subtotal
    }

    CONTENT_ANNOUNCEMENT {
        bigint id PK
        bigint publisher_id FK
        varchar title
        text content
        varchar status
        datetime published_at
        datetime created_at
        datetime updated_at
    }

    CONTENT_RECOMMENDATION {
        bigint id PK
        bigint product_id FK_UK
        int sort_order
        varchar status
        datetime created_at
        datetime updated_at
    }
```

## 9. Django Models 草案

> 说明：以下为面向 `Django` / `Django REST Framework` 的模型草案，用于指导后续 `models.py` 编写。  
> 当前以单体架构为前提，按业务模块拆分 app。

### 9.1 `users` app

```python
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ("user", "普通用户"),
        ("merchant", "商家"),
    )
    STATUS_CHOICES = (
        ("enabled", "启用"),
        ("disabled", "禁用"),
    )

    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="enabled")
    updated_at = models.DateTimeField(auto_now=True)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    receiver_name = models.CharField(max_length=50)
    receiver_phone = models.CharField(max_length=20)
    province = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    detail_address = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 9.2 `products` app

```python
from django.db import models


class Category(models.Model):
    STATUS_CHOICES = (
        ("enabled", "启用"),
        ("disabled", "禁用"),
    )

    name = models.CharField(max_length=50, unique=True)
    sort_order = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="enabled")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    STATUS_CHOICES = (
        ("on_shelf", "上架"),
        ("off_shelf", "下架"),
    )

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to="products/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="off_shelf")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 9.3 `inventory` app

```python
from django.db import models
from products.models import Product
from users.models import User


class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="stock")
    quantity = models.IntegerField(default=0)
    alert_threshold = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)


class StockLog(models.Model):
    CHANGE_TYPE_CHOICES = (
        ("in", "入库"),
        ("out", "出库"),
        ("rollback", "回补"),
        ("manual", "人工调整"),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_logs")
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPE_CHOICES)
    change_amount = models.IntegerField()
    before_qty = models.IntegerField()
    after_qty = models.IntegerField()
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### 9.4 `cart` app

```python
from django.db import models
from products.models import Product
from users.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    selected = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 9.5 `orders` app

```python
from django.db import models
from users.models import User, Address


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending_payment", "待支付"),
        ("paid", "已支付"),
        ("completed", "已完成"),
        ("cancelled", "已取消"),
    )
    PAYMENT_METHOD_CHOICES = (
        ("wechat", "微信支付"),
        ("alipay", "支付宝"),
        ("balance", "余额支付"),
    )

    order_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending_payment")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    address_snapshot = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    product_image = models.CharField(max_length=255, blank=True, null=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
```

### 9.6 `content` app

```python
from django.db import models
from products.models import Product
from users.models import User


class Announcement(models.Model):
    STATUS_CHOICES = (
        ("draft", "草稿"),
        ("published", "已发布"),
    )

    title = models.CharField(max_length=100)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    publisher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Recommendation(models.Model):
    STATUS_CHOICES = (
        ("enabled", "启用"),
        ("disabled", "禁用"),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="recommendations")
    sort_order = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="enabled")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 9.7 `vision` app（可选）

```python
from django.db import models
from users.models import User
from products.models import Category


class RecognitionRecord(models.Model):
    image_path = models.CharField(max_length=255)
    recognized_name = models.CharField(max_length=100, blank=True, null=True)
    recommended_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    confidence = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    raw_result = models.JSONField(blank=True, null=True)
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### 9.8 建模说明

- `User` 继承 `AbstractUser`，避免重复实现登录字段
- `Stock` 使用 `OneToOneField(Product)`，明确一个商品只对应一份当前库存
- `OrderItem` 使用商品快照字段，而不是直接依赖 `Product` 当前信息
- `address_snapshot` 建议使用 `JSONField`，适合保存历史地址快照
- `RecognitionRecord` 属于可选实现，第一版可不创建

### 9.9 下一步建议

- 继续补 `Serializer` / `ViewSet` 草案
- 输出数据库 E-R 图
- 生成 `Django app` 目录结构建议
