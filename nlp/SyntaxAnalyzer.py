from teanaps.visualization import GraphVisualizer

class SyntaxAnalyzer():  
    def __init__(self):
        None
    
    def syntax(self, word_tagged_pos_list, word_tagged_ner_list):
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
                sa_result.append((name, pos, "UNK", loc))
        return sa_result
    
    def get_sentence_tree(self, sentence, sa_result):
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
        eojeol_list.append(temp_phrase_list)
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
        return gv.draw_sentence_tree(sentence, label_list, edge_list)