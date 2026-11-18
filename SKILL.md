---
name: starry-memory-ocean
description: 把智能体的记忆渲染成一片可交互的宇宙星空「记忆海」——每条记忆是一颗发光星，按层级分成同心星环，同项目/共享标签的记忆连成星座，支持旋转、缩放、搜索、层级筛选、时间轴回放、点击看全文。同时提供记忆写入端，可持续记录新记忆并让星图增长。当用户提出「星空记忆海 / 记忆星图 / 记忆宇宙 / 把记忆可视化成星空 / 记录一条记忆到记忆海 / 看看我的记忆星空」等需求时使用本技能。产出为单文件、离线可开、零外部依赖的 HTML。
agent_created: true
---

# 星空记忆海 · Starry Memory Ocean

## 用途

把分散的智能体记忆（WorkBuddy 的记忆文件体系）汇聚、结构化，渲染成一片**宇宙星空风格的可交互记忆海**：

- **每条记忆 = 一颗星**：importance 决定大小、亮度与星芒。
- **四旋臂银河布局**：星点沿四条对数螺旋臂分布，重要性越高越靠近银心，盘面由内向外变薄，中心有暖白紫核球与十字光芒；层级用颜色区分（soul / user / rules / project / topic / fact / lesson / daily）。
- **关联 = 星座连线**：同项目或共享标签的记忆之间自动连线。
- **三层视觉叠加**：AI 生成的壁纸级深空星云（base64 内嵌）作底 → 2200 颗程序化天球星场（随视角旋转/闪烁/视差）→ 四旋臂银河数据星。Canvas 2D 手写 3D 投影，发光玻璃拟态 UI，零外部依赖。

同时提供**写入端**：可把新记忆结构化落盘，星图随之增长。

产出物是一个**自包含 HTML**（数据、背景、样式、脚本全部内嵌），双击即可离线打开，不依赖网络 —— 适合现场演示、断网环境。

## 何时使用

- 用户说「星空记忆海 / 记忆星图 / 记忆宇宙 / 把我的记忆变成星空 / 可视化智能体记忆」。
- 用户想「记录一条记忆」并希望它体现在星图里。
- 用户想查看/回顾某项目积累的记忆分布、时间演化。
- 用户提到要做记忆可视化、知识星系、二创星空类作品（本技能内置二创参考画廊）。

## 资源清单

- `scripts/collect_memories.py` — 采集器：把 Markdown 记忆文件解析成结构化 JSON。
- `scripts/render.py` — 渲染器：把 JSON + 星云背景注入模板，生成单文件 HTML。
- `scripts/add_memory.py` — 写入器：向记忆海新增一条结构化记忆。
- `assets/ocean-template.html` — 星图模板（视觉与交互全在此）。
- `assets/nebula-bg.png` — AI 生成的壁纸级深空星云背景（韦布风格暖金核心 + 紫青丝状尘埃），已清除生成水印/幻觉框。渲染时以 base64 内嵌并自动加 `has-img` 类激活；`--no-bg` 时不激活。
- `references/inspiration-gallery.md` — 二创参考画廊（STELLORA、human-memory、meow-constellation 等 8 个作品及借鉴点）。

## 工作流

### A. 生成星图（最常用）

1. 确认工作区路径 `<workspace>`（含 `.workbuddy/memory/`）。默认当前目录。
2. 采集记忆。想连用户级 SOUL/IDENTITY/USER/MEMORY 一起纳入时加 `--include-user`：

   ```bash
   python scripts/collect_memories.py --workspace "<workspace>" --include-user --out memories.json
   ```

3. 渲染星图（背景默认用内嵌星云图）：

   ```bash
   python scripts/render.py --data memories.json --out "星空记忆海.html" --title "我的记忆宇宙"
   ```

4. 用 present_files 打开生成的 HTML 供用户查看。

> 脚本用纯标准库，任何 Python 3 均可运行，无需安装依赖。

### B. 记录一条新记忆

```bash
python scripts/add_memory.py \
  --text "闯子偏好先给结论再给理由" \
  --layer user --importance 5 --tags 偏好 汇报 \
  --workspace "<workspace>"
```

写入到 `<workspace>/.workbuddy/memory/ocean-notes.md`，采集器会自动读取。之后重跑工作流 A 即可看到新星点亮起。

支持的 `--layer`：`soul`（灵魂/人格）、`user`（用户画像）、`rules`（长期规则）、`project`（项目知识）、`topic`（主题）、`fact`（事实）、`lesson`（经验教训）、`daily`（日常日志）。`--importance` 取 1–5。

### C. 二创 / 定制视觉

先读 `references/inspiration-gallery.md` 选方向，再改 `assets/ocean-template.html`：
- 配色改 `:root` 的 CSS 变量与脚本里的 `LAYERS`；
- 布局改 `layout()`；连线规则改 `draw()` 里的 `showLinks` 段；
- 保持「单文件、离线、零 CDN 依赖」的底线。

## 数据来源与层级映射

采集器读取（存在才读，缺失自动跳过）：

| 文件 | 层级 |
|---|---|
| `~/.workbuddy/SOUL.md`、`IDENTITY.md` | soul |
| `~/.workbuddy/USER.md` | user |
| `~/.workbuddy/MEMORY.md` | rules |
| `<ws>/.workbuddy/memory/MEMORY.md` | project |
| `<ws>/.workbuddy/memory/YYYY-MM-DD.md` | daily |
| `<ws>/.workbuddy/memory/ocean-notes.md` | 依条目元数据 |
| `<ws>/.workbuddy/memory/其它.md` | topic |

层级到颜色的映射见模板 `LAYERS`；用户可在页面左侧图例点击隐藏/显示某个星域。

## 交互说明（页面内）

- 拖拽旋转星空，滚轮 / `+` `−` 缩放，`⌂ 复位` 还原视角。
- `⟳ 自动` 切换自动旋转；`✧ 连线` 切换星座连线。
- 顶部搜索框按标题、正文、项目、标签过滤。
- 点击星点 → 右侧玻璃面板看层级、日期、项目、重要性星级、正文、标签。
- 底部时间轴 / `▶` 按记忆日期回放星图演化。
- 左侧图例点击可单独隐藏/显示某层。

## 约定

- 保持离线自包含：数据、背景、脚本全部内嵌，不引外部 CDN。
- 不上传用户记忆到任何网络服务；所有处理在本地完成。
- 背景图为一次性 AI 生成资产，后续渲染复用，不再产生生成成本。
- 星图为空时，页面会提示用 `add_memory.py` 记录或检查采集路径。
