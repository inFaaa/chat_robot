import jieba
import jieba.posseg as pseg
from openpyxl import load_workbook
import re


#待完善
weight_dict = {
    "n":2.0,
    'v':1.5,
    'vn':1.5,
    'r':1.0,
    'd':0.4,
    'm':0.3,
}
DEFAULT_WEIGHT = 0.3

SIMILAR_WORD_PATH = './similar_words.txt'

def load_similar_dict(path):
    with open(path,'r',encoding='utf-8') as f:
        data = f.readlines()

    similar_dict = {}
    for line in data:
        temp = line.split('，')
        similar_dict.update({temp[0] : '|'.join(temp[1:])})  #"区别":"不同|差异|差别"
    return similar_dict

similar_dict = load_similar_dict(SIMILAR_WORD_PATH)

def sub_similar_word(string):
    for key in similar_dict.keys():
        if(re.search(similar_dict[key],string)):
            string = re.sub(similar_dict[key], key, string)
    return string


def load_special_words(file_path):
    wb = load_workbook(filename=file_path)
    sheet_first = wb.get_sheet_by_name(wb.get_sheet_names()[0])
    rows = sheet_first.rows
    words = []
    for row in rows:
        words.append(row[0].value)
    return words

def add_to_jieba(pairs):
    for pair in pairs:
        jieba.add_word(pair[0],tag=pair[1])

##################filepath###################
special_words = load_special_words('./new_sheet.xlsx')

def get_entity(string):
    pair = pseg.cut(string)
    word_list = []
    for each in pair:
        if(each.flag=='n'):#直接把名字作为关键词
            word_list.append(each.word)
    return word_list

def get_target_sentenses_index(user_str,example_strs):#进一步选择

    user_str_pos_pair = []
    user_str_words = []
    for i in pseg.cut(user_str):
        if(i.flag in weight_dict):
            if (i.word in special_words):
                user_str_pos_pair.append((i.word, weight_dict[i.flag]+0.5))  # 二元组比如('TCP',1.5)
            else:
                user_str_pos_pair.append((i.word,weight_dict[i.flag]))#二元组比如('TCP',1.5)
        else:
            user_str_pos_pair.append((i.word, DEFAULT_WEIGHT))  # 二元组比如('TCP',1.5)

    #构造用户输入句子的分词列表
    user_str_pos_pair = sorted(user_str_pos_pair,key=lambda x:x[1],reverse=True)
    for pair in user_str_pos_pair:
        user_str_words.append(pair[0])
    # user_str_words中的词是按优先级排好了的

    #所有备选句子的分词列表的列表
    all_example_str_pair = []
    all_example_str_words = []
    for example_str in example_strs:
        one_example_words = []
        one_example_pairs = []
        for i in pseg.cut(example_str):
            if (i.flag in weight_dict):
                if (i.word in special_words):
                    one_example_pairs.append((i.word,weight_dict[i.flag]+0.5))#人为增加权重
                else:
                    one_example_pairs.append((i.word, weight_dict[i.flag]))
            else:
                one_example_pairs.append((i.word, DEFAULT_WEIGHT))

            one_example_words.append(i.word)
        all_example_str_words.append(one_example_words)
        one_example_pairs = sorted(one_example_pairs,key=lambda x:x[1],reverse=True)
        all_example_str_pair.append(one_example_pairs)

    selected_str_index = []#选中项的索引
    not_found_flag = False
    while(len(selected_str_index)==0):#找到为止
        for i in range(len(all_example_str_words)):
            if(set(user_str_words)<=set(all_example_str_words[i])):  #前者是后者的子集
                selected_str_index.append(i)
        if(len(selected_str_index)==0):#此轮寻找未找到
            if(len(user_str_words)>1):
                user_str_words.pop()
            else:
                not_found_flag = True
                break

    if(not_found_flag):
        # TODO: 更科学的报错
        print("Not Found")#出错处理
        return
    else:
        similarity_set = []
        for i in selected_str_index:
            #计算相似度
            up = 0#分子
            for pair in user_str_pos_pair:
                up+=int(str(pair[0]) in all_example_str_words[i])*pair[1]
            up = 2*up

            low = 0
            for pair in user_str_pos_pair:
                low += pair[1]
            for pair in all_example_str_pair[i]:
                low += pair[1]
            similarity_set.append((i,up/low))
        similarity_set = sorted(similarity_set,key=lambda x:x[1],reverse=True)

        if(len(similarity_set)>3):
            return similarity_set[:3]#top3
        else:
            return similarity_set
