# dvlyadmin-mini 后端多环境配置说明

> 本文档说明 backend 多环境配置（开发/生产）的区分机制与部署用法。
> 相关代码：`backend/config.py`（`_select_env_file` / `_load_env_file`）。

## 一、环境档案文件

| 文件 | 环境 | 是否进 git | 内容要点 |
|---|---|---|---|
| `.env.dev` | 本地开发 | ✅ 进 | SQLite、`DEBUG=True`、`http://127.0.0.1:8000`、邮件输出到控制台、内存缓存 |
| `.env.prod` | 生产模板 | ✅ 进（仅占位密码） | `https://www.lybbn.cn`、`DEBUG=False`、MySQL、真实 SMTP |
| `.env` | 实际生效配置 | ❌ gitignore 忽略 | 服务器上 `cp .env.prod .env` 后填入真实密钥 |

- 两个档案文件都躺在仓库里，内容都是安全的（prod 里密钥是占位符）。
- 它们只是"档案"，**不会同时生效**——每次启动只会挑其中一个加载。

## 二、选择流程（每次 Python 进程启动都会执行一次）

`config.py` 按"优先级链"决定加载哪个文件，**命中即停**：

```
Python 进程启动（manage.py / daphne / 面板的 python 项目）
        │
        ▼
① backend/.env 存在？
        │ 是 → 加载 .env，结束          ← 服务器部署的推荐方式
        │ 否 ↓
② 真实环境变量 DVLYADMIN_ENV 有值？（如 prod）
        │ 有 → 加载 .env.prod，结束     ← 面板环境变量切换方式
        │      （文件不存在则打印警告，继续往下）
        │ 无 ↓
③ backend/.env.dev 存在？
        │ 是 → 加载 .env.dev，结束      ← 本地开发自动命中这一步
        │ 否 ↓
④ 什么都不加载 → 用 config.py 里写死的默认值
```

**区分的本质：文件名后缀 + 一个选择变量。**

## 三、三个场景实际走哪一步

| 场景 | 走哪步 | 为什么 |
|---|---|---|
| 本地 `python manage.py runserver` | ③ `.env.dev` | 本地没有 `.env` 文件，也没设 `DVLYADMIN_ENV` |
| 如意面板/宝塔部署 | ① `.env` | 服务器上执行了 `cp .env.prod .env`，文件存在即命中 |
| 同机多套环境 | ② `.env.prod` / `.env.staging` | 面板里给 A 项目设 `DVLYADMIN_ENV=prod`、B 项目设 `DVLYADMIN_ENV=staging`，不用 cp，档案直接跟代码走 |

以后新增环境（如测试机）：新建 `.env.staging` 之类的档案文件即可，机制自动识别。

## 四、为什么不会"抢配置"（优先级铁律）

`_load_env_file` 加载时有一条铁律：**真实环境变量里已有的 key 一律跳过**
（实现：`if key and key not in os.environ`）。

因此：

- **面板手工设置的环境变量** → 同样优先于档案文件

总优先级：**真实环境变量 > backend/.env > .env.{DVLYADMIN_ENV} > .env.dev > config.py 内置默认值**

## 五、部署操作指引

### 本地开发

零操作。无 `.env` 且未设 `DVLYADMIN_ENV` 时自动加载 `.env.dev`。

### 如意面板/宝塔部署（非 Docker）

```bash
# 1. 前端构建（本地执行，产物进入 backend/frontend/lyadmin）
cd dvlyadmin-mini/frontend && npm run build:backend

# 2. 拷贝 backend 全部代码到面板 Python 项目目录（注意：不要覆盖服务器上已配置好的 .env）

# 3. 服务器上初始化环境配置（首次部署执行一次）
cp .env.prod .env
vi .env   # 填入真实数据库密码、SMTP 授权码等敏感项

# 4. 重启 Python 项目
```

## 六、安全注意事项

1. **真实密钥只存在于服务器上的 `.env`**（数据库密码、SMTP 授权码、SECRET_KEY），该文件已被 `.gitignore` 忽略，永不进 git。
2. **整目录覆盖式拷贝部署的坑**：如果部署方式是"先清空目标目录再整拷"，服务器上的 `.env` 会被删掉——拷贝时排除 `.env`。
3. `.env.prod` 可进 git，但**修改真实密钥后不要误填回这个文件提交**。
