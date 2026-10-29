# H3 分镜契约

本文件只规定 `short-drama-h3-storyboard` 的字段、模式映射和完成检查。项目已有 `short-drama.json`、
《剧本.md》和《视觉设定.md》时，以项目事实为最高优先级；本文件不创造剧情、身份或用户未选择的生产参数。

## 1. 先登记三类 ID

### 生成单元与镜头

- `H3-UNIT-<EP>-<SEQ>`：一次 H3 job。时长 4–15 秒。
- `SHOT-<EP>-<SEQ>`：单元内的镜头。一个单镜单元仍写 `[Shot 1]`。
- `来源`：指向《剧本.md》中真实存在的场景 ID，必要时附短引文。

### 主体与图片

- `<Subject N>`：需要跨镜保持的人物、地点、道具或可见内容。
- `<Picture N>`：按本 job 的实际挂图顺序编号。每个 `<Picture N>` 必须能在参考清单里找到同一顺序。
- `用途`：继续使用项目的封闭集合
  `身份 / 造型状态 / 地理 / 构图 / 尺度 / 效果 / 起始帧 / 结束帧 / 风格`。
- “站位参考帧”“轴线参考帧”“站位图”统一映射为 `用途：构图`，并在 `控制` 写明
  屏幕左右、朝向、轴线、入口方向和禁止镜像。

示例：

```markdown
- 参考图：REF-SHINIANG（顺序：1）· 输入/参考图/师娘.png《师娘定妆图》（用途：身份；控制：脸型、发型剪影、体型、固定服装；不得控制：本镜站位、动作、表情）；REF-QINGER-BLOCK（顺序：5）· 输入/参考图/青儿站位.png《青儿站位参考帧》（用途：构图；控制：屏幕左右、人物间距、进入方向、轴线；不得控制：人物脸型、服装、道具）
```

`REF-...` 只表示文件此刻在项目中可读；创作者在生成时自行挂图的图片使用项目约定的 `PLAN-...`。
两种槽位都决定 H3 正文里的 `<Picture N>` 编号。

### 说话人

- `S1`、`S2` 等是跨单元稳定的说话人 ID。
- 推荐 `<Subject N>` 与 `Sx` 采用同一数字，但项目已有声线表时以项目为准，并在每个单元显式写映射。
- 不允许只写 `S4` 却只在正文中定义了 `<Subject 3>`，也不允许同一角色在不同单元更换 `Sx`。

## 2. 模式映射

| 本次 job 的图片组合 | `模式` | H3 正文结构 |
|---|---|---|
| 无图，且创作者明确选择文生视频 | `base` | 三段 |
| 只有一张 `用途：起始帧` | `first_frame` | 三段 |
| 一张起始帧 + 一张结束帧 | `first_last_frame` | 三段 |
| 角色、场景、道具、造型或构图参考与起始帧混用，或只有这些参考图 | `reference` | 六段 |

H3 的首尾帧输入和参考输入互斥。“起始帧 + 角色图 + 场景图 + 站位图”整组走 `reference`，不要让
同一 job 同时出现 `first_frame` 和 `reference_image` 两套互斥输入。模式由图片用途读出，不由用户的
“参考生”口头叫法猜测。

## 3. H3 六段字段

### `subject_definitions`

把所有标签绑定到可见事实。每句话只让一张图负责它真正能控制的东西。

```text
subject_definitions: <Subject 1> is Shiniang in <Picture 1>, with ..., preserving face, costume and body proportions from the reference. <Subject 2> is Feng in <Picture 2>, ... <Picture 3> anchors the environment: ..., preserving layout, palette and lighting. <Picture 5> is the locked blocking reference: preserve screen arrangement and axis; do not mirror it.
```

不要在这里写“角色会做某动作”。动作属于 `detailed_description`。

### `summary`

用一到三句概括本单元的可见状态变化。只写画面和声音能验证的结果，不写“她明白了一切”这类抽象结论。

### `retention_analysis`

逐条写标签、出现镜次和保留强度：

```text
retention_analysis: <Subject 1> (appears in [Shot 1]–[Shot 3]): fully_preserved - face shape, costume layers, body proportions and height relationship stay identical; pose follows this unit. <Picture 3> (appears in [Shot 1]–[Shot 3]): partially_preserved - pond-side layout, lantern tree, pavilion direction and night palette are kept. <Picture 5> (appears in [Shot 1]–[Shot 3]): fully_preserved - Shiniang stays screen-LEFT, Feng stays screen-RIGHT, the camera never crosses the axis and the arrangement is never mirrored.
```

