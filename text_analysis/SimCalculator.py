from teanaps import configure as con

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import manhattan_distances

class SimCalculator():  
    def __init__(self):
        None
        
    def jaso_similarity(self, sim_type, string_1, string_2):
        jaso_result_1 = self.__jaso_parse(string_1)
        jaso_result_2 = self.__jaso_parse(string_2) 
        jaso_list_1 = jaso_result_1["jaso_list"]
        jaso_list_2 = jaso_result_2["jaso_list"]
        dence_jaso_list_1 = jaso_result_1["dence_jaso_list"]
        dence_jaso_list_2 = jaso_result_2["dence_jaso_list"]
        _dence_jaso_list_1 = []
        _dence_jaso_list_2 = []
        for dence_jaso_1, dence_jaso_2 in zip(dence_jaso_list_1, dence_jaso_list_2):
            if dence_jaso_1+dence_jaso_1 != 0:
                _dence_jaso_list_1.append(dence_jaso_1)
                _dence_jaso_list_2.append(dence_jaso_2)
        if sim_type == "jacard":
            item_set1 = set(jaso_list_1)
            item_set2 = set(jaso_list_2)
            child = len(item_set1 & item_set2)
            parent = len(item_set1 | item_set2)
            sim = child / parent
        elif sim_type == "cosine":
            sim = cosine_similarity([_dence_jaso_list_1], [_dence_jaso_list_2])[0][0]
        elif sim_type == "euclidean":
            sim = euclidean_distances([_dence_jaso_list_1], [_dence_jaso_list_2])[0][0]
        elif sim_type == "manhattan":
            sim = manhattan_distances([_dence_jaso_list_1], [_dence_jaso_list_2])[0][0]
        return sim

    def char_similarity(self, sim_type, string_1, string_2):
        char_list = []
        for char in string_1+string_2:
            if char not in char_list:
                char_list.append(char)
        char_index_list_1 = [0 for i in char_list]
        char_index_list_2 = [0 for i in char_list]
        for char in string_1:
            char_index_list_1[char_list.index(char)] += 1
        for char in string_2:
            char_index_list_2[char_list.index(char)] += 1
        if sim_type == "jacard":
            item_set1 = set(jaso_list_1)
            item_set2 = set(jaso_list_2)
            child = len(item_set1 & item_set2)
            parent = len(item_set1 | item_set2)
            sim = child / parent
        elif sim_type == "cosine":
            sim = cosine_similarity([char_index_list_1], [char_index_list_2])[0][0]
        elif sim_type == "euclidean":
            sim = euclidean_distances([char_index_list_1], [char_index_list_2])[0][0]
        elif sim_type == "manhattan":
            sim = manhattan_distances([char_index_list_1], [char_index_list_2])[0][0]
        return sim
    
    def __jaso_parse(self, string):
        CHO_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 
                    'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        JUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 
                     'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
        JONG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 
                     'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 
                     'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        jaso_list = []
        jaso_index_list = []
        for char in string.strip():
            if '가' <= char <= '힣':
                cho = (ord(char) - ord('가')) // 588
                jung = ((ord(char) - ord('가')) - (588*cho)) // 28
                jong = (ord(char) - ord('가')) - (588*cho) - 28 * jung
                jaso_list += [CHO_LIST[cho], JUNG_LIST[jung], JONG_LIST[jong]]
                jaso_index_list += [cho, len(CHO_LIST)+jung, len(CHO_LIST)+len(JUNG_LIST)+jong]
            else:
                jaso_list += [-1]
                jaso_index_list += [-1]
        dence_jaso_list = [0 for i in range(len(CHO_LIST)+len(JUNG_LIST)+len(JONG_LIST))]
        for l in jaso_index_list:
            dence_jaso_list[l] += 1
        return {"jaso_list": jaso_list, "jaso_index_list": jaso_index_list, "dence_jaso_list": dence_jaso_list}