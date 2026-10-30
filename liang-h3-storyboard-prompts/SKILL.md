---
name: liang-h3-storyboard-prompts
description: 把已确认的中文短剧剧本与视觉设定拆成 MiniMax H3（海螺）参考生视频的 H3-UNIT 分镜和可整体复制的提示词，覆盖 H3 全部模式（base / first_frame / first_last_frame / reference 六段），以参考生视频为主；支持文戏、高动态武戏、人物设定图三条分支，成稿保持中英文对照格式。用户点名 H3、参考生、六段式、多主体参考、站位锁、口型纪律、武戏高动态、定妆照/四视图或"把这场戏拆成 H3 分镜"时使用；普通分镜走 $short-drama-storyboard，不生成媒体。
license: MIT
---

# H3 参考生视频分镜提示词

把剧本事实、视觉设定与真实参考图编排成可提交给 MiniMax H3 的生成单元。
骨架沿用 `$short-drama-h3-storyboard`：`H3-UNIT-...` 是一份独立 job，内部含一个或多个
`[Shot N]`，最终交付**可整体复制的 H3 正文 + 逐段中文对照**。

参考生视频（`reference` 六段）是主路径；三段模式（base / first_frame /
first_last_frame）与人物设定图（定妆照 / 四视图）作为配套能力同时维护。

## 先选分支

| 用户说 | 分支 | 读哪个文件 |
|---|---|---|
| 分镜 / 镜头 / 对话 / 文戏 / 默认 | **文戏参考生** | [references/h3-reference-guide.md](references/h3-reference-guide.md)，全程走六段 |
| **高动态** / 打斗 / 武戏 / 动作戏 | **武戏参考生** | [references/mode-action.md](references/mode-action.md)，六段壳＋中文动作＋镜头纪律 |
| **人物提示词** / 定妆照 / 四视图 | **人物模式** | [references/mode-character.md](references/mode-character.md)，产出是上游参考图 |
| 指定了目标视频模型为 H3 但只有起始帧 / 首尾帧 | 三段模式 | [references/base-modes.md](references/base-modes.md) |

人物模式在整条链的上游：定妆照/四视图出片后直接成为分镜的 `<Picture N>`/`<Subject N>`，
少写一项识别特征，分镜里"保持参考图五官"就少一个抓手。

## 使用边界

- 仅针对 `minimax-h3`（海螺）。项目档案已写 `target_video_model: minimax-h3` 或本轮点名才使用。
- 不生成图片、视频或配音；不凭文件名声称图片存在；不改写剧情、人物身份或台词。
- 对白必须逐字来自《剧本.md》、已接受分镜或用户明确提供的文本；需要新台词先回写作阶段。
- H3 单元时长 4–15 秒（整数）。上游写了 16 秒或更长时拆单元，不硬塞。
- 参考生（六段）是最常见也最容易写错的模式：H3 的首/尾帧输入与参考输入**互斥**，
  "起始帧 + 角色图 + 场景图 + 站位图"整组统一走 `reference`，起始帧也以 `reference_image`
  送入，不要拆成 `first_frame` 加 `reference_image` 两套。
- 不覆盖通用《分镜.md》；默认输出 `剧集/<EP>/H3分镜.md`。

## 硬门禁（参数确认卡）

调用后先读取现有事实（`short-drama.json`、目标场次《剧本.md》《视觉设定.md》、
已有《分镜.md》《图片提示词.md》、项目内当前可读的参考图），只输出
《H3 分镜参数确认卡》然后**停止**。确认前不写最终文件、不调生成、"继续"不算确认。

确认卡至少包含：

```markdown
## H3 分镜参数确认卡
- 项目 / 剧集 / 场次：
- 目标模型：minimax-h3
- 输出文件：
- 原生时长约束：每个 H3-UNIT 4–15 秒（整数）
- 拟拆生成单元：
- 每个单元的 H3 模式：reference / first_frame / first_last_frame / base
- 参考图槽位与顺序（REF/PLAN）：
- 主体映射：<Subject N> ↔ 角色 / 视觉设定 / <Picture N>
- 声线映射：角色 ↔ <Subject N> ↔ Sx（含固定音色）
- 空间锁：屏幕左右、朝向、轴线、出入口、禁止镜像
- 台词来源：剧本场景 ID 与逐字文本
- 对白容量：各镜可发声字数 ÷ 约 4.1 字/秒（中文小样本参考值）
- 多镜容器门槛：每一刀是否都有已接受起始关键帧
- 镜头边界类型：紧接 / 跳切省略 / 换场（逐边界）
- 待创作者决定：只列真正影响成稿的选择
```

确认后再按"单元元数据 → 逐镜表 → H3 可复制正文（英文）→ 逐段中文对照"的顺序成稿。

## 生成单元结构

