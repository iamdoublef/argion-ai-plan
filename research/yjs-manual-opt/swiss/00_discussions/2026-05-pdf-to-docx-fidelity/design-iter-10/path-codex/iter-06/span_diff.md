# 逐页精确设计差异（target PDF vs winner DOCX→PDF）

两侧都用 LibreOffice/Pymupdf 渲染到同一坐标空间。font/size/color 直接来自 OOXML/PDF metadata。


## 第 1 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 6 | 8 | +2 |
| drawings | 5 | 2 | -3 |
| 彩色 drawings | 4 | 0 | -4 |
| images | 1 | 1 | +0 |
| accent 红色文字数 | 1 | 3 | +2 |

**字体使用 — TARGET**: `{'MicrosoftYaHei-Bold': 2, 'NSimSun': 2, 'CourierNewPS-BoldMT': 1, 'MicrosoftYaHei': 1}`
**字体使用 — WINNER**: `{'MicrosoftYaHei-Bold': 4, 'MicrosoftYaHei': 3, 'CourierNewPS-BoldMT': 1}`

❗ 仅 target 用的字体（winner 缺失）: ['NSimSun']

**主字号** — TARGET top5: `{7.5: 2, 5.4: 2, 6.0: 1, 18.0: 1}` | WINNER top5: `{7.5: 3, 5.0: 2, 6.0: 1, 18.0: 1, 7.0: 1}`
**非黑配色** — TARGET: `{'#8E8E93': 3, '#E63946': 1}` | WINNER: `{'#E63946': 3, '#8E8E93': 3, '#1A1A1A': 1}`

红色文字差异：
  - TARGET: ['M O D E L  I M T 0 5 0']
  - WINNER: ['━━', 'MODEL IMT050', '━━━━']

## 第 2 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 38 | 38 | +0 |
| drawings | 14 | 3 | -11 |
| 彩色 drawings | 13 | 1 | -12 |
| images | 0 | 0 | +0 |
| accent 红色文字数 | 10 | 10 | +0 |

**字体使用 — TARGET**: `{'CourierNewPSMT': 13, 'MicrosoftYaHei-Bold': 12, 'CourierNewPS-BoldMT': 10, 'NSimSun': 3}`
**字体使用 — WINNER**: `{'CourierNewPSMT': 12, 'MicrosoftYaHei-Bold': 12, 'CourierNewPS-BoldMT': 10, 'MicrosoftYaHei': 3, 'ArialMT': 1}`

