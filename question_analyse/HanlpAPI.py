import hanlp

# 分词模型
tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
# 词性标注模型
pos = hanlp.load(hanlp.pretrained.pos.PKU_POS_ELECTRA_SMALL)


# hanlp分词且词性标注
def hanlp_nlp_segment(sentence: str):
    # Hanlp = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)
    majors_dict = build_local_dict("../data/dict/majors.txt")
    courses_dict = build_local_dict("../data/dict/courses.txt")
    # school_dict = build_local_dict("../data/dict/school.txt")
    tok.dict_force = tok.dict_combine = majors_dict + courses_dict
    post_dict = {}
    for major in majors_dict:
        post_dict[major] = "major"
    for course in courses_dict:
        post_dict[course] = "course"
    # for school in school_dict:
    #     post_dict[school] = "school"
    pos.dict_tags = post_dict
    return tok(sentence), pos(tok(sentence))


# 构造自定义字典
def build_local_dict(path):
    local_dict = []
    with open(path, 'r', encoding='UTF-8') as file:
        for line in file.readlines():
            local_dict.append(line.strip("\n"))
    return local_dict


# 文本相似度计算
def calculate_semantic_similarity(sentence_couple):
    sts = hanlp.load(hanlp.pretrained.sts.STS_ELECTRA_BASE_ZH)
    return sts(sentence_couple)


if __name__ == "__main__":
    # print(hanlp_nlp_segment("2017汕大计算机科学与技术理工类在广东省招多少人？"))
    print(calculate_semantic_similarity(['年份汕头大学专业类型科在省份录取分数', '年份专业省份类型']))
