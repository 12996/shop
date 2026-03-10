# 无人超市管理系统

## 环境准备

- Conda 环境：`shop`
- Python 3.11
- Node.js 22+
- MySQL 8（后续切换到正式数据库时使用）

## 安装依赖

- backend: `conda run -n shop python -m pip install -r backend/requirements.txt`
- frontend mobile: `cd frontend/mobile && npm install`
- frontend web: `cd frontend/web && npm install`

## 启动方式

- backend: `conda run -n shop python .\backend\manage.py runserver 127.0.0.1:18000`
- frontend mobile: `cd frontend/mobile && npm run dev -- --host 127.0.0.1 --port 5173`
- frontend web: `cd frontend/web && npm run dev -- --host 127.0.0.1 --port 5174`

## 演示数据

- 执行 `conda run -n shop python .\backend\manage.py migrate` 后，会自动写入默认演示分类、商品和库存数据
- 商家商品管理页、库存页和用户端商品列表可直接使用这些演示数据

## 后端验证命令

- Django 检查：`conda run -n shop python .\backend\manage.py check`
- 用户模块测试：`conda run -n shop python -m pytest .\backend\apps\users\tests\test_auth.py -v`
- 商品库存测试：`conda run -n shop python -m pytest .\backend\apps\products\tests\test_product_models.py -v`

## 说明

- 当前后端开发默认使用 `conda` 环境 `shop`
- `pytest.ini` 已配置 `DJANGO_SETTINGS_MODULE=config.settings`
- 后续新会话应优先沿用该环境和这些命令

## 目录说明

- `backend/`: Django + DRF 后端
- `frontend/mobile/`: 用户端 H5
- `frontend/web/`: Web 统一管理端
- `docs/`: PRD、设计文档、开发计划
