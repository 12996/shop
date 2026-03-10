# 商家端 API 文档

本文档仅整理前端商家端要调用的接口，包括：
- 接口 URL
- 请求所需字段
- 字段含义

说明：
- 商家端接口基础前缀为 `/api/admin`
- 以下内容以当前后端实际代码为准

## 1. 商品管理

### 1.1 获取商品列表
- **URL**: `GET /api/admin/products`

**请求字段**
- 无

### 1.2 新增商品
- **URL**: `POST /api/admin/products`

**请求字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `category` | 是 | 商品分类 ID |
| `name` | 是 | 商品名称 |
| `main_image` | 是 | 商品主图地址或图片标识 |
| `description` | 否 | 商品描述 |
| `price` | 是 | 商品价格 |
| `status` | 是 | 商品上架状态 |
| `quantity` | 是 | 初始库存数量 |
| `alert_threshold` | 是 | 库存预警阈值 |

**status 可选值**

| 值 | 含义 |
|---|---|
| `on_shelf` | 上架 |
| `off_shelf` | 下架 |

### 1.3 编辑商品
- **URL**: `PUT /api/admin/products/{product_id}`

**路径字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `product_id` | 是 | 商品 ID |

**请求字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `category` | 是 | 商品分类 ID |
| `name` | 是 | 商品名称 |
| `main_image` | 是 | 商品主图地址或图片标识 |
| `description` | 否 | 商品描述 |
| `price` | 是 | 商品价格 |
| `status` | 是 | 商品上架状态 |
| `quantity` | 是 | 当前库存数量 |
| `alert_threshold` | 是 | 库存预警阈值 |

### 1.4 商品上架
- **URL**: `POST /api/admin/products/{product_id}/on_shelf`

**路径字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `product_id` | 是 | 商品 ID |

**请求字段**
- 无

### 1.5 商品下架
- **URL**: `POST /api/admin/products/{product_id}/off_shelf`

**路径字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `product_id` | 是 | 商品 ID |

**请求字段**
- 无

## 2. 分类管理

说明：当前实际代码仅提供用户端分类列表接口，**没有实现商家端分类增删改接口**。

## 3. 库存管理

### 3.1 获取库存列表
- **URL**: `GET /api/admin/inventory`

**请求字段**
- 无

### 3.2 调整库存
- **URL**: `POST /api/admin/inventory/{product_id}/adjust`

**路径字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `product_id` | 是 | 商品 ID |

**请求字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `quantity` | 是 | 调整后的最新库存数量，最小为 0 |
| `remark` | 否 | 本次库存调整备注 |

说明：
- 当前后端实现是**直接传最终库存数量**，不是传增减值

## 4. 订单管理

### 4.1 获取订单列表
- **URL**: `GET /api/admin/orders`

**查询字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `status` | 否 | 按订单状态筛选 |

### 4.2 获取订单详情
- **URL**: `GET /api/admin/orders/{order_id}`

**路径字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `order_id` | 是 | 订单 ID |

### 4.3 完成订单
- **URL**: `POST /api/admin/orders/{order_id}/complete`

**路径字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `order_id` | 是 | 订单 ID |

**请求字段**
- 无

## 5. 公告管理

### 5.1 获取公告列表
- **URL**: `GET /api/admin/announcements`

**请求字段**
- 无

### 5.2 新增公告
- **URL**: `POST /api/admin/announcements`

**请求字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `title` | 是 | 公告标题 |
| `content` | 是 | 公告正文 |
| `status` | 是 | 公告状态 |

**status 可选值**

| 值 | 含义 |
|---|---|
| `draft` | 草稿 |
| `published` | 已发布 |

### 5.3 编辑公告
- **URL**: `PUT /api/admin/announcements/{announcement_id}`

**路径字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `announcement_id` | 是 | 公告 ID |

**请求字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `title` | 是 | 公告标题 |
| `content` | 是 | 公告正文 |
| `status` | 是 | 公告状态 |

### 5.4 删除公告
- **URL**: `DELETE /api/admin/announcements/{announcement_id}`

**路径字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `announcement_id` | 是 | 公告 ID |

## 6. 推荐位管理

### 6.1 获取推荐商品列表
- **URL**: `GET /api/admin/recommendations`