```markdown
## H3-UNIT-EP001-007A · 青儿催归
- 时长：11 秒
- 模式：reference
- 来源：SC-EP001-007
- 参考图：REF-...（顺序：1）· ...（用途：身份；控制：...；不得控制：...）
- 主体映射：<Subject 1> = 师娘 = <Picture 1> = S1
- 声线映射：师娘 = <Subject 1> = S1 = <固定音色与说话方式>
- 空间锁：...
- 口型纪律：...
- 状态链：... → ... → ...
- 声音：...
- 镜头边界：紧接 / 跳切省略 / 换场（每刀一个类型）

### SHOT-EP001-007A-01 · ...
- 职责：
- 起点：
- 唯一动作：
- 终点：
- 景别 / 机位 / 运镜：
- 声音 / 对白：

### H3 提示词（reference：六段；base / first_frame / first_last_frame：三段）

```text
subject_definitions:
<Subject 1> is 【角色】 in <Picture 1>, with 【脸型骨相 + 五官 + 识别特征 + 服装各层】.
<Picture 3> anchors the environment: 【布局、家具、光、色】.
summary: [reference generation] 【一到三句可见状态变化】
retention_analysis: <Subject 1> (appears in [Shot 1]–[Shot N]): fully_preserved - 【保留什么】.
detailed_description: [Shot 1] ... <Subject 1> (S1) says: <d>[Chinese]逐字台词</d> [Shot 2] At 00:03.500, ...
overall_soundscape: ...
non_diegetic_music: N/A
```

六段是一条提示词、一次整体提交：`retention_analysis` 引用的 `<Subject N>`
在 `subject_definitions` 里定义，`<Picture N>` 按本单元参考图顺序编号——
拆开提交后面几段就没有指代对象了。

**标签行只准住在英文 H3 块里。** `<Subject N> is ...` / `<Subject N> 是 ...` /
`<Picture N> ...` 这类标签行，只能出现在 `### H3 提示词` 下面的英文 ```text 块中
`subject_definitions` 段落内。单元元数据列表（`- 主体映射：` 之外）、文件头、
分镜表、中文对照块里都不许另起一行写标签定义——写成行内引用可以
（`- 主体映射：<Subject 1> = 母亲 = <Picture 1> = S1`），独立成行的标签定义
只会被当成正文粘进错误位置，是"英文块里混进中文主体定义"这类事故的源头。
`validate_h3_storyboard.py` 会把代码块外的标签行直接报错。

## 参考图怎么分工

沿用项目 `用途` 封闭集合：`身份 / 造型状态 / 地理 / 构图 / 尺度 / 效果 / 起始帧 / 结束帧 / 风格`。
"站位参考帧 / 轴线参考帧 / 站位图"归入 `用途：构图`，在 `控制` 里写死
屏幕左右、朝向、轴线、入口方向、禁止镜像（`do not mirror <Picture N>`）。

- `身份`：脸型、发型剪影、体型、比例、固定服装 → 图不决定站位。
- `造型状态`：服装层叠、妆容、损污、配饰状态。
- `地理`：场景布局、固定家具、光源方向、色彩。
- `构图`：起始框取景、屏幕方向、站位、轴线、禁止镜像。
- `起始帧`：本单元第一格构图姿态；一镜最多一张。
- `结束帧`：已接受终态，必须与起始帧同时出现（本套件不用 L2VA 尾帧推断开场）。

每张参考图只承担它在 `用途` 和 `控制` 里声明的事。角色图不决定站位，场景图不决定脸，
**图归属铁律（一张图只能属于一个主体）。** `<Picture 1>` 是"第 1 张挂图"，不是"第 1 个角色"。
`<Subject N>` 与 `<Picture N>` 是两套独立编号：

- 图归属由 `- 主体映射：` 写死：`<Subject 2> = 女儿 = <Picture 1> = S2` 表示
  `<Picture 1>` 是女儿的图，**只有女儿**能在定义行里写 `in <Picture 1>`。
- 同一单元里另一个角色（画外、只作身份定义）**没有图**，定义行不许写 `in <Picture N>`，要写
  `<Subject 1> is the … , defined by this description only (no reference picture for her in this
  clip), with …`；中文写 `<Subject 1> 是…（本单元没有她的参考图，只按文字定义）：…`。
  否则模型会把同一张脸安到两个人身上——母女变同一张脸，是本套件最常见的翻车。
- `<Picture N>` 的角色行必须点名归属：`<Picture 1> defines the identity, face and costume of
  <Subject 2> only`，不写"这张图定义身份"这种无主句。
- `<Picture N> anchors the environment` 只能给 `用途：地理` 的图；身份图不许当场景锚。
- 因此"身份图是 `<Picture 1>`、环境图是 `<Picture 2>`"完全正常：不要为了编号好看把场景图排到 1，
  也不要因为"母亲是 Subject 1"就以为她是 `Picture 1`。

