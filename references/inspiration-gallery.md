# 星空记忆海 · 二创参考画廊

本 Skill 的视觉与交互设计借鉴了以下社区开源作品（均已核实许可/定位）。
需要在本 Skill 上做二次创作时，先读这里，选一个方向再改 `assets/ocean-template.html`。

> 调研日期：2026-11-18。链接可能变化，以实际访问为准。

---

## 1. STELLORA —「每段记忆是一颗星，每段故事是一个星座」
- 地址：https://github.com/PeepSick/STELLORA/
- 技术：React 19 + Three.js (R3F) + Zustand + Vite，MIT
- 亮点：
  - **知识星系**：Markdown 笔记 = 星，`[[wikilink]]` = 可见连线 —— 本 Skill 的「星座连线」直接借鉴此思路。
  - **Memory Score**：用收藏/重要/归档标记驱动星星的渲染显著度 —— 本 Skill 的 `importance` 字段同源。
  - **时间轴视图**、**AI Chat**、**MCP Server**、**导出/导入**、主题引擎。
- 可二创点：接入 wikilink 解析、加 AI 对话检索节点、加 JSON 导入导出。

## 2. human-memory · 类人脑记忆与「记忆宇宙」
- 地址：https://github.com/zyj52742-cloud/human-memory
- 定位：**本 Skill 最直接的精神原型**。给 AI 装类人脑记忆（重要的记牢、日常的会淡），并把记忆导出成可离线打开的三维视图。
- 亮点：
  - **八类天体**：行星、带环行星、冰封、熔岩、海洋、恒星、小行星、彗星；四旋臂银河、银河天幕、立体环绕。
  - **两种视图**：关联网络 + 真实行星。
  - **本项目自带 Skill**（`skills/memory-universe/`），可直接研究其数据结构。
- 可二创点：把本 Skill 的「层级圆点」升级为八类天体外观；加四旋臂银河布局。

## 3. dsh-meow-constellation — 七层记忆 3D 星图
- 地址：https://dshpluginhub.ai/zh/plugins/dsh-meow-constellation （源：github:yuyun-git/dsh-meow-constellation）
- 技术：宿主读 SQLite，浏览器 **Canvas 2D** 手写 3D 投影（**与本 Skill 渲染方式一致，无 Three.js 依赖**）
- 亮点：
  - **七层同心环**：soul/user/rules/project/topic/fact/lesson 各占一环一纵深平面 —— **本 Skill 的层级与同心环布局即参考此七层**。
  - 拖拽旋转、滚轮缩放、拖动光点、自动旋转、中心「此刻」核心。
  - 点击光点 → 玻璃拟态详情面板（层级/状态/重要性星级/关键词/全文/关联）。
  - mtime 轮询增量同步、层级筛选、全文搜索。
- 可二创点：加「拖动光点并持久化位置」、加 mtime 轮询自动刷新。

## 4. dsh-memory-nebula — 带证据链的记忆星云
- 地址：https://dshhub.org/ja/plugins/hanhan9999999999999999999/dsh-memory-nebula
- 亮点：只读星云、**扩散召回**（顺着连接读出关联记忆）、**证据链**、离线自包含 HTML 导出、可插拔记忆适配器。
- 可二创点：给本 Skill 的连线加「证据链」展示、加扩散式关联高亮。

## 5. UluP Life — 把一生变成星座
- 地址：https://www.indiehackers.com/post/i-built-a-place-where-your-memories-become-stars-11a71ad6c9
- 亮点：
  - 记忆 → 星，分组 → 星系（关系/旅程/成长/里程碑…）。
  - **未点燃的星**代表未来目标，达成时点亮 —— 很有叙事感的交互概念。
  - 时间流逝回放（time-lapse）、导出星座海报、MCP 对话式增删改。
- 可二创点：加入「未点亮的目标星」与达成点亮动画；导出 PNG 海报。

## 6. memory-constellation — 心形爱情星座
- 地址：https://github.com/sakibnjr/memory-constellation
- 技术：React 18 + TS + Vite + Tailwind + Supabase
- 亮点：记忆沿**心形曲线**排布、分享只读链接、探索解锁隐藏星、导出图片。
- 可二创点：提供「主题形状」布局切换（心形/银河/螺旋）。

## 7. Phoenix Grove — 3D Mind Constellations（高维嵌入投影）
- 地址：https://pgsgrove.com/mind-constellations
- 亮点：把 AI 的高维记忆嵌入降维到 3D，邻近=语义相近；**年代滑块**回放心智成长；聚类自动命名并着色。
- 可二创点：接入真实 embedding 做语义布局（取代当前的确定性圆周布局），加聚类自动命名。

## 8. Starlogue — 生活瞬间星座 + AI 向导
- 地址：https://www.github.com/NidhiIyer04/Starlogue
- 亮点：时间胶囊彗星、AI 导航员发现被遗忘的记忆、主题切换（哥特/霓虹/动漫）、数字剪贴簿。
- 可二创点：主题配色切换；加「AI 发现被遗忘的记忆」高亮。

---

## 本 Skill 当前采用的设计（Mixin 结果）
- **数据来源**：WorkBuddy 记忆体系（MEMORY / SOUL / IDENTITY / USER / 项目日志）— 借鉴 human-memory 的「真实数据、离线优先」。
- **视觉**：AI 生成壁纸级深空星云背景（韦布船底座风格：暖金核心 + 紫青丝状尘埃 + 密集星场，见 `assets/nebula-bg.png`）+ 2200 颗程序化天球星场 + Canvas 2D 发光星点 — 借鉴 meow-constellation 的深蓝发光风格与无依赖渲染。背景加 brightness(.82) 压暗以突出前景数据星。
- **布局**：四旋臂对数螺旋银河（当前版本）— 借鉴 human-memory 四旋臂银河；importance 决定半径（越重要越靠银心），盘面厚度由银心向外递减，暖白紫核球 + 十字光芒。旧的八层同心星环方案见 git/历史版本，可随时切回。
- **星座连线**：同项目 / 共享标签连成星座 — 借鉴 STELLORA 的 wikilink 图。
- **重要性**：importance 1-5 驱动大小、亮度、星芒 — 借鉴 STELLORA Memory Score、meow 星级。
- **交互**：拖拽旋转、滚轮缩放、点击详情、搜索、层级筛选、时间轴回放、自动旋转 — 综合上述作品。

## 二创注意事项
- 保持**单文件、离线可开、零外部依赖**（不引 CDN）——这是现场演示不翻车的底线。
- 数据随 Skill 走，不上传云端；背景图以 base64 内嵌。
- 新增视觉元素优先改 `assets/ocean-template.html` 的 CSS 变量与 `LAYERS` 配色，别改渲染内核。
