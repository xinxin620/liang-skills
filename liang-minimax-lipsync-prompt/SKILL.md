---
name: liang-minimax-lipsync-prompt
description: 为 MiniMax H3 / Hailuo 写数字人对口型分镜。三个画面分支：MV 唱歌、讲解口播、脱口秀。共用原音频、SRT、角色参考、liangmv:v1、六段式。当用户提到对口型、MV、Hailuo、liangmv、数字人、讲解、口播、脱口秀、坐凳固定机位时使用。不要用于电商随拍、打戏、对白短剧。
---

# MiniMax H3 数字人对口型

听不到音频。词、节奏、停顿以大桶的文字和 SRT 为准，不要假装听过附件。

产出是可粘贴给 H3 的多段提示词，不是成片。对口型由大桶挂 `<Audio N>`。

和现有 skill 分工：

- `minimax-video-prompt`：通用六段式。本 skill 复用它的六段式、硬切、禁字幕条。
- `短剧创作`：对白叙事。本 skill 不是短剧。
- `minimax-high-dynamics`：打戏。
- 电商带货 skill：随拍、默认无台词。

旧入口 `minimax-mv-prompt` / `minimax-presenter-prompt` 已并入本 skill，不要再用。

## 先选分支

| 分支 | 画面在干什么 | 触发 |
|---|---|---|
| **MV** | 唱歌。先选剧情向或画面向。 | 歌、MV、副歌、对嘴唱歌 |
| **讲解** | 口播介绍。结论对嘴，过程用表演和镜内特效。 | 数字人讲解、口播、教程、产品介绍 |
| **脱口秀** | 坐着讲段子。固定机位，不离座。表情手势跟内容走。 | 脱口秀、坐凳、固定画面、单口 |

大桶没说就问一句，不要两个都做。

读文件：

- 切段（共用）：[references/srt-timing.md](references/srt-timing.md)
- **MV** 共用刀数：[references/mv-grammar.md](references/mv-grammar.md)；剧情向：[references/song-map.md](references/song-map.md)；画面向：[references/visual-mv.md](references/visual-mv.md)；表演：[references/lipsync-performance.md](references/lipsync-performance.md)；行文：[references/example-mv.md](references/example-mv.md)
- **讲解**：[references/presenter-grammar.md](references/presenter-grammar.md)；行文：[references/example-presenter.md](references/example-presenter.md)
- **脱口秀**：[references/standup-grammar.md](references/standup-grammar.md)；行文：[references/example-standup.md](references/example-standup.md)

## 缺什么就问

必收：音频总时长 **T**（一位小数）、分支、角色参考、SRT/VTT（优先）。没给 T 先问，不要出地图。

选收：画幅、场景/产品参考。MV 还要氛围和剧情向/画面向。讲解还要主题。脱口秀默认图1 锁构图，图2 可锁脸。

默认：单段 **3–15 秒，切点最多一位小数**；16:9（竖屏才 9:16）；提示词英文、地图中文；**画面无字幕**。不描写长相。所有段相加 = T。

## 工作流（两层，共用）

**A. 全片地图**

读 srt-timing。切点一位小数。地图必须带可复制的 `liangmv:v1`。停。等大桶改切点或说可以出提示词。短片（约 ≤45 秒）或正在改切点时，地图和提示词可以一起出。

**B. 段内分镜 + 提示词**

只读本分支的 grammar / example。Look 全片一句锁定。每段：中文资产表 + 一条六段式英文提示词。

归档按分支：

- MV → `D:\提示词库\视频\minimax MV提示词\YYYY-MM\`
- 讲解 → `D:\提示词库\视频\minimax数字人讲解\YYYY-MM\`
- 脱口秀 → `D:\提示词库\视频\minimax脱口秀\YYYY-MM\`

## 每段输出（共用壳）

六段顺序固定，不要 markdown 标题：subject_definitions → retention_analysis → Look → Timeline → Editing rules → Audio / Text。

Timeline 用本段相对时间。第一镜直接开；从第二镜起 `Hard cut:`。不描写五官服装。**禁止把台词/歌词原文写进 Timeline**（中英都不贴）。口型只写 `Mouth speaking` / `Mouth singing`，内容用英文标签（the punchline, the name line）。

Audio 协议按分支选，写在对应 grammar 里。Editing rules 和 Audio / Text **每段都贴**下面这句，不要改软、不要删：

```
No burnt-in text of any kind. Forbidden: subtitle bar, closed captions, karaoke, lyric cards, lower thirds, speech bubbles, chyrons, any Chinese or English transcript of the audio. The picture has no readable caption overlay.
```

Look 再加：`no caption overlay` 和 `Bottom of the frame empty: no bar, no strip, no lower third.`
Timeline 每一镜末尾：`Clean frame bottom.`

**触发词（比贴原文更毒）。** Timeline / Look 出现下面这些词，H3 会在画面底栏烧字幕——**即使口播没在念这些字，尤其口播本身在讲「提示词 / 文字 / 字幕」时几乎必烧**：

禁止写入 Timeline（中英都禁）：`subtitle` / `caption` / `SRT` / `字幕` / `prompt` / `提示词` / `text` / `文字` / `transcript` / `lyrics` / `karaoke` / `台词`

改用英文标签：`the wrap-up line` / `the next-step line` / `speech-to-text` / `timecode-file` / `instruction-box` / `copy-block`。讲解细则见 presenter-grammar。

## 铁律（共用）

1. **先选分支，再设计。** 不要把 MV 的唱歌写进讲解，不要把讲解全息写进脱口秀，不要把脱口秀坐凳写进 MV。
2. **切点最多一位小数，不要收成整秒。** 单段 3–15 秒。所有段相加 = T。禁止用 SRT 最后一条代替全片。禁止切在半句上。
3. **镜间只硬切。** 禁止溶解、叠化、用推镜当转场。禁止黑场、白场、闪白。
4. **不描写角色长相。** 接触点写 `clearly separated, never fusing`。
5. **给节点的只有时间线字符串。** 提示词按段填进对话框，不塞进 `liangmv:v1`。
6. **对口型要嘴，但不封死遮挡。** 对嘴镜嘴可见时贴原声。欢呼、笑声、演戏镜、片头片尾不对嘴。
7. **画面默认无字幕。** 尾句写 `No on-screen transcript` 挡不住 H3：它会把 Timeline 里的汉字台词烧成字幕。所以台词只留在音频里，Timeline 不引原词。Look 加 `no caption overlay` 和空底栏。讲解例外：专有名词可以是镜内体积物，但绝不是口播逐字字幕。**口播在讲提示词 / 文字 / 字幕时升一档**：Timeline 连英文 trigger 词都不要写，每镜 `Clean frame bottom`，高危段一镜锁死少特效。

分支加则在各自 grammar 里，不要在这里展开。

## 完成后

`liangmv:v1` 贴进 ComfyUI 切音频节点。提示词按段复制。要改某段说段号即可重出。