站位图不决定人物身份。素材编号按同类素材**在本单元「输入参考图」里**的 `顺序` 递增：
第 1 张图是 `<Picture 1>`，视频、音频各自从 1 数起（每个单元/job 各自从 1 起，
多镜容器合法重编号的前提）；编号必须和挂图顺序一致，
两套编号不一致时模型会收到矛盾说明而接口不报错。

## H3 正文规则（reference 六段为主）

- `subject_definitions`：每个条目独立一行，标签打头（官方写法）：
  `<Subject 1>` 独立成行，定义行写 `<Subject 1> is the ... in <Picture 2>, with ...`，
  逐字抄视觉设定里的脸型/五官/识别特征/服装各层；图只用于定义某个 Subject 时
  在定义行内引用（`in <Picture 2>`），不另起独立行；
  图本身锚场景/站位/成品帧/关键帧才单独成行
  （`<Picture 1> is the opening composition of this shot` /
  `anchors the environment` / `is the previous shot's frame`）。不写动作。
- `summary`：一到三句写本单元的可见状态变化，不写抽象情绪结论；
  **首行官方任务类型前缀**（常用 `[reference generation]`；关键帧当首/尾帧用
  `keyframe completion`，续接上一段实际视频 `video continuation`，多关系 ` + ` 拼接）；
  前缀后只用已定义标签，不引入新标签。
- `retention_analysis`：逐条写标签、出现镜次、保留强度（`fully_preserved /
  partially_preserved / attribute_transfer / weak_reference`；音频
  `fully_copy / partially_copy / reference / weak_reference`）。站位图必须写明
  屏幕布置、轴线、禁止镜像被保留。
- `detailed_description`：逐镜 `[Shot 1]`（无时间戳）、`[Shot 2] At 00:03.500`
  严格递增且落在单元时长内；台词跟说话人可见动作同放一个事件；
  逐字对白只写一次在 `<d>[Chinese] ...</d>` 内，语言标签外口语特征。
- `overall_soundscape`：只汇总环境声、物理音效、非语言人声；不重复对白。
- `non_diegetic_music`：无非画内配乐写 `N/A`，不留空让模型补乐。
- 把"无字幕、无水印、禁换位、禁手脸融合"等约束**折进对应段落**，不另开 H3 不认识的
  字段；只保留针对本镜真实风险的约束，不堆通用负面词。

文戏的逐镜写法、嘴型纪律（单人镜覆盖法）、声音锁两截、成品帧续拍、接戏三类型、
不可能动作三拍结构、Forbidden 三层，全部见
[references/h3-reference-guide.md](references/h3-reference-guide.md)。

## 对白、时长与多镜容器

- 先估完整发声时间再定单元时长；H3 中文小样本约 4.1 个可发声字/秒，
  放不下就延长或拆镜，不靠加快语速塞台词。
- 一个单元推荐只装一个主要动作。多镜容器（一次生成装多 `[Shot N]`）资格：
  每一刀都有已接受的起始关键帧（`REF-...` 或 `PLAN-...` 的 `用途：起始帧`），
  成员时长之和落在 4–15 秒，`<Picture N>` 按容器清单重编号，正文第一行写对齐句
  （`<Picture 1> aligns with the 0.00-second mark ...`）。缺一刀关键帧就逐镜生成。
- 台词与口型同轨不是模型保证：生成后仍核听逐字文本、停顿、尾音和口型落点。

## 交付格式（中英文对照，缺一不可）

每次交付按顺序：

1. **中文标题 + 一句设定**（如「汉服石阶对峙」）
2. **关键处理说明**——最容易拍坏的点、用什么手法绕过去了（给用户复核判断用，不能省）
3. **分镜表**：镜头 / 景别 / 内容，一镜一行，中文
4. **英文 H3 正文代码块**（` ```text `，可直接整段复制投喂 H3）
5. **逐段中文对照代码块**（另起一个 ` ```text ` 块，紧跟在英文块下面）——
   六段/三段一段不落、顺序相同、逐句翻译；台词 `<d>[Chinese]…</d>` 是中文，
   原样保留不翻译

**双块铁律（每个 H3-UNIT 两个块，不合并、不交叉）：**

- 英文块只放英文 H3 正文；中文块只放中文对照。中文混进英文块会污染提示词解析，
  英文混进中文块会让"整段复制中文给创作者看"失效。
- 两块的段落顺序、字段名逐条对应（`subject_definitions` ↔ **主体定义：**，
  `summary` ↔ **概要：**，依次类推），块内不再加标题、不加小标题。
