# 无人超市管理系统：接口设计文档

> 状态：当前实现版  
> 作用：定义前后端接口契约，明确请求路径、请求参数、返回结构、权限边界和主要错误场景。

## 1. 文档用途

这份文档用于回答三件事：

- 前端页面该调用哪些接口
- 后端每个接口该接收什么参数、返回什么数据
- 用户端和商家端分别能访问哪些接口

文档分工如下：

- `docs/prd/unmanned-store-prd.md`
  - 负责需求、流程、用户故事、业务规则
- `docs/design/database-design.md`
  - 负责数据库、类定义、模型关系
- `docs/design/api-design.md`
  - 负责接口契约和前后端联调规范

## 2. 设计范围

本文档覆盖以下接口模块：

- 认证与用户
- 首页与商品浏览
- 购物车
- 订单
- 商家商品与库存管理
- 商家订单管理与经营分析
- 公告与推荐位管理
- 图像识别辅助录入

## 3. 全局约定

### 3.1 接口前缀

- 用户端：`/api`
- 商家端：`/api/admin`

### 3.2 认证方式

- 采用 `JWT`
- 登录成功后返回：
  - `access_token`
  - `refresh_token`（可选，建议保留）
- 需要登录的接口通过请求头传递：

```http
Authorization: Bearer <access_token>
```

### 3.3 数据格式

- 请求体默认使用 `application/json`
- 上传图片接口使用 `multipart/form-data`
- 时间字段统一使用 `YYYY-MM-DD HH:mm:ss`
- 金额字段统一保留两位小数

### 3.4 统一响应结构

成功响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

失败响应：

```json
{
  "code": 1,
  "message": "error message",
  "data": null
}
```

分页响应建议：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [],
    "pagination": {
      "page": 1,
      "page_size": 10,
      "total": 100
    }
  }
}
```

### 3.5 通用错误码建议

- `0`：成功
- `1001`：参数错误
- `1002`：未登录或 token 无效
- `1003`：无权限访问
- `1004`：资源不存在
- `1005`：状态不允许当前操作
- `1006`：库存不足
- `1007`：手机号已存在
- `1008`：用户名已存在
- `1009`：验证码错误或失效
- `1010`：密码错误
- `1011`：图片上传失败
- `1012`：图像识别失败

### 3.6 权限边界

- 普通用户：
  - 可访问用户端接口
- 商家：
  - 可访问商家端接口
- Web 用户端和 Web 商家端共用系统壳，但菜单和接口权限不同

## 4. 认证与用户接口

### 4.1 `POST /api/auth/register`

**用途**
- 用户注册

**请求参数**
- `username`：`string`，必填，长度 `3-50`
- `password`：`string`，必填，长度建议不少于 `6`
- `phone`：`string`，可选；若填写则必须唯一

**成功返回**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "username": "zhangsan",
    "phone": "13800000000",
    "role": "user"
  }
}
```

**错误场景**
- 用户名已存在
- 手机号已存在
- 参数格式不正确

### 4.2 `POST /api/auth/login/password`

**用途**
- 用户名密码登录

**请求参数**
- `username`：`string`，必填
- `password`：`string`，必填

**成功返回**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "access_token": "xxx",
    "refresh_token": "xxx",
    "user": {
      "id": 1,
      "username": "zhangsan",
      "phone": "13800000000",
      "avatar": "/media/avatars/a.png",
      "role": "user"
    }
  }
}
```

**错误场景**
- 账号不存在
- 密码错误
- 用户已被禁用

### 4.3 `POST /api/auth/login/code`

**用途**
- 手机号验证码登录

**请求参数**
- `phone`：`string`，必填
- `code`：`string`，必填

**成功返回**
- 同 `POST /api/auth/login/password`

**错误场景**
- 手机号不存在
- 验证码错误或失效
- 用户已被禁用

### 4.4 `GET /api/auth/profile`

**用途**
- 获取当前登录用户信息

**成功返回**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "username": "zhangsan",
    "phone": "13800000000",
    "avatar": "/media/avatars/a.png",
    "role": "user",
    "status": "enabled"
  }
}
```

### 4.5 `PUT /api/auth/profile`

**用途**
- 修改个人资料

**请求参数**
- `username`：`string`，可选
- `phone`：`string`，可选

**错误场景**
- 新手机号已被占用
- 用户名已被占用

