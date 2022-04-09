import distance


def calculate_distance(sentence1: str, sentences2: list):
    res = []
    for index, sentence in enumerate(sentences2):
        res.append((distance.nlevenshtein(sentence1, sentence), index, sentence))
    return res


if __name__ == "__main__":
    sentence = "我是学生"
    sentences = ["我是汕头大学的学生", "我是大学生", "我是学生"]
    print(calculate_distance(sentence, sentences))