❗ 仅 target 用的字体（winner 缺失）: ['NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['ArialMT', 'MicrosoftYaHei']

**主字号** — TARGET top5: `{6.75: 11, 7.5: 10, 6.38: 10, 5.25: 4, 5.62: 2}` | WINNER top5: `{6.5: 11, 7.5: 10, 6.0: 10, 5.0: 6, 15.0: 1}`
**非黑配色** — TARGET: `{'#8E8E93': 16, '#E63946': 10}` | WINNER: `{'#8E8E93': 16, '#E63946': 10}`

## 第 3 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 59 | 59 | +0 |
| drawings | 6 | 9 | +3 |
| 彩色 drawings | 4 | 5 | +1 |
| images | 1 | 1 | +0 |
| accent 红色文字数 | 27 | 27 | +0 |

**字体使用 — TARGET**: `{'Arial-Black': 26, 'MicrosoftYaHei': 25, 'MicrosoftYaHei-Bold': 3, 'CourierNewPSMT': 3, 'NSimSun': 2}`
**字体使用 — WINNER**: `{'MicrosoftYaHei': 27, 'MicrosoftYaHei-Bold': 27, 'CourierNewPSMT': 2, 'Arial-Black': 2, 'ArialMT': 1}`

❗ 仅 target 用的字体（winner 缺失）: ['NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['ArialMT']

**主字号** — TARGET top5: `{5.25: 28, 6.98: 24, 13.5: 2, 6.38: 2, 6.75: 1}` | WINNER top5: `{5.0: 29, 6.5: 25, 6.0: 2, 13.5: 1, 11.0: 1}`
**非黑配色** — TARGET: `{'#E63946': 27, '#8E8E93': 5, '#222222': 1}` | WINNER: `{'#E63946': 27, '#8E8E93': 5, '#1A1A1A': 1}`

## 第 4 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 46 | 46 | +0 |
| drawings | 8 | 11 | +3 |
| 彩色 drawings | 5 | 3 | -2 |
| images | 0 | 0 | +0 |
| accent 红色文字数 | 10 | 10 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 17, 'Arial-Black': 12, 'ArialMT': 8, 'MicrosoftYaHei-Bold': 4, 'CourierNewPSMT': 3, 'NSimSun': 2}`
**字体使用 — WINNER**: `{'MicrosoftYaHei': 15, 'MicrosoftYaHei-Bold': 13, 'ArialMT': 9, 'LiSu': 4, 'Arial-Black': 3, 'CourierNewPSMT': 2}`

❗ 仅 target 用的字体（winner 缺失）: ['NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['LiSu']

**主字号** — TARGET top5: `{6.98: 25, 5.25: 13, 6.38: 4, 13.5: 2, 6.75: 1}` | WINNER top5: `{6.5: 26, 5.0: 14, 6.0: 4, 13.5: 1, 11.0: 1}`
**非黑配色** — TARGET: `{'#444444': 16, '#E63946': 10, '#8E8E93': 5, '#333333': 2}` | WINNER: `{'#E63946': 10, '#8E8E93': 5}`

## 第 5 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 53 | 53 | +0 |
| drawings | 8 | 11 | +3 |
| 彩色 drawings | 3 | 1 | -2 |
| images | 0 | 0 | +0 |
| accent 红色文字数 | 14 | 14 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 21, 'Arial-Black': 14, 'ArialMT': 7, 'MicrosoftYaHei-Bold': 6, 'CourierNewPSMT': 3, 'NSimSun': 2}`
**字体使用 — WINNER**: `{'MicrosoftYaHei': 23, 'MicrosoftYaHei-Bold': 19, 'ArialMT': 8, 'CourierNewPSMT': 2, 'Arial-Black': 1}`

❗ 仅 target 用的字体（winner 缺失）: ['NSimSun']

**主字号** — TARGET top5: `{7.5: 32, 6.0: 13, 5.25: 4, 13.5: 2, 6.75: 1}` | WINNER top5: `{7.0: 29, 6.0: 13, 5.0: 5, 7.5: 3, 6.5: 1}`
**非黑配色** — TARGET: `{'#E63946': 14, '#8E8E93': 5}` | WINNER: `{'#E63946': 14, '#8E8E93': 5}`

## 第 6 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 26 | 26 | +0 |
| drawings | 57 | 51 | -6 |
| 彩色 drawings | 44 | 47 | +3 |
| images | 1 | 1 | +0 |
| accent 红色文字数 | 1 | 1 | +0 |

**字体使用 — TARGET**: `{'ArialMT': 7, 'MicrosoftYaHei': 7, 'MicrosoftYaHei-Bold': 6, 'CourierNewPSMT': 3, 'NSimSun': 2, 'Arial-Black': 1}`
**字体使用 — WINNER**: `{'MicrosoftYaHei': 9, 'ArialMT': 8, 'MicrosoftYaHei-Bold': 6, 'CourierNewPSMT': 2, 'Arial-Black': 1}`

❗ 仅 target 用的字体（winner 缺失）: ['NSimSun']

**主字号** — TARGET top5: `{6.6: 14, 6.0: 4, 5.25: 4, 13.5: 2, 6.75: 1}` | WINNER top5: `{6.5: 15, 5.0: 5, 6.0: 4, 13.5: 1, 11.0: 1}`
**非黑配色** — TARGET: `{'#1A1A1A': 14, '#8E8E93': 5, '#FFFFFF': 4, '#E63946': 1}` | WINNER: `{'#1A1A1A': 14, '#8E8E93': 5, '#FFFFFF': 4, '#E63946': 1}`

## 第 7 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 37 | 33 | -4 |
| drawings | 48 | 36 | -12 |
| 彩色 drawings | 39 | 32 | -7 |
| images | 2 | 2 | +0 |
| accent 红色文字数 | 1 | 1 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 13, 'ArialMT': 8, 'CourierNewPS-BoldMT': 5, 'MicrosoftYaHei-Bold': 4, 'CourierNewPSMT': 3, 'NSimSun': 2, 'Arial-Black': 1, 'Arial-BoldMT': 1}`
**字体使用 — WINNER**: `{'MicrosoftYaHei': 13, 'ArialMT': 12, 'MicrosoftYaHei-Bold': 4, 'CourierNewPSMT': 2, 'Arial-Black': 2}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-BoldMT', 'CourierNewPS-BoldMT', 'NSimSun']

