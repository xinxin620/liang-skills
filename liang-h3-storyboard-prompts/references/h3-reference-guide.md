# H3 参考生全模式指南（reference 六段为主）

目标档案：`target_video_model: minimimax-h3`（海螺）。本指南管**参考生视频**（`reference`
六段）的完整写法；三段模式见 [base-modes.md](base-modes.md)，武戏见
[mode-action.md](mode-action.md)，人物图见 [mode-character.md](mode-character.md)。

## 1. 模式怎么定

| 本单元绑定的图 | H3 模式 | 正文结构 |
|---|---|---|
| 没有图，且创作者**明确**选择文生视频 | `base` | 三段 |
| 只有一张 `用途：起始帧` | `first_frame` | 三段 |
| 一张 `用途：起始帧` + 一张 `用途：结束帧` | `first_last_frame` | 三段 |
| 角色、场景、道具、造型、构图参考与起始帧混用，或只有这些参考图 | `reference` | **六段（主路径）** |

- 模式由 `用途` 组合读出，不由"想不想用多模态"决定；"参考生"口头叫法不算文生视频授权。
- H3 首/尾帧输入与参考输入**互斥**：「起始帧 + 角色板 + 场景板 + 站位图」整组走
  `reference`，起始帧也以 `reference_image` 送入，不要拆成两套互斥输入。
- 结束帧只在同时绑定起始帧时出现。本套件不使用 H3 官方的 L2VA 尾帧推断开场：
  开场由已接受起点决定，交给模型推断会让镜头起点失去权威。

## 2. 全局编号规则

- `<Picture N>` 是**全局素材编号**，跨场次累加：一张图定号终身不变，新图按上传顺序接号，
  不重排、不复用、不跳号。同一场引用不相邻的号（1、2、7、10）正常，不要为"连续好看"改号。
- `<Subject N>` 编号独立于 Picture：Subject 是主体的抽象定义，指向哪张图由文字写明
  （`<Subject 3> is Feng in <Picture 7>`）。**Subject 编号 ≠ Picture 编号，允许。**
- 有台词的角色，`S` 编号与 `Subject` 编号对齐（`<Subject 1>, S1`）；没有台词的角色不写声音锁。
- 同一场景里角色的描述文字**逐字复制**，不做同义替换——改写会让模型以为换了人。
- 写六段正文前，先把本单元参考图按 `顺序` 列一遍：

```text
REF-SHOT-START（顺序：1；用途：起始帧）  -> <Picture 1>
REF-XIAOYU-SHEET（顺序：2；用途：身份）  -> <Picture 2>
REF-STUDY-PLATE（顺序：3；用途：地理）    -> <Picture 3>
```

手写编号必须与挂图 `顺序` 一致：两套编号不一致时模型收到矛盾素材说明，接口不会报错。

素材五种角色：

| 类型 | 写法 | 锁住什么 |
|---|---|---|
| 角色图 | `<Picture N>` + `<Subject N>` 定义 | 脸、服装、身材、发式 |
| 场景图 | `<Picture N> anchors the environment` | 布局、色调、光效 |
| 站位帧 | `<Picture N> is the locked blocking reference` | 屏幕左右、机位侧、轴线 |
| **成品帧** | `<Picture N> is the previous shot's frame` | 一图顶三图：场景＋站位＋道具＋光线＋动作接续点 |
| 道具图 | 特写镜里引用，retention 里加"形状每镜一致" | 道具细节 |

**成品帧续拍**（最省素材）：上一镜已出片时直接引用，配
`reproduce this arrangement exactly, do not mirror it, do not rearrange it`，
一并封掉道具被挪、光线换向、人物换位三种漂移。

素材不足（只给了角色图）：`<Picture N>` 只留给真实上传的图，不要引用不存在的号——
缺场景图用一行 `Environment: …` 文字锁死；缺站位帧用一行 `Locked blocking (do not mirror): …`
写成死规则，后续镜头原样复述。

## 3. 六段字段逐段写法

六段是**同一条正文、一次提交**。顺序固定，段名英文。

