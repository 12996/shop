# Demo Product Seeding Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 通过 Django 数据迁移内置演示分类、商品和库存，让项目迁移完成后即可直接用于商品管理和答辩演示。

**Architecture:** 在 `products` 应用中新增一个数据迁移，使用 `RunPython` 幂等写入演示分类、商品和库存。真实接口不增加额外分支；页面继续读取现有后端接口，自动获得演示数据。测试通过真实 API 验证迁移数据已打通到用户端和商家端。

**Tech Stack:** `Django`, `Django ORM`, `Django migrations`, `DRF`, `pytest`

---

### Task 1: 写失败测试，定义演示数据应出现在真实接口中

**Files:**
- Modify: `backend/apps/products/tests/test_product_api.py`
- Modify: `backend/apps/products/tests/test_admin_product_api.py`

**Step 1: 为用户商品列表补一条演示数据存在性测试**

在 [test_product_api.py](F:\work\project\shop\backend\apps\products\tests\test_product_api.py) 新增测试，断言迁移后的演示商品名称至少出现在商品列表中。

**Step 2: 为商家商品列表补一条演示数据存在性测试**

在 [test_admin_product_api.py](F:\work\project\shop\backend\apps\products\tests\test_admin_product_api.py) 新增测试，断言商家列表里能看到演示商品和库存字段。

**Step 3: 先运行定向测试，确认当前失败**

Run:
```powershell
conda run -n shop python -m pytest .\backend\apps\products\tests\test_product_api.py -v
conda run -n shop python -m pytest .\backend\apps\products\tests\test_admin_product_api.py -v
```

Expected:
- 新增断言失败，因为迁移数据尚未写入

### Task 2: 实现幂等的数据迁移

**Files:**
- Create: `backend/apps/products/migrations/0002_seed_demo_products.py`

**Step 1: 新增演示数据迁移**

创建 `RunPython` 迁移，写入：

- 分类：饮料、零食、日用品
- 商品：`3-5` 个演示商品
- 每个商品对应一条库存记录

**Step 2: 实现幂等创建逻辑**

要求：

- 分类按 `name` 查找或创建
- 商品按 `name` 查找或创建
- 库存按 `product` 查找或创建
- 不覆盖已存在商品的业务字段，只补缺失演示项

**Step 3: 实现安全回滚逻辑**

要求：

- 回滚时先删对应 `Stock`
- 再删演示 `Product`
- 仅删除空分类，避免误删已有业务数据

### Task 3: 迁移并验证真实接口

**Files:**
- Modify: `backend/db.sqlite3`（迁移执行后本地数据库变化）

**Step 1: 运行迁移**

Run:
```powershell
conda run -n shop python .\backend\manage.py migrate
```

Expected:
- 新的 `0002_seed_demo_products` 迁移执行成功

**Step 2: 重新运行商品相关测试**

Run:
```powershell
conda run -n shop python -m pytest .\backend\apps\products\tests\test_product_api.py -v
conda run -n shop python -m pytest .\backend\apps\products\tests\test_admin_product_api.py -v
```

Expected:
- 所有新增测试通过

**Step 3: 手动抽查接口**

Run:
```powershell
Invoke-WebRequest 'http://127.0.0.1:18000/api/products' -UseBasicParsing
Invoke-WebRequest 'http://127.0.0.1:18000/api/admin/products' -UseBasicParsing
```

Expected:
- 用户端接口能返回已上架演示商品
- 商家端接口能返回全部演示商品和库存字段

### Task 4: 更新文档

**Files:**
- Modify: `README.md`
- Modify: `docs/demo/demo-script.md`

**Step 1: 更新 README**

补充说明：项目迁移完成后会自动带演示商品数据。

**Step 2: 更新演示脚本**

把“提前准备 3 到 5 个已上架商品”改成“首次迁移后默认已内置演示商品，如需可继续新增”。

**Step 3: 回归验证**

Run:
```powershell
conda run -n shop python .\backend\manage.py check
```

Expected:
- Django check 通过