允许的视觉保留强度：

- `fully_preserved`
- `partially_preserved`
- `attribute_transfer`
- `weak_reference`

### `detailed_description`

逐镜写动作、说话人和同步声音：

```text
detailed_description: [Shot 1] Medium shot. Qing'er descends from the railing in the background and walks ... [Shot 2] At 00:03.500, medium shot on Qing'er ... <Subject 3> (S3) says: <d>[Chinese]时间不早了，娘子，我们该回去了。</d> The other women keep their lips completely closed. [Shot 3] At 00:07.000, two-shot of the seated pair; neither speaks and both mouths remain closed.
```

规则：

- 第一镜不要求时间戳；`[Shot 2]` 起使用 `At MM:SS.mmm`，严格递增且小于单元时长。
- 对白只放在说话人的动作事件里，`<d>[Chinese] ...</d>` 内只保留语言标签和逐字台词。
- 台词期间有其他正脸角色时，明确写 `keeps lips completely closed`。
- 动作负载过大时拆单元，不靠抽象“自然过渡”让模型补写。

### `overall_soundscape`

只汇总环境声、物理音效和非语言人声，不重复对白。没有对白时仍写清底声或静默。

### `non_diegetic_music`

没有非画内配乐时写 `N/A`。明确只要环境声时，同时在这一段和 `overall_soundscape` 里写清，
不要让模型自行补 BGM。

## 4. 三段模式

`base`、`first_frame` 和 `first_last_frame` 使用：

```text
integrated_multimodal_description: [Shot 1] ...
overall_soundscape: ...
non_diegetic_music: N/A
```

三段仍是一次整体提交。`first_frame` 从输入帧可见姿态开始；`first_last_frame` 只能到达已接受的
结束状态。不要把六段例子机械替换成三段，也不要删掉对白的时间位置。

## 5. 多镜容器

一个 H3 单元可包含多个 `[Shot N]`，但必须同时满足：

1. 每一个切点都有已接受的起始关键帧（真实 `REF-...` 或可分为 `PLAN-...`）；
2. 全部成员时长之和仍在 4–15 秒；
3. 参考图标号重新按本 job 的挂图顺序编号，并写清哪张对齐哪一刀；
4. `detailed_description` 的每一切点有明确时间戳。

如果只准备第一刀的关键帧，其余镜头逐镜生成。没有逐切关键帧时不要伪装成容器。

## 6. 训练样本的完整映射

用户给出的 `镜 7E` 可以按下面方式吸收：

| 原写法 | H3 分镜里的位置 |
|---|---|
| `<Subject 1/2/3>` 定义角色 | `subject_definitions` |
| `<Picture 3>` 锁场景 | `subject_definitions` + `retention_analysis` |
| `<Picture 5>` 锁站位、不得镜像 | `用途：构图` 的参考槽位 + `retention_analysis` |
| `S1/S2/S4` 固定声线 | 单元元数据 `声线映射` + 台词外的声音描述 |
| `Mouth discipline` | `detailed_description` 的对白事件和多人约束 |
| `Spatial axis` | `空间锁` + `detailed_description` |
| `Audio` | `overall_soundscape` |
| `no BGM` | `non_diegetic_music: N/A` |
| `Forbidden` / `Mandatory` | 拆进主体、保留分析、逐镜和声音段的风险专项约束 |

原样本里需要修正的地方：

- `Qing'er (S4)` 与 `<Subject 3>` 没有显式映射；
- `Mouth discipline` 最后一句停在 `Every`，必须补完整；
- 16 秒超过当前 H3 4–15 秒上限，应拆成两个单元或压缩；
- `[Shot 2]` 之后没有切镜时间戳；
- “新写台词”不能由视频分镜阶段产生，必须先进入写作或剧本修订。

## 7. 交付前检查

- 每个单元只有一个主要状态转换和合法时长。
- 每个 `<Subject N>`、`<Picture N>`、`Sx` 都有定义并使用一致。
- `reference` 六段完整，其他模式三段完整。
- 每个后续切点有时间戳；台词属于对应说话人和镜头。
- 非说话者口型闭合；双人无对白镜两人嘴都闭合。
- 屏幕左右、轴线、进入方向、身高和持物连续。
- 无 BGM 时写 `non_diegetic_music: N/A`。
- 没有把通用负面词堆成模板；每条禁令都对应一个具体风险。