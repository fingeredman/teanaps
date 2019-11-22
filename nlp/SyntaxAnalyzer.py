from teanaps.nlp import RegexpReplacer 
from teanaps import configure as con
PLOTLY_USERNAME = con.PLOTLY_USERNAME
PLOTLY_API_KEY = con.PLOTLY_API_KEY

import plotly 
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.figure_factory as ff
from plotly import tools
plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)
plotly.tools.set_config_file(world_readable=False, sharing='private')
init_notebook_mode(connected=True)

from IPython.display import display

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
        self.ner_lexicon = {}
    
    def syntax(self, word_tagged_pos_list, word_tagged_ner_list):
        sa_result = []
        last_loc = 0
        word_tagged_ner_list.sort(key=lambda elem: len(elem[0]), reverse=True)
        for name, pos, loc in word_tagged_pos_list:
            is_ner = False
            for ner_name, ner_tag, ner_loc in word_tagged_ner_list:
                if loc[0] >= ner_loc[0] and loc[1] <= ner_loc[1]:
                    if len(sa_result) == 0:
                        sa_result.append((ner_name, pos, ner_tag, ner_loc))
                    elif sa_result[-1] != (ner_name, pos, ner_tag, ner_loc):
                        sa_result.append((ner_name, pos, ner_tag, ner_loc))
                    is_ner = True
                    break
            if not is_ner:
                sa_result.append((name, pos, "UN", loc))
        return sa_result
        
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
                    compound_len = loc[-1][1] - loc[0][0] - 1
                    compound_word = ""
                    for w in window:
                        compound_word += w
                    if len(compound_word) < 2:
                        continue
                    if compound_word in self.ner_lexicon.keys():
                        word_tagged_ner_list.append((compound_word, self.ner_lexicon[compound_word][0], (loc[0][0], loc[-1][1])))
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
        sentence_org = sentence
        language = self.__language_detector(sentence)
        sentence = self.__iteration_remover(sentence)
        # Korean
        if language == "ko":
            sentence = sentence.lower()
            word_tagged_pos_list = self.__parse(sentence)
        # English
        else:
            sentence = self.replacer.replace(sentence)
            sentence = sentence.lower()
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
                else:
                    pos = "SW"
                lemmatized_word_list.append((word.lower(), pos))
            word_tagged_pos_list = lemmatized_word_list
            word_tagged_pos_list = self.__get_word_position(sentence_org, word_tagged_pos_list)
        return word_tagged_pos_list
    
    def set_plotly(self):
        import IPython
        display(IPython.core.display.HTML('''
            <script src="/static/components/requirejs/require.js"></script>
            <script>
              requirejs.config({
                paths: {
                  base: '/static/base',
                  plotly: 'https://cdn.plot.ly/plotly-latest.min.js?noext',
                },
              });
            </script>
            '''))
        
    def get_tag_evaluation_graph(self, tag_evaluation_result):
        tag_name_list = ['형태소단위', '어절단위', '명사추출']
        precision_list = [tag_evaluation_result["precision_total"], 
                          tag_evaluation_result["precision_phrase"], 
                          tag_evaluation_result["precision_noun"]]
        recall_list = [tag_evaluation_result["recall_total"], 
                       tag_evaluation_result["recall_phrase"], 
                       tag_evaluation_result["recall_noun"]]
        f1_score_list = [tag_evaluation_result["f1_score_total"], 
                         tag_evaluation_result["f1_score_phrase"], 
                         tag_evaluation_result["f1_score_noun"]]
        trace1 = go.Bar(
            x=tag_name_list,
            y=precision_list,
            name='Precision'
        )
        trace2 = go.Bar(
            x=tag_name_list,
            y=recall_list,
            name='Recall'
        )
        trace3 = go.Bar(
            x=tag_name_list,
            y=f1_score_list,
            name='F1-score'
        )

        data = [trace1, trace2, trace3]
        layout = go.Layout(
            barmode='group',
            title='Tagging Evaluation Graph',
            xaxis=dict(
                title='Evaluation Items',
                titlefont=dict(
                    size=10,
                    color='black'
                ),
                showticklabels=True,
                #tickangle=-45,
                tickfont=dict(
                    size=10,
                    color='black'
                ),
                exponentformat='e',
                showexponent='all'
            ),
            yaxis=dict(
                title='Result',
                #nticks=4,
                range=[0, 100],
                titlefont=dict(
                    size=10,
                    color='black'
                ),
                showticklabels=True,
                tickangle=0,
                tickfont=dict(
                    size=10,
                    color='black'
                ),
                exponentformat='e',
                showexponent='all',
                #overlaying='y',
            ),
        )
        fig = go.Figure(data=data, layout=layout)
        return iplot(fig, filename='grouped-bar')
        
    def tag_evaluation(self, expert_token_sentence_list, challenger_token_sentence_list, user_tag_list=[]):
        total_tag_count_expert = 0
        total_tag_count_challenger = 0
        noun_tag_count_expert = 0
        noun_tag_count_challenger = 0
        total_phrase_count_expert = 0
        total_phrase_count_challenger = 0
        tp_count = 0
        tp_noun_count = 0
        tp_phrase_count = 0
        # POS Tag List
        tag_list = ['NNG', 'NNB', 'NNP', 'NP', 'NR', 'VV', 
                    'VX', 'VA', 'VCN', 'VCP', 'MM', 'MAG', 
                    'MAJ', 'IC', 'DT', 'EX', 'IN', 'MD', 'PDT', 
                    'RP', 'TO', 'WDT', 'WP', 'WP$', 'WRB', 'JKB', 
                    'JKC', 'JKG', 'JKO', 'JKQ', 'JKS', 'JKV', 'JC', 
                    'JX', 'EC', 'EP', 'EF', 'ETN', 'ETM', 'XPN', 
                    'XSN', 'XSV', 'XSA', 'XR', 'SW', 'OL', 'SN', 'UN', 'SL'] + user_tag_list
        # Counting
        for expert_token_sentence, challenger_token_sentence in zip(expert_token_sentence_list, challenger_token_sentence_list):
            # Counting in Token
            total_tag_count_challenger += len(challenger_token_sentence)
            noun_tag_count_challenger += sum([1 for ct in challenger_token_sentence if ct[1] in ["NNP", "NNG"]])
            for expert_token in expert_token_sentence:
                total_tag_count_expert += 1
                expert_token_sub = expert_token
                if expert_token[1] == "NNP":
                    noun_tag_count_expert += 1
                    expert_token_sub = (expert_token[0], "NNG", expert_token[2])
                elif expert_token[1] == "NNG":
                    noun_tag_count_expert += 1
                    expert_token_sub = (expert_token[0], "NNP", expert_token[2])
                #print(expert_token)
                if expert_token in challenger_token_sentence or expert_token_sub in challenger_token_sentence:
                    tp_count += 1
                    if expert_token[1] in ["NNP", "NNG"]:
                        tp_noun_count += 1

            # Counting in Phrase
            last_index = 0
            phrase_list = []
            for expert_token in expert_token_sentence:
                #print(expert_token[2][0], last_index)
                if expert_token[2][0] != last_index or last_index == 0:
                    is_tp_phrase = True
                    for phrase in phrase_list:
                        phrase_sub = phrase
                        if phrase[1] == "NNP":
                            phrase_sub = (expert_token[0], "NNG", expert_token[2])
                        elif phrase[1] == "NNG":
                            phrase_sub = (expert_token[0], "NNP", expert_token[2])
                        if phrase not in challenger_token_sentence and phrase_sub not in challenger_token_sentence:
                            is_tp_phrase = False
                    if is_tp_phrase:
                        tp_phrase_count += 1
                    total_phrase_count_expert += 1
                    phrase_list = []
                last_index = expert_token[2][1]
                phrase_list.append(expert_token)
                #print(phrase_list)
            for challenger_token in challenger_token_sentence:
                if challenger_token[2][0] != last_index or last_index == 0:
                    total_phrase_count_challenger += 1
                last_index = challenger_token[2][1]
        # Evaluation
        #recall = tp_count/noun_tag_count_expert
        #precision = tp_count/tag_count
        #f1_score = (2*recall*precision)/(recall+precision)
        recall_total = round(tp_count/total_tag_count_expert*100, 2)
        recall_noun = round(tp_noun_count/noun_tag_count_expert*100, 2)
        recall_phrase = round(tp_phrase_count/total_phrase_count_expert*100, 2)
        precision_total = round(tp_count/total_tag_count_challenger*100, 2)
        precision_noun = round(tp_noun_count/noun_tag_count_challenger*100, 2)
        precision_phrase = round(tp_phrase_count/total_phrase_count_challenger*100, 2)
        f1_score_total = round((2*recall_total*precision_total)/(recall_total+precision_total))
        f1_score_noun = round((2*recall_noun*precision_noun)/(recall_noun+precision_noun))
        f1_score_phrase = round((2*recall_phrase*precision_phrase)/(recall_phrase+precision_phrase))
        result = {
            #
            "total_tag_count_expert": total_tag_count_expert,
            "total_tag_count_challenger": total_tag_count_challenger,
            "total_phrase_count_expert": total_phrase_count_expert,
            "total_phrase_count_challenger": total_phrase_count_challenger,
            "noun_tag_count_expert": noun_tag_count_expert,
            "noun_tag_count_challenger": noun_tag_count_challenger,
            "tp_token_count": tp_count,
            "tp_token_noun_count": tp_noun_count,
            "tp_phrase_count": tp_phrase_count,
            "recall_total": recall_total,
            "recall_noun": recall_noun,
            "recall_phrase": recall_phrase,
            "precision_total": precision_total,
            "precision_noun": precision_noun,
            "precision_phrase": precision_phrase,
            "f1_score_total": f1_score_total,
            "f1_score_noun": f1_score_noun,
            "f1_score_phrase": f1_score_phrase,
        }
        return result
    
    def get_plain_text(self, sentence_list, pos_list=[], word_index=0, tag_index=1):
        plain_text_sentence_list = []
        for sentence in sentence_list:
            plain_text_sentence = ""
            for token in sentence:
                if len(pos_list) > 0:
                    if token[tag_index] in pos_list:
                        plain_text_sentence += token[word_index] + "/" + token[tag_index] + " "
                else:
                    plain_text_sentence += token[word_index] + "/" + token[tag_index] + " "
            plain_text_sentence_list.append(plain_text_sentence.strip())
        return plain_text_sentence_list
    
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