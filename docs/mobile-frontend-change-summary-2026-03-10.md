# 移动端改动总结（2026-03-10）

## 1. 本次目标

- 登录页补齐注册能力，并与登录放在同一页面切换。
- 首页顶部改为全局头部组件，支持头像菜单、用户中心入口、退出登录。
- 增加用户中心页面，支持修改基本信息、头像、密码。
- 首页推荐区改为轮播；首页下方增加“商品列表区块”。
- 商品页与首页商品区支持滚动到底自动加载（无限加载）和加载栏。
- 商品“加入购物车”提供就地交互反馈（按钮附近气泡）。
- 修复联调期间常见错误提示可读性问题（网络断连/空响应等）。

## 2. 前端主要改动

### 2.1 全局布局与导航

- `frontend/mobile/src/App.vue`
  - 统一渲染全局 `HomeTopNav` + 全局 `MobileTabBar`。
  - 通过路由 `meta.showTopNav` 控制登录页隐藏头部。
- `frontend/mobile/src/components/HomeTopNav.vue`
  - 头部支持根据路由 `meta.title` 自动显示标题。
  - 右侧头像下拉：用户中心、退出登录。
- `frontend/mobile/src/router/index.ts`
  - 各页面补充 `meta.title`。
  - 新增用户中心路由 `/profile`。

### 2.2 登录/注册

- `frontend/mobile/src/views/LoginView.vue`
  - 登录与注册整合在一个页面内。
  - 注册支持用户名、密码、确认密码、手机号、邮箱。
  - 注册成功后自动登录并进入首页。

### 2.3 用户中心

- `frontend/mobile/src/views/ProfileView.vue`
  - 三个独立区块：
    - 基本信息（用户名/手机号/邮箱）
    - 头像上传
    - 密码修改
  - 分块提交，互不影响。
- `frontend/mobile/src/api/auth.ts`
  - 新增：
    - `updateProfile`
    - `uploadAvatar`
    - `updatePassword`

### 2.4 首页与商品展示

- `frontend/mobile/src/views/HomeView.vue`
  - 保留公告区。
  - 推荐商品改为轮播展示。
  - 搜索回车跳转商品页（携带 `keyword`）。
  - 引入首页商品区组件 `HomeProductSection`。
- `frontend/mobile/src/components/HomeProductSection.vue`
  - 抽象自商品页的商品卡片展示逻辑。
  - 支持分类筛选。
  - 支持无限加载与加载栏。
  - 支持“加入购物车”按钮附近气泡反馈。

### 2.5 商品页无限加载

- `frontend/mobile/src/views/ProductListView.vue`
  - 增加分页加载状态（初次加载/加载更多/无更多）。
  - 增加 `IntersectionObserver` 底部触发自动请求下一页。
  - 保留分类筛选和关键词搜索。
  - 增加“加入购物车”按钮附近气泡反馈。

### 2.6 请求与错误提示

- `frontend/mobile/src/api/http.ts`
  - 改进非 JSON/空响应解析。
  - 网络异常统一提示：`error:与服务器断连`。

## 3. 后端配合改动

- `backend/apps/products/views.py`
  - `GET /api/products` 增加分页参数支持：
    - `page`（默认 1）
    - `size`（默认 10，最大 50）
  - 未传分页参数时保持兼容（返回原列表结构）。

- `frontend/mobile/src/api/products.ts`
  - `fetchProducts` 新增 `page`、`size` 查询参数支持。

## 4. 交互细节（当前行为）

- 加入购物车反馈：
  - 成功：`已加入购物车`
  - 失败：`加入购物车失败`
  - 未登录：`请先登录`
  - 反馈显示为“按钮附近上浮气泡”，约 1.2 秒自动消失。
- 无限加载触发：
  - 页面滚动到底部触发后续请求。
  - 有“正在加载更多...”提示栏。
  - 数据结束显示“没有更多商品了”。

## 5. 验证结果

- 前端构建验证：
  - `npm run build`（`frontend/mobile`）通过。
- 后端配置检查：
  - `conda run -n shop python .\\backend\\manage.py check` 通过。

## 6. 说明

- 文案中出现乱码的问题来自历史文件编码混用，后续建议统一为 UTF-8（无 BOM）并做一次全量清理。