**主字号** — TARGET top5: `{6.6: 21, 6.29: 5, 5.25: 4, 6.0: 3, 13.5: 2}` | WINNER top5: `{6.5: 23, 5.0: 5, 6.0: 3, 13.5: 1, 11.0: 1}`
**非黑配色** — TARGET: `{'#1A1A1A': 21, '#8E8E93': 5, '#FFFFFF': 3, '#E63946': 1}` | WINNER: `{'#1A1A1A': 22, '#8E8E93': 5, '#FFFFFF': 3, '#E63946': 1}`

## 第 8 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 54 | 54 | +0 |
| drawings | 110 | 96 | -14 |
| 彩色 drawings | 46 | 50 | +4 |
| images | 0 | 0 | +0 |
| accent 红色文字数 | 1 | 1 | +0 |

**字体使用 — TARGET**: `{'ArialMT': 23, 'MicrosoftYaHei': 21, 'MicrosoftYaHei-Bold': 4, 'CourierNewPSMT': 3, 'NSimSun': 2, 'Arial-Black': 1}`
**字体使用 — WINNER**: `{'ArialMT': 24, 'MicrosoftYaHei': 22, 'MicrosoftYaHei-Bold': 4, 'CourierNewPSMT': 2, 'Arial-Black': 1, 'LiSu': 1}`

❗ 仅 target 用的字体（winner 缺失）: ['NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['LiSu']

**主字号** — TARGET top5: `{6.67: 44, 5.25: 4, 13.5: 2, 6.0: 2, 6.75: 1}` | WINNER top5: `{6.5: 45, 5.0: 5, 6.0: 2, 13.5: 1, 11.0: 1}`
**非黑配色** — TARGET: `{'#1A1A1A': 44, '#8E8E93': 5, '#FFFFFF': 2, '#E63946': 1}` | WINNER: `{'#1A1A1A': 44, '#8E8E93': 5, '#FFFFFF': 2, '#E63946': 1}`

## 第 9 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 41 | 39 | -2 |
| drawings | 11 | 14 | +3 |
| 彩色 drawings | 3 | 1 | -2 |
| images | 3 | 3 | +0 |
| accent 红色文字数 | 5 | 5 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 15, 'Arial-Black': 8, 'ArialMT': 7, 'MicrosoftYaHei-Bold': 5, 'CourierNewPSMT': 3, 'NSimSun': 2, 'Arial-BoldMT': 1}`
**字体使用 — WINNER**: `{'MicrosoftYaHei': 15, 'MicrosoftYaHei-Bold': 9, 'ArialMT': 8, 'Arial-Black': 5, 'CourierNewPSMT': 2}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-BoldMT', 'NSimSun']

**主字号** — TARGET top5: `{7.5: 26, 6.75: 4, 6.0: 4, 5.25: 4, 13.5: 2}` | WINNER top5: `{7.0: 24, 5.0: 5, 6.0: 4, 7.5: 3, 6.5: 1}`
**非黑配色** — TARGET: `{'#8E8E93': 5, '#E63946': 5, '#222222': 3, '#FFFFFF': 3}` | WINNER: `{'#8E8E93': 5, '#E63946': 5, '#FFFFFF': 3}`

