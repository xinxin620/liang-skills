# 讲解场景、动作、特效

目标：做出**剪辑贴字做不到的镜头**。口播是声轨，画面是事件，不是卡拉 OK 加条目卡片。

## 场景跟讲词走

讲到什么环境，人就在什么环境。一段一个主空间。换空间用硬切，人已经在新空间里，不要走进三个房间当推进。

全片 **2–4 个空间**。竖屏默认中近半身；远 / 全尽量不用，硬顶 3 秒。不走全身。

## 对嘴还是画面

不是全程对口型。按这一句的功能选：

| 这一句在干什么 | 用什么镜 |
|---|---|
| 称呼、结论、专有名词、看镜头交代 | `Mouth speaking` |
| 列举、过程、辛苦、对比、吐槽旧方案 | `Acting, mouth closed, not speaking`，原声当 VO |
| 片头片尾无声 | 不对嘴 |

同一段里应对嘴和画面切开，不要整段站桩讲完再补一刀特写。

演戏镜要有一件具体的事：敲键盘、划掉付费倒计时、屏幕里崩坏的生成、手捏碎旧模型窗口。不要对着空气比划。

## 文字（极严）

默认无字幕。Timeline **禁止出现口播原文**（不要写 `Mouth speaking 开源第三天`）。口型用 `Mouth speaking the opening` / `the product name`。

只允许三类，且必须是镜内体积物，有组装 / 碎裂 / 旋转，**禁止弹出一行扁平字**：

- 专有名词（MiniMax H3、产品名）
- 标题（文生图）
- 关键数字（5090、100+）

禁止：把口播要点做成卡片（测评 / 教程 / 社区优化）、整句汉字、字幕条、caption、条目清单、口播逐字烧录。这些内容改成表演或动画。

Look 加 `no caption overlay`。Look 再加：`Bottom of the frame empty: no bar, no strip, no lower third.` Timeline 每一镜末尾：`Clean frame bottom.` Editing 和 Audio 每段贴 SKILL.md 那句禁令，讲解再加一句：`Volumetric glyphs only for proper nouns, titles or key numbers, never as a caption of the spoken sentence.`

### 触发词：口播在讲「提示词 / 文字 / 字幕」时升一档

H3 不只烧汉字台词。Timeline 里出现下面这些词，就会在画面底部烧一条字幕——**即使口播没在念这些字**。教程体裁先验更强：训练数据里「人在讲课」经常带底栏字幕。

禁止写入 Timeline / Look 的调度句（中英都禁，retention 里描述 UI 布局时也尽量避开）：

| 禁 | 改写成 |
|---|---|
| subtitle / captions / SRT / 字幕 / 字幕条 | speech-to-text, timecode-file, wrap-up line |
| prompt / prompts / 提示词 | instruction-box, copy-block, the wrap-up line, the next-step line |
| text / 文字 / transcript / lyrics / karaoke / 台词 | 不提字，只写动作：type, paste, box the field |

**最高危：口播本身在讲这些东西。** 「把提示词贴进去」「导出字幕」「识别文字」这类句子，H3 几乎必烧底栏。这时比平时更严：

1. Timeline 连英文 trigger 词都不要写，口型标签用 `the wrap-up line` / `the next-step line` / `the Jianying-import line`。
2. 一镜锁死半身近景，少切、少特效。切多 + 触发词 = 更爱烧字幕。
3. UI 只活在屏玻璃或旁置面板上，写 `on the screen glass only` / `never as a bar under the presenter`。
4. 截图里如果自带「字幕」二字或底栏预览，先裁掉再当 Picture 3。
5. 体积字仍然只给专有名词 / 标题 / 关键数字。讲 prompt 的段宁可不做体积字，省得模型当成字幕条。

还是烧：回头查 Timeline 有没有 prompt / text / subtitle；截图再裁一刀。不要靠加更长的禁令堆字，H3 会把禁令里的词也当要画的东西。

## 特效（镜内事件，不是花活）

特效必须让物体**动起来**，并贴这一句的意思：

| 讲词意思 | 不要 | 要 |
|---|---|---|
| 免费 / 不再付费 | 弹出「本地免费」 | 付费倒计时、会员闸机在手里碎掉 |
| 刷屏 | 弹出模型名卡片 | 一圈生成视频窗口涌过来再吸进一个标题 |
| 测评很累 | 三张文字卡 | 人在电脑前焦头烂额狂敲键盘，屏幕多窗口 |
| 5090 / 一百条 | 弹出「100+」字卡 | 体积 GPU 亮起，成片在屏幕上计数往上跳 |
| 旧模型差 | 弹出「理解差」 | 屏幕里物理崩坏、生成融化 |
| 几乎不抽卡 | 弹出口号 | 一次生成直接成片 |

禁止：无意义粒子风暴、闪白当转场、每段同一套飞入图标。特效是镜内的，不是转场。

手、脸、屏幕、物体：`clearly separated, never fusing`。

## 动作

站桩张嘴是失败。竖屏半身走两步够了，不要全身走位。

| 倾向 | 动作 |
|---|---|
| 看镜头讲 | 换重心、小手势 |
| 画面镜 | 敲键、划屏幕、捏窗口、看崩坏的生成 |
| 半身走 | 腰以上平移两步，停 |

禁止：甩头踱步、进门偷瞄、舞蹈化手势、全程 `She is still`。

## 运镜

该静锁死，该动极慢推 / 侧移。镜间只硬切。禁止黑场、白场、闪白。
