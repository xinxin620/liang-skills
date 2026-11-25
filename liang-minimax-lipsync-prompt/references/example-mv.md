# 行文示例

先看分支。剧情向 4 刀、景别跳两级。画面向大约 3 刀、约 5 秒、同景别换轴合法。

剧情向可以：`3/4/3/5`。不行：`5+5+5`、`12+3`、一镜 8 秒。
画面向可以：`6/5/4`、`5/6/4`。不行：`MLS→CU→MLS→CU`。

## 剧情向 — 走进教室坐下偷瞄

输入：校园甜歌、16:9、女主 / 教室 / 男生参考。故事：进来 → 坐下写作业 → 偷瞄 → 近景唱。

```
subject_definitions:
<Subject 1>: lead vocalist identity from <Picture 1>
<Subject 3>: sunlit classroom, afternoon, to be supplied as <Picture 3>
<Subject 4>: the boy she likes, identity from <Picture 4>

retention_analysis:
<Subject 1> fully_preserved, keep face body and wardrobe consistent with reference.
<Subject 3> fully_preserved, keep the classroom layout and window light consistent once the location still is set.
<Subject 4> fully_preserved, keep face body and wardrobe consistent with reference.

Look:
16:9 youthful sweet-pop music-video, airy afternoon sun, warm pale highlights, light grain, 35mm, no caption overlay. Style from <Picture 1>.

Timeline:
[0s-3s] Medium-long of <Subject 1> walking into <Subject 3>, books in hand. Acting, mouth closed, not singing. Locked-off.
[3s-7s] Hard cut: close-up of <Subject 1> sitting down, notebook opening on the desk. Hands and face clearly separated, never fusing. Acting, mouth closed, not singing. Eyes on the page.
[7s-11s] Hard cut: medium-long two-shot. <Subject 1> at her desk in the foreground, peeking over the notebook toward <Subject 4> a few rows away. She writes then glances. Acting, mouth closed, not singing. Both clearly separated, never fusing. Locked-off.
[11s-15s] Hard cut: close-up of <Subject 1> at the desk. Mouth singing. Eyes flick toward him then back to the page.

Editing rules:
Hard cuts only, no dissolves, no push-ins as transitions. Four shots, about 3-4s each, unequal. Each cut is the next story beat, not coverage. Two-size leaps. Acting shots do not sing. No burnt-in text of any kind. Forbidden: subtitle bar, closed captions, karaoke, lyric cards, lower thirds, speech bubbles, chyrons, any Chinese or English transcript of the audio. The picture has no readable caption overlay.

Audio / Text:
<audio 2> plays the original vocal unchanged; do not dub or re-sing. On singing shots, when the mouth is visible, <Subject 1>'s mouth, jaw, breath and micro-expression lock to the vocal phoneme by phoneme. On acting shots, do not lip-sync: mouth closed or following the acting, not the lyric. Brief motivated occlusions and reveals are allowed. No burnt-in text of any kind. Forbidden: subtitle bar, closed captions, karaoke, lyric cards, lower thirds, speech bubbles, chyrons, any Chinese or English transcript of the audio. The picture has no readable caption overlay.
```

上一格若是「走廊看见他」，这一格必须从进教室开始。

## 画面向 — 词换景，人在空间里唱

输入：民谣情歌、16:9、一张人物参考。不编情节。两句两个有关联的夜景，不是一扇窗换角度。

```
subject_definitions:
<Subject 1>: lead vocalist identity from <Picture 1>
<Subject 2>: empty rural night road, distant village lights, overcast, no location still
<Subject 3>: old kitchen doorway, wood smoke, warm lamp, no location still

retention_analysis:
<Subject 1> fully_preserved, keep face body and wardrobe consistent with reference.
<Subject 2> fully_preserved, keep the road, sky and distant lights consistent once established.
<Subject 3> fully_preserved, keep the doorway, smoke direction and lamp consistent once established.

Look:
16:9 overcast Chinese-folk music-video, muted sage and grey, wet air, fine grain, 35mm, no caption overlay. Style from <Picture 1>.

Timeline:
[0s-5.5s] Medium shot on the night road. <Subject 1> in the frame with the road and distant lights. Soft overcast. Focus on her, background a little soft. Mouth singing the whole first line. Slow walk two steps toward camera, then almost stop. Very slow push in, no lock-off. Eyes down the road.
[5.5s-12s] Hard cut: medium close-up already in the kitchen doorway. Warm lamp, wood smoke as a thin foreground layer. She has stopped walking. Looks at the smoke, inhales, then Mouth singing the second line. Rack from the smoke to the mouth. No camera move after the rack. Weight shifts once on the breath.

Editing rules:
Hard cuts only, no dissolves, no fade to black, no fade to white, no white flash, no push-ins as transitions. Two lyric images, two related spaces. First shot places the body in the place; second shot is closer. Intra-shot move only when the line needs it. No burnt-in text of any kind. Forbidden: subtitle bar, closed captions, karaoke, lyric cards, lower thirds, speech bubbles, chyrons, any Chinese or English transcript of the audio. The picture has no readable caption overlay.

Audio / Text:
<audio 1> is the lip-sync and rhythm source. Play the original vocal unchanged; do not dub or re-sing. When the mouth is visible, <Subject 1>'s mouth, jaw, breath and micro-expression lock to the vocal phoneme by phoneme. Brief motivated occlusions and reveals are allowed. No burnt-in text of any kind. Forbidden: subtitle bar, closed captions, karaoke, lyric cards, lower thirds, speech bubbles, chyrons, any Chinese or English transcript of the audio. The picture has no readable caption overlay.
```

不要把这一格改成窗边正面侧面再特写。也不要写成远近远近。
