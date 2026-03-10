# Demo Product Seeding Design

**Date:** 2026-03-10

**Goal:** 在数据库迁移阶段内置演示分类、商品和库存数据，保证项目启动并完成迁移后，商家商品管理页、库存页和用户商品浏览页都能直接展示可演示的数据。

## Context

- `docs/demo/demo-script.md` 要求演示前提前准备 `2-3` 个商品分类和 `3-5` 个已上架商品。
- 当前商家商品管理页和用户商品页都直接读取后端真实接口，不存在前端本地 mock 层。
- 用户希望“启动项目后自动有这些演示商品”，并选择通过数据库迁移内置这批数据。

## Approaches Considered

### 1. 启动时自动补数据

- 优点：严格贴合“每次启动都自动补齐”。
- 缺点：需要在运行时引入副作用，测试隔离更麻烦，也会让正式环境开关更敏感。

### 2. 数据迁移内置演示数据

- 优点：最稳定，数据库迁移完成后数据确定存在；逻辑清晰，便于版本化管理。
- 缺点：更新演示数据需要新增迁移或调整已有迁移。

### 3. 前端页面层 mock

- 优点：实现最轻。
- 缺点：与真实后端脱节，库存、商品详情、用户端浏览页会不一致。

## Chosen Design

采用“数据迁移内置演示数据”。

实现上在 `backend/apps/products/migrations/` 新增一个数据迁移，使用 `RunPython` 写入：

- `3` 个启用分类
- `5` 个商品
- 每个商品对应一条 `Stock`

这批数据会覆盖答辩演示常用场景：

- 至少 `3` 个上架商品，用户端商品页可直接展示
- 至少 `1` 个下架商品，商家端可演示上下架
- 至少 `1` 个低库存商品，库存页可演示预警

## Data Shape

建议内置如下演示数据：

- 分类：饮料、零食、日用品
- 商品：
  - 可口可乐 500ml
  - 雪碧 500ml
  - 原味薯片
  - 纸巾抽取式 3 包装
  - 苏打水 330ml

字段要求：

- `Product.status` 同时包含 `on_shelf` 和 `off_shelf`
- `Stock.quantity` 覆盖充足库存和低库存场景
- `Stock.alert_threshold` 至少让一个商品满足 `quantity <= alert_threshold`

## Idempotency Strategy

迁移必须幂等，避免重复创建。

- 分类按 `name` 查重，不存在才创建。
- 商品按 `name` 查重，不存在才创建。
- 库存按 `product` 一对一关系查重，不存在才创建。
- 若分类或商品已存在，迁移不覆盖用户后续人工修改的数据，只补缺失项。

## Rollback Strategy

反向迁移只删除当前迁移创建的演示商品和对应库存。

- 按约定商品名集合删除 `Stock`
- 再删除对应 `Product`
- 分类仅在没有其他商品引用时删除，避免误删用户后续新增数据

## Testing

增加一条后端测试验证演示数据已进入真实接口链路：

- 分类列表接口能返回演示分类
- 用户商品列表接口能返回已上架演示商品
- 商家商品列表接口能返回全部演示商品并带库存字段

验证命令：

- `conda run -n shop python -m pytest .\backend\apps\products\tests\test_product_api.py -v`
- `conda run -n shop python -m pytest .\backend\apps\products\tests\test_admin_product_api.py -v`

## Docs Impact

需要同步更新：

- `README.md`
- `docs/demo/demo-script.md`

说明项目迁移完成后默认包含演示商品数据，不再需要手工先录入一批商品。
