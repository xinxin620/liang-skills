# 分镜提示词空白模板

复制整段，把 【】 填掉。【】 之外的英文句式不要改，它们是稳定出片的固定句式。

镜号行（中文，放在代码块外）：

```
镜【N】·【小标题】（参考生：角色×【n】 + 场景×1 + 站位参考帧×1，【秒数】秒；【衔接说明 / 备注】）
```

开头一行参考图清单（中文，可省）：

```
建议时长【N】秒。参考图：<Picture 1>【角色】、<Picture 2>【角色】、<Picture 7>【角色】、<Picture 10>【上场成品帧】（站位与场景基准）。
```

提示词正文：

```text
<Subject 1> is 【角色名】 in <Picture 1>: 【身份 + 服装 + 发式 + 佩饰的一句话描述】. Preserve the facial features, hairstyle, costume, body proportions, and overall appearance from the reference image.
<Subject 2> is 【角色名】 in <Picture 2>: 【身份 + 服装 + 发式】. Preserve the facial features, hairstyle, costume, body proportions, and overall appearance from the reference image.
<Subject 3> is 【角色名】 in <Picture 7>: 【身份 + 服装 + 发式 + 特征】. Preserve the facial features, hairstyle, costume, body proportions, and overall appearance from the reference image.
<Picture 10> is the previous shot's frame: the exact 【地点】, lighting, prop arrangement and character positions to continue from.

<Subject 1>, S1 is always the speaker. S1 always uses one fixed voice: 【固定音色】 - now 【本场状态】. Do not change.
<Subject 3>, S3 is always the speaker. S3 always uses one fixed voice: 【固定音色】 - now 【本场状态】. Do not change.
【不写没有台词的角色音色】

Scene: continue directly from the frame in <Picture 10> - reproduce this arrangement exactly, do not mirror it, do not rearrange it. 【时间 + 地点 + 简陈设】. 【质感：realistic period-drama film look, warm slanting sunlight, muted palette, shallow depth of field】.

Heights stay fixed in every shot: 【角色 A】 is tallest; the top of 【B】's head reaches about 【A】's brow level; 【C】 is the shortest, the top of her head reaching only about 【A】's nose level.

Spatial axis (180-degree rule): 【A】 stands in the 【middle-left】 of the screen, body facing screen-right. 【B】 stands facing her on the right, body facing screen-left, by 【道具】. 【C】 stands far in the background on the left by 【位置】, 【holding ...】, watching from a distance, soft focus. The camera stays on the 【机位侧】 for the entire scene; no crossing to the other side, no swapping left and right.

[Shot 1] 【景别】, 【角色】 alone, sharp: 【情绪副词，each word costing her something】; 【可见的身体小动作】. S3 says:
<d>[Chinese]【台词】</d>
Mouth discipline: only 【角色】 moves her lips; no other character shares the frame.
[Shot 2] Two-shot, no dialogue: 【谁的连续动作 + 物理结果】. Mouths closed, both still.
[Shot 3] 【景别】, 【角色】 alone, sharp: 【情绪副词】; 【可见动作】. S1 says:
<d>[Chinese]【台词】</d>
Mouth discipline: only 【角色】 moves her lips; no other character shares the frame.
[Shot 4] 【景别】, 【角色】 alone, sharp: 【反应：眼睛抬起、嘴唇压住、眼泪将落未落】. No dialogue, mouth closed.

Forbidden: no subtitles, no on-screen text, no watermark; no fades, no dissolves, no push transitions; no left-right swaps, no face or hand fusion; no simultaneous mouth movement - every dialogue line is covered by a shot in which only ONE face is in sharp focus, the listener is either out of frame or a soft foreground blur.
Mandatory: no BGM; ambient + voices only (【环境声 2–3 项】); hard cuts only between shots.
```

## 填空提示

- **每句台词一个单人镜**，该镜必须带 `Mouth discipline: only <角色> moves her lips; no other character shares the frame.`——这是防串嘴最有效的一条。
- **情绪配动作**：情绪副词 + 可见的身体小动作，两句都给（`quiet and halting, each word costing her something; one hand tightens on her sleeve`）。
- **声音锁写两截**：破折号前是终身固定的音色，`- now …` 后是本场状态。本场不说话的角色，音色一个字不写。
- **场景陈设和道具摆位每段重述**（青瓷茶壶在矮木几上、扫帚在青儿手里），否则模型会重排院子。
- **待机角色必须给一个明确动作**（`holding her bamboo broom, watching from a distance`），否则会被模型删掉或乱走。
- **站位要写身体朝向**（`body facing screen-right`），只写 screen-LEFT/RIGHT 不够。
- **无台词的镜头**必须显式写 `Mouths closed, both still.` 或 `No dialogue; both mouths stay closed.`
- **成品帧续拍**必写 `do not mirror it, do not rearrange it`。
- **道具特写**单独成镜，并在 Forbidden 里加 `hairpin shapes stay consistent in every close-up` 这类句子。
- 台词里不要出现引号、括号、停顿符号；要让角色停一下，就在文字里用句号断开。

---

# 中文对照模板（强制，跟在英文代码块后面）

```markdown
### 中文对照

**<Subject 1>** 是 <Picture 1> 中的【角色名】：【身份 + 服装 + 发式 + 佩饰】。保持参考图中的五官、发型、服装、身材比例与整体形象。

**<Subject 2>** 是 <Picture 2> 中的【角色名】：【服装 + 发式】。保持参考图中的五官、发型、服装、身材比例与整体形象。

**<Picture 10>** 是上一镜成品帧：可直接接续的【地点】、光效、道具摆位与人物位置。

**<Subject 1>, S1** 始终是说话方。声音固定：【音色】——本场【状态】。不变。

**Scene:** 直接接 <Picture 10> 的画面——原位复现，不镜像、不重排。【时间 + 地点 + 陈设】。【质感】。

**身高固定:** 每一镜【A】最高；【B】头顶到【A】的眉线；【C】最矮，头顶到【A】的鼻线。

**180 度轴:** 【A】站在画面中左，身体朝右；【B】在右侧面对她，身体朝左；【C】在左后方远处【拿着扫帚】远远看着，虚焦。摄影机整场在【机位侧】，不越到另一侧，不换左右。

**[Shot 1]** 【景别】，【角色】单人，实焦：【情绪】；【可见动作】。S3 说：
<d>[Chinese]台词</d>
**嘴型纪律:** 只有【角色】动唇，本镜无他人入画。

**[Shot 2]** 双人镜，无台词：【连续动作 + 物理结果】。双唇闭合，两人静止。

**[Shot 3]** 【景别】，【角色】单人，实焦：【情绪】；【可见动作】。S1 说：
<d>[Chinese]台词</d>
**嘴型纪律:** 只有【角色】动唇，本镜无他人入画。

**[Shot 4]** 【景别】，【角色】单人，实焦：【反应】。无台词，双唇闭合。

**Forbidden:** 无字幕、无屏幕文字、无水印；无淡入淡出、无叠化、无推镜转场；不许左右互换，不许脸与手融合；不许同时动嘴——每句台词都由"只有一张脸实焦"的镜头承担，听者要么在画外、要么是前景虚化。

**Mandatory:** 无 BGM；只留环境声与人声（【环境声】）；镜与镜之间只做硬切。
```

对照三条硬要求：逐段不落、逐句翻译、台词原样保留。
