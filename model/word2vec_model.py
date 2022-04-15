from gensim.models import Word2Vec
from sklearn.cluster import KMeans

from model.text_pretreatment import sentence_pretreatment, show_word_cloud


# 构建word2vec模型
def build_word2vec_model(data_path, model_name):
    text_treatment_list = sentence_pretreatment(data_path)
    word2vec_model = Word2Vec(text_treatment_list, vector_size=200, window=15)
    word2vec_model.init_sims(replace=True)
    word2vec_model.save("{}.model".format(model_name))
    word2vec_model.wv.save_word2vec_format('{}.txt'.format(model_name), binary=False)
    return word2vec_model


# 基于模型进行Kmeans聚类
def Kmeans_cluster(model_path):
    model = Word2Vec.load(model_path)
    keys = model.wv.index_to_key
    # print(keys)
    word_vector = []
    for key in keys:
        word_vector.append(model.wv[key])

    classCount = 7
    km_cluster = KMeans(n_clusters=classCount)
    s = km_cluster.fit(word_vector)

    labels = km_cluster.labels_

    classCollects = {}
    for i in range(len(keys)):
        # print(list(classCollects.keys()))

        if labels[i] in list(classCollects.keys()):
            # print('-----------------')
            classCollects[labels[i]].append(list(keys)[i])
        else:
            classCollects = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        # print('0类：', classCollects[0])
        # print('1类：', classCollects[1])
        # print('2类：', classCollects[2])
        # print('3类：', classCollects[3])
        # print('4类：', classCollects[4])
        # print('5类：', classCollects[5])
        # print('6类：', classCollects[6])

    for count in range(classCount):
        temp = ''
        for word in classCollects.get(count):
            temp += word + ' '
        show_word_cloud(temp[:-1], '{}_word_cloud.jpg'.format(count))

    return classCollects


if __name__ == '__main__':
    build_word2vec_model('data/question_answer.csv', 'word2vec_model')
    Kmeans_cluster('word2vec_model.model')
