---
name: video-storyboard
description: 生成 MiniMax H3（海螺）参考生视频的提示词，三种模式：文戏分镜、高动态武戏、人物设定图（定妆照/四视图）。文戏走 Subject/Picture 绑定、逐镜 Shot、声音锁、嘴型纪律、180 度轴；武戏走 12 拍三段式、镜头有物理反应、无胜负收尾；人物模式写定妆照与四宫格四视图，量化脸型骨相与识别特征供分镜锁定。三者共用 Subject 标签，分镜强制附逐段中文对照。当用户提到分镜、镜号（镜7E、镜8、幕五）、参考生、镜头脚本、高动态、打斗、武戏、人物提示词、角色设定、定妆照、四视图、四宫格、把这场戏拆成分镜、改写某个镜头的提示词时使用。
---

# 视频分镜提示词（参考生）

**先选模式**——这是动手前第一件事。

| 用户说 | 模式 | 读哪个文件 |
|---|---|---|
| 分镜 / 镜头 / 对话 / 文戏 / 默认 | **文戏模式** | 本文档（SKILL.md），全流程 |
| **高动态** / 打斗 / 武戏 / 动作戏 / 近身缠斗 / 用高动态那套词 | **高动态模式** | `references/mode-action.md`，**先读它，结构完全不同** |
| **人物提示词** / 角色设定 / 定妆照 / 四视图 / 四宫格 / 人物设定图 | **人物模式** | `references/mode-character.md`，**先读它**——它产出的是分镜的上游素材 |

三种模式是一条链：

```
人物模式 → 出人物参考图 → 成为分镜的 <Subject N> → 文戏 / 高动态模式 → 出视频
```

**人物模式在整条链的上游**：这里少写一项识别特征，分镜里那句"保持参考图中的五官"就少一个抓手，换个角度就可能换人。

文戏与高动态的差异是根本性的：文戏全英文、`[Shot N]` 分段自足、禁 BGM；高动态**中文写动作 + 英文写镜头指令**、一整条拍链、**必须有配乐**。用错模式会全盘返工，所以**用户没说清时必须先问一句**。

用户没指定模式时，按题材判断：要出**角色设定图/定妆照/四视图**走人物模式；有交手、追逐、瞬移、变身走**高动态**；其余走**文戏**。

三种模式**共用同一套素材标签** `<Subject N>`（见下）。

---

一句话：**每个镜头段都是一份自足的英文 prompt——模型只看这一份，就必须还原出正确的角色、场景、站位、身高、道具、嘴型和声音；同时必须给用户一份中文对照，让他看懂每一句在说什么。**

## 一、动手前先确认

| 需要 | 说明 |
|---|---|
| 场次剧本 | 本镜的动作、对白、情绪转折。缺的信息向用户要，不要编。 |
| 参考图编号表 | Picture 1..N 分别对应哪张图，跨镜保持不变。 |
| 时长 | 决定镜数。 |
| 站位帧 | 同场景首次出现时建立，后续镜头一律复用同一张。 |

**编号规则：全局资产编号，跨场次累加**

- `<Picture N>` 是**全局素材编号**，不是每场从 1 重排。一张图一旦定号就终身不变——`<Picture 7>` 是封三娘、`<Picture 10>` 是幕四成品帧，到幕五、幕六还叫这个号。
- 新图按上传顺序往后接号；已定号的图不重排、不复用、不跳号。
- 同一场里同时引用不相邻的号（如 1、2、7、10）是**正常的**，不要为了"连续好看"去改号。
- `<Subject N>` 编号独立于 Picture：Subject 是"主体的抽象定义"，指向哪张图由文字写明（`<Subject 3> is Feng in <Picture 7>`）。**所以 Subject 编号 ≠ Picture 编号，是允许的。**
- 有台词的角色，`S` 编号与 `Subject` 编号对齐（`<Subject 1>, S1`）；**没有台词的角色不写声音锁**。
- 同一场景里角色的描述文字**逐字复制**，不做改写、不做同义替换——改写会让模型以为换了人。

