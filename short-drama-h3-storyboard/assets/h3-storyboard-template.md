# H3 分镜 · <项目/集数>

- 目标模型：minimax-h3
- 单单元时长：4–15 秒
- 输出说明：每个 `H3-UNIT` 是一次独立 job；`H3 提示词` 整体复制提交。

## H3-UNIT-<EP>-<SEQ> · <单元名>
- 时长：<4–15> 秒
- 模式：<reference / first_frame / first_last_frame / base>
- 来源：<真实剧本场景 ID>
- 参考图：<REF/PLAN 槽位，逐项写顺序、路径或条目 ID、中文名称、用途、控制、不得控制>
- 主体映射：<Subject 1> = <角色> = <Picture N> = <Sx>
- 声线映射：<角色> = <Subject N> = <Sx> = <固定音色与说话方式>
- 空间锁：<屏幕左右、朝向、轴线、出入口、禁止镜像>
- 口型纪律：<只有谁可以动嘴；其他人嘴部状态；无对白镜的嘴部状态>
- 状态链：<起点> → <唯一主变化> → <可验证终点>
- 声音：<环境声、物理音效、非语言人声、对白来源>

### SHOT-<EP>-<SEQ>-01 · <镜头名>
- 职责：<观众看到这一刀后多知道/多感受到什么>
- 起点：<可见起始姿态、位置、持物、朝向>
- 唯一动作：<主体、方向、幅度、速度、先后关系>
- 终点：<可验证停止状态>
- 景别 / 机位 / 运镜：<景别、机位高度、镜头行为与理由>
- 声音 / 对白：<底声；若说话则写来源与逐字文本>

### SHOT-<EP>-<SEQ>-02 · <镜头名>
- 职责：<...>
- 起点：<...>
- 唯一动作：<...>
- 终点：<...>
- 景别 / 机位 / 运镜：<...>
- 声音 / 对白：<...>

### H3 提示词

```text
subject_definitions: <Subject 1> is ... in <Picture N>, with ... <Subject 2> is ... <Picture N> anchors the environment: ... <Picture N> is the locked blocking reference: preserve screen arrangement and axis; do not mirror it.
summary: ...
retention_analysis: <Subject 1> (appears in [Shot 1]–[Shot N]): fully_preserved - ... <Picture N> (appears in [Shot 1]–[Shot N]): partially_preserved - ... <Picture N> (appears in [Shot 1]–[Shot N]): fully_preserved - screen-left/right arrangement and axis stay locked; preserve the reference and do not mirror it.
detailed_description: [Shot 1] ... [Shot 2] At 00:03.500, ... <说话人> (Sx) says: <d>[Chinese]逐字台词</d> Every other character keeps their lips completely closed. [Shot 3] At 00:07.000, ... neither character speaks and both mouths remain closed.
overall_soundscape: ...
non_diegetic_music: N/A
```

## H3-UNIT-<EP>-<SEQ+1> · <单元名>
- 时长：<4–15> 秒
- 模式：<reference / first_frame / first_last_frame / base>
- 来源：<真实剧本场景 ID>
- 参考图：<...>
- 主体映射：<...>
- 声线映射：<...>
- 空间锁：<...>
- 口型纪律：<...>
- 状态链：<...> → <...> → <...>
- 声音：<...>

### SHOT-<EP>-<SEQ+1>-01 · <镜头名>
- 职责：<...>
- 起点：<...>
- 唯一动作：<...>
- 终点：<...>
- 景别 / 机位 / 运镜：<...>
- 声音 / 对白：<...>

### H3 提示词

```text
integrated_multimodal_description: [Shot 1] ...
overall_soundscape: ...
non_diegetic_music: N/A
```

## 交付报告

- 已拆生成单元：<数量与总时长>
- 多镜容器：<单元、资格、每个切点的关键帧>
- 参考缺口：<无 / 逐项>
- 待创作者决定：<无 / 逐项>