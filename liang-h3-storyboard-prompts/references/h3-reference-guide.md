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

- `<Picture N>` 是**本 job（本单元）内的挂图顺序编号**：第 1 张图是 `<Picture 1>`，视频、
  音频各自从 1 数起。**不同单元各自从 1 重新编号**——这是官方规则，也是多镜容器合法
  重编号的前提（见第 4 节），不要写成"跨场次累加、终身不变"。
- 同一单元里，手写编号必须与挂图 `顺序` 一致：两套编号不一致时模型收到矛盾素材说明，
  接口不会报错。同一单元内引用不相邻的号（1、2、7、10）正常，不要为"连续好看"改号。
- `<Subject N>` 编号独立于 Picture：Subject 是主体的抽象定义，指向哪张图由文字写明
  （`<Subject 3> is Feng in <Picture 7>`）。**Subject 编号 ≠ Picture 编号，允许。**
- 有台词的角色，`S` 编号与 `Subject` 编号对齐（`<Subject 1>, S1`；正文里说话时写
  `<Subject 1> (S1)`）；没有台词的角色不写声音锁。
- 同一场景里角色的描述文字**逐字复制**，不做同义替换——改写会让模型以为换了人。
- 写六段正文前，先把本单元参考图按 `顺序` 列一遍：

```text
REF-SHOT-START（顺序：1；用途：起始帧）  -> <Picture 1>
REF-XIAOYU-SHEET（顺序：2；用途：身份）  -> <Picture 2>
REF-STUDY-PLATE（顺序：3；用途：地理）    -> <Picture 3>
```

手写编号必须与挂图 `顺序` 一致：两套编号不一致时模型收到矛盾素材说明，接口不会报错。

素材五种角色（外加两类素材标签）：

| 类型 | 写法 | 锁住什么 |
|---|---|---|
| 角色图 | `<Picture N>` + `<Subject N>` 定义 | 脸、服装、身材、发式 |
| 场景图 | `<Subject N> is the … environment in <Picture N>, featuring …` | 布局、色调、光效 |
| 站位帧 | `<Picture N> is the locked blocking reference` | 屏幕左右、机位侧、轴线 |
| **成品帧** | `<Picture N> is the previous shot's frame` | 一图顶三图：场景＋站位＋道具＋光线＋动作接续点 |
| 道具图 | 特写镜里引用，retention 里加"形状每镜一致" | 道具细节 |
| **参考视频** | `<Video 1> is the source video ...` | 只用于"续接/剪辑上一段实际视频"：动作、节奏、镜头与时间结构 |
| **参考音频** | `<Audio 1> is the voice-timbre reference for <Subject N> (Sx)` | 音色/音乐风格/对白内容/音效质感；`<Video N>` 与 `<Audio N>` 各自从 1 编号、互不配对 |

**成品帧续拍**（最省素材）：上一镜已出片时直接引用，配
`reproduce this arrangement exactly, do not mirror it, do not rearrange it`，
一并封掉道具被挪、光线换向、人物换位三种漂移。

**一张图只属于一个主体。** 角色图挂成 `<Picture 1>` 后，只有 `- 主体映射：` 里对应它的那个
`<Subject N>` 能写 `in <Picture 1>`，绝不能两个人共用一个 `in <Picture 1>`——那会让两个人共用一张脸。

**每单元重编号（默认做法）。** 每个单元是独立 job，两套编号各自从 1 起：

- `<Subject 1>` = `<Picture 1>` = **本单元入画的那个角色**（定妆图）。
- `<Subject 2>` = `<Picture 2>` = **环境**，写成
  `<Subject 2> is the dining-room environment in <Picture 2>, featuring …`
  （中文 `<Subject 2> 是 <Picture 2> 中的餐厅环境：…`）。官方示例就是
  `<Subject 1> is the coffee-shop environment in <Picture 1>, featuring …`，环境本来就该用 Subject 标记。
- **画外角色不定义**：本单元不入画、不发声的人，整条不写 `<Subject N>`、不占编号、不写音色，
  也不写 `defined by this description only` / `never borrow a face from <Picture 1>` 这类兜底句。
- 同一场里 A 单元女儿是 S1、B 单元母亲也是 S1，合法；文件头不要写"主体编号跨单元固定"。

素材不足（只给了角色图）：`<Picture N>` 只留给真实上传的图，不要引用不存在的号——
缺场景图用一行 `Environment: …` 文字锁死；缺站位帧用一行 `Locked blocking (do not mirror): …`
写成死规则，后续镜头原样复述。

