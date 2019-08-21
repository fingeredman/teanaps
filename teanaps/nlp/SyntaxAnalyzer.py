from teanaps.nlp.Replacers import RegexpReplacer 
from teanaps import configure as con
PLOTLY_USERNAME = con.PLOTLY_USERNAME
PLOTLY_API_KEY = con.PLOTLY_API_KEY

import nltk
#nltk.data.path.append("/home/ubuntu/euc-rest-api/euc_api/api/eucalyptus/nltk_data")
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

#import MeCab

import re

class SyntaxAnalyzer():  
    def __init__(self):
        self.replacer = RegexpReplacer()      
        self.lemmatizer = WordNetLemmatizer()
        self.set_tagger("mecab")
    
    def __parse(self, sentence):
        word_tagged_pos_list = []
        if self.tagger == "mecab":
            sentence_tagged = self.mecab.parse(sentence)
            word_tagged_comma_list = [word_tagged.split("\t") for word_tagged in sentence_tagged.split("\n")[:-2]]
            word_tagged_total_list = [(word_tagged[0], word_tagged[1].split(",")) for word_tagged in word_tagged_comma_list]
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
                    tagged_set_list = [(tag_split.split("/")[:2][0], tag_split.split("/")[:2][1]) for tag_split in pos_tag_split.split("+")]
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
        return word_tagged_pos_list
        
    def __language_detector(self, sentence):
        len_ko = len(re.sub("[^가-힇]", "", sentence))
        len_en = len(re.sub("[^a-zA-Z]", "", sentence))
        return "ko" if len_ko >= len_en else "en"

    def __iteration_remover(self, sentence):
        pattern_list = [r'(.)\1+', r'(..)\1+', r'(...)\1+']
        for pattern in pattern_list:
            matcher= re.compile(pattern)
            iteration_term_list = [match.group() for match in matcher.finditer(sentence)]
            for iteration_term in iteration_term_list:
                sentence = sentence.replace(iteration_term, iteration_term[:pattern.count(".")])
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
            import MeCab
            self.mecab = MeCab.Tagger()
        elif tagger == "kkma":
            from konlpy.tag import Kkma
            self.kkma = Kkma()
        elif tagger == "okt":
            from konlpy.tag import Okt
            self.okt = Okt()