**素材的五种角色**

| 类型 | 写法 | 锁住什么 |
|---|---|---|
| 角色图 | `<Picture N>` + `<Subject N>` 定义 | 脸、服装、身材、发式 |
| 场景图 | `<Picture N>` anchors the environment | 布局、色调、光效 |
| 站位帧 | `<Picture N>` is the locked blocking reference | 屏幕左右、机位侧 |
| **成品帧** | `<Picture N>` is the previous shot's frame | 一图顶三图：场景＋站位＋道具＋光线＋动作接续点 |
| 道具图 | 特写镜里引用，并在 Forbidden 加"形状每镜一致" | 道具细节 |

**成品帧续拍（最省素材的写法）**

上一镜已经出片时，直接把它当新素材引用，一次锁死场景、站位、道具摆位和光线方向：

```
<Picture N> is the previous shot's frame: the exact courtyard, lighting, prop arrangement and character positions to continue from.
Scene: continue directly from the frame in <Picture N> - reproduce this arrangement exactly, do not mirror it, do not rearrange it. …
```

这是接戏最稳的写法：`do not rearrange it` 一并封掉了道具被挪动、光线换方向、人物换位置三种漂移。

**素材不足时怎么办（常见：只给了角色图）**

- `<Picture N>` 只留给真实上传的图。没有场景图、没有站位帧，就**不要写** `<Picture 3>` / `<Picture 5>`——引用不存在的素材会直接报错。
- 缺场景图：用一行 `Environment: … Keep this layout, palette and lighting exactly in every shot.` 文字锁死，写清前景／标志物／左右两侧／远景。
- 缺站位帧：用一行 `Locked blocking (do not mirror): …` 把机位侧、屏幕左右、入场方向写成死规则，后续镜头原样复述这一行。
- 后续真的补了场景图或站位帧，再从全局最大编号往后接，不跳号、不复用旧号。
- 换场次的连续性写在**镜号行**里（如"接幕四成品帧 <Picture 10>"），不靠改编号来表达。

## 二、时长 → 镜数

| 时长 | 镜数 | 节奏 |
|---|---|---|
| 8–11 秒 | 3 镜 | 约 3–4 秒/镜 |
| 12–16 秒 | 4–6 镜 | 约 2.5–4 秒/镜 |
| 20 秒以上 | 拆成两个镜号 | 单个段不超过 20 秒 |

**镜数由"动作单元 + 台词条数"决定，不由秒数决定**，时长只用来校验节奏：

- 每句台词**独占一镜**（配合单人镜覆盖法）；台词越长，这一镜越长。
- 一个无台词的连续动作（走近、握手、抬头）**独占一镜**。
- 一段长独白（30 字以上）可以占满 6–8 秒的单个近景，不必为了凑镜数切碎——长台词切碎反而容易串嘴。
- 15 秒 4 镜（3 句台词 + 1 个无台词反应）是完全正常的配比。

原则：**一个镜头只做一个动作单元**。复杂动作（起身＋走位＋说话）拆成多镜；特写可以短到 1–2 秒；无台词的双人反应镜头可以长。

## 三、输出结构（11 段，顺序固定）

1. 角色声明（每个 Subject 一段）
2. 场景段（场景图 `<Picture N> anchors the environment` **或** 成品帧 `<Picture N> is the previous shot's frame`）
3. 站位锁定（站位帧 **或** 写进 Scene 段的 `Spatial axis`；有成品帧时两者合一）
4. 背景待机角色（可选，注明 "watching from a distance, soft focus"）
5. 声音锁定（`<Subject N>, S<N> is always the speaker.` + 固定音色 `- now 本场状态`；无台词角色不写）
6. Scene 段：时间、地点、陈设与道具摆位、待机角色状态、质感、`Heights stay fixed`
7. Mouth discipline（升级为"每句台词由单人镜承担"的分配声明）
8. Spatial axis (180-degree rule)（含身体朝向）
9. `[Shot N]` × N（每镜带自己的 `Mouth discipline` 行）
10. Audio
11. Forbidden / Mandatory

