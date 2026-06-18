#!/usr/bin/env python3
"""
紫微斗數排盤計算工具
Zi Wei Dou Shu (Purple Star Astrology) Calculator

簡化版排盤工具，提供基本的紫微斗數命盤計算。
"""

from datetime import datetime, date, timedelta
from typing import Tuple, Dict, List, Optional
import math

# ============================================================
# 基礎數據
# ============================================================

# 天干
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 地支
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 十二宮位名稱
GONG_NAMES = ["命宮", "兄弟宮", "夫妻宮", "子女宮", "財帛宮", "疾厄宮",
              "遷移宮", "交友宮", "事業宮", "田宅宮", "福德宮", "父母宮"]

# 十四主星
ZHUXING = ["紫微", "天機", "太陽", "武曲", "天同", "廉貞", "天府",
           "太陰", "貪狼", "巨門", "天相", "天梁", "七殺", "破軍"]

# 紫微星系 (紫微星位置決定以下星曜位置)
ZIWEI_GROUP = ["紫微", "天機", "太陽", "武曲", "天同", "廉貞"]
# 天府星系
TIANFU_GROUP = ["天府", "太陰", "貪狼", "巨門", "天相", "天梁", "七殺", "破軍"]

# 輔星
FUZHU_STARS = ["左輔", "右弼", "文昌", "文曲", "天魁", "天鉞"]

# 煞星
SHA_STARS = ["擎羊", "陀羅", "火星", "鈴星", "地空", "地劫"]

# 四化星
SIHUA = {
    "甲": {"祿": "廉貞", "權": "破軍", "科": "武曲", "忌": "太陽"},
    "乙": {"祿": "天機", "權": "天梁", "科": "紫微", "忌": "太陰"},
    "丙": {"祿": "天同", "權": "天機", "科": "文昌", "忌": "廉貞"},
    "丁": {"祿": "太陰", "權": "天同", "科": "天機", "忌": "巨門"},
    "戊": {"祿": "貪狼", "權": "太陰", "科": "右弼", "忌": "天機"},
    "己": {"祿": "武曲", "權": "貪狼", "科": "天梁", "忌": "文曲"},
    "庚": {"祿": "太陽", "權": "武曲", "科": "太陰", "忌": "天同"},
    "辛": {"祿": "巨門", "權": "太陽", "科": "文曲", "忌": "文昌"},
    "壬": {"祿": "天梁", "權": "紫微", "科": "左輔", "忌": "武曲"},
    "癸": {"祿": "破軍", "權": "巨門", "科": "太陰", "忌": "貪狼"},
}

# 時辰對照
SHICHEN = {
    23: 0, 0: 0,   # 子時
    1: 1, 2: 1,    # 丑時
    3: 2, 4: 2,    # 寅時
    5: 3, 6: 3,    # 卯時
    7: 4, 8: 4,    # 辰時
    9: 5, 10: 5,   # 巳時
    11: 6, 12: 6,  # 午時
    13: 7, 14: 7,  # 未時
    15: 8, 16: 8,  # 申時
    17: 9, 18: 9,  # 酉時
    19: 10, 20: 10, # 戌時
    21: 11, 22: 11, # 亥時
}

# 農曆數據
YEAR_INFOS = [
    0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,
    0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,
    0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,
    0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,
    0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,
    0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5d0, 0x14573, 0x052d0, 0x0a9a8, 0x0e950, 0x06aa0,
    0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,
    0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b5a0, 0x195a6,
    0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,
    0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x05ac0, 0x0ab60, 0x096d5, 0x092e0,
    0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,
    0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,
    0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,
    0x05aa0, 0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,
    0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0,
    0x14b63, 0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, 0x0ea50, 0x06aa0, 0x1a6c4, 0x0aae0,
    0x092e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4,
    0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0,
    0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160,
    0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0, 0x0d150, 0x0f252,
]

LUNAR_START_DATE = date(1900, 1, 31)


# ============================================================
# 農曆轉換
# ============================================================

def _year_days(year_info: int) -> int:
    days = 29 * 12
    leap_month = year_info & 0xF
    if leap_month:
        days += 29
        if (year_info >> 16) & 1:
            days += 1
    for month in range(1, 13):
        if (year_info >> (16 - month)) & 1:
            days += 1
    return days