### 4.6 `POST /api/auth/avatar`

**用途**
- 上传或修改用户头像

**请求类型**
- `multipart/form-data`

**请求参数**
- `avatar`：文件，必填

**成功返回**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "avatar": "/media/avatars/new-avatar.png"
  }
}
```

### 4.7 `PUT /api/auth/password`

**用途**
- 修改密码

**请求参数**
- `old_password`：`string`，必填
- `new_password`：`string`，必填

**错误场景**
- 原密码错误
- 新密码不符合规则

## 5. 首页与商品浏览接口

### 5.1 `GET /api/home`

**用途**
- 获取首页数据

**返回内容**
- 最新公告 1 条
- 推荐商品列表
- 商品分类列表

**成功返回**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "latest_announcement": {
      "id": 1,
      "title": "今日优惠",
      "content": "部分商品限时优惠"
    },
    "categories": [
      { "id": 1, "name": "饮料" }
    ],
    "recommendations": [
      {
        "id": 10,
        "name": "可口可乐 500ml",
        "main_image": "/media/products/coke.png",
        "price": "3.50",
        "stock_status": "available"
      }
    ]
  }
}
```

### 5.2 `GET /api/categories`

**用途**
- 获取可用商品分类列表

### 5.3 `GET /api/products`

**用途**
- 获取商品列表

**查询参数**
- `keyword`：`string`，可选
- `category_id`：`number`，可选
- `page`：`number`，默认 `1`
- `page_size`：`number`，默认 `10`

**返回字段建议**
- `id`
- `name`
- `main_image`
- `price`
- `stock_quantity`
- `stock_status`
- `status`

**库存状态枚举建议**
- `available`：库存充足
- `low_stock`：库存不足但仍可购买
- `sold_out`：已售罄

### 5.4 `GET /api/products/{id}`

**用途**
- 获取商品详情

**返回字段建议**
- `id`
- `name`
- `category`
- `main_image`
- `description`
- `price`
- `stock_quantity`
- `stock_status`

**错误场景**
- 商品不存在
- 商品已下架

## 6. 购物车接口

### 6.1 `GET /api/cart`

**用途**
- 获取当前用户购物车

**返回字段建议**
- `cart_id`
- `items`
  - `id`
  - `product_id`
  - `product_name`
  - `product_image`
  - `product_price`
  - `quantity`
  - `selected`
  - `stock_status`
- `total_amount`

### 6.2 `POST /api/cart/items`

**用途**
- 加入购物车

**请求参数**
- `product_id`：`number`，必填
- `quantity`：`number`，必填，`> 0`

**业务规则**
- 同一商品再次加入时，数量累加
- 游客调用时返回未登录错误

**错误场景**
- 商品不存在
- 商品已下架
- 库存不足

### 6.3 `PUT /api/cart/items/{id}`

**用途**
- 修改购物车项

**请求参数**
- `quantity`：`number`，可选
- `selected`：`boolean`，可选

**错误场景**
- 购物车项不存在
- 库存不足

### 6.4 `DELETE /api/cart/items/{id}`

**用途**
- 删除购物车商品

### 6.5 `POST /api/cart/checkout`

**用途**
- 生成结算预览

**请求参数**
- `item_ids`：`array<number>`，必填

**返回字段建议**
- `items`
- `total_amount`
- `address_info`
  - 当前可为 `null`
  - 由前端解释为“店内自助购物，无需收货地址”

**错误场景**
- 结算商品为空
- 存在无效购物车项
- 存在下架商品
- 存在库存不足商品

## 7. 订单接口

### 7.1 `POST /api/orders`

**用途**
- 提交订单

**请求参数**
- `item_ids`：`array<number>`，必填
- `payment_method`：`string`，必填
  - `wechat`
  - `alipay`
  - `balance`
- `address_id`：`number`，可空

**业务规则**
- 提交时生成 `pending_payment` 订单
- 提交时校验库存并完成库存锁定/扣减
- 当前场景允许 `address_id` 为空

