from teanaps import configure as con
PLOTLY_USERNAME = con.PLOTLY_USERNAME
PLOTLY_API_KEY = con.PLOTLY_API_KEY

from soynlp.utils import DoublespaceLineCorpus
from soynlp.noun import LRNounExtractor_v2

import re
import requests
import json

class NamedEntityTagger():  
    def __init__(self):
        self.ner_lexicon = {}
    
    def ner(self, sentence_pos_list):
        word_tagged_ner_list = []
        window_size = 5
        compound_pos_list = ["NNG", "NNP", "XSV+EC+JKS"]
        word_list = [w[0] for w in sentence_pos_list]
        pos_list = [w[1] for w in sentence_pos_list]
        loc_list = [w[2] for w in sentence_pos_list]
        for index in range(len(word_list)):
            for size in range(window_size+1):
                window = word_list[index:index+size+1]
                pos = pos_list[index:index+size+1]
                loc = loc_list[index:index+size+1]
                is_compound = True
                for p in pos:
                    if p not in compound_pos_list:
                        is_compound = False
                        break
                if not is_compound:
                    continue
                else:
                    compound_word = ""
                    for w in window:
                        compound_word += w
                    if len(compound_word) < 2:
                        continue
                    if compound_word in self.ner_lexicon.keys():
                        word_tagged_ner_list.append((compound_word, self.ner_lexicon[compound_word][0], (loc[0][0], loc[-1][1])))
        return word_tagged_ner_list
    
    def set_ner_lexicon(self, access_token="", ner_lexicon_list=[]):
        if access_token == "":
            None
        else:
            self.ner_lexicon = self.__get_lexicon(access_token)
        for word, ner_tag in ner_lexicon_list:
            if word in self.ner_lexicon.keys():
                self.ner_lexicon[word] = [ner_tag] + self.ner_lexicon[word]
            else:
                self.ner_lexicon[word] = [ner_tag]
                
    def train_lexicon(self, document_path):
        sentence_list = DoublespaceLineCorpus(document_path, iter_sent=True)
        compound_extractor = LRNounExtractor_v2(verbose=True)
        compounds = compound_extractor.train_extract(sentence_list)
        p = re.compile("[^a-zA-Z0-9가-힣_]+")
        compound_list = [n for n, score in compounds.items() 
                         if len(p.findall(n)) == 0 and score[0] + score[1] > 5 and len(n) > 2]
        train_ner_lexicon = []
        for compound in compound_list:
            train_ner_lexicon.append((compound, "UNK")) 
        for word, ner_tag in train_ner_lexicon:
            if word not in self.ner_lexicon.keys():
                self.ner_lexicon[word] = [ner_tag]
    
    def __get_lexicon(self, access_token):
        try:
            url = con.ENTITY_API_URL
            print("lexicon loading...")
            data = {"access_token": access_token}
            r = requests.post(url, data=data)
            j = json.loads(r.text)
            print("done.")
            return j["result"]
        except:
            print("failed.")
            return {}