## 第 10 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 48 | 49 | +1 |
| drawings | 10 | 10 | +0 |
| 彩色 drawings | 5 | 3 | -2 |
| images | 6 | 6 | +0 |
| accent 红色文字数 | 5 | 5 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 14, 'ArialMT': 12, 'Arial-Black': 9, 'Arial-BoldMT': 5, 'MicrosoftYaHei-Bold': 3, 'CourierNewPSMT': 3, 'NSimSun': 2}`
**字体使用 — WINNER**: `{'MicrosoftYaHei': 16, 'ArialMT': 12, 'Arial-Black': 10, 'MicrosoftYaHei-Bold': 7, 'CourierNewPSMT': 2, 'Cambria': 2}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-BoldMT', 'NSimSun']
❗ 仅 winner 用的字体（target 没有）: ['Cambria']

**主字号** — TARGET top5: `{7.04: 20, 7.5: 9, 5.25: 8, 6.75: 6, 13.5: 2}` | WINNER top5: `{7.0: 31, 5.0: 9, 6.5: 3, 11.0: 3, 6.0: 2}`
**非黑配色** — TARGET: `{'#444444': 20, '#222222': 9, '#8E8E93': 5, '#E63946': 5, '#FFFFFF': 3, '#333333': 2}` | WINNER: `{'#8E8E93': 5, '#E63946': 5, '#FFFFFF': 3}`

## 第 11 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 60 | 61 | +1 |
| drawings | 87 | 79 | -8 |
| 彩色 drawings | 45 | 50 | +5 |
| images | 0 | 0 | +0 |
| accent 红色文字数 | 1 | 1 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 40, 'ArialMT': 7, 'MicrosoftYaHei-Bold': 6, 'CourierNewPSMT': 3, 'Arial-Black': 2, 'NSimSun': 2}`
**字体使用 — WINNER**: `{'MicrosoftYaHei': 43, 'ArialMT': 8, 'MicrosoftYaHei-Bold': 6, 'CourierNewPSMT': 2, 'Arial-Black': 2}`

❗ 仅 target 用的字体（winner 缺失）: ['NSimSun']

**主字号** — TARGET top5: `{6.52: 46, 5.25: 4, 6.0: 3, 13.5: 2, 6.38: 2}` | WINNER top5: `{6.5: 49, 5.0: 5, 6.0: 3, 7.0: 2, 13.5: 1}`
**非黑配色** — TARGET: `{'#1A1A1A': 46, '#8E8E93': 5, '#FFFFFF': 3, '#E63946': 1}` | WINNER: `{'#1A1A1A': 46, '#8E8E93': 5, '#FFFFFF': 3, '#E63946': 1}`

## 第 12 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 37 | 42 | +5 |
| drawings | 14 | 17 | +3 |
| 彩色 drawings | 3 | 1 | -2 |
| images | 2 | 2 | +0 |
| accent 红色文字数 | 5 | 5 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 12, 'Arial-Black': 11, 'MicrosoftYaHei-Bold': 6, 'CourierNewPSMT': 3, 'ArialMT': 2, 'NSimSun': 2, 'Arial-BoldMT': 1}`
**字体使用 — WINNER**: `{'MicrosoftYaHei': 14, 'MicrosoftYaHei-Bold': 10, 'ArialMT': 8, 'Arial-Black': 8, 'CourierNewPSMT': 2}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-BoldMT', 'NSimSun']

**主字号** — TARGET top5: `{7.5: 19, 6.75: 7, 6.0: 4, 5.25: 4, 13.5: 2}` | WINNER top5: `{7.0: 27, 5.0: 5, 6.0: 4, 7.5: 3, 6.5: 1}`
**非黑配色** — TARGET: `{'#222222': 10, '#FFFFFF': 6, '#8E8E93': 5, '#E63946': 5}` | WINNER: `{'#FFFFFF': 6, '#8E8E93': 5, '#E63946': 5}`

## 第 13 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 46 | 46 | +0 |
| drawings | 10 | 13 | +3 |
| 彩色 drawings | 5 | 3 | -2 |
| images | 0 | 0 | +0 |
| accent 红色文字数 | 12 | 12 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 18, 'Arial-Black': 13, 'MicrosoftYaHei-Bold': 5, 'ArialMT': 5, 'CourierNewPSMT': 3, 'NSimSun': 2}`
**字体使用 — WINNER**: `{'MicrosoftYaHei': 20, 'MicrosoftYaHei-Bold': 16, 'ArialMT': 6, 'CourierNewPSMT': 2, 'Arial-Black': 2}`