**成功返回**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "order_id": 1001,
    "order_number": "202603090001",
    "status": "pending_payment",
    "total_amount": "32.00",
    "pay_amount": "32.00"
  }
}
```

**错误场景**
- 购物车项不存在
- 商品库存不足
- 商品已下架
- 支付方式非法

### 7.2 `GET /api/orders`

**用途**
- 获取当前用户订单列表

**查询参数**
- `status`：可选
  - `pending_payment`
  - `paid`
  - `completed`
  - `cancelled`
- `page`
- `page_size`

**返回字段建议**
- `id`
- `order_number`
- `status`
- `total_amount`
- `created_at`
- `item_summary`

### 7.3 `GET /api/orders/{id}`

**用途**
- 获取订单详情

**返回字段建议**
- `id`
- `order_number`
- `status`
- `payment_method`
- `total_amount`
- `pay_amount`
- `created_at`
- `paid_at`
- `completed_at`
- `cancelled_at`
- `items`
- `address_info`
  - 有地址时返回地址对象
  - 无地址时返回说明字段：`本订单为店内自助购物，无收货地址`

### 7.4 `POST /api/orders/{id}/pay`

**用途**
- mock 支付

**请求参数**
- `payment_method`：`string`，必填

**业务规则**
- 仅 `pending_payment` 订单允许支付
- 支付成功后订单状态改为 `paid`
- 支付失败时订单保持 `pending_payment`

### 7.5 `POST /api/orders/{id}/cancel`

**用途**
- 取消订单

**业务规则**
- 仅 `pending_payment` 订单允许取消
- 取消成功后状态改为 `cancelled`
- 取消后回补库存

**错误场景**
- 订单不存在
- 订单状态不允许取消

## 8. 商家商品与库存管理接口

### 8.1 `GET /api/admin/products`

**用途**
- 商家查看商品列表

**查询参数**
- `keyword`
- `category_id`
- `status`
- `page`
- `page_size`

**返回字段建议**
- `id`
- `name`
- `category_name`
- `price`
- `quantity`
- `alert_threshold`
- `status`
- `is_alerting`

### 8.2 `POST /api/admin/products`

**用途**
- 商家新增商品

**请求参数**
- `category_id`：`number`，必填
- `name`：`string`，必填
- `main_image`：`string` 或文件，必填
- `description`：`string`，可空
- `price`：`decimal`，必填
- `quantity`：`number`，必填
- `alert_threshold`：`number`，必填
- `status`：`string`，必填
  - `on_shelf`
  - `off_shelf`

### 8.3 `PUT /api/admin/products/{id}`

**用途**
- 商家编辑商品

### 8.4 `POST /api/admin/products/{id}/on_shelf`

**用途**
- 商品上架

### 8.5 `POST /api/admin/products/{id}/off_shelf`

**用途**
- 商品下架

### 8.6 `GET /api/admin/categories`

**用途**
- 分类列表

### 8.7 `POST /api/admin/categories`

**用途**
- 新增分类

**请求参数**
- `name`
- `sort_order`
- `status`

### 8.8 `PUT /api/admin/categories/{id}`

**用途**
- 编辑分类

### 8.9 `GET /api/admin/inventory`

**用途**
- 查看库存列表与库存预警信息

**查询参数**
- `keyword`
- `category_id`
- `is_alerting`
- `page`
- `page_size`

### 8.10 `POST /api/admin/inventory/{product_id}/adjust`

**用途**
- 调整库存

**请求参数**
- `change_type`：`string`，必填
  - `in`
  - `manual`
- `change_amount`：`number`，必填
- `remark`：`string`，可空

**业务规则**
- 库存调整后写入 `inventory_stock_log`
- 调整后库存不可小于 `0`

## 9. 图像识别接口

### 9.1 `POST /api/admin/vision/recognize`

**用途**
- 上传商品图片并触发 `YOLO` 识别

**请求类型**
- `multipart/form-data`

**请求参数**
- `image`：文件，必填

**成功返回**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "recognized_name": "可口可乐 500ml",
    "recommended_category_id": 1,
    "recommended_category_name": "饮料",
    "confidence": "0.91",
    "image_url": "/media/products/tmp-coke.png"
  }
}
```

**错误场景**
- 图片上传失败
- 图像识别失败

**说明**
- 识别结果仅用于辅助录入
- 商家必须手动确认后才能保存商品

## 10. 商家订单管理与经营分析接口

### 10.1 `GET /api/admin/orders`

**用途**
- 查看所有订单

**查询参数**
- `status`
- `keyword`
  - 可按 `order_number` 或用户名模糊查询
- `page`
- `page_size`

### 10.2 `GET /api/admin/orders/{id}`

