from teanaps.nlp import Processing
from teanaps import configure as con
PLOTLY_USERNAME = con.PLOTLY_USERNAME
PLOTLY_API_KEY = con.PLOTLY_API_KEY

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class MorphologicalAnalyzer():  
    def __init__(self):
        self.processing = Processing()
        self.lemmatizer = WordNetLemmatizer()
        self.set_tagger(con.POS_TAGGER)
        self.ner_lexicon = {}
    
    def parse(self, sentence):
        sentence_org = sentence
        language = self.processing.language_detector(sentence)
        sentence = self.processing.iteration_remover(sentence)
        # Korean
        if language == "ko":
            #sentence = sentence.lower()
            word_tagged_pos_list = self.__parse(sentence)
        # English
        else:
            sentence = sentence.lower()
            sentence = self.processing.replacer(sentence)
            sentence_org = sentence
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
                elif word == "be":
                    pos = "JKS"
                else:
                    pos = "UN"
                lemmatized_word_list.append((word.lower(), pos))
            word_tagged_pos_list = lemmatized_word_list
            word_tagged_pos_list = self.processing.get_token_position(sentence_org, word_tagged_pos_list)
        return word_tagged_pos_list
    
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
            
    def __parse(self, sentence):
        sentence_org = sentence
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
                #word = str(word_tagged[0])
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
        word_tagged_pos_list = self.processing.get_token_position(sentence_org, word_tagged_pos_list)
        return word_tagged_pos_list