固定句式见 `references/template.md`，可直接复制填空。

## 四、中英对照（强制，不许省）

分镜提示词一律英文，但**每次输出都必须紧跟一份完整中文对照**——用户看不懂英文，没有对照等于没交付。

**格式**

1. 先用 `text` 代码块给英文 prompt 全文（可直接复制投喂）。
2. 代码块**外面**接一级小节 `### 中文对照`。
3. 对照**逐段对应**：11 段一段不落，顺序相同，段落标签照抄（`<Subject 1>`、`Scene:`、`Mouth discipline:`、`[Shot 1]`……）。
4. `[Shot N]` 按编号逐条翻译，景别、动作、物理结果、焦点变化、镜内否定句都要译到；**不许只写"两人对视"这类大意**。
5. 台词本来就在 `<d>[Chinese]…</d>` 里，是中文，**原样保留，不翻译、不改写**。
6. 中文对照不要混进英文代码块，否则复制时会一起被带走。

**固定句式的统一译法**（每次都这么译，保持一致）

| 英文 | 中文 |
|---|---|
| Preserve the facial features, costume, body proportions, and overall appearance from the reference image. | 保持参考图中的五官、服装、身材比例与整体形象。 |
| Preserve its layout, palette and lighting exactly. | 严格保持其布局、色调与光效。 |
| keep the same screen arrangement - do not mirror it. | 保持同一画面站位，禁止镜像。 |
| always uses one fixed voice: … Do not change. | 声音固定为……，不变。 |
| Mouth discipline: only the character who is speaking moves their lips. | 嘴型纪律：只有正在说话的角色动唇。 |
| No dialogue; both mouths stay closed. | 无台词，两人双唇闭合。 |
| Neither speaks; both mouths stay closed. | 谁也没有出声，双唇闭合。 |
| no simultaneous mouth movement | 不得同时动嘴 |
| hard cuts only between shots. | 镜与镜之间只做硬切。 |
| no BGM | 无 BGM |
| `<Picture N>` is the previous shot's frame: … to continue from. | `<Picture N>` 是上一镜成品帧：可直接接续的……。 |
| reproduce this arrangement exactly, do not mirror it, do not rearrange it. | 原位复现，不镜像、不重排。 |
| Mouth discipline: only X moves her lips; no other character shares the frame. | 嘴型纪律：只有 X 动唇，本镜无他人入画。 |
| Mouths closed, both still. | 双唇闭合，两人静止。 |
| body facing screen-right / screen-left | 身体朝画面右 / 朝画面左 |
| stands in the middle-left of the screen | 站在画面中左 |
| watching from a distance, soft focus | 远远看着，虚焦 |
| Heights stay fixed in every shot | 每一镜身高固定 |
| Preserve the facial features, hairstyle, costume, body proportions, and overall appearance from the reference image. | 保持参考图中的五官、发型、服装、身材比例与整体形象。 |
| no fades, no dissolves, no push transitions | 无淡入淡出、无叠化、无推镜转场 |

## 五、逐镜写法

```
[Shot N] <景别>, <主体>, <清晰/虚焦状态>: <表演 + 动作 + 物理结果>。S<N> says:
<d>[Chinese]台词。</d>
Mouth discipline: only <角色> moves <his/her> lips; no other character shares the frame.
```

- **景别 + 主体 + 焦点状态**三件套写在最前：`Medium close shot, Feng alone, sharp`。
- 动作要可拍：**动词 + 物理结果**（`slides down off the stone railing`、`one hand tightens on her sleeve`），不写"她很痛苦"。
- **情绪给副词，身体给小动作**：`quiet and halting, each word costing her something` 是情绪，`one hand tightens on her sleeve as she speaks` 是观众能看见的东西。两句一起给，表演才落地。
- 焦点变化当成动作写（`she comes into sharp focus as she approaches`）。
- 台词格式：`S1 says:` 独占一行，台词另起一行用 `<d>[Chinese]…</d>`，不加引号、不加括号。
- **没有台词的镜头必须显式否定**：`No dialogue; both mouths stay closed.` 或 `Mouths closed, both still.`——不写，模型就会让人物乱动嘴。
- **有台词的镜头，把嘴型纪律写进这一镜**（见下节），不要只在段首写一遍。

