from teanaps import configure as con

import re
import requests
import json

class SyntaxAnalyzer():  
    def __init__(self):
        None
    
    def syntax(self, word_tagged_pos_list, word_tagged_ner_list):
        sa_result = []
        last_loc = 0
        word_tagged_ner_list.sort(key=lambda elem: len(elem[0]), reverse=True)
        for name, pos, loc in word_tagged_pos_list:
            is_ner = False
            ner_pos = "NNP"
            for ner_name, ner_tag, ner_loc in word_tagged_ner_list:
                if loc[0] >= ner_loc[0] and loc[1] <= ner_loc[1]:
                    if len(sa_result) == 0:
                        if (ner_name, ner_pos, ner_tag, ner_loc) not in sa_result:
                            sa_result.append((ner_name, ner_pos, ner_tag, ner_loc))
                            is_ner = True
                            break
                    elif sa_result[-1] != (ner_name, ner_pos, ner_tag, ner_loc):
                        if (ner_name, ner_pos, ner_tag, ner_loc) not in sa_result:
                            sa_result.append((ner_name, ner_pos, ner_tag, ner_loc)) 
                            is_ner = True
                            break
                    is_ner = True
            if not is_ner:
                sa_result.append((name, pos, "UN", loc))
        return sa_result