- **英文块允许的两处中文，只有这两处：**
  1. 台词行 `<d>[Chinese]…</d>`——必须原样保留中文逐字台词，这是 H3 的台词格式，
     不是中文污染，不要翻译、不要删、不要改成英文。
  2. 服装/材质的中文名括注，如 `oatmeal fine-knit cardigan (燕麦色细针织开衫)`——
     与视觉设定的服装中文名对齐，保留。
  除这两处外，英文块里出现任何中文（中文标签、中文句子、中文段落）都算污染，必须删。
  典型事故：把中文 `<Subject N> 是 …` 定义行插进英文块，英文块整段投喂会被干扰。
- 中文块用 ` ```text ` 而不是 ` ```markdown `，避免对照里的 `-`、`|`、`<d>` 被渲染成列表或表格。
- 结构校验器同时兼容两种排法（对照在块外或块内），`validate_h3_storyboard.py`
  只要求 `### 中文对照` 出现在 `### H3 提示词` 之后。

## 自检清单（交付前逐条过）

- [ ] 每单元有唯一状态链、4–15 秒整数时长、明确模式、完整六段（或三段）正文
- [ ] 代码块外没有任何独立成行的 `<Subject N>` / `<Picture N>` 标签定义（文件头、单元元数据、分镜表都不许）
- [ ] 每个 `<Subject N>`、`<Picture N>`、`Sx` 都有唯一定义且跨单元一致；编号与挂图 `顺序` 一致
- [ ] 一张图只属于一个主体：无参考图的角色写成 `defined by this description only`，没写 `in <Picture N>`；场景锚只给 `用途：地理` 的图
- [ ] 每张参考图有 `顺序`、中文名、`用途`、`控制`、`不得控制`
- [ ] 分镜表里每句台词都在某 `[Shot N]` 里以 `<d>[Chinese]…</d>` 落地
- [ ] 每句台词有单人镜覆盖（或过肩虚化/双人单实焦兜底），该镜有 Mouth discipline 行
- [ ] 无台词镜写了 `Mouths closed, both still.` 或等价的嘴部状态
- [ ] 不说话的角色的音色一个字没写，且写了 `stays silent` 声明
- [ ] 屏幕左右、身体朝向、轴线、身高差、道具摆位、待机角色状态在每镜重述
- [ ] 每个镜头边界都定了类型（紧接/跳切/换场）；紧接有承接三件套，跳切有主动断
- [ ] 不可能动作走三拍结构；位移后保持原屏幕侧
- [ ] 无 BGM 时 `non_diegetic_music: N/A`；有 BGM 时写清切断点
- [ ] 每个单元两个代码块：英文正文块 + 中文对照块，各自可整段复制，块内不混语言
- [ ] 中文对照块紧跟英文块，段落顺序与字段名逐条对应、逐句翻译
- [ ] 结构校验只跑过一次且通过（`python scripts/validate_h3_storyboard.py <成稿路径>`）

修订时保留未受影响的 `H3-UNIT-...` 和 `SHOT-...` ID；拆分、合并或改参考图后，
明确哪些下游 job 需要重新生成。

**交付节奏（防拖慢）：** 读事实 → 弹确认卡停 → 一次写成稿 → 跑一次校验 → 交付。
中途不要边写边跑脚本，不要为某个单元单独建测试稿，也不要顺手"优化"校验器。

**校验只跑一次，不迭代。** 成稿写完跑一次 `python scripts/validate_h3_storyboard.py <成稿路径>`：

- Windows 用 `python`，不要用 `python3`（`python3` 常是 Microsoft Store 占位别名，会报错或弹商店）。
  用系统已装的解释器，不要去找 ComfyUI、其他软件自带的 python 当运行时。
- 有报错就按报错改**成稿**一轮，再跑一次确认；两次仍不过，把剩余问题写进交付说明交创作者判断，
  不要继续循环。
- **不要改 `scripts/validate_h3_storyboard.py` 去迁就成稿**，也不要为验证校验器另造反例文件
  （`_neg*.md`、`_test_*.md`、`tmp_*.py`）。校验器是尺子，不是交付物。
- 交付前把临时脚本和测试稿删干净。

## 按需知识

- 六段全字段、模式映射、逐镜手法、接戏、词表与中英对照译法：[H3 参考生全模式指南](references/h3-reference-guide.md)
- 三段模式（base / first_frame / first_last_frame）：[references/base-modes.md](references/base-modes.md)
- 高动态武戏（12 拍三段式、镜头纪律、无胜负收尾）：[references/mode-action.md](references/mode-action.md)
- 人物模式（定妆照七段、四视图、量化精度、识别特征）：[references/mode-character.md](references/mode-character.md)
- 可复制空模板：[H3 参考生模板](assets/h3-reference-template.md)
- 结构检查（只跑一次）：`python scripts/validate_h3_storyboard.py <成稿路径>`
