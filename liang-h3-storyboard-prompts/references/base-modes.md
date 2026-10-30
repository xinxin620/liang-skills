# H3 三段模式（base / first_frame / first_last_frame）

`short-drama-h3-storyboard` 骨架下的三段模式规格。正文只有三个字段，**仍是一次整体提交**，
不要拆成三次生成。

```text
integrated_multimodal_description: [Shot 1] ...
overall_soundscape: ...
non_diegetic_music: N/A
```

## 各模式起点

- **base（文生）**：只在全单元无任何参考图、且创作者**明确**选择文生视频时使用。
  完整视听时间线从文字构建；风格词（Cinematic / live-action / 2D-animated / 3D CG /
  claymation / watercolor / vintage film…）在 `[Shot 1]` 开头声明。
- **first_frame（首帧）**：从输入帧的可见姿态开始发展；先建立该帧的风格、主体、构图与场景锚点，
  再描述下一个动作。推荐结构：首帧锚点 → 动作起始 → 连续发展 → 结果或反应。
  角色身份、服装、颜色、关键物件、空间关系保持一致。
- **first_last_frame（首尾帧）**：描述首帧到尾帧的**连续路径**——主体怎么移动、姿态怎么变、
  物件怎么被操作、构图怎么演进、光线怎么过渡。一般单镜插值；尾帧必须由最后一个
  `[Shot N]` 在视频结尾到达。推荐结构：首帧状态 → 可观察的中间变化 → 差异逐渐收窄 → 尾帧状态。

## 字段规则

- `integrated_multimodal_description` 是主体：视觉、动作、镜头、说话人、对白、歌唱与画内音
  沿时间线展开。首镜无时间戳；后续刀默认也不写时间点，直接 `[Shot 2] ...` 顺序切镜；
  要写就统一 `[Shot 2] At 00:03.500, ...` 严格递增且落在生成时长内，全不写合法。
- `overall_soundscape`：1–4 句汇总环境声、物理音效、非语言人声；对白与画内音乐不重复到这里。
- `non_diegetic_music`：1–3 句，无配乐写 `N/A`。
- 首帧模式的对齐句（可选，放正文第一行）：
  `For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.`
- 首尾帧模式的对齐句：
  `How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the
  0.00-second mark; Picture 2 (from Shot N) aligns with the S.SS-second mark.`（`S.SS` 为有效时长，
  两位小数）

## 与其他模式互斥

三段输入与六段参考输入在同一请求内互斥：有 `reference_image / reference_video /
reference_audio` 任一项进入任务时改用六段（见 [h3-reference-guide.md](h3-reference-guide.md)）。
连续段（从上一段实际视频续接）统一走六段：上一段实际视频是 `<Video 1>`（`reference_video`），
其实际尾帧是 `<Picture 1>`（`reference_image`），不在三段模式里混用。