**请求字段**
- 无

### 6.2 新增推荐商品
- **URL**: `POST /api/admin/recommendations`

**请求字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `sort_order` | 是 | 推荐排序值，值越小越靠前 |
| `status` | 是 | 推荐状态 |
| `product` | 是 | 商品 ID |

**status 可选值**

| 值 | 含义 |
|---|---|
| `enabled` | 启用推荐 |
| `disabled` | 停用推荐 |

### 6.3 编辑推荐商品
- **URL**: `PUT /api/admin/recommendations/{recommendation_id}`

**路径字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `recommendation_id` | 是 | 推荐记录 ID |

**请求字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `sort_order` | 是 | 推荐排序值，值越小越靠前 |
| `status` | 是 | 推荐状态 |
| `product` | 是 | 商品 ID |

### 6.4 删除推荐商品
- **URL**: `DELETE /api/admin/recommendations/{recommendation_id}`

**路径字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `recommendation_id` | 是 | 推荐记录 ID |

## 7. 经营统计

### 7.1 获取经营概览
- **URL**: `GET /api/admin/statistics/overview`

**请求字段**
- 无

### 7.2 获取热销商品排行
- **URL**: `GET /api/admin/statistics/hot-products`

**请求字段**
- 无

## 8. 图像识别

### 8.1 商品图片识别
- **URL**: `POST /api/admin/vision/recognize`

**请求类型**
- `multipart/form-data`

**请求字段**

| 字段名 | 是否必填 | 含义 |
|---|---|---|
| `image` | 是 | 要上传识别的商品图片文件 |

## 9. 前端联调补充说明

### 9.1 商品管理常见返回字段

| 字段名 | 含义 |
|---|---|
| `id` | 商品 ID |
| `category` | 分类 ID |
| `category_name` | 分类名称 |
| `name` | 商品名称 |
| `main_image` | 商品主图 |
| `description` | 商品描述 |
| `price` | 商品价格 |
| `status` | 商品状态 |
| `quantity` | 当前库存数量 |
| `alert_threshold` | 库存预警阈值 |

### 9.2 库存管理常见返回字段

| 字段名 | 含义 |
|---|---|
| `product_id` | 商品 ID |
| `product_name` | 商品名称 |
| `category_name` | 商品分类名称 |
| `product_status` | 商品上下架状态 |
| `quantity` | 当前库存 |
| `alert_threshold` | 预警阈值 |
| `is_alert` | 是否触发库存预警 |
| `updated_at` | 最近更新时间 |

### 9.3 商家订单常见返回字段

| 字段名 | 含义 |
|---|---|
| `id` | 订单 ID |
| `order_number` | 订单编号 |
| `user` | 下单用户 ID |
| `username` | 下单用户名 |
| `status` | 订单状态 |
| `total_amount` | 订单总金额 |
| `pay_amount` | 实付金额 |
| `payment_method` | 支付方式 |
| `address_id` | 地址 ID，当前可能为空 |
| `address_snapshot` | 地址快照，当前可能为空 |
| `created_at` | 下单时间 |
| `items` | 订单商品列表 |

### 9.4 公告常见返回字段

| 字段名 | 含义 |
|---|---|
| `id` | 公告 ID |
| `title` | 公告标题 |
| `content` | 公告内容 |
| `status` | 公告状态 |
| `published_at` | 发布时间 |

### 9.5 推荐位常见返回字段

| 字段名 | 含义 |
|---|---|
| `id` | 推荐记录 ID |
| `sort_order` | 排序值 |
| `status` | 推荐状态 |
| `product` | 商品 ID |
| `product_name` | 商品名称 |
| `product_price` | 商品价格 |
| `product_image` | 商品图片 |

### 9.6 经营统计常见返回字段

#### `/api/admin/statistics/overview`

| 字段名 | 含义 |
|---|---|
| `order_count` | 订单总数 |
| `completed_order_count` | 已完成订单数 |
| `sales_amount` | 销售总金额 |

#### `/api/admin/statistics/hot-products`

| 字段名 | 含义 |
|---|---|
| `product_id` | 商品 ID |
| `product_name` | 商品名称 |
| `sales_count` | 销量 |
| `order_count` | 关联订单数 |