## 3. 六段字段逐段写法

六段是**同一条正文、一次提交**。顺序固定，段名英文。

### `subject_definitions`

- **每个被单独追踪的条目独立一行，标签打头**（官方写法）：
  `<Subject 1> is the ... in <Picture 2>, with ...`。逐字抄视觉设定里的
  脸型/五官/识别特征/服装各层（内层也写）。
- **图只用于定义某个 Subject 时，在定义行内引用（`in <Picture 2>`），不另起独立行**；
  只有图本身是"某个镜头的首帧/关键帧/尾帧/构图锚"才单独成行
  （`<Picture 1> is the opening composition of this shot` /
  `is the previous shot's frame` / `is the locked blocking reference`）。
  环境例外：场景图也写成 Subject 条目（`<Subject 2> is the … environment in <Picture 2>, featuring …`），
  不要写孤立的 `<Picture 2> anchors the environment:` 行。
- 同一主体来自多张素材时合并来源并写清各素材提供什么：
  `<Subject 1> is the woman whose appearance comes from <Picture 1> and whose
  walking motion comes from <Video 1>.`
- 不写"角色会做某动作"——动作属于 `detailed_description`。
- **标签行只准住在这个代码块里。** `<Subject N> is …` / `<Subject N> 是 …` /
  `<Picture N> …` 独立成行时，只能出现在 `### H3 提示词` 下的英文 ```text 块内。
  文件头、单元元数据列表、分镜表、中文对照块都不许另起一行写标签定义
  （行内引用合法：`- 主体映射：<Subject 1> = 母亲 = <Picture 1> = S1`）。
  代码块外游离的标签行会被整段粘进错误位置，是"英文块里混进中文主体定义"的源头。
  这条靠人工核对，校验器不查。
- 官方完整示例（独立成行、标签打头）：

```text
subject_definitions:
<Subject 1> is the coffee-shop environment in <Picture 1>, featuring an exposed brick wall, an orange tufted sofa, and a wooden coffee table.
<Subject 2> is the fluffy white Samoyed in <Picture 2>, <Picture 3>, and <Picture 4>, with thick white fur, pointed ears, and a curved tail.
<Audio 1> is the voice-timbre reference for <Subject 3> (S1), containing a spoken vocal layer.
```

### `summary`

一到三句写本单元可见状态变化，只写画面和声音能验证的结果，不写"她明白了一切"。
**首行任务类型前缀（官方要求，方括号）**：常用 `[reference generation]`；
关键帧当首/尾帧用则 `keyframe completion`；续接上一段实际视频则 `video continuation`；
多个关系用 ` + ` 拼接不重复。例：

```text
[reference generation] The target video continues from the previous scene:
Qing'er sets down the firewood and hands Shiniang a water dipper; ...
```

前缀后只用已定义的 `<Subject N>` / `<Picture N>` / `<Video N>` / `<Audio N>`，
不在本段引入新标签。

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

- 六段模式下，`[Shot 1]` 之前先写一到两句风格/基调句（T2VA 把风格放在 `[Shot 1]` 后，
  full-reference 放在前）：`The target video uses a cinematic live-action style with ...`。
- 第一镜无时间戳；`[Shot 2] At 00:03.500, ...` 起严格递增且小于单元时长。
- 切镜用 `the camera cuts to / the shot transitions to / the shot changes to`；
  用户明确要求才用 cross-dissolve / fade / wipe。
- 运镜写成自然英语动作（运动类型 + 幅度 + 速度，中幅中速可省）：
  `The camera pushes in with small amplitude at slow speed toward the folded letter in her hands.`
  可用词：Zoom/Push In-Out, Pan, Truck, Tilt, Pedestal, Arc, Tracking, Static, Shake,
  POV, Roll；`with small/large amplitude`，`at slow/fast speed`。
- 官方建议正文 350–500 词（对白密集的内容优先装下完整发声时间线，不凑字数）；
  细节按各镜信息量分配，单镜不自动变短。
- 说话人写法：被参考主体在画内说话时写 `<Subject N> (Sx) says ...`；
  同一主体画外音保持同一写法并标 `off-screen`；说话人不对应已定义 Subject 时，
  用稳定声音描述 + `(Sx)`。`(Sx)` 按目标视频实际发声事件顺序首次分配，之后每个发声事件
  复用同一 ID；`retention_analysis` 里不写 `(Sx)`。
- 对白只放说话人的动作事件里；`<d>[Chinese] 逐字台词</d>` 内只有语言标签和逐字原文，
  不翻译不改写，逐字台词在对白中只出现一次；句末标点用 `. ? !`。
- 听不清的参考音频原声写 `[unclear]`，不猜不意译。
- 台词期间有其他正脸角色：明写 `The messenger does not speak; his lips remain completely closed.`
- 画外音：`says in an off-screen voiceover` + `while his lips remain completely closed`。
- 对白跨切点：`<scenetrans>` 并声明 `continues seamlessly across the cut`；
  视频结束截断：`<cutoff>`（只用于剧本已要求的截断）。
- 画面可见文字（霓虹、标牌、屏幕）原样保留原文并加英文双引号，如 `"营业中"`；
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

写在说话者 `<Subject N>` 的 `subject_definitions` 条目尾部（官方写法，不单独成段）：

```text
<Subject 1> (S1) always uses one fixed voice:
a clear, cool young woman's voice, soft in volume - now low and earnest. Do not change.
```

- 破折号前是**终身音色**（跨场次逐字复制）；`- now …` 后是**本场状态**（可改）。
- 本场不说话的角色：音色一个字不写（写了等于告诉模型他准备说话），
  显式声明 `<Subject 2> (S2) stays silent in this scene and does not speak at all.`
  （无台词角色不分配 `(Sx)`，只写 Subject 标签。）

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

### Forbidden 三层（折进六段，不另开字段）

video-storyboard 里的 `Forbidden:` / `Mandatory:` 行在 H3 六段里**不另开字段**——
H3 只认六段。把三层风险逐项折进对应段落，每条禁令对应一个本镜真实风险，
不堆通用负面词（短剧分镜契约的原文规则）：

| 层 | 折进哪 | 写什么 |
|---|---|---|
| 通用（字幕/水印/越轴/镜像/脸手融合） | `retention_analysis` 站位条目 + `detailed_description` 各镜 | "不生成字幕/水印"在正文直接写明；越轴/镜像写进站位条目（`do not mirror it`）；贴身镜在动作当场补分离句 |
| 特效（不可能动作路径、慢动作、特效化） | `detailed_description` 事件帧 | 三拍结构（前一态 → 无脸闪光帧 → 硬切后一态）；不写过程；不出现 slow motion / speed ramp |
| AI 感（磨皮、塑料反光、奇幻光晕） | 各镜 + 声音段之外的视觉风险句 | 具体到本镜最可能出感的那张脸/那件道具；无对应风险就不写 |

武戏分支的"已知可改进处 1. 缺全局 Forbidden 收尾"就是这一条的官方化说法：
末尾不补 `Forbidden:` 独立行，改为把通用层逐条折进六段对应位置。

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

交付五件：中文标题 → 关键处理说明 → 分镜表 → 英文 H3 正文代码块 → 逐段中文对照代码块。

每个 H3-UNIT 出**两个** ` ```text ` 块：英文块只放英文正文，中文块只放中文对照，
中文块紧跟在英文块下面。两块段落顺序与字段名逐条对应，块内不加标题。
中文不要混进英文块（会污染提示词解析），英文也不要混进中文块。
六段一段不落、顺序相同、逐句翻译；台词 `<d>[Chinese]…</d>` 原样保留不翻译。

### 六段字段的对照译法

| 字段 | 中文译法 |
|---|---|
| `subject_definitions:` | **主体定义：**（逐条译，标签 `<Subject N>`/`<Picture N>`/`<Video N>`/`<Audio N>` 保留） |
| `summary:` | **概要：**（首行任务类型前缀译法：`[reference generation]` 参考生成 / `keyframe completion` 关键帧补全 / `video continuation` 视频续接 / `video editing` 视频剪辑 / `audio reuse` 音频复用 / `audio reference` 音频参考） |
| `retention_analysis:` | **保留分析：**（保留强度译法见下） |
| `detailed_description:` | **分镜正文：**（逐镜译，`[Shot N]` 保留编号） |
| `overall_soundscape:` | **环境声底：** |
| `non_diegetic_music:` | **非画内配乐：**（`N/A` 译"无"） |

补充译法：`<Video 1> is the source video ...` 译"是源视频…"；
`<Audio 1> is the voice-timbre reference for <Subject 3> (S1)` 译"是 <Subject 3> (S1) 的音色参考"。

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