**用途**
- 查看订单详情

**返回内容**
- 订单基础信息
- 订单项列表
- 用户信息摘要
- 地址信息或店内自助购物说明

### 10.3 `POST /api/admin/orders/{id}/complete`

**用途**
- 将 `paid` 订单标记为 `completed`

**错误场景**
- 订单不存在
- 订单状态不是 `paid`

### 10.4 `GET /api/admin/statistics/overview`

**用途**
- 获取经营概览

**返回字段**
- `order_total`
- `sales_total_amount`
- `completed_order_total`

### 10.5 `GET /api/admin/statistics/hot-products`

**用途**
- 获取热销商品排行

**查询参数**
- `limit`：默认 `10`

**返回字段**
- `product_id`
- `product_name`
- `sales_count`

## 11. 公告与推荐位管理接口

### 11.1 `GET /api/admin/announcements`

**用途**
- 公告列表

**查询参数**
- `status`
- `page`
- `page_size`

### 11.2 `POST /api/admin/announcements`

**用途**
- 发布公告

**请求参数**
- `title`
- `content`
- `status`
  - `draft`
  - `published`

### 11.3 `PUT /api/admin/announcements/{id}`

**用途**
- 编辑公告

### 11.4 `DELETE /api/admin/announcements/{id}`

**用途**
- 删除公告

### 11.5 `GET /api/admin/recommendations`

**用途**
- 获取推荐商品列表

### 11.6 `POST /api/admin/recommendations`

**用途**
- 添加推荐商品

**请求参数**
- `product_id`：`number`，必填
- `sort_order`：`number`，必填

**业务规则**
- 同一商品只允许存在一条推荐记录

### 11.7 `PUT /api/admin/recommendations/{id}`

**用途**
- 修改推荐展示顺序

**请求参数**
- `sort_order`：`number`，必填

### 11.8 `DELETE /api/admin/recommendations/{id}`

**用途**
- 取消推荐

**业务规则**
- 删除推荐记录

## 12. 接口与页面映射建议

### 12.1 移动端用户页面

- 登录页
  - `POST /api/auth/login/password`
  - `POST /api/auth/login/code`
- 注册页
  - `POST /api/auth/register`
- 首页
  - `GET /api/home`
- 商品列表/详情
  - `GET /api/products`
  - `GET /api/products/{id}`
- 购物车
  - `GET /api/cart`
  - `POST /api/cart/items`
  - `PUT /api/cart/items/{id}`
  - `DELETE /api/cart/items/{id}`
- 结算页
  - `POST /api/cart/checkout`
  - `POST /api/orders`
- 订单页
  - `GET /api/orders`
  - `GET /api/orders/{id}`
  - `POST /api/orders/{id}/pay`
  - `POST /api/orders/{id}/cancel`

### 12.2 商家端页面

- 商品管理
  - `GET /api/admin/products`
  - `POST /api/admin/products`
  - `PUT /api/admin/products/{id}`
  - `POST /api/admin/products/{id}/on_shelf`
  - `POST /api/admin/products/{id}/off_shelf`
- 图像识别辅助上架
  - `POST /api/admin/vision/recognize`
- 分类管理
  - `GET /api/admin/categories`
  - `POST /api/admin/categories`
  - `PUT /api/admin/categories/{id}`
- 库存管理
  - `GET /api/admin/inventory`
  - `POST /api/admin/inventory/{product_id}/adjust`
- 订单管理
  - `GET /api/admin/orders`
  - `GET /api/admin/orders/{id}`
  - `POST /api/admin/orders/{id}/complete`
- 销售统计
  - `GET /api/admin/statistics/overview`
  - `GET /api/admin/statistics/hot-products`
- 公告与推荐
  - `GET /api/admin/announcements`
  - `POST /api/admin/announcements`
  - `PUT /api/admin/announcements/{id}`
  - `DELETE /api/admin/announcements/{id}`
  - `GET /api/admin/recommendations`
  - `POST /api/admin/recommendations`
  - `PUT /api/admin/recommendations/{id}`
  - `DELETE /api/admin/recommendations/{id}`

## 13. 下一步建议

基于这份接口设计文档，后续可以继续补：

- `Serializer` 草案
- `ViewSet` 草案
- 权限类设计
- 接口状态码明细表
- 前端页面与接口字段对照表
