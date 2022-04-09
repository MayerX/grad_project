import hanlp


def hanlp_nlp_segment(sentence: str):
    # Hanlp = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)
    tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
    pos = hanlp.load(hanlp.pretrained.pos.PKU_POS_ELECTRA_SMALL)
    majors_dict = build_local_dict("../crwal/data/majors.txt")
    courses_dict = build_local_dict("../crwal/data/courses.txt")
    tok.dict_force = tok.dict_combine = majors_dict + courses_dict
    post_dict = {}
    for major in majors_dict:
        post_dict[major] = "major"
    for course in courses_dict:
        post_dict[course] = "course"
    pos.dict_tags = post_dict
    return tok(sentence), pos(tok(sentence))


def build_local_dict(path):
    local_dict = []
    with open(path, 'r', encoding='UTF-8') as file:
        for line in file.readlines():
            local_dict.append(line.strip("\n"))
    return local_dict


if __name__ == "__main__":
    print(hanlp_nlp_segment("2015年广东省计算机科学与技术理工类招多少人？"))