### `subject_definitions`

- 句式 `<Subject 1> is ... in <Picture 2>, with ...`，把每个主体绑到标签；
  逐字抄视觉设定里的脸型骨相、五官、识别特征、服装各层（内层也写）。
- `<Picture N>` 单独锚场景（`anchors the environment`）、站位
（`is the locked blocking reference: keep the same screen arrangement – do not mirror it`）、
  成品帧（`is the previous shot's frame: the exact … to continue from`）。
- 不写"角色会做某动作"——动作属于 `detailed_description`。

### `summary`

一到三句写本单元可见状态变化，只写画面和声音能验证的结果，不写"她明白了一切"。

### `retention_analysis`

逐条写标签、出现镜次、保留强度：

- 视觉：`fully_preserved / partially_preserved / attribute_transfer / weak_reference`
- 音频：`fully_copy / partially_copy / reference / weak_reference`

```text
retention_analysis: <Subject 1> (appears in [Shot 1]–[Shot 3]): fully_preserved - face shape,
costume layers, body proportions and height relationship stay identical; pose follows this unit.
<Picture 3> (appears in [Shot 1]–[Shot 3]): partially_preserved - pond-side layout, lantern tree
and night palette are kept. <Picture 5> (appears in [Shot 1]–[Shot 3]): fully_preserved -
Shiniang stays screen-LEFT, Feng stays screen-RIGHT; the camera never crosses the axis and
the arrangement is never mirrored.
```

- 每张图只负责它 `用途` 声明的事：角色板不决定构图，场景板不决定人物长相，
  站位图把"屏幕布置、轴线、禁止镜像被保留"写进来。
- `PLAN-...` 的图套件没看过像素：保留强度按它 `用途` 必须保留什么写，事实取自
  视觉设定和本镜冻结关键帧，不写"未验证"或省略。

### `detailed_description`

逐镜写动作、说话人、同步声音：

- 第一镜无时间戳；`[Shot 2] At 00:03.500, ...` 起严格递增且小于单元时长。
- 切镜用 `the camera cuts to / the shot transitions to / the shot changes to`；
  用户明确要求才用 cross-dissolve / fade / wipe。
- 运镜写成自然英语动作（运动类型 + 幅度 + 速度，中幅中速可省）：
  `The camera pushes in with small amplitude at slow speed toward the folded letter in her hands.`
  可用词：Zoom/Push In-Out, Pan, Truck, Tilt, Pedestal, Arc, Tracking, Static, Shake,
  POV, Roll；`with small/large amplitude`，`at slow/fast speed`。
- 对白只放说话人的动作事件里；`<d>[Chinese] 逐字台词</d>` 内只有语言标签和原文，
  不翻译不改写，逐字在对白中只出现一次。
- 台词期间有其他正脸角色：明写 `The messenger does not speak; his lips remain completely closed.`
- 画外音：`says in an off-screen voiceover` + `while his lips remain completely closed`。
- 对白跨切点：`<scenetrans>` 并声明 `continues seamlessly across the cut`；
  视频结束截断：`<cutoff>`（只用于剧本已要求的截断）。
- 画面可见文字（霓虹、标牌、屏幕）用英文双引号原样保留，如 `"营业中"`；
  非画内字幕/caption/对白叠加默认不生成，正文直接写明。

### `overall_soundscape`

一到四句、一段：全片环境声、物理音效、非语言人声（风雨、脚步、呼吸、笑、喘息）。
对白、歌、画内音乐不重复到这里。

### `non_diegetic_music`

一到三句：观众才听得到的 BGM，写乐器/速度/节奏/动态变化，不用抽象情绪词。
没有就写 `N/A`，**不留空让模型补乐**（有实测支撑）。角色听得见的音乐属于
`detailed_description`。

## 4. 文戏逐镜手法

### 嘴型纪律：单人镜覆盖法（强烈推荐）

**每一句台词，都由一个"只有说话者一张脸在画面里、且实焦"的镜头承担。**