def _month_days(year_info: int, month: int, is_leap: bool = False) -> int:
    if is_leap:
        return 30 if (year_info >> 16) & 1 else 29
    return 30 if (year_info >> (16 - month)) & 1 else 29


def gregorian_to_lunar(year: int, month: int, day: int) -> Tuple[int, int, int, bool]:
    """西曆轉農曆"""
    if year < 1900 or year > 2099:
        raise ValueError(f"年份 {year} 超出支援範圍 (1900-2099)")
    
    target_date = date(year, month, day)
    offset = (target_date - LUNAR_START_DATE).days
    
    if offset < 0:
        raise ValueError("日期早於1900年1月31日")
    
    lunar_year = 1900
    year_index = 0
    
    while year_index < len(YEAR_INFOS):
        year_info = YEAR_INFOS[year_index]
        year_days = _year_days(year_info)
        if offset < year_days:
            break
        offset -= year_days
        lunar_year += 1
        year_index += 1
    
    if year_index >= len(YEAR_INFOS):
        raise ValueError("日期超出支援範圍")
    
    year_info = YEAR_INFOS[year_index]
    leap_month = year_info & 0xF
    
    for m in range(1, 13):
        days = _month_days(year_info, m, False)
        if offset < days:
            return (lunar_year, m, offset + 1, False)
        offset -= days
        
        if m == leap_month:
            days = _month_days(year_info, m, True)
            if offset < days:
                return (lunar_year, m, offset + 1, True)
            offset -= days
    
    raise ValueError("日期計算錯誤")


# ============================================================
# 命盤計算
# ============================================================

def get_year_ganzhi(year: int) -> Tuple[int, int]:
    """計算年干支"""
    offset = year - 1984
    gan = offset % 10
    zhi = offset % 12
    return (gan, zhi)


def get_ming_gong(lunar_month: int, hour_index: int) -> int:
    """
    計算命宮位置
    lunar_month: 農曆月份 (1-12)
    hour_index: 時辰索引 (0-11，子時=0)
    返回: 宮位索引 (0-11，對應子丑寅卯...)
    
    計算方法：
    1. 從寅宮順數到出生月份
    2. 從該宮位逆數到出生時辰
    公式簡化為：(寅的索引 + 月 - 1 - 時) % 12 = (1 + 月 - 時) % 12
    為確保結果為正數，使用 (13 + 月 - 時) % 12
    """
    ming_gong = (13 + lunar_month - hour_index) % 12
    return ming_gong


def get_shen_gong(lunar_month: int, hour_index: int) -> int:
    """
    計算身宮位置
    
    計算方法：
    1. 從寅宮順數到出生月份
    2. 從該宮位順數到出生時辰
    公式簡化為：(1 + 月 + 時) % 12
    """
    shen_gong = (1 + lunar_month + hour_index) % 12
    return shen_gong

# 五行局（納音五行局）計算
# 舊版的 WUXING_JU_TABLE 查表數據有誤，已改用傳統納音算法：
#   年干 → 五虎遁定寅宮天干 → 順排至命宮得命宮天干 → 命宮干支查納音 → 五行局

# 六十甲子納音五行（每兩柱共一納音，共三十組，甲子=0 起算）
NAYIN_ELEMENTS = [
    "金", "火", "木", "土", "金", "火", "水", "土", "金", "木",
    "水", "土", "火", "木", "水", "金", "火", "木", "土", "金",
    "火", "水", "土", "金", "木", "水", "土", "火", "木", "水",
]

# 納音五行 → 五行局數
ELEMENT_TO_JU = {"金": 4, "木": 3, "水": 2, "火": 6, "土": 5}

JU_TO_NAME = {2: "水二局", 3: "木三局", 4: "金四局", 5: "土五局", 6: "火六局"}


def _ganzhi_index(gan: int, zhi: int) -> int:
    """由天干(0-9)、地支(0-11)反查六十甲子序號(0-59)"""
    for n in range(60):
        if n % 10 == gan and n % 12 == zhi:
            return n
    raise ValueError(f"無效的干支組合 gan={gan} zhi={zhi}")


