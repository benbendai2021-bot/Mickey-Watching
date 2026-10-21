# 🐭 Is Mickey LeetCoding?

> **全网监督米奇刷题计划：这周米奇敲代码了吗？**  
> The internet is watching. Mickey better be coding. 👀

各位亲朋好友、路过的观察员，欢迎来到 **Mickey Watching 总部**。本项目存在的唯一意义：**让米奇不能悄悄摆烂。**

🌐 **[打开米奇观察站](https://is-mickey-leetcoding.netlify.app/)**（域名需在 Netlify 创建部署后才会生效）  
📋 [NeetCode 150 题单](https://neetcode.io/roadmap) · 🧑‍💻 [米奇的 LeetCode](https://leetcode.com/u/Y7CXvSGRIL/) · 💬 [前往吐槽区](https://github.com/benbendai2021-bot/Mickey-Watching/issues)

## 🕵️ 观察员指南

不需要注册就能看到米奇的刷题进度。打开网页就能查：

- 🌱 **每周热力图**：本周有没有刷？没刷一眼看穿。
- 🧩 **18 个题型、150 道题**：哪些会了，哪些还在装死。
- ⏱️ **当前速度 & 预计完工日期**：按照最近速度什么时候刷完。
- 🚨 **冲刺倒计时**：要在 **2026 年 12 月 20 日** 前完成，平均每周还得刷多少。
- 📣 **每周吐槽区**：欢迎公开催更、加油或阴阳怪气（友善版）。

**重要约定：每周至少刷一次，没有每周必须做多少题的硬 KPI。** 如果这一周刷过，哪怕只做了一题，也是有动静的鼠。

## 📣 怎么吐槽米奇？

1. 在网页找到 **「🐭 本周米奇观察站 · 吐槽区」**。
2. 在吐槽区填写昵称和留言，无需跳转 GitHub。
3. 输入昵称和吐槽内容直接发送，不需要登录；留言公开显示。
4. 每周一自动建立新的观察帖，旧帖会保留供后人考古。

**吐槽守则：** 可以催更、发梗、夸夸，但请别辱骂、曝光隐私或者贴敏感内容。所有留言公开，匿名昵称不代表经过身份验证。

## 🧠 数据怎么计算？

`LeetCode → GitHub Actions → JSON 历史快照 → Dashboard → Netlify / GitHub Pages`

- **热力图**：来自 LeetCode 的公开提交日历，衡量练习活跃度。
- **NeetCode 完成度**：以固定 150 道题为准，按 LeetCode 题目 slug 匹配已通过的题，而不是拿 LeetCode 总题数冒充。
- **近期速度**：用历史快照推算每周新增、且属于题单内的题目数量。
- **目标速度**：`剩余题数 ÷ 距离 2026-12-20 的剩余周数`。
- **预计完成日**：`今天 + (剩余题数 ÷ 当前每周速度) 周`。历史不足或速度为 0 时不会瞎报完工日期。

⚠️ **数据限制：** LeetCode 公开接口通常只提供近期 AC 列表，并不保证返回全部历史题目。首次历史完成量可能偏低，可在 [`data/manual.json`](data/manual.json) 中补充 `completedSlugs`。每天的历史快照会由 GitHub Actions 保存以供后续预测。

## ⚙️ 项目维护说明

- `index.html`：静态 Dashboard，部署时无需构建。
- `scripts/sync.py`：抓取公开统计、核对 NeetCode 150 并保存历史。
- `data/*.json`：配置、题单、快照与人工校准数据。
- `.github/workflows/pages.yml`：每天同步数据，更新 GitHub 仓库。
- `netlify/functions/roasts.mjs`：匿名留言 API、输入校验、基础限流。\n- `netlify/functions/_roast-core.mjs`：每周归档与数据逻辑。\n- `tests/roasts.test.mjs`：本地自动测试。
- `netlify.toml`：Netlify 发布静态站点的配置。

### 免费发布到 Netlify

1. 在 [Netlify](https://app.netlify.com/) 用 GitHub 登录，选择 **Add new project → Import an existing project**。
2. 授权并选择 `benbendai2021-bot/Mickey-Watching`，分支为 `main`。
3. Build command 留空，Publish directory 填 `.`；部署设置也已写在 `netlify.toml`。
4. 到 **Site configuration → Domain management** 设置站点名为 `is-mickey-leetcoding`（**需看实际是否可用**）。
5. GitHub Actions 的定时同步会提交更新后的 JSON，Netlify 连接仓库后会重新部署。

数据同步独立运行，不依赖网站托管平台；Netlify 连接仓库之后会自动部署最新内容。

---

**鼠鼠可以休息，但不能偷偷消失。** 🐭

### 🐭 匿名留言技术说明

- Netlify Functions 提供公开 GET/POST 接口 `/api/roasts`；Netlify Blobs 存储每条留言，不需要第三方登录。
- 分周归档，按太平洋时间周一切换；输入有长度验证和蜜罐字段，Netlify 对接口设置 IP 限流。
- 匿名留言仍可能遇到恶意内容或刷屏；如需长期对外开放，建议未来追加人工审核/举报与删除机制。
- 本功能先在 `feature/anonymous-weekly-roasts` 分支测试，通过后再合并生产。