```text
[Shot 1] Medium close shot, Feng alone, sharp: her eyes stay lowered, quiet and halting,
each word costing her something; one hand tightens on her sleeve as she speaks. S3 says:
<d>[Chinese]我娘其实在很远的地方。</d>
Mouth discipline: only Feng moves her lips; no other character shares the frame.
```

三种覆盖按优先级：

1. **单人镜（最佳）**：听者画外，零串嘴风险。
2. **过肩 + 听者前景虚化**：`over-the-shoulder, the listener a soft foreground blur`，脸不入画。
3. **双人镜但只一人实焦**：换镜成本太高时兜底，段尾写死。

**禁止**：一句台词配"两张脸都实焦"的双人镜——这是串嘴和换脸的主要来源。
无台词镜必须显式否定：`No dialogue; both mouths stay closed.` / `Mouths closed, both still.`
省略会让模型让人物乱动嘴。

### 声音锁两截

```text
<Subject 1>, S1 is always the speaker. S1 always uses one fixed voice:
a clear, cool young woman's voice, soft in volume - now low and earnest. Do not change.
```

- 破折号前是**终身音色**（跨场次逐字复制）；`- now …` 后是**本场状态**（可改）。
- 本场不说话的角色：音色一个字不写（写了等于告诉模型他准备说话），
  显式声明 `<Subject 2>, S2 stays silent in this scene and does not speak at all.`

### 接戏：先定类型，默认硬切

逐边界单独决定，不整场统一。**不写"接"就是不接**——反过来默认接会把硬切渲染成缓慢滑动。

| 类型 | 写法 |
|---|---|
| **紧接** | 引上一镜成品帧 + 三件套：镜尾停在哪一拍、镜首从哪一拍起、`no restarting the movement, no re-playing the step from the beginning`。只引帧不写动作进度会跳帧；不写第 3 条模型会把做完的动作重做。 |
| **跳切 / 省略** | **不**引上一帧，主动断：`no matching eyeline to the previous shot, no re-playing the previous pose, no continuous action carrying across the cut.` |
| **换场** | 重新锚定场景与站位；轴线**要么显式延续、要么显式重建**，不能沉默；镜号行注明场次关系。 |

### 不可能动作：拍前后，不拍过程

瞬移、变身、凭空出现道具——不写过程怎么发生，模型默认渲染成缓慢淡出或飘移。三拍：

| 拍 | 内容 |
|---|---|
| 前一态 | 人还在原处，实焦，画面干净，站位清楚 |
| 事件帧 | 闪光/脆响/冲击波，**固定机位、画面无人脸**，只一帧 |
| 后一态 | 硬切，人已经在新位置；用**余韵**代替过程——衣袍还在落、头发回位、尘土滚开、雾合拢 |

配 `No travel, no run, no arc - she was not there, now she is.` 位移后落点**保持原屏幕侧**，
轴线才不断。

### 身高与一致性每镜重述

以下信息**每个镜头段都要重写**，不因为"上一镜说过"省略：

身高差（角色换高度差落点时**分情况写**：台阶上她高、平地他高）、固定道具佩戴位置、
场景陈设（成品帧续拍尤其）、服装发式（逐字复制）、屏幕左右、**视线方向与身体朝向**
（`body facing screen-right`，站位描述最容易漏的一项）、说话人声音特征、
待机角色状态（必须给明确动作，`holding her bamboo broom, watching from a distance, soft focus`，
否则被模型删掉或乱走）。

### 镜头边界与容器内时间戳

多镜容器（一个 job 多个 `[Shot N]`）资格三条件：

1. 每一刀都有已接受的起始关键帧（`REF-...` 或 `PLAN-...` 的 `用途：起始帧`），缺一刀就逐镜生成；
2. 成员时长之和 4–15 秒（整数）；
3. 参考图按容器清单重编号，正文第一行写对齐句
   `<Picture 1> aligns with the 0.00-second mark as the opening frame of [Shot 1]; ...`，
   各切点 `At MM:SS.mmm` 与对齐句一致。

