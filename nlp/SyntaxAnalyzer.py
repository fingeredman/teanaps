import warnings
warnings.filterwarnings(action='ignore')

from teanaps import configure as con
from teanaps.visualization import GraphVisualizer

class SyntaxAnalyzer():  
    def __init__(self):
        None
    
    def parse(self, word_tagged_pos_list, word_tagged_ner_list):
        sa_result = []
        ner_pos = "NNP"
        word_tagged_ner_list.sort(key=lambda elem: len(elem[0]), reverse=True)
        for name, pos, loc in word_tagged_pos_list:
            is_ner = False
            for ner_name, ner_tag, ner_loc in word_tagged_ner_list:
                if loc[0] >= ner_loc[0] and loc[1] <= ner_loc[1]:
                    if len(sa_result) == 0:
                        if (ner_name, ner_pos, ner_tag, ner_loc) not in sa_result:
                            sa_result.append((ner_name, ner_pos, ner_tag, ner_loc))
                    if sa_result[-1] != (ner_name, ner_pos, ner_tag, ner_loc):
                        if (ner_name, ner_pos, ner_tag, ner_loc) not in sa_result:
                            sa_result.append((ner_name, ner_pos, ner_tag, ner_loc)) 
                    is_ner = True
                    break
            if not is_ner:
                sa_result.append((name, pos, "UN", loc))
                
        # Compound Noun
        max_window_size = 3
        candidate_cnoun_list = []
        cnoun_list = self.__get_cnoun_list()

        for window_size in range(max_window_size, 1, -1):
            for i in range(len(sa_result)-window_size):
                candidate_list = [[word, loc] for word, pos_tag, ner_tag, loc in sa_result[i:i+window_size]]
                candidate_word = ''.join([candidate[0] for candidate in candidate_list])
                if candidate_word in cnoun_list:
                    candidate_cnoun_list.append([candidate_word, (candidate_list[0][1][0], candidate_list[-1][1][1])])
                    
        remove_index_list = []
        for candidate_cnoun in candidate_cnoun_list:
            for i, syntax in enumerate(sa_result):
                word, pos_tag, ner_tag, loc = syntax[0], syntax[1], syntax[2], syntax[3]
                if loc[0] >= candidate_cnoun[1][0] and loc[1] <= candidate_cnoun[1][1]:
                    remove_index_list.append(i)
        remove_index_list.sort(reverse=True)
        for remove_index in remove_index_list:
            # 임시조치
            if remove_index < len(sa_result):
                del sa_result[remove_index]
        for word, loc in candidate_cnoun_list:
            sa_result.append((word, "NNG", "UN", loc))
        sa_result.sort(key=lambda elem: elem[3][0])
        
        # Synonym
        synonym_dict = self.__get_synonym_dict()
        _sa_result = []
        for word, pos_tag, ner_tag, loc in sa_result:
            if word in synonym_dict.keys():
                word = synonym_dict[word]
            _sa_result.append((word, pos_tag, ner_tag, loc))
        sa_result = _sa_result
        return sa_result
    
    def __get_synonym_dict(self):
        synonym_list = open(con.SYNONYM_PATH, encoding="utf-8").read().strip().split("\n")
        synonym_dict = {}
        for synonym in synonym_list:
            for i, word in enumerate(synonym.split("\t")):
                if i == 0:
                    representative_word = word
                synonym_dict[word] = representative_word
        return synonym_dict
    
    def __get_cnoun_list(self):
        cnoun_list = open(con.CNOUN_PATH, encoding="utf-8").read().strip().split("\n")
        return cnoun_list
    
    def get_phrase(self, sentence, sa_result):
        noun_list = ["NNP", "NNG", "NR", "NP", "MM", "XSN", "VA", "VV", "VX"]#, "NNB"]
        josa_list = ["JKS", "JKC", "JKG", "JKO", "JKB", "JKV", "JKQ", "JC", "JX", "EC", "EF", "EP"]
        phrase_list = []
        temp_phrase = []
        if len(sa_result) == 0:
            None
        elif len(sa_result) < 2:
            None
        temp_phrase.append(sa_result[0])
        for index in range(1, len(sa_result)):
            pre_sa = sa_result[index-1]
            sa = sa_result[index]
            pre_pos_tag = pre_sa[1]
            token = sa[0]
            pos_tag = sa[1]
            if pre_pos_tag in noun_list and pos_tag in noun_list:
                temp_phrase.append(sa)
            elif pre_pos_tag in josa_list and pos_tag in josa_list:
                temp_phrase.append(sa)
            elif pre_pos_tag not in noun_list and pos_tag not in noun_list and pre_pos_tag not in josa_list and pos_tag not in josa_list:
                temp_phrase.append(sa)
            else:
                phrase_list.append(temp_phrase)
                temp_phrase = [sa]
            if index == len(sa_result)-1:
                phrase_list.append(temp_phrase)
        temp_phrase_list = []
        eojeol_list = []
        for phrase in phrase_list:
            temp_phrase_list.append(phrase)
            pos_tag = phrase[-1][1][0]
            if pos_tag in ["E", "J"]:
                eojeol_list.append(temp_phrase_list)
                temp_phrase_list = []
        if len(temp_phrase_list) != 0:
            eojeol_list.append(temp_phrase_list)
        result = []
        for eojeol in eojeol_list:
            result.append(sentence[eojeol[0][0][3][0]:eojeol[-1][-1][3][1]])
        return eojeol_list, result
    
    def get_sentence_tree(self, sentence, sa_result):
        eojeol_list, _ = self.get_phrase(sentence, sa_result)
        eojeol_len = len(eojeol_list)
        phrase_len = sum([len(eojeol) for eojeol in eojeol_list])
        eojeol_root = []
        phrase_root = []
        token_root = []
        edge_list = []
        '''
        syntax_dict = {"SUBJECT": [], "ADVERB": [], "OBJECT": [], "PHRASE": [], 
                       "VERB": [], "ADJECTIVE": [],"EC": [], "EF": []}
        '''
        for phrase_list in eojeol_list:
            if phrase_list[-1][-1][1].split("+")[-1] in ["JX", "JKS"]:
                eojeol_type = "SUBJECT"
            elif phrase_list[-1][-1][1].split("+")[-1] in ["JKB"]:
                eojeol_type = "ADVERB"
            elif phrase_list[-1][-1][1].split("+")[-1] in ["JKO"]:
                eojeol_type = "OBJECT"
            elif phrase_list[-1][-1][1].split("+")[-1] in ["JKG"]:
                eojeol_type = "ADJECTIVE"
            elif phrase_list[-1][-1][1].split("+")[-1] in ["JC"]:
                eojeol_type = "PHRASE"
            elif phrase_list[-1][-1][1].split("+")[-1] in ["EC", "EF", "EP", "ETM", "ETN"]:
                if phrase_list[-2][-1][1].split("+")[-1] in ["VV"]:
                    eojeol_type = "VERB"
                elif phrase_list[-2][-1][1].split("+")[-1] in ["VA"]:
                    eojeol_type = "ADJECTIVE"
                else:
                    eojeol_type = "EC"
            else:
                eojeol_type = "EF"
            eojeol_root.append(sentence[phrase_list[0][0][3][0]:phrase_list[-1][-1][3][1]] + "<br>/" + eojeol_type)
            #syntax_dict[eojeol_type].append(phrase_list[:-1])
            edge_list.append((0, len(eojeol_root)))
            for phrase in phrase_list:
                phrase_type = phrase[-1][1][0]
                phrase_root.append(sentence[phrase[0][3][0]:phrase[-1][3][1]] + "<br>/" + phrase_type)
                edge_list.append((len(eojeol_root), eojeol_len+len(phrase_root)))
                for token in phrase:
                    token_root.append(token[0] + "<br>/" + token[1] + "<br>/" + token[2])
                    edge_list.append((eojeol_len+len(phrase_root), eojeol_len+phrase_len+len(token_root)))
        label_list = [sentence+"<br>/SENTENCE"] + eojeol_root + phrase_root + token_root
        return label_list, edge_list#, syntax_dict
    
    def draw_sentence_tree(self, sentence, label_list, edge_list):
        gv = GraphVisualizer()
        gv.set_plotly()
        return gv.draw_sentence_tree(sentence, label_list, edge_list)