## 五之二、嘴型纪律：单人镜覆盖法（强烈推荐）

**规则：每一句台词，都由一个"只有说话者一张脸在画面里、且实焦"的镜头承担。**

```
[Shot 1] Medium close shot, Feng alone, sharp: … S3 says:
<d>[Chinese]…</d>
Mouth discipline: only Feng moves her lips; no other character shares the frame.
```

三种覆盖方式，按优先级：

1. **单人镜（最佳）**：画面里只有说话者，听者在画外。零串嘴风险。
2. **过肩 + 听者前景虚化**：听者只作为一个虚焦的肩或后背边缘在画面角落，脸不入画。
3. **双人镜但只有一人实焦**：仅在换镜成本太高时用，且必须在段尾写死。

**禁止**：任何一句台词配一个"两张脸都实焦"的双人镜——这是串嘴和换脸的主要来源。

与之配套，段首的 `Mouth discipline` 段升级为**分配声明**，把每句台词归到哪一镜一次讲清：

```
Mouth discipline: no simultaneous mouth movement - every dialogue line is covered by a shot in which only ONE face is in sharp focus, the listener is either out of frame or a soft foreground blur.
```

无台词镜头仍用 `Mouths closed, both still.` 收尾。Forbidden 段把这条再钉一次。

## 五之三、声音锁的两种写法

角色音色是**终身不变**的，但同一场戏里的**状态会变**（音量、快慢、情绪）。两者分开放：

```
<Subject 1>, S1 is always the speaker. S1 always uses one fixed voice: a clear, cool young woman's voice, soft in volume - now low and earnest. Do not change.
```

- 破折号前是**固定音色**（跨场次逐字复制）。
- `- now …` 后是**本场状态**（每场可以改）。
- 不写 `now` 时，默认沿用固定音色的常态。

**本场不说话的角色的写法**：不写音色（写了等于告诉模型"这人准备说话"），但要**显式声明沉默**：

```
<Subject 2>, S2 stays silent in this scene and does not speak at all.
```

省略是含糊的，声明是命令。角色在场却全程没台词时，这一行必须写。

## 五之四、不可能动作：拍前后，不拍过程 ⭐

当一个动作物理上不可能、或模型一定会渲染坏——**瞬移、变身、凭空出现道具、瞬间换装、超高速位移**——不要写这个过程怎么发生。

**三拍结构**

| 拍 | 内容 | 要点 |
|---|---|---|
| 前一态 | 人还在原处 | 实焦，画面干净，站位清楚 |
| 事件 | 闪光 / 脆响 / 冲击波 | **固定机位，画面里没有人脸**；只给一帧，把雾、灰、衣料残影掀开 |
| 后一态 | 人已在新位置 | 硬切过去；用**余韵**代替过程——衣服还在落、头发还在回位、尘土还在滚、雾还在合拢 |

```
[Shot 2] Locked-off wide of the stairway, no faces in frame. The step where she stood is now empty. A hard white-green flash, one frame, then a ring of air bursts outward from that spot and blows the fog and the loose dust off the stone. The step is bare. One sharp cracking sound, like a whip close to the ear.

[Shot 3] Hard cut. She is already standing on the flat stone courtyard at the foot of the stairs… Her robe is still settling, the loose strands of hair fall back into place, dust rolls away from her feet and the fog folds back around her legs. She is still. No travel, no run, no arc - she was not there, now she is.
```

**为什么必须这么写**：模型看到"消失""瞬移"这类词，默认渲染成**缓慢淡出或飘移**。`原地闪一下 + 空出的台阶 + 已经站好的她` 比任何"瞬间消失"的措辞都可靠。

**位移后的落点必须保持原屏幕侧**：她从台阶移到平地，仍站在画面左侧——位置变了，屏幕侧不变，轴线才不断，后面接着打不会翻边。

