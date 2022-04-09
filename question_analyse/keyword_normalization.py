# -*- coding: utf-8 -*-
"""
@File  : KeywordNormalize.py
@Author: SangYu
@Date  : 2019/3/18 10:35
@Desc  : 关键词正则化
"""

from question_analyse.province_normalization import text_to_province
from question_analyse.time_normalization import text_to_year


# 时间正则化
def time_word_normalize(text: str) -> str:
    year_list = text_to_year(text)
    if year_list:
        return str(year_list[0])
    else:
        return ""


# 地点正则化
def province_word_normalize(text: str) -> str:
    province_list = text_to_province(text)
    # print(province_list)
    if province_list:
        province = province_list[0]
        return province[:-1]
    else:
        return ""


if __name__ == '__main__':
    test_time_word = "今年农历四月初五"
    test_district_word = "我要去哈尔滨吃卤鸭, 我该怎么走?"
    print(time_word_normalize(test_time_word))
    print(province_word_normalize(test_district_word))
