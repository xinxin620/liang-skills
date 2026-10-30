# H3 参考生分镜 · 空白模板

复制整段填占位。【】之外的固定句式不要改——它们是稳定出片的锚点。

每个单元出**两个** ` ```text ` 块：上面是英文 H3 正文（整段复制投喂），
下面是中文对照（整段复制给人看）。中文不要混进英文块。

## H3-UNIT-<EP>-<SEQ> · <单元名>
- 时长：<4–15 整数> 秒
- 模式：reference
- 来源：<真实剧本场景 ID>
- 参考图：<REF/PLAN 槽位，逐项：顺序、路径或条目 ID、中文名称、用途、控制、不得控制；按顺序编号成 <Picture N>>
- 主体映射：<Subject 1> = <角色> = <Picture N> = <Sx>
- 声线映射：<角色> = <Subject N> = <Sx> = <固定音色 - now 本场状态>
- 空间锁：<屏幕左右、朝向、轴线、出入口、禁止镜像>
- 口型纪律：<只有谁可以动嘴；其他人嘴部状态；无对白镜写双唇闭合>
- 状态链：<起点> → <唯一主变化> → <可验证终点>
- 声音：<环境声、物理音效、对白来源>
- 镜头边界：<紧接 / 跳切省略 / 换场，逐边界>

### H3 提示词（一次整体提交）

```text
subject_definitions:
<Subject 1> is 【角色名】 in <Picture 1>, with 【身份 + 脸型骨相 + 五官 + 识别特征 + 服装各层，逐字抄视觉设定】. Preserve the facial features, hairstyle, costume, body proportions, and overall appearance from the reference image. <Subject 1> (S1) always uses one fixed voice: 【终身固定音色】 - now 【本场状态】. Do not change.
<Subject 2> is 【角色名】 in <Picture 2>, with 【身份 + 脸型 + 服装各层】. Preserve the facial features, hairstyle, costume, body proportions, and overall appearance from the reference image.
<Picture 3> anchors the environment: 【场景 + 固定家具 + 光源方向 + 色调】. Preserve its layout, palette and lighting exactly.
<Picture 4> is the locked blocking reference: keep the same screen arrangement - do not mirror it.
<Picture 5> is the previous shot's frame: the exact 【地点】, lighting, prop arrangement and character positions to continue from.
【不说话的成员：在对应 Subject 条目尾部声明 <Subject N> (SN) stays silent in this scene and does not speak at all.（音色一个字不写；无台词角色不写声音锁）】
【多镜容器时，正文第一行（subject_definitions 之前）加对齐句：<Picture 1> aligns with the 0.00-second mark as the opening frame of [Shot 1]; <Picture 2> aligns with the 3.00-second mark as the frame of [Shot 2]; ...（各切点秒数与 [Shot N] 的 At 时间戳一致）】
【风格基调句放 [Shot 1] 之前（六段模式要求）：The target video uses a cinematic live-action style with 【色调 + 光质 + 质感】.】
summary: [reference generation] 【一到三句本单元可见状态变化，不写抽象结论；前缀按实际任务类型选，如 keyframe completion / video continuation，多关系用 + 拼接】
retention_analysis: <Subject 1> (appears in [Shot 1]–[Shot N]): fully_preserved - 【脸型、服装层、比例、身高关系】; pose follows this unit. <Picture 3> (appears in [Shot 1]–[Shot N]): partially_preserved - 【布局与色光保留，道具摆位随本单元】. <Picture 4> (appears in [Shot 1]–[Shot N]): fully_preserved - 【A stays screen-LEFT, B stays screen-RIGHT; axis never crossed; arrangement never mirrored】.
detailed_description: [Shot 1] 【景别】, <Subject 1> (S1) alone, sharp: 【情绪副词；可见身体小动作】. <Subject 1> (S1) says:
<d>[Chinese]【逐字台词】</d>
Mouth discipline: only 【角色】 moves her lips; no other character shares the frame. [Shot 2] At 00:03.500, 【景别】: 【动作 + 物理结果】. No dialogue; both mouths stay closed.
overall_soundscape: 【一到四句：环境声 + 物理音效 + 非语言人声，不重复对白】
non_diegetic_music: N/A
```

### 中文对照

```text
主体定义：
<Subject 1> 是 <Picture 1> 中的【角色名】，【身份 + 脸型骨相 + 五官 + 识别特征 + 服装各层】。保持参考图中的五官、发型、服装、身材比例与整体形象。<Subject 1> (S1) 声音固定为【终身固定音色】——现在是【本场状态】，不变。
<Picture 3> 锚定环境：【场景 + 固定家具 + 光源方向 + 色调】。严格保持其布局、色调与光效。
概要：参考生成。【一到三句可见状态变化】
保留分析：<Subject 1>（出现于 [Shot 1]–[Shot N]）：完整保留——【脸型、服装层、比例、身高关系】；姿势随本单元。
分镜正文：[Shot 1]【景别】，<Subject 1> (S1) 单人，实焦：【情绪 + 可见小动作】。<Subject 1> (S1) 说：
<d>[Chinese]【逐字台词】</d>
嘴型纪律：只有【角色】动唇，本镜无他人入画。
环境声底：【环境声 + 物理音效 + 非语言人声】
非画内配乐：无
```

## 填空提示

- **结构顺序固定**：`subject_definitions → summary → retention_analysis → detailed_description → overall_soundscape → non_diegetic_music`，六段同一条正文一次提交；
  多镜容器的对齐句写在 `subject_definitions` 之前（正文第一行），风格基调句写在 `[Shot 1]` 之前。
- **条目独立成行、标签打头**：`subject_definitions:` 之后每个被单独追踪的主体各占一行，标签写在行首（官方写法）；
  图只用于定义某个 Subject 时在定义行内写 `in <Picture N>`，不另起一行。
- **summary 首行任务类型前缀**：默认 `[reference generation]`；关键帧当首/尾帧用写 `keyframe completion`，
  续接上一段实际视频写 `video continuation`，多关系用 ` + ` 拼接不重复。
- **声音锁折进 Subject 条目**：终身音色写在说话者 Subject 条目尾部
  （`<Subject 1> (S1) always uses one fixed voice: … - now …`），不再单独成段；
  不说话的成员写 `stays silent` 声明，音色一个字不写。
- **说话人写法 `<Subject N> (Sx)`**：被参考主体在画内说话时两者同写；画外音标 `off-screen`；
  无台词角色不分配也不复用 `(Sx)`。
- **每句台词一个单人镜**：`<Subject N> (Sx) alone, sharp` + 该镜 `Mouth discipline: only <角色> moves her lips; no other character shares the frame.`——防串嘴最有效的一条。禁止"两张脸都实焦"的双人镜配台词。
- **情绪配动作**：情绪副词 + 可见身体小动作，两句都给（`quiet and halting, each word costing her something; one hand tightens on her sleeve`）。
- **声音锁两截**：破折号前终身音色，`- now …` 本场状态。
- **场景陈设与道具摆位每镜重述**；成品帧续拍必写 `do not mirror it, do not rearrange it`。
- **待机角色给明确动作**（`holding her bamboo broom, watching from a distance, soft focus`）。
- **站位写身体朝向**（`body facing screen-right`），只写左右不够。
- **紧接三件套**：镜尾停在哪拍 / 镜首从哪拍起 / `no restarting the movement`；跳切**不**引上一帧并主动断。
- **不可能动作三拍**：前一态 → 无脸闪光帧 → 硬切后一态 + 余韵；位移后保持原屏幕侧。
- **时长**：4–15 整数秒；对白按约 4.1 可发声字/秒 估容量，放不下拆镜。
- **参考图上限**：9 张 reference_image + 1 起始帧 + 1 尾帧 + 3 段参考视频 + 3 段参考音频（各 2–15 秒、合计 ≤15 秒）。

## 逐段中文对照（强制，紧跟英文代码块之后，放代码块外面）

```markdown
### 中文对照

**<Subject 1>** 是 <Picture 1> 中的【角色名】：【身份 + 服装 + 发式 + 佩饰】。保持参考图中的五官、发型、服装、身材比例与整体形象。
**主体定义 / 概要 / 保留分析 / 分镜正文 / 环境声底 / 非画内配乐**：六段一段不落，顺序相同，逐句翻译；
`[Shot N]` 按编号逐条译；台词 `<d>[Chinese]…</d>` 原样保留，不翻译不改写；
`retention_analysis` 的保留强度按统一译法（完整保留 / 部分保留 / 属性转移 / 弱参考）。
**嘴型纪律**：只有【角色】动唇，本镜无他人入画。
```