❗ 仅 target 用的字体（winner 缺失）: ['NSimSun']

**主字号** — TARGET top5: `{7.5: 24, 6.0: 11, 5.25: 4, 6.75: 3, 13.5: 2}` | WINNER top5: `{7.0: 23, 6.0: 11, 5.0: 5, 7.5: 3, 6.5: 2}`
**非黑配色** — TARGET: `{'#E63946': 12, '#8E8E93': 5, '#444444': 2, '#333333': 1}` | WINNER: `{'#E63946': 12, '#8E8E93': 5}`

## 第 14 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 59 | 53 | -6 |
| drawings | 57 | 64 | +7 |
| 彩色 drawings | 42 | 50 | +8 |
| images | 1 | 1 | +0 |
| accent 红色文字数 | 4 | 4 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 23, 'ArialMT': 13, 'MicrosoftYaHei-Bold': 11, 'Arial-Black': 4, 'CourierNewPSMT': 3, 'Arial-BoldMT': 3, 'NSimSun': 2}`
**字体使用 — WINNER**: `{'MicrosoftYaHei': 24, 'ArialMT': 14, 'MicrosoftYaHei-Bold': 12, 'CourierNewPSMT': 2, 'Arial-Black': 1}`

❗ 仅 target 用的字体（winner 缺失）: ['Arial-BoldMT', 'NSimSun']

**主字号** — TARGET top5: `{7.5: 23, 6.67: 21, 6.0: 7, 5.25: 4, 13.5: 2}` | WINNER top5: `{6.5: 22, 7.0: 14, 6.0: 7, 5.0: 5, 7.5: 3}`
**非黑配色** — TARGET: `{'#1A1A1A': 20, '#222222': 15, '#8E8E93': 6, '#E63946': 4, '#FFFFFF': 4}` | WINNER: `{'#1A1A1A': 30, '#8E8E93': 5, '#E63946': 4, '#FFFFFF': 4}`

## 第 15 页

| 维度 | TARGET | WINNER | 差异 |
|---|---|---|---|
| text spans | 22 | 22 | +0 |
| drawings | 61 | 56 | -5 |
| 彩色 drawings | 47 | 50 | +3 |
| images | 0 | 0 | +0 |
| accent 红色文字数 | 1 | 1 | +0 |

**字体使用 — TARGET**: `{'MicrosoftYaHei': 11, 'MicrosoftYaHei-Bold': 3, 'CourierNewPSMT': 3, 'ArialMT': 2, 'NSimSun': 2, 'Arial-Black': 1}`
**字体使用 — WINNER**: `{'MicrosoftYaHei': 12, 'MicrosoftYaHei-Bold': 4, 'ArialMT': 3, 'CourierNewPSMT': 2, 'Arial-Black': 1}`

❗ 仅 target 用的字体（winner 缺失）: ['NSimSun']

**主字号** — TARGET top5: `{6.67: 13, 5.25: 4, 13.5: 2, 6.75: 1, 5.62: 1}` | WINNER top5: `{6.5: 13, 5.0: 5, 13.5: 1, 11.0: 1, 7.5: 1}`
**非黑配色** — TARGET: `{'#1A1A1A': 13, '#8E8E93': 5, '#E63946': 1}` | WINNER: `{'#1A1A1A': 12, '#8E8E93': 5, '#E63946': 1, '#FFFFFF': 1}`