# 紫微斗數 Zi Wei Dou Shu

[繁體中文](README.md) | [English](README_EN.md)

紫微斗數（Purple Star Astrology）是中國傳統命理學中最完整、最精密的星命學系統。本專案提供專業的紫微斗數技能，適用於 Claude、ChatGPT、Gemini、DeepSeek 等 AI/LLM。

## 什麼是紫微斗數？

紫微斗數，又稱「紫微星命術」，是以出生的年月日時為基礎，將十四主星及眾多輔煞星安排在十二宮位中，形成獨特的星盤，據此分析人的命運、性格與運勢。

### 核心概念

- **十二宮位**：命宮、兄弟宮、夫妻宮、子女宮、財帛宮、疾厄宮、遷移宮、交友宮、事業宮、田宅宮、福德宮、父母宮
- **十四主星**：紫微、天機、太陽、武曲、天同、廉貞、天府、太陰、貪狼、巨門、天相、天梁、七殺、破軍
- **輔星**：左輔、右弼、文昌、文曲、天魁、天鉞
- **煞星**：擎羊、陀羅、火星、鈴星、地空、地劫
- **四化**：化祿、化權、化科、化忌

### 為什麼使用紫微斗數？

1. **精密分析**：比八字更詳細的命運分析
2. **宮位系統**：清晰的人生各面向分析框架
3. **星曜組合**：豐富的星曜組合變化
4. **運勢預測**：大限、流年精確預測
5. **個性解析**：深入的性格特質分析

## 功能特色

### 排盤功能

- ✅ 十二宮位排列
- ✅ 十四主星定位
- ✅ 輔煞星安排
- ✅ 四化飛星計算
- ✅ 五行局判斷

### 分析功能

- ✅ 命宮主星分析
- ✅ 格局判斷
- ✅ 星曜組合解讀
- ✅ 大限流年推算
- ✅ 運勢預測

### 專項解讀

- ✅ 事業財運分析
- ✅ 婚姻感情分析
- ✅ 健康養生建議
- ✅ 流年運勢預測

## 專案結構

```
ziwei-doushu/
├── SKILL.md                  ← 核心技能指南（必讀）
├── ETHICS.md                 ← 倫理準則
├── README.md                 ← 本文件
├── references/
│   ├── shier-gong.md             ← 十二宮位詳解
│   ├── shisi-zhuixing.md         ← 十四主星詳解
│   ├── fuzhu-xing.md             ← 輔星詳解
│   ├── sha-xing.md               ← 煞星詳解
│   ├── sihua.md                  ← 四化飛星
│   ├── geju.md                   ← 格局分析
│   ├── daxian-liunian.md         ← 大限流年
│   ├── hunyin.md                 ← 婚姻分析
│   ├── shiye-caifu.md            ← 事業財富
│   └── jiankang.md               ← 健康分析
└── scripts/
    └── ziwei_calc.py             ← Python 計算工具
```

## 使用方式

### 作為 AI Skill 安裝

**簡易方式**：在 Claude Code 中貼上此 URL 並說「請安裝這個技能」：

```
https://github.com/your-username/ziwei-doushu
```

**手動安裝**：

```bash
# 個人技能（跨專案使用）
git clone https://github.com/your-username/ziwei-doushu.git ~/.claude/skills/ziwei-doushu

# 或特定專案使用
git clone https://github.com/your-username/ziwei-doushu.git .claude/skills/ziwei-doushu
```

安裝後，使用「紫微」「斗數」「命盤」等關鍵詞即可啟用技能。

### 使用 Python 工具

```bash
# 排盤示例
python scripts/ziwei_calc.py 1990 8 15 14 男

# 以當前時間排盤
python scripts/ziwei_calc.py
```

## 觸發詞

當用戶使用以下詞彙時，技能會自動啟用：

- 紫微斗數、紫微、斗數
- 命盤、排盤、星盤
- 十二宮、命宮、夫妻宮
- 四化、大限、流年
- 紫微星、天機星等星曜名

## 範例對話

**用戶**：幫我排紫微斗數，我是 1990 年 8 月 15 日下午 2 點出生的男性

**AI**：好的，讓我為您排出紫微斗數命盤...

（AI 會根據 SKILL.md 的指南進行排盤和解讀）

## 倫理準則

本技能遵循嚴格的倫理準則：

- **中立客觀**：吉凶並陳，不迎合期望
- **責任界限**：僅供參考，不替代專業諮詢
- **語言規範**：使用「可能」「傾向」等非絕對用語
- **尊重隱私**：未經同意不分析他人命盤
- **心理關懷**：遇到心理脆弱者提供適當支持

詳見 [ETHICS.md](ETHICS.md)

## 相關資源

- **iztro**：輕量級紫微斗數 JavaScript 庫 [https://github.com/SylarLong/iztro](https://github.com/SylarLong/iztro)
- **紫微派**：線上排盤工具 [https://ziwei.pub](https://ziwei.pub)

## 授權

CC BY-NC-SA 4.0

---

> 「命由天造，運由己生。」
>
> 紫微斗數的真諦在於認識自己，把握機遇，創造美好人生。