实测：只挂第一刀关键帧时后续切点构图明显偏离——**没有逐切关键帧不装容器**。

## 5. 对白容量

H3 中文小样本约 **4.1 个可发声字/秒**，较密的输入会赶词或静默截断。先估完整发声时间
再定单元时长；分镜镜长够长但开口太晚一样赶词。官方接口没有独立语速参数，
提示词里的语速与时机是生成指导，不是秒级保证。生成后核听逐字内容、停顿、尾音与口型。

## 6. 交付与对照

交付五件：中文标题 → 关键处理说明 → 分镜表 → 英文 H3 正文代码块 → 逐段中文对照。
对照放代码块**外面**，六段一段不落、顺序相同、逐句翻译；台词 `<d>[Chinese]…</d>` 原样保留。

### 六段字段的对照译法

| 字段 | 中文译法 |
|---|---|
| `subject_definitions:` | **主体定义：**（逐条译，标签 `<Subject N>` 保留） |
| `summary:` | **概要：** |
| `retention_analysis:` | **保留分析：**（保留强度译法见下） |
| `detailed_description:` | **分镜正文：**（逐镜译，`[Shot N]` 保留编号） |
| `overall_soundscape:` | **环境声底：** |
| `non_diegetic_music:` | **非画内配乐：**（`N/A` 译"无"） |

保留强度：`fully_preserved` 完整保留 / `partially_preserved` 部分保留 /
`attribute_transfer` 属性转移 / `weak_reference` 弱参考；
`fully_copy` 完整复制 / `partially_copy` 部分复制 / `reference` 仅参考 / `weak_reference` 弱参考。

### 固定句式的统一译法（每次都这么译）

| 英文 | 中文 |
|---|---|
| Preserve the facial features, hairstyle, costume, body proportions, and overall appearance from the reference image. | 保持参考图中的五官、发型、服装、身材比例与整体形象。 |
| Preserve its layout, palette and lighting exactly. | 严格保持其布局、色调与光效。 |
| keep the same screen arrangement – do not mirror it. | 保持同一画面站位，禁止镜像。 |
| is the previous shot's frame: … to continue from. | 是上一镜成品帧：可直接接续的……。 |
| reproduce this arrangement exactly, do not mirror it, do not rearrange it. | 原位复现，不镜像、不重排。 |
| always uses one fixed voice: … Do not change. | 声音固定为……，不变。 |
| Mouth discipline: only X moves her lips; no other character shares the frame. | 嘴型纪律：只有 X 动唇，本镜无他人入画。 |
| No dialogue; both mouths stay closed. | 无台词，双唇闭合。 |
| Neither speaks; both mouths stay closed. | 谁也没有出声，双唇闭合。 |
| while his lips remain completely closed | 而他双唇完全闭合 |
| continues seamlessly across the cut | 声音无缝跨过剪辑 |
| no restart/re-play of the previous pose | 不重演上一镜姿势 |
| body facing screen-right / screen-left | 身体朝画面右 / 朝画面左 |
| stands in the middle-left of the screen | 站在画面中左 |
| watching from a distance, soft focus | 远远看着，虚焦 |
| Heights stay fixed in every shot | 每一镜身高固定 |
| no BGM | 无 BGM |
| hard cuts only between shots. | 镜与镜之间只做硬切。 |
| no fades, no dissolves, no push transitions | 无淡入淡出、无叠化、无推镜转场 |

## 7. 素材数量上限

一次生成：最多 1 张首帧、1 张尾帧、9 张 `reference_image`、3 段 `reference_video`、
3 段 `reference_audio`；视频与音频每段 2–15 秒且各自合计 ≤15 秒；分辨率 `768P` 或 `2K`
（`MiniMax-H3-Max` 另为 480P/768P，且 Max 不支持六段参考模式，不要套用本页规则）。
超上限时在分镜阶段按失去它的代价从高到低取舍：起始帧 > 正在说话/做主动作的人物 >
必须认得出的道具 > 地点 > 其余入画人物 > 定调图；放弃的写明，必要事实进正文。
