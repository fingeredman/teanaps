from teanaps.nlp.Replacers import RegexpReplacer 
from teanaps import configure as con
PLOTLY_USERNAME = con.PLOTLY_USERNAME
PLOTLY_API_KEY = con.PLOTLY_API_KEY

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

import nltk
#nltk.data.path.append("/home/ubuntu/euc-rest-api/euc_api/api/eucalyptus/nltk_data")
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from pykospacing import spacing
from soynlp.utils import DoublespaceLineCorpus
from soynlp.noun import LRNounExtractor_v2

import re
import requests
import json

class SyntaxAnalyzer():  
    def __init__(self):
        self.replacer = RegexpReplacer()      
        self.lemmatizer = WordNetLemmatizer()
        self.set_tagger(con.POS_TAGGER)
        self.user_ner_lexicon = []
        self.train_ner_lexicon = []
    
    def __get_lexicon(self, access_token):
        try:
            url = con.ENTITY_API_URL + "/?access_token=" + str(access_token)
            print("lexicon loading...")
            r = requests.get(url)
            j = json.loads(r.text)
            return j["data"]
        except:
            return {}
       
    def set_ner_lexicon(self, ner_lexicon_list):
        self.user_ner_lexicon += ner_lexicon_list
        
    def train_lexicon(self, document_path):
        sentence_list = DoublespaceLineCorpus(document_path, iter_sent=True)
        compound_extractor = LRNounExtractor_v2(verbose=True)
        compounds = compound_extractor.train_extract(sentence_list)
        p = re.compile("[^a-zA-Z0-9가-힣_]+")
        compound_list = [n for n, score in compounds.items() 
                         if len(p.findall(n)) == 0 and score[0] + score[1] > 5 and len(n) > 2]
        for compound in compound_list:
            self.train_ner_lexicon.append((compound, "UNK"))        
        
    def ner(self, sentence_pos_list, access_token):
        ner_lexicon = self.__get_lexicon(access_token)
        for word, ner_tag in self.user_ner_lexicon:
            if word in ner_lexicon.keys():
                ner_lexicon[word] = [ner_tag] + ner_lexicon[word]
            else:
                ner_lexicon[word] = [ner_tag]
        for word, ner_tag in self.train_ner_lexicon:
            if word not in ner_lexicon.keys():
                ner_lexicon[word] = [ner_tag]
        word_tagged_ner_list = []
        window_size = 5
        compound_pos_list = ["NNG", "NNP"]
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
                    compound_len = loc[-1][1] - loc[0][0] - 1
                    compound_word = ""
                    for w in window:
                        compound_word += w
                    if len(compound_word) < 2:
                        continue
                    if compound_word in ner_lexicon.keys():
                        word_tagged_ner_list.append([compound_word, ner_lexicon[compound_word][0], (loc[0][0], loc[-1][1])])
        return word_tagged_ner_list
    
    def __parse(self, sentence):
        sentence_org = sentence
        if len(sentence) < 195:
            sentence = spacing(sentence)
        word_tagged_pos_list = []
        if self.tagger == "mecab":
            word_tagged_total_list = self.mecab.pos(sentence)
            for word_tagged in word_tagged_total_list:
                word = word_tagged[0]
                if word in con.SKIP_WORD_LIST:
                    continue
                if "+" in word_tagged[1]:
                    pos_tag = word_tagged[1]
                else:
                    pos_tag = con.POS_TAG_MAP[word_tagged[1]]
                tagged_set = (word, pos_tag)
                word_tagged_pos_list.append(tagged_set)
        elif self.tagger == "mecab-ko":
            sentence_tagged = self.mecab_ko.parse(sentence)
            word_tagged_comma_list = [word_tagged.split("\t") for word_tagged in sentence_tagged.split("\n")[:-2]]
            word_tagged_total_list = [(word_tagged[0], word_tagged[1].split(",")) 
                                      for word_tagged in word_tagged_comma_list]
            for word_tagged in word_tagged_total_list:
                word = word_tagged[0]
                if word in con.SKIP_WORD_LIST:
                    continue
                pos_tag = word_tagged[1][0]
                pos_tag_split = word_tagged[1][7]
                if "+" not in pos_tag:
                    pos_tag = con.POS_TAG_MAP[pos_tag]
                    tagged_set = (word, pos_tag)
                    word_tagged_pos_list.append(tagged_set)
                else:
                    tagged_set_list = [(tag_split.split("/")[:2][0], tag_split.split("/")[:2][1]) 
                                       for tag_split in pos_tag_split.split("+")]
                    word_tagged_pos_list.extend(tagged_set_list)
        elif self.tagger == "kkma":
            word_tagged_total_list = self.kkma.pos(sentence)
            for word_tagged in word_tagged_total_list:
                word = word_tagged[0]
                if word in con.SKIP_WORD_LIST:
                    continue
                pos_tag = con.POS_TAG_MAP[word_tagged[1]]
                tagged_set = (word, pos_tag)
                word_tagged_pos_list.append(tagged_set)
        elif self.tagger == "okt":
            word_tagged_total_list = self.okt.pos(sentence)
            for word_tagged in word_tagged_total_list:
                word = word_tagged[0]
                if word in con.SKIP_WORD_LIST:
                    continue
                pos_tag = con.POS_TAG_MAP[word_tagged[1]]
                tagged_set = (word, pos_tag)
                word_tagged_pos_list.append(tagged_set)
        word_tagged_pos_list = self.__get_word_position(sentence_org, word_tagged_pos_list)
        return word_tagged_pos_list
        
    def __get_word_position(self, sentence_org, word_tagged_pos_list):
        content_ = sentence_org
        position = 0
        word_tagged_pos_loc_list = []
        for word, pos in word_tagged_pos_list:
            loc = content_.find(word)
            if loc != -1:
                position += loc
                content_ = content_[loc:]
                start = position
                end = position + len(word)
            else:
                start = 0
                end = 0
            word_tagged_pos_loc_list.append((word, pos, (start, end)))
        return word_tagged_pos_loc_list
        
    def __language_detector(self, sentence):
        len_ko = len(re.sub("[^가-힇]", "", sentence))
        len_en = len(re.sub("[^a-zA-Z]", "", sentence))
        return "ko" if len_ko >= len_en else "en"

    def __iteration_remover(self, sentence):
        pattern_list = [r'(.)\1{5,}', r'(..)\1{5,}', r'(...)\1{5,}']
        for pattern in pattern_list:
            matcher= re.compile(pattern)
            iteration_term_list = [match.group() for match in matcher.finditer(sentence)]
            for iteration_term in iteration_term_list:
                sentence = sentence.replace(iteration_term, 
                                            iteration_term[:pattern.count(".")] + "."*(len(iteration_term)-pattern.count(".")))
        return sentence
    
    def __pos_tagging(self, sentence):
        language = self.__language_detector(sentence)
        sentence = self.__iteration_remover(sentence)
        # Korean
        if language == "ko":
            sentence = sentence.lower()
            word_tagged_pos_list = self.__parse(sentence)
        # English
        else:
            sentence = self.replacer.replace(sentence)
            word_list = word_tokenize(sentence)
            word_tagged_pos_list = nltk.pos_tag(word_list)
            lemmatized_word_list = []
            for word, pos in word_tagged_pos_list:
                if pos[0] in con.LEMMATIZER_POS_MAP.keys():
                    lemmatizer_pos = con.LEMMATIZER_POS_MAP[pos[0]]
                    word = self.lemmatizer.lemmatize(word, lemmatizer_pos)
                if pos in con.POS_TAG_MAP.keys():
                    pos = con.POS_TAG_MAP[pos]
                elif pos in con.SYMBOLS_POS_MAP.keys():
                    pos = con.SYMBOLS_POS_MAP[pos]
                else:
                    pos = "SW"
                lemmatized_word_list.append((word.lower(), pos))
            word_tagged_pos_list = lemmatized_word_list
        return word_tagged_pos_list

    def parse(self, sentence):
        result_list = self.__pos_tagging(sentence)
        return result_list
    
    def set_tagger(self, tagger):
        self.tagger = tagger
        if tagger == "mecab":
            from konlpy.tag import Mecab
            self.mecab = Mecab()
        elif tagger == "mecab-ko":
            import MeCab
            self.mecab_ko = MeCab.Tagger()
        elif tagger == "kkma":
            from konlpy.tag import Kkma
            self.kkma = Kkma()
        elif tagger == "okt":
            from konlpy.tag import Okt
            self.okt = Okt()