**同时必须否掉的东西**（写进 Forbidden 的特效层，见下节）：位移路径、慢动作、特效化三类，一条都不能省。

## 五之五、Forbidden 分三层写

禁止项不是一个句子，是三层清单。**没过脑子写下来的禁止项不算数**——每一条都要对得上本镜的真实风险。

**第一层：通用层**（每条 prompt 都写）

```
no subtitles, no on-screen text, no watermark, no lower-thirds; no soft dissolves, fades, wipes, zoom or dolly push transitions - hard cuts only; no crossing the 180-degree axis, no left-right swap, no mirroring; no face or hand fusion, no extra fingers; no costume, hairpin or staff change between shots; no BGM, no mood music.
```

**第二层：特效层**（按本镜实际风险定制，逐条列）

瞬移 / 位移类必写：

```
no visible travel path, no running, no jump, no leap, no flying, no arcing trajectory; no glowing trail, no light beam, no magic particles, no energy aura, no CG smoke, no sparkling dust; no slow motion, no speed ramp, no freeze frame.
```

再补一句**唯一的例外**，把口子收紧：`the girl's feet never leave the ground except in Shot 2's flash.`

**第三层：AI 感抑制层**（写实 / 古装题材必写）

```
no modern objects; no glossy beauty-retouch skin, no plastic sheen; no fantasy glow; no oversaturated colour.
```

这一层专治"一眼 AI"：假滑的皮肤、塑料反光、滤镜式柔光、高饱和。

## 五之六、身高要分情况写

`Heights stay fixed in every shot` 只解决静态。**角色会换到高度差明显的落点时**（台阶↔平地、坐↔站、马↔地），要分情况写清，否则模型会在台阶上把两人拍成一样高：

```
Heights stay fixed in every shot: on level ground the Elder stands a full head taller than the Girl with a straighter back; on the stairway she is higher because she stands steps above him. When they both stand on the flat courtyard, he is again a full head taller.
```

## 五之七、交付格式：先分镜表，再提示词

每次交付按这个顺序，缺一不可：

1. **中文标题 + 一句设定**（如「汉服石阶对峙」）
2. **关键处理说明**——这一条里最容易拍坏的地方是什么、你用什么办法绕过去了（如"她瞬间消失的那一段不拍位移过程，否则模型一定会渲染成慢速飘移"）。**这段是给用户复核你的判断用的，不能省。**
3. **分镜表**：`镜头 / 景别 / 内容`，一镜一行，中文，让用户能一眼看完节奏
4. **英文 prompt 代码块**
5. **中文对照**

**分镜表里出现的每一句台词，必须在某个 `[Shot N]` 里以 `<d>[Chinese]…</d>` 落地**——不能只在表里写"说完那句话"而 prompt 里没有台词行，这是最常见的漏交付。

## 五之八、接戏：先定类型，再写 prompt ⭐

**接不接，是逐个镜头边界单独决定的，不是整场统一的。** 有些边界要让动作跨过剪切继续，有些就是该硬切跳开——**默认是硬切，不写"接"就是不接。**

这句默认必须立住。反过来（默认接、要断才写断）会出大问题：模型会试图把两个镜头插值成一段连续运动，硬切被渲染成缓慢滑动，整场的节奏全糊掉。

### 三种边界类型

| 类型 | 什么时候用 | 怎么写 |
|---|---|---|
| **紧接** | 一个动作跨剪切继续；观众要看清过程（递簪、起身、逼近） | 引用上一镜成品帧 + 写明停在哪一拍、从哪一拍起 |
| **跳切 / 省略** | 时间或动作有意跳过；节奏需要顿一下 | **不引用上一帧**，并主动否掉承续 |
| **换场** | 地点、时间、人物组合换了 | 重新锚定场景，站位轴重新建立或显式延续 |

### 紧接：三件都要写

```
<Picture N> is the previous shot's frame: the exact courtyard, lighting, prop arrangement and character positions to continue from.
Scene: continue directly from the frame in <Picture N> - reproduce this arrangement exactly, do not mirror it, do not rearrange it. … 【写清承接时人物的姿势 / 手的位置 / 动作进度】
```

