import distance
from sentence_transformers import SentenceTransformer as SBert
from sentence_transformers.util import cos_sim

from question_analyse.HanlpAPI import calculate_semantic_similarity

# 文本相似性模型
model = SBert('paraphrase-multilingual-MiniLM-L12-v2')


def calculate_distance(sentence_couple):
    return distance.nlevenshtein(sentence_couple[0], sentence_couple[1])


def hanlp_semantic_similarity(sentence_couple):
    return calculate_semantic_similarity(sentence_couple)


def SBert_semantic_similarity(sentence_couple):
    embeddings1 = model.encode(sentence_couple[0])
    embeddings2 = model.encode(sentence_couple[1])
    cosine_scores = cos_sim(embeddings1, embeddings2)
    return float(cosine_scores)


if __name__ == "__main__":
    sentence = "我是学生"
    sentences = ["我是汕头大学的学生", "我是大学生", "我是学生"]
    sentence_couple = ['年份 汕头大学 专业 类型 科 在 省份 录取 分数 ', '年份 专业 省份 类型 ']
    # print(calculate_distance(sentence, sentences))
    # print(calculate_distance(sentence_couple))
    print(SBert_semantic_similarity(['年份 汕头大学 专业 类型 科 在 省份 录取 分数 ', '年份']))
    print(SBert_semantic_similarity(['年份 汕头大学 专业 类型 科 在 省份 录取 分数 ', '年份 专业 省份 类型 ']))
    print(SBert_semantic_similarity(['年份 汕头大学 专业 类型 科 在 省份 录取 分数 ', '省份 类型 ']))
    print(SBert_semantic_similarity(['年份 汕头大学 专业 类型 科 在 省份 录取 分数 ', '年份 省份 类型 ']))
    # print(hanlp_semantic_similarity(sentence_couple))
