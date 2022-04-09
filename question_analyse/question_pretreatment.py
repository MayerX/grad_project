from HanlpAPI import hanlp_nlp_segment


# 对问句进行hanlp处理
def question_segment(sentence: str):
    return hanlp_nlp_segment(sentence)


def match_question_template(question_segment_list):

    pass