**光引用成品帧只锁住了"画面长什么样"，没锁住"动作做到哪一步"。** 紧接时必须把这三件补齐：

1. **镜尾落在哪一拍**——上一镜末句写明动作没做完：`她的手指还停在袖口上，没有收回去。`
2. **镜首从哪一拍起**——下一镜首句明写从中途接上：`延续同一个半步，尚未站定。`
3. **不许重来**——否掉动作重置：`no restarting the movement, no re-playing the step from the beginning.`

漏掉第 1 条，观众会看到跳帧；漏掉第 3 条，模型会把已经做完的动作再做一遍。

### 跳切 / 省略：要主动否掉承续

这才是**不写"接"时的正确做法**——不只是不写，还要把承续关掉：

```
Forbidden: no matching eyeline to the previous shot, no re-playing the previous pose, no continuous action carrying across the cut.
```

否则模型仍可能自己脑补一个过渡。跳切的力量来自**断**，必须明说断。

### 换场：锚点重排，轴线要表态

换场不必沿用上一场的站位帧，但**轴线要么显式延续，要么显式重建**，不能沉默——沉默就等于把决定权交给模型。

换场时镜号行注明关系：`（接幕四成品帧 <Picture 10>）` / `（同日，换场至……）` / `（三日后，全新场次）`。

### 高动态：拍链内部不叫接戏

12 拍是一条连续运动，拍与拍之间由 `the camera cuts to` 串起，**不是三个独立提示词的接缝**。拍链被打断后要单独重做某一拍时，那一拍要重新引用前后两拍的成品帧，并在正文里写明"这一拍停在哪、下一拍从哪起"。

## 六、台词

- 古风白话：短句、句号断句、少用问号（改成陈述或短问）。
- 自称按身份：娘子 / 妾身 / 我；称呼对方用关系词（"姐姐"）。
- 硬话用短句砸（"拿着。不许推。"），软话用文雅长句（"改日，姐姐来，妾身扫榻相候。"）。
- 每镜 1–2 句，总台词量 ≤ 镜数 × 1.5 句。
- 新写的台词，在镜号行注明"新写台词"；台词逐字定稿后再进 prompt，不要边写边改。

## 七、必须复述的一致性要点

以下信息**每个镜头段都要重写一遍**，不能因为"上一镜说过"而省略：

- 身高差（`the top of Feng's head reaches only about Shiniang's eyebrow level`）
- 固定道具与佩戴位置（金凤簪在髻上、绿玉簪在发间）
- **道具摆位与场景陈设**（茶壶在矮木几右侧、扫帚在青儿手里）——成品帧续拍时尤其要写，否则模型会重排院子
- 服装与发式（逐字复制参考图描述）
- 屏幕左右（screen-LEFT / screen-RIGHT / middle-left）
- **视线方向与身体朝向**（`body facing screen-right`）——站位描述里最容易漏的一项
- 说话人的声音特征
- **待机角色的状态**（`holding her bamboo broom, watching from a distance, soft focus`）——背景人物必须给一个明确动作，否则会被模型删掉或乱走

## 八、自检清单

交付前逐条过：

