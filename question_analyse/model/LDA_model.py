import gensim
import jieba
import numpy as np
import pandas as pd
from gensim import corpora, models

doc1 = "从海南、安徽、上海等省市的互联网医院管理规定来看，关于复诊、医生执业要求，虽然都在国家卫健委文件的框架之内，但各地形成了不同的细化版本。相关负责人认为，在《意见》指导下，未来互联网医院可能会在审批、医生执业、互联网诊疗科目范围、服务流程等方面有更明确的界定；行业标准的补位和监管政策的统一，能在一定程度上改善目前市场某些机构和服务参差不齐的情况，有利于行业更规范、更健康发展。尽管文件中“全国统一的互联网医疗审批标准”这一表述可能包含很多方面，可能是准入标准，可能是审批流程，也可能是对不同主体的开放程度，无论是包含哪些方面，能做到最大程度的统一，就能促进行业的进一步规范。"
doc2 = "近年来，农业机械化已经取得了长足的进步，包括整地，播种，采收等等工作都可以通过机械来完成，大大的解放了劳动力。在此基础上，农业机械正朝着无人操作的全自动化方向发展，包括利用GPS技术和感应技术的无人驾驶除草机，喷药机，还有结合仿生学的果实采摘机器人。很多公司已经投入了大量的资金和技术努力实现作物生产过程中全面的机器人操作。可以想象，未来的农业，再也不需要人们在极端的环境条件下挥汗如雨，辛勤劳作。采用机器人，让他们按照设定好的程序完成指定的任务，不仅能够节约人工成本，还能够突破时间的限制，实现24小时作业，同时更能够达到精准的操作，保证产品的一致性。"
doc3 = "在这个特殊时期，热身赛也有特殊的意义。CBA早已恢复正常，而美国由于大环境糟糕，现在还只能试水热身赛。无论如何，总算迈出了第一步。詹姆斯已经迫不及待，“开工吧，今天重返赛场，我已经等不及了，这只是一场热身赛，但对于我而言，这场比赛的意义不止于此，要时刻保持冠军心态。”詹姆斯写道。开场后，两队大举对攻，防守都比较松，完全是热身赛的架势。两队的命中率也都很高，特别是独行侠首发的小库里，三分球连连命中。前几分钟，独行侠弹无虚发，两队得分很快就达到两位数。不过独行侠提前变阵，换上了“大杀器”马扬诺维奇和巴里亚，命中率略有下降，而湖人继续猛攻。韦特斯投中本节的压哨三分，湖人以29-22结束首节。"
doc4 = "当前医疗的问题仍然是医疗资源分布不均带来的‘看病贵、看病难’以及分级诊疗的切实落实。”39互联网医院相关负责人称，“互联网医疗产品和平台能解决这些问题，能带来根本性的改变。对此，中国社科院经济研究所公共政策研究中心主任朱恒鹏则建议，放开处方药的网上销售；放开医生网上诊断，患者在网上获取医生的处方后能在线买药；开放医保账户针对医生网上诊疗费用的支付，让医生可以从网上收取诊疗费。同时，由于处方在网上公开，极大强化了个人声誉，让医生更重医德不贪小利。"
content = [doc1, doc2, doc3, doc4]

# 分词
content_S = []
for line in content:
    current_segment = [w for w in jieba.cut(line) if len(w) > 1]  # 分词并去除单字词
    if len(current_segment) > 1 and current_segment != '\r\t':
        content_S.append(current_segment)
# 分词结果转为DataFrame
df_content = pd.DataFrame({'content_S': content_S})

# 停用词加载
stopwords = pd.read_table('stop_words.txt', names=['stopword'], quoting=3)


# 去除停用词
def drop_stopwords(contents, stopwords):
    contents_clean = []
    all_words = []
    for line in contents:
        line_clean = []
        for word in line:
            if word in stopwords:
                continue
            line_clean.append(word)
            all_words.append(word)
        contents_clean.append(line_clean)
    return contents_clean, all_words


contents = df_content.content_S.values.tolist()
stopwords = stopwords.stopword.values.tolist()
# contents_clean存储的是一个文本处理结果一个数组，all_words是将所有文本处理结果存储为1个数组
contents_clean, all_words = drop_stopwords(contents, stopwords)

# 处理后的结果转化为DataFrame
df_content = pd.DataFrame({'contents_clean': contents_clean})  # 文本处理结果
df_all_words = pd.DataFrame({'all_words': all_words})  # 语料词典

# 统计语料词典中的词出现频率
# words_count = df_all_words.groupby(by=['all_words'])['all_words'].agg({'count': np.size})
# words_count = words_count.reset_index().sort_values(by=['count'], ascending=False)  # 降序
words_count = df_all_words.groupby('all_words').agg(
    count=pd.NamedAgg(column='all_words', aggfunc=np.size)).reset_index().sort_values(by='count', ascending=False)

dictionary = corpora.Dictionary(contents_clean)
corpus = [dictionary.doc2bow(sentence) for sentence in contents_clean]
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=3, random_state=3)

print(lda.print_topics(num_topics=3, num_words=3))
# 预测文本的主题
for e, values in enumerate(lda.inference(corpus)[0]):
    print(content[e])
    for ee, value in enumerate(values):
        print('\t主题%d推断值%.2f' % (ee, value))