def get_nayin_ju(gan: int, zhi: int) -> int:
    """由干支取納音五行局數"""
    return ELEMENT_TO_JU[NAYIN_ELEMENTS[_ganzhi_index(gan, zhi) // 2]]


def get_yin_gong_gan(year_gan: int) -> int:
    """五虎遁：由年干求寅宮天干索引
    甲己→丙, 乙庚→戊, 丙辛→庚, 丁壬→壬, 戊癸→甲"""
    return ((year_gan % 5) * 2 + 2) % 10


def get_wuxing_ju(year_gan: int, ming_gong: int) -> Tuple[str, int]:
    """
    計算五行局
    year_gan: 年干索引 (0-9，甲=0)
    ming_gong: 命宮地支位置 (0-11，子=0)
    返回: (五行局名稱, 局數)

    計算方法：
    1. 根據年干用「五虎遁」確定寅宮天干
    2. 順排天干到命宮，得到命宮天干
    3. 命宮干支組合查納音五行，得五行局
    """
    yin_gan = get_yin_gong_gan(year_gan)
    # 寅為地支索引 2，由寅順數至命宮的步數即天干遞增數
    ming_gan = (yin_gan + (ming_gong - 2)) % 10
    ju = get_nayin_ju(ming_gan, ming_gong)
    return (JU_TO_NAME[ju], ju)


# 紫微星位置表（從 iztro-py 開源庫驗證收集）
# ZIWEI_POS_TABLE[局數][日-1] = 地支索引
# 地支：子=0, 丑=1, 寅=2, ..., 亥=11
ZIWEI_POS_TABLE = {
    2: [1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 0, 0, 1, 1, 2, 2, 3, 3, 4],  # 水二局
    3: [4, 1, 2, 5, 2, 3, 6, 3, 4, 7, 4, 5, 8, 5, 6, 9, 6, 7, 10, 7, 8, 11, 8, 9, 0, 9, 10, 1, 10, 11],  # 木三局
    4: [11, 4, 1, 2, 0, 5, 2, 3, 1, 6, 3, 4, 2, 7, 4, 5, 3, 8, 5, 6, 4, 9, 6, 7, 5, 10, 7, 8, 6, 11],  # 金四局
    5: [6, 11, 4, 1, 2, 7, 0, 5, 2, 3, 8, 1, 6, 3, 4, 9, 2, 7, 4, 5, 10, 3, 8, 5, 6, 11, 4, 9, 6, 7],  # 土五局
    6: [9, 6, 11, 4, 1, 2, 10, 7, 0, 5, 2, 3, 11, 8, 1, 6, 3, 4, 0, 9, 2, 7, 4, 5, 1, 10, 3, 8, 5, 6],  # 火六局
}


def get_ziwei_position(lunar_day: int, ju: int) -> int:
    """
    計算紫微星位置
    lunar_day: 農曆日期 (1-30)
    ju: 五行局數 (2-6)
    返回: 紫微星所在宮位索引 (0-11，子=0)
    
    使用預先計算的對照表，確保與開源庫一致
    """
    if ju not in ZIWEI_POS_TABLE:
        ju = 3  # 預設木三局
    day_index = min(max(lunar_day - 1, 0), 29)  # 確保索引在 0-29 範圍內
    return ZIWEI_POS_TABLE[ju][day_index]


def arrange_ziwei_stars(ziwei_pos: int) -> Dict[int, List[str]]:
    """
    根據紫微星位置安排紫微星系
    """
    stars = {}
    
    # 紫微星系的相對位置
    ziwei_offsets = {
        "紫微": 0,
        "天機": 11,  # 紫微前一宮
        "太陽": 9,   # 紫微前三宮
        "武曲": 8,   # 紫微前四宮
        "天同": 7,   # 紫微前五宮  
        "廉貞": 4,   # 紫微前八宮
    }
    
    for star, offset in ziwei_offsets.items():
        pos = (ziwei_pos + offset) % 12
        if pos not in stars:
            stars[pos] = []
        stars[pos].append(star)
    
    return stars

# 紫微→天府位置對照表（從 iztro-py 驗證）
ZIWEI_TO_TIANFU = {
    0: 4,   # 紫微在子，天府在辰
    1: 3,   # 紫微在丑，天府在卯
    2: 2,   # 紫微在寅，天府在寅
    3: 1,   # 紫微在卯，天府在丑
    4: 0,   # 紫微在辰，天府在子
    5: 11,  # 紫微在巳，天府在亥
    6: 10,  # 紫微在午，天府在戌
    7: 9,   # 紫微在未，天府在酉
    8: 8,   # 紫微在申，天府在申
    9: 7,   # 紫微在酉，天府在未
    10: 6,  # 紫微在戌，天府在午
    11: 5,  # 紫微在亥，天府在巳
}


def arrange_tianfu_stars(ziwei_pos: int) -> Dict[int, List[str]]:
    """
    根據紫微星位置安排天府星系
    使用預先計算的對照表確定天府位置
    """
    stars = {}
    
    # 天府位置（根據對照表）
    tianfu_pos = ZIWEI_TO_TIANFU[ziwei_pos % 12]
    
    # 天府星系的相對位置
    tianfu_offsets = {
        "天府": 0,
        "太陰": 1,
        "貪狼": 2,
        "巨門": 3,
        "天相": 4,
        "天梁": 5,
        "七殺": 6,
        "破軍": 10,
    }
    
    for star, offset in tianfu_offsets.items():
        pos = (tianfu_pos + offset) % 12
        if pos not in stars:
            stars[pos] = []
        stars[pos].append(star)
    
    return stars


def arrange_fuzhu_stars(year_gan: int, year_zhi: int, hour_index: int) -> Dict[int, List[str]]:
    """
    安排輔星位置
    """
    stars = {}
    
    # 左輔：辰順時針數月份
    zuofu_pos = (hour_index + 4) % 12
    # 右弼：戌逆時針數月份
    youbi_pos = (10 - hour_index) % 12
    
    # 文昌：由時辰決定
    wenchang_pos = (10 - hour_index) % 12
    # 文曲：由時辰決定
    wenqu_pos = (4 + hour_index) % 12
    
    # 天魁天鉞：由年干決定（簡化）
    tiankui_pos = (year_gan + 6) % 12
    tianyue_pos = (year_gan + 2) % 12
    
    for pos, star in [(zuofu_pos, "左輔"), (youbi_pos, "右弼"),
                      (wenchang_pos, "文昌"), (wenqu_pos, "文曲"),
                      (tiankui_pos, "天魁"), (tianyue_pos, "天鉞")]:
        if pos not in stars:
            stars[pos] = []
        stars[pos].append(star)
    
    return stars


def arrange_sha_stars(year_zhi: int, hour_index: int) -> Dict[int, List[str]]:
    """
    安排煞星位置
    """
    stars = {}
    
    # 擎羊陀羅：由年干的祿存位置推算（簡化）
    qingyang_pos = (year_zhi + 1) % 12
    tuoluo_pos = (year_zhi - 1) % 12
    
    # 火星鈴星：由年支和時辰決定（簡化）
    huoxing_pos = (year_zhi + hour_index) % 12
    lingxing_pos = (year_zhi - hour_index) % 12
    
    # 地空地劫：由時辰決定（簡化）
    dikong_pos = (11 - hour_index) % 12
    dijie_pos = (hour_index + 11) % 12
    
    for pos, star in [(qingyang_pos, "擎羊"), (tuoluo_pos, "陀羅"),
                      (huoxing_pos, "火星"), (lingxing_pos, "鈴星"),
                      (dikong_pos, "地空"), (dijie_pos, "地劫")]:
        if pos not in stars:
            stars[pos] = []
        stars[pos].append(star)
    
    return stars


def get_sihua(year_gan: int) -> Dict[str, str]:
    """獲取年干的四化"""
    gan_name = TIANGAN[year_gan]
    return SIHUA.get(gan_name, {})


def get_daxian(ming_gong: int, wuxing_ju: int, gender: str, year_yinyang: str) -> List[Dict]:
    """
    計算大限
    ming_gong: 命宮位置
    wuxing_ju: 五行局數
    gender: 性別
    year_yinyang: 年干陰陽
    """
    # 判斷順逆
    if (year_yinyang == "陽" and gender == "男") or (year_yinyang == "陰" and gender == "女"):
        direction = 1  # 順行
    else:
        direction = -1  # 逆行
    
    daxian_list = []
    start_age = wuxing_ju  # 起運年齡，局數即為起運歲數
    
    for i in range(12):
        gong_index = (ming_gong + i * direction) % 12
        age_start = start_age + i * 10
        age_end = age_start + 9
        
        daxian_list.append({
            "宮位": DIZHI[gong_index],
            "年齡": f"{age_start}-{age_end}歲",
        })
    
    return daxian_list[:8]  # 只取前8個大限


# ============================================================
# 真太陽時校正
# ============================================================

def equation_of_time(dt: datetime) -> float:
    """均時差（分鐘），近似公式。
    因地球公轉橢圓軌道與黃赤交角，視太陽時與平太陽時有偏差，約 ±16 分鐘。"""
    n = dt.timetuple().tm_yday
    b = math.radians(360.0 / 365.0 * (n - 81))
    return 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)


def to_true_solar_time(dt: datetime, longitude: float) -> datetime:
    """
    將鐘錶時間（北京時間 UTC+8）校正為真太陽時。
    校正量 = 經度時差 + 均時差
      經度時差 = (出生地經度 - 120) × 4 分鐘（東經為正，120°E 為北京時間基準經線）
      均時差   = equation_of_time(dt)
    例：烏魯木齊約 87.6°E、北京約 116.4°E。
    """
    delta_min = (longitude - 120.0) * 4.0 + equation_of_time(dt)
    return dt + timedelta(minutes=delta_min)


def paipan(year: int, month: int, day: int, hour: int, minute: int = 0,
           gender: str = "男", longitude: Optional[float] = None) -> Dict:
    """
    紫微斗數排盤主函數

    Args:
        year: 西曆年份
        month: 西曆月份
        day: 西曆日期
        hour: 小時 (0-23)
        minute: 分鐘 (0-59)，用於真太陽時校正
        gender: "男" 或 "女"
        longitude: 出生地經度（東經為正，例：北京116.4、烏魯木齊87.6）。
                   提供時自動套用真太陽時校正；不提供則直接用鐘錶時間。

    Returns:
        命盤資訊
    """
    # 0. 真太陽時校正（提供經度時）
    clock_dt = datetime(year, month, day, hour, minute)
    solar_dt = to_true_solar_time(clock_dt, longitude) if longitude is not None else clock_dt

    # 1. 轉換農曆（以校正後日期為準）
    lunar_year, lunar_month, lunar_day, is_leap = gregorian_to_lunar(
        solar_dt.year, solar_dt.month, solar_dt.day)

    # 2. 計算年干支
    year_gan, year_zhi = get_year_ganzhi(lunar_year)

    # 3. 計算時辰（以校正後小時為準）
    hour_index = SHICHEN.get(solar_dt.hour, 0)
    
    # 4. 計算命宮
    ming_gong = get_ming_gong(lunar_month, hour_index)
    
    # 5. 計算身宮
    shen_gong = get_shen_gong(lunar_month, hour_index)
    
    # 6. 計算五行局
    wuxing_name, wuxing_ju = get_wuxing_ju(year_gan, ming_gong)
    
    # 7. 計算紫微星位置
    ziwei_pos = get_ziwei_position(lunar_day, wuxing_ju)
    
    # 8. 安排星曜
    all_stars = {}
    
    # 安排紫微星系
    ziwei_stars = arrange_ziwei_stars(ziwei_pos)
    for pos, stars in ziwei_stars.items():
        if pos not in all_stars:
            all_stars[pos] = {"主星": [], "輔星": [], "煞星": []}
        all_stars[pos]["主星"].extend(stars)
    
    # 安排天府星系
    tianfu_stars = arrange_tianfu_stars(ziwei_pos)
    for pos, stars in tianfu_stars.items():
        if pos not in all_stars:
            all_stars[pos] = {"主星": [], "輔星": [], "煞星": []}
        all_stars[pos]["主星"].extend(stars)
    
    # 安排輔星
    fuzhu_stars = arrange_fuzhu_stars(year_gan, year_zhi, hour_index)
    for pos, stars in fuzhu_stars.items():
        if pos not in all_stars:
            all_stars[pos] = {"主星": [], "輔星": [], "煞星": []}
        all_stars[pos]["輔星"].extend(stars)
    
    # 安排煞星
    sha_stars = arrange_sha_stars(year_zhi, hour_index)
    for pos, stars in sha_stars.items():
        if pos not in all_stars:
            all_stars[pos] = {"主星": [], "輔星": [], "煞星": []}
        all_stars[pos]["煞星"].extend(stars)
    
    # 9. 排列十二宮
    gong_list = []
    for i in range(12):
        gong_pos = (ming_gong - i) % 12
        gong_name = GONG_NAMES[i]
        
        gong_info = {
            "宮位": gong_name,
            "地支": DIZHI[gong_pos],
            "主星": all_stars.get(gong_pos, {}).get("主星", []),
            "輔星": all_stars.get(gong_pos, {}).get("輔星", []),
            "煞星": all_stars.get(gong_pos, {}).get("煞星", []),
        }
        gong_list.append(gong_info)
    
    # 10. 獲取四化
    sihua = get_sihua(year_gan)
    
    # 11. 計算大限
    year_yinyang = "陽" if year_gan % 2 == 0 else "陰"
    daxian = get_daxian(ming_gong, wuxing_ju, gender, year_yinyang)
    
    # 12. 組裝結果
    jiben = {
        "西曆": f"{year}年{month}月{day}日 {hour:02d}:{minute:02d}",
    }
    if longitude is not None:
        jiben["出生經度"] = f"{longitude}°E"
        jiben["真太陽時"] = solar_dt.strftime("%Y-%m-%d %H:%M")
    jiben["農曆"] = f"{lunar_year}年{'閏' if is_leap else ''}{lunar_month}月{lunar_day}日"
    jiben["性別"] = gender
    jiben["年干支"] = f"{TIANGAN[year_gan]}{DIZHI[year_zhi]}年"
    jiben["時辰"] = f"{DIZHI[hour_index]}時"

    result = {
        "基本資訊": jiben,
        "命盤結構": {
            "命宮": f"{DIZHI[ming_gong]}宮",
            "身宮": f"{DIZHI[shen_gong]}宮",
            "五行局": wuxing_name,
        },
        "四化": {
            "化祿": sihua.get("祿", ""),
            "化權": sihua.get("權", ""),
            "化科": sihua.get("科", ""),
            "化忌": sihua.get("忌", ""),
        },
        "十二宮": gong_list,
        "大限": daxian,
    }
    
    return result


def print_result(result: Dict):
    """格式化輸出結果"""
    print("\n" + "=" * 70)
    print("🌟 紫微斗數命盤排列結果")
    print("=" * 70)
    
    print("\n【基本資訊】")
    for key, value in result["基本資訊"].items():
        print(f"  {key}：{value}")
    
    print("\n【命盤結構】")
    for key, value in result["命盤結構"].items():
        print(f"  {key}：{value}")
    
    print("\n【年干四化】")
    sihua = result["四化"]
    print(f"  化祿：{sihua['化祿']}  化權：{sihua['化權']}  化科：{sihua['化科']}  化忌：{sihua['化忌']}")
    
    print("\n【十二宮位】")
    print("  " + "-" * 60)
    for gong in result["十二宮"]:
        zhu = "、".join(gong["主星"]) if gong["主星"] else "（空宮）"
        fu = "、".join(gong["輔星"]) if gong["輔星"] else ""
        sha = "、".join(gong["煞星"]) if gong["煞星"] else ""
        
        print(f"  {gong['宮位']:6} ({gong['地支']}): {zhu}")
        if fu:
            print(f"         輔星: {fu}")
        if sha:
            print(f"         煞星: {sha}")
    print("  " + "-" * 60)
    
    print("\n【大限運程】")
    for dx in result["大限"]:
        print(f"  {dx['年齡']:12} | {dx['宮位']}宮")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="紫微斗數排盤（支援真太陽時校正）",
        epilog="例：python ziwei_calc.py 1993 1 15 18 男 --min 30 --lon 87.6")
    parser.add_argument("year", type=int, help="西曆年")
    parser.add_argument("month", type=int, help="西曆月")
    parser.add_argument("day", type=int, help="西曆日")
    parser.add_argument("hour", type=int, help="小時 (0-23)")
    parser.add_argument("gender", nargs="?", default="男", help="性別 男/女（預設男）")
    parser.add_argument("--min", "--minute", type=int, default=0, dest="minute",
                        help="分鐘 (0-59)，用於真太陽時校正")
    parser.add_argument("--lon", "--longitude", type=float, default=None, dest="longitude",
                        help="出生地經度（東經為正，例：116.4）。提供則套用真太陽時校正")
    args = parser.parse_args()

    result = paipan(args.year, args.month, args.day, args.hour,
                    args.minute, args.gender, args.longitude)
    print_result(result)
