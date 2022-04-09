# -*- coding: utf-8 -*-
"""
@File  : LocationNER.py
@Author: SangYu
@Date  : 2019/3/28 20:38
@Desc  : 地点词识别
"""
import json
import os

# from HanLP.HanLPTest import hanlp_nlp_segmentor
from HanlpAPI import hanlp_nlp_segment


# 加载行政区划json文件
def load_location():
    os.chdir(os.path.split(os.path.realpath(__file__))[0])
    path = "Area/province_city.json"
    with open(path, "r", encoding="utf-8") as load_f:
        load_dict = json.load(load_f)
    # 所有省
    province_dict = {}
    for province in load_dict:
        province_dict[province["code"][:2]] = province["name"]
    # for index in range(len(load_dict)):
    #     province_dict[load_dict[index]["code"][:2]] = load_dict[index]["name"]
    # 所有市
    city_dict = {}
    for province in load_dict[:-3]:
        if len(province["city"]) == 1:
            city_dict[province["code"]] = province["name"]
            continue
        for city in province["city"]:
            city_dict[city["code"]] = city["name"]
    # for key in city_dict:
    #     print(key + city_dict[key])
    return province_dict, city_dict


def province_normalize(msg: str) -> str:
    """
    省份的正则化
    :param msg: 输入地点词
    :return: 输出省份
    """
    sub_word = ["省", "市"]
    for sw in sub_word:
        msg = msg.replace(sw, "")
    province_dict, city_dict = load_location()
    # 省
    for province in province_dict:
        if msg in province_dict[province]:
            return province_dict[province]
    # 市
    city_id = 0
    for city in city_dict:
        if msg in city_dict[city]:
            city_id = city
            break
    if city_id != 0:
        return province_dict[city_id[:2]]
    else:
        return ""


def location_extract(text: str) -> list:
    """
    使用hanlp分词，提取带有地点词性的词
    :param text:含有地点词的文本
    :return:时间词列表
    """
    location_res = []
    # print("分词结果"+str(hanlp_nlp_segmentor(text)))
    words, natures = hanlp_nlp_segment(text)
    for seg_index in range(len(words)):
        if natures[seg_index] in ["ns", "nr"]:
            location_res.append(words[seg_index])
    return location_res


def text_to_province(text: str) -> list:
    """
    输入文本，返回文本中的地点列表
    :param text: 文本
    :return: 地点列表
    """
    if text == "":
        return []
    location_res = location_extract(text)
    return [province_normalize(msg) for msg in location_res]


if __name__ == '__main__':
    # pro_dict, city_dict = load_location()
    # print(len(pro_dict))
    # print(pro_dict)
    # print(len(city_dict))
    # for key in city_dict:
    #     print(city_dict[key])
    texts = ["广东省", "广东省中山市", "中山市",
             "中山", "广东汕头", "汕头"]
    for text in texts:
        location_list = text_to_province(text)
        print(location_list)
