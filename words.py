import jieba
import re
import matplotlib.pyplot as plt
import networkx as nx


def move_stopwords(sentence_list, stopwords_list):
    """去除停用词"""
    out_list = []
    for word in sentence_list:
        if word not in stopwords_list:
            if word != '\t':
                out_list.append(word)
    return out_list


def check_chinese(check_str):
    """判断一个字符串是否为中文"""
    for ch in check_str:
        if ch < u'\u4e00' or ch > u'\u9fff':
            return False
    return True


# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

s = [line.strip() for line in open('chinese_dict.txt').readlines()]  # 中文词典
words = [i for i in s if i != '']  # 去除空行
stopwords = [line.strip() for line in open('ChineseStopWords.txt').readlines()]  # 停用词列表
remove_chars = '[·’!"\#$%&\'()＃！（）*+,-./｜:;<=>?\@，：?￥★、…．＞【】［］〈〉《》？“”‘’\[\\]^_`{|}~]+'  # 标点符号

kk = 25
G = nx.DiGraph()  # 有向图
for i in words:
    key = re.findall('【(.+?)】', i)  # 键，词语
    value = i.split('】')  # 值，解释
    if key:
        new_value = re.sub(remove_chars, "", value[1])  # 去除特殊符号
        value_separate = jieba.cut(new_value.strip())  # jieba分词，精确模式
        value_separate = move_stopwords(value_separate, stopwords)  # 去除停用词
        for v in value_separate:  # 构建网络
            if check_chinese(v):  # 中文字符串
                G.add_edge(key[0], v)  # 词语 分层后的解释
G.remove_edges_from(nx.selfloop_edges(G))  # 移除自环

subgraph = nx.k_shell(G)  # k_shell算法剥离节点
print("k_shell:")
basic_word = []  # 基本词集合
degree = nx.degree(subgraph)  # 节点的度
degree_sort = sorted(degree, key=lambda x: x[1], reverse=True)
for i in range(len(degree_sort)):
    if i >= kk:
        break
    basic_word.append(degree_sort[i][0])
print(basic_word)

print("page rank:")
basic_word = []  # 基本词集合
pagerank_res = nx.pagerank(G)  # pagerank 评价
pagerank_res = sorted(pagerank_res.items(), key=lambda kv: kv[1], reverse=True)
for i in range(len(pagerank_res)):
    if i >= kk:
        break
    basic_word.append(pagerank_res[i][0])
print(basic_word)

# basic_word = []  # 基本词集合
# all_article = "".join(words)  # 将所有的文本整合为一个大文本
# keywords = textrank(all_article, topK=kk, withWeight=True)
# print("text rank:")
# for word, weight in keywords:
#     basic_word.append(word)
# print(basic_word)