- [ ] 英文 prompt 后紧跟完整中文对照，11 段一段不落
- [ ] 对照是逐句译的，不是概括大意；台词未翻译
- [ ] 交付含：标题 → 关键处理说明 → 分镜表 → 英文 prompt → 中文对照（五件齐）
- [ ] **每个镜头边界都定了类型**（紧接 / 跳切省略 / 换场），没有含糊带过
- [ ] 紧接的边界：引用了上一镜成品帧，**且**写明了动作停在哪一拍、从哪一拍起、`no restarting the movement`
- [ ] 跳切省略的边界：**没有**引用上一帧，并在 Forbidden 主动否掉承续
- [ ] 换场的边界：轴线显式延续或显式重建，镜号行注明了场次关系
- [ ] 分镜表里出现的每句话，都在某个 `[Shot N]` 里有 `<d>[Chinese]…</d>` 落地
- [ ] `S` 编号 = `Subject` 编号；不说话的角色的音色一个字没写，且写了"stays silent"声明
- [ ] Picture 编号是全局累加，未重排、未复用、未跳号
- [ ] 引用的 `<Picture N>` 全部真实存在；缺场景图／站位帧时已用 `Environment:` / `Locked blocking:` 文字补位
- [ ] 成品帧续拍写了 `do not mirror it, do not rearrange it`
- [ ] **每句台词都有单人镜覆盖**，且该镜有 `Mouth discipline: only <角色> moves lips; no other character shares the frame.`
- [ ] 无台词镜头写了 `Mouths closed, both still.` / `both mouths stay closed`
- [ ] `screen-LEFT / screen-RIGHT` 与**身体朝向**在每个镜头段里重述
- [ ] 身高差、道具摆位、待机角色状态在每段重述；**角色换高度差落点时写了分情况身高**
- [ ] **不可能动作走了三拍结构**（前一态 / 无脸的闪光帧 / 硬切到后一态＋余韵），且位移后仍保持原屏幕侧
- [ ] 位移类写了"无路径、无慢动作、无特效化"三组否定，并给了唯一例外
- [ ] Forbidden 分三层：通用层 / 本镜特效层 / AI 感抑制层
- [ ] 情绪都配了可见的小动作（不只写"她很伤心"）
- [ ] 没有被截断的句子（原稿常见毛病：`…moves their lips. Every` / `over.`）
- [ ] Mandatory 覆盖：无 BGM、只留环境声、硬切，并点明"是物理冲击不是魔法"
- [ ] 镜数 = 台词条数 + 无台词动作单元数，与时长节奏相符

**高动态武戏模式另有独立清单**（镜头纪律三条、每击撞镜头、前景遮挡、双语镜头词、封面数），见 `references/mode-action.md`。

## 九、参考文件

- `references/template.md` —— 文戏空白模板（英文 + 中文对照双份），复制填空即可
- `references/mode-character.md` —— **人物模式**：定妆照七段结构、四宫格四视图结构、左上格蒙脸的设计原理、量化精度、识别特征作为跨镜锁脸的抓手、与分镜的接口。用户说"人物提示词/定妆照/四视图"时先读它。
- `references/mode-action.md` —— **高动态武戏模式**：12 拍三段式、单拍公式、镜头纪律、反融合、无胜负收尾、状态锚点、`overall_soundscape` / `non_diegetic_music` 写法。用户说"高动态/打斗/武戏"时先读它。
- `references/phrasebook.md` —— 景别 / 动作 / 声音 / 质感 / 镜头覆盖 / 不可能动作 / AI 感抑制 的英文标准词表
- `references/examples.md` —— 六条定稿样例，风格与手法的基准：
  - **镜7E、镜8**：双人戏、道具交换、虚焦走位（旧写法，嘴型纪律在段首统一写）
  - **幕五「不许解」**：⭐ 文戏最高基准。单人镜覆盖法、成品帧续拍、声音锁两截、情绪配可见动作，全部齐备。
  - **汉服石阶对峙**：⭐ 特效/不可能动作唯一基准。三拍结构处理瞬移、Forbidden 三层、身高分情况写。
    ⚠️ 该条**台词没落地**（分镜表里有"说完那句话"，prompt 里没有 `<d>`），examples.md 末尾给了改写版，是**反面教材＋修正示范**。
  - **青石广场缠斗 v1 → v2 → v3**：⭐ 高动态唯一基准系列。
    **v1** 是基线；**v2** 是用户反馈"力量感不够、角度普通、固定机位"后的升级（镜头纪律、每击撞镜头、前景遮挡、双语镜头词、结尾不止静）；**v3** 是续写追击段（状态锚点取代成品帧、剑尖视点、物件打飞甩出甩回、接触面分离、一拍内交替攻防）。
    三版连读能看出武戏的完整迭代路径。规则见 `references/mode-action.md`。
