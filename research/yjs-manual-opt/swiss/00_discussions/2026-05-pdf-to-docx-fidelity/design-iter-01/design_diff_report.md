# 逐页精确设计差异（target PDF vs winner DOCX→PDF）

两侧都用 LibreOffice/Pymupdf 渲染到同一坐标空间。font/size/color 直接来自 OOXML/PDF metadata。


## 第 1 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 6 | 5 | -1 |
| drawings | 5 | 6 | +1 |
| 彩色 drawings | 4 | 6 | +2 |
| images | 1 | 1 | +0 |
| accent 红色文字数 | 1 | 1 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei-Bold': 2, 'NSimSun': 2, 'CourierNewPS-BoldMT': 1, 'MicrosoftYaHei': 1}`
**字体使用 — WINNER**: `{'SimHei': 2, 'SimSun': 2, 'ArialMT': 1}`

❗ 仅 target 用的字体（winner 缺失）: ['CourierNewPS-BoldMT', 'MicrosoftYaHei', 'MicrosoftYaHei-Bold', 'NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['ArialMT', 'SimHei', 'SimSun']

**主字号** — TARGET top5: `{7.5: 2, 5.4: 2, 6.0: 1, 18.0: 1}` | WINNER top5: `{8.0: 2, 14.0: 1, 12.0: 1, 7.5: 1}`
**非黑配色** — TARGET: `{'#8E8E93': 3, '#E63946': 1}` | WINNER: `{'#9A9A9A': 2, '#E63946': 1, '#1A1A1A': 1, '#666666': 1}`

红色文字差异：
  - TARGET: ['M O D E L  I M T 0 5 0']
  - WINNER: ['威富可']

## 第 2 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 38 | 39 | +1 |
| drawings | 14 | 14 | +0 |
| 彩色 drawings | 13 | 14 | +1 |
| images | 0 | 0 | +0 |
| accent 红色文字数 | 10 | 10 | +0 |

**字体使用 — TARGET**: `{'CourierNewPSMT': 13, 'MicrosoftYaHei-Bold': 12, 'CourierNewPS-BoldMT': 10, 'NSimSun': 3}`
**字体使用 — WINNER**: `{'ArialMT': 13, 'SimHei': 11, 'Arial-BoldMT': 10, 'SimSun': 5}`

❗ 仅 target 用的字体（winner 缺失）: ['CourierNewPS-BoldMT', 'CourierNewPSMT', 'MicrosoftYaHei-Bold', 'NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['Arial-BoldMT', 'ArialMT', 'SimHei', 'SimSun']

**主字号** — TARGET top5: `{6.75: 11, 7.5: 10, 6.38: 10, 5.25: 4, 5.62: 2}` | WINNER top5: `{6.5: 17, 8.0: 11, 8.5: 10, 14.0: 1}`
**非黑配色** — TARGET: `{'#8E8E93': 16, '#E63946': 10}` | WINNER: `{'#1A1A1A': 12, '#E63946': 10, '#9A9A9A': 10, '#8A8A8A': 4, '#7A7A7A': 2}`

## 第 3 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 59 | 62 | +3 |
| drawings | 6 | 10 | +4 |
| 彩色 drawings | 4 | 8 | +4 |
| images | 1 | 1 | +0 |
| accent 红色文字数 | 27 | 27 | +0 |

**字体使用 — TARGET**: `{'Arial-Black': 26, 'MicrosoftYaHei': 25, 'MicrosoftYaHei-Bold': 3, 'CourierNewPSMT': 3, 'NSimSun': 2}`
**字体使用 — WINNER**: `{'SimSun': 30, 'ArialMT': 28, 'Arial-BoldMT': 2, 'SimHei': 2}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-Black', 'CourierNewPSMT', 'MicrosoftYaHei', 'MicrosoftYaHei-Bold', 'NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['Arial-BoldMT', 'ArialMT', 'SimHei', 'SimSun']

**主字号** — TARGET top5: `{5.25: 28, 6.98: 24, 13.5: 2, 6.38: 2, 6.75: 1}` | WINNER top5: `{8.0: 51, 6.5: 7, 12.0: 2, 9.0: 2}`
**非黑配色** — TARGET: `{'#E63946': 27, '#8E8E93': 5, '#222222': 1}` | WINNER: `{'#1A1A1A': 28, '#E63946': 27, '#8A8A8A': 5, '#7A7A7A': 1}`

## 第 4 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 46 | 47 | +1 |
| drawings | 8 | 16 | +8 |
| 彩色 drawings | 5 | 14 | +9 |
| images | 0 | 0 | +0 |
| accent 红色文字数 | 10 | 10 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 17, 'Arial-Black': 12, 'ArialMT': 8, 'MicrosoftYaHei-Bold': 4, 'CourierNewPSMT': 3, 'NSimSun': 2}`
**字体使用 — WINNER**: `{'ArialMT': 20, 'SimSun': 17, 'LiSu': 4, 'Arial-BoldMT': 3, 'SimHei': 3}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-Black', 'CourierNewPSMT', 'MicrosoftYaHei', 'MicrosoftYaHei-Bold', 'NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['Arial-BoldMT', 'LiSu', 'SimHei', 'SimSun']

**主字号** — TARGET top5: `{6.98: 25, 5.25: 13, 6.38: 4, 13.5: 2, 6.75: 1}` | WINNER top5: `{8.0: 35, 6.5: 6, 9.0: 4, 12.0: 2}`
**非黑配色** — TARGET: `{'#444444': 16, '#E63946': 10, '#8E8E93': 5, '#333333': 2}` | WINNER: `{'#1A1A1A': 31, '#E63946': 10, '#8A8A8A': 4, '#7A7A7A': 1}`

## 第 5 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 53 | 54 | +1 |
| drawings | 8 | 12 | +4 |
| 彩色 drawings | 3 | 10 | +7 |
| images | 0 | 0 | +0 |
| accent 红色文字数 | 14 | 14 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 21, 'Arial-Black': 14, 'ArialMT': 7, 'MicrosoftYaHei-Bold': 6, 'CourierNewPSMT': 3, 'NSimSun': 2}`
**字体使用 — WINNER**: `{'SimSun': 25, 'ArialMT': 24, 'SimHei': 4, 'Arial-BoldMT': 1}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-Black', 'CourierNewPSMT', 'MicrosoftYaHei', 'MicrosoftYaHei-Bold', 'NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['Arial-BoldMT', 'SimHei', 'SimSun']

**主字号** — TARGET top5: `{7.5: 32, 6.0: 13, 5.25: 4, 13.5: 2, 6.75: 1}` | WINNER top5: `{8.0: 42, 6.5: 7, 10.0: 3, 12.0: 2}`
**非黑配色** — TARGET: `{'#E63946': 14, '#8E8E93': 5}` | WINNER: `{'#1A1A1A': 33, '#E63946': 14, '#8A8A8A': 5, '#7A7A7A': 1}`

## 第 6 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 26 | 28 | +2 |
| drawings | 57 | 41 | -16 |
| 彩色 drawings | 44 | 39 | -5 |
| images | 1 | 1 | +0 |
| accent 红色文字数 | 1 | 1 | +0 |

**字体使用 — TARGET**: `{'ArialMT': 7, 'MicrosoftYaHei': 7, 'MicrosoftYaHei-Bold': 6, 'CourierNewPSMT': 3, 'NSimSun': 2, 'Arial-Black': 1}`
**字体使用 — WINNER**: `{'SimSun': 15, 'ArialMT': 11, 'Arial-BoldMT': 1, 'SimHei': 1}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-Black', 'CourierNewPSMT', 'MicrosoftYaHei', 'MicrosoftYaHei-Bold', 'NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['Arial-BoldMT', 'SimHei', 'SimSun']

**主字号** — TARGET top5: `{6.6: 14, 6.0: 4, 5.25: 4, 13.5: 2, 6.75: 1}` | WINNER top5: `{7.5: 14, 6.5: 7, 7.0: 4, 12.0: 2, 8.0: 1}`
**非黑配色** — TARGET: `{'#1A1A1A': 14, '#8E8E93': 5, '#FFFFFF': 4, '#E63946': 1}` | WINNER: `{'#1A1A1A': 16, '#8A8A8A': 5, '#FFFFFF': 4, '#7A7A7A': 1, '#E63946': 1}`

## 第 7 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 37 | 31 | -6 |
| drawings | 48 | 28 | -20 |
| 彩色 drawings | 39 | 26 | -13 |
| images | 2 | 2 | +0 |
| accent 红色文字数 | 1 | 1 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 13, 'ArialMT': 8, 'CourierNewPS-BoldMT': 5, 'MicrosoftYaHei-Bold': 4, 'CourierNewPSMT': 3, 'NSimSun': 2, 'Arial-Black': 1, 'Arial-BoldMT': 1}`
**字体使用 — WINNER**: `{'SimSun': 18, 'ArialMT': 10, 'Arial-BoldMT': 2, 'SimHei': 1}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-Black', 'CourierNewPS-BoldMT', 'CourierNewPSMT', 'MicrosoftYaHei', 'MicrosoftYaHei-Bold', 'NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['SimHei', 'SimSun']

**主字号** — TARGET top5: `{6.6: 21, 6.29: 5, 5.25: 4, 6.0: 3, 13.5: 2}` | WINNER top5: `{7.5: 18, 6.5: 7, 7.0: 3, 12.0: 2, 8.0: 1}`
**非黑配色** — TARGET: `{'#1A1A1A': 21, '#8E8E93': 5, '#FFFFFF': 3, '#E63946': 1}` | WINNER: `{'#1A1A1A': 20, '#8A8A8A': 5, '#FFFFFF': 3, '#7A7A7A': 1, '#E63946': 1}`

## 第 8 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 54 | 56 | +2 |
| drawings | 110 | 64 | -46 |
| 彩色 drawings | 46 | 50 | +4 |
| images | 0 | 0 | +0 |
| accent 红色文字数 | 1 | 1 | +0 |

**字体使用 — TARGET**: `{'ArialMT': 23, 'MicrosoftYaHei': 21, 'MicrosoftYaHei-Bold': 4, 'CourierNewPSMT': 3, 'NSimSun': 2, 'Arial-Black': 1}`
**字体使用 — WINNER**: `{'SimSun': 26, 'ArialMT': 21, 'Arial-BoldMT': 7, 'SimHei': 1, 'LiSu': 1}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-Black', 'CourierNewPSMT', 'MicrosoftYaHei', 'MicrosoftYaHei-Bold', 'NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['Arial-BoldMT', 'LiSu', 'SimHei', 'SimSun']

**主字号** — TARGET top5: `{6.67: 44, 5.25: 4, 13.5: 2, 6.0: 2, 6.75: 1}` | WINNER top5: `{6.5: 51, 12.0: 2, 7.0: 2, 8.0: 1}`
**非黑配色** — TARGET: `{'#1A1A1A': 44, '#8E8E93': 5, '#FFFFFF': 2, '#E63946': 1}` | WINNER: `{'#1A1A1A': 46, '#8A8A8A': 5, '#FFFFFF': 2, '#7A7A7A': 1, '#E63946': 1}`

## 第 9 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 41 | 36 | -5 |
| drawings | 11 | 21 | +10 |
| 彩色 drawings | 3 | 19 | +16 |
| images | 3 | 3 | +0 |
| accent 红色文字数 | 5 | 5 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 15, 'Arial-Black': 8, 'ArialMT': 7, 'MicrosoftYaHei-Bold': 5, 'CourierNewPSMT': 3, 'NSimSun': 2, 'Arial-BoldMT': 1}`
**字体使用 — WINNER**: `{'SimSun': 16, 'ArialMT': 12, 'Arial-BoldMT': 4, 'SimHei': 4}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-Black', 'CourierNewPSMT', 'MicrosoftYaHei', 'MicrosoftYaHei-Bold', 'NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['SimHei', 'SimSun']

**主字号** — TARGET top5: `{7.5: 26, 6.75: 4, 6.0: 4, 5.25: 4, 13.5: 2}` | WINNER top5: `{8.0: 18, 6.5: 10, 10.0: 3, 7.0: 3, 12.0: 2}`
**非黑配色** — TARGET: `{'#8E8E93': 5, '#E63946': 5, '#222222': 3, '#FFFFFF': 3}` | WINNER: `{'#1A1A1A': 21, '#8A8A8A': 5, '#E63946': 5, '#FFFFFF': 3, '#7A7A7A': 1}`

## 第 10 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 48 | 41 | -7 |
| drawings | 10 | 21 | +11 |
| 彩色 drawings | 5 | 19 | +14 |
| images | 6 | 6 | +0 |
| accent 红色文字数 | 5 | 5 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 14, 'ArialMT': 12, 'Arial-Black': 9, 'Arial-BoldMT': 5, 'MicrosoftYaHei-Bold': 3, 'CourierNewPSMT': 3, 'NSimSun': 2}`
**字体使用 — WINNER**: `{'SimSun': 19, 'ArialMT': 13, 'Arial-BoldMT': 7, 'SimHei': 2}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-Black', 'CourierNewPSMT', 'MicrosoftYaHei', 'MicrosoftYaHei-Bold', 'NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['SimHei', 'SimSun']

**主字号** — TARGET top5: `{7.04: 20, 7.5: 9, 5.25: 8, 6.75: 6, 13.5: 2}` | WINNER top5: `{8.0: 19, 6.5: 15, 7.0: 3, 12.0: 2, 9.0: 2}`
**非黑配色** — TARGET: `{'#444444': 20, '#222222': 9, '#8E8E93': 5, '#E63946': 5, '#FFFFFF': 3, '#333333': 2}` | WINNER: `{'#1A1A1A': 27, '#E63946': 5, '#8A8A8A': 4, '#FFFFFF': 3, '#7A7A7A': 1}`

## 第 11 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 60 | 64 | +4 |
| drawings | 87 | 55 | -32 |
| 彩色 drawings | 45 | 50 | +5 |
| images | 0 | 0 | +0 |
| accent 红色文字数 | 1 | 1 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 40, 'ArialMT': 7, 'MicrosoftYaHei-Bold': 6, 'CourierNewPSMT': 3, 'Arial-Black': 2, 'NSimSun': 2}`
**字体使用 — WINNER**: `{'SimSun': 49, 'ArialMT': 11, 'Arial-BoldMT': 2, 'SimHei': 2}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-Black', 'CourierNewPSMT', 'MicrosoftYaHei', 'MicrosoftYaHei-Bold', 'NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['Arial-BoldMT', 'SimHei', 'SimSun']

**主字号** — TARGET top5: `{6.52: 46, 5.25: 4, 6.0: 3, 13.5: 2, 6.38: 2}` | WINNER top5: `{6.5: 54, 8.0: 3, 7.0: 3, 12.0: 2, 9.0: 2}`
**非黑配色** — TARGET: `{'#1A1A1A': 46, '#8E8E93': 5, '#FFFFFF': 3, '#E63946': 1}` | WINNER: `{'#1A1A1A': 53, '#8A8A8A': 5, '#FFFFFF': 3, '#7A7A7A': 1, '#E63946': 1}`

## 第 12 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 37 | 35 | -2 |
| drawings | 14 | 30 | +16 |
| 彩色 drawings | 3 | 28 | +25 |
| images | 2 | 2 | +0 |
| accent 红色文字数 | 5 | 5 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 12, 'Arial-Black': 11, 'MicrosoftYaHei-Bold': 6, 'CourierNewPSMT': 3, 'ArialMT': 2, 'NSimSun': 2, 'Arial-BoldMT': 1}`
**字体使用 — WINNER**: `{'SimSun': 15, 'ArialMT': 9, 'Arial-BoldMT': 7, 'SimHei': 4}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-Black', 'CourierNewPSMT', 'MicrosoftYaHei', 'MicrosoftYaHei-Bold', 'NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['SimHei', 'SimSun']

**主字号** — TARGET top5: `{7.5: 19, 6.75: 7, 6.0: 4, 5.25: 4, 13.5: 2}` | WINNER top5: `{6.5: 15, 8.0: 9, 7.0: 6, 10.0: 3, 12.0: 2}`
**非黑配色** — TARGET: `{'#222222': 10, '#FFFFFF': 6, '#8E8E93': 5, '#E63946': 5}` | WINNER: `{'#1A1A1A': 17, '#FFFFFF': 6, '#8A8A8A': 5, '#E63946': 5, '#7A7A7A': 1}`

## 第 13 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 46 | 48 | +2 |
| drawings | 10 | 18 | +8 |
| 彩色 drawings | 5 | 16 | +11 |
| images | 0 | 0 | +0 |
| accent 红色文字数 | 12 | 12 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 18, 'Arial-Black': 13, 'MicrosoftYaHei-Bold': 5, 'ArialMT': 5, 'CourierNewPSMT': 3, 'NSimSun': 2}`
**字体使用 — WINNER**: `{'SimSun': 22, 'ArialMT': 20, 'SimHei': 4, 'Arial-BoldMT': 2}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-Black', 'CourierNewPSMT', 'MicrosoftYaHei', 'MicrosoftYaHei-Bold', 'NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['Arial-BoldMT', 'SimHei', 'SimSun']

**主字号** — TARGET top5: `{7.5: 24, 6.0: 11, 5.25: 4, 6.75: 3, 13.5: 2}` | WINNER top5: `{8.0: 35, 6.5: 7, 10.0: 3, 12.0: 2, 9.0: 1}`
**非黑配色** — TARGET: `{'#E63946': 12, '#8E8E93': 5, '#444444': 2, '#333333': 1}` | WINNER: `{'#1A1A1A': 29, '#E63946': 12, '#8A8A8A': 5, '#7A7A7A': 1}`

## 第 14 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 59 | 52 | -7 |
| drawings | 57 | 41 | -16 |
| 彩色 drawings | 42 | 39 | -3 |
| images | 1 | 1 | +0 |
| accent 红色文字数 | 4 | 4 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 23, 'ArialMT': 13, 'MicrosoftYaHei-Bold': 11, 'Arial-Black': 4, 'CourierNewPSMT': 3, 'Arial-BoldMT': 3, 'NSimSun': 2}`
**字体使用 — WINNER**: `{'SimSun': 27, 'ArialMT': 20, 'SimHei': 4, 'Arial-BoldMT': 1}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-Black', 'CourierNewPSMT', 'MicrosoftYaHei', 'MicrosoftYaHei-Bold', 'NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['SimHei', 'SimSun']

**主字号** — TARGET top5: `{7.5: 23, 6.67: 21, 6.0: 7, 5.25: 4, 13.5: 2}` | WINNER top5: `{7.5: 21, 8.0: 19, 6.5: 7, 10.0: 3, 12.0: 2}`
**非黑配色** — TARGET: `{'#1A1A1A': 20, '#222222': 15, '#8E8E93': 6, '#E63946': 4, '#FFFFFF': 4}` | WINNER: `{'#1A1A1A': 41, '#8A8A8A': 5, '#E63946': 4, '#7A7A7A': 1}`

## 第 15 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 22 | 23 | +1 |
| drawings | 61 | 39 | -22 |
| 彩色 drawings | 47 | 37 | -10 |
| images | 0 | 0 | +0 |
| accent 红色文字数 | 1 | 1 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 11, 'MicrosoftYaHei-Bold': 3, 'CourierNewPSMT': 3, 'ArialMT': 2, 'NSimSun': 2, 'Arial-Black': 1}`
**字体使用 — WINNER**: `{'SimSun': 15, 'ArialMT': 3, 'Arial-BoldMT': 3, 'SimHei': 2}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-Black', 'CourierNewPSMT', 'MicrosoftYaHei', 'MicrosoftYaHei-Bold', 'NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['Arial-BoldMT', 'SimHei', 'SimSun']

**主字号** — TARGET top5: `{6.67: 13, 5.25: 4, 13.5: 2, 6.75: 1, 5.62: 1}` | WINNER top5: `{7.5: 13, 6.5: 6, 12.0: 2, 8.0: 1, 10.0: 1}`
**非黑配色** — TARGET: `{'#1A1A1A': 13, '#8E8E93': 5, '#E63946': 1}` | WINNER: `{'#1A1A1A': 16, '#8A8A8A': 4, '#7A7A7A': 1, '#E63946': 1}`