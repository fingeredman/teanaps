from teanaps import configure as con
from teanaps.nlp import NamedEntityRecognizer
#from konlpy.tag import Kkma
from kss import split_sentences
      
import re
import time
#from pykospacing import spacing

class Processing():  
    def __init__(self):
        self.stopword_path = con.STOPWORD_PATH
        self.stopword_org_path = con.STOPWORD_ORG_PATH
        self.cnoun_path = con.CNOUN_PATH
        self.cnoun_org_path = con.CNOUN_ORG_PATH
        self.synonym_path = con.SYNONYM_PATH
        self.synonym_org_path = con.SYNONYM_ORG_PATH
        #self.kkma = Kkma()
        
    def get_synonym(self):        
        synonym_list = open(con.SYNONYM_PATH, encoding="utf-8").read().strip().split("\n")
        synonym_dict = {}
        for synonym in synonym_list:
            for i, word in enumerate(synonym.split("\t")):
                if i == 0:
                    representative_word = word
            synonym_dict[representative_word] = synonym.split("\t")
        return synonym_dict
    
    def add_synonym(self, add_dict={}):
        synonym_dict = self.get_synonym()
        for representative_word, synonym_list in add_dict.items():
            if representative_word in synonym_dict.keys():
                for synonym in synonym_list:
                    if synonym not in synonym_dict[representative_word]:
                        synonym_dict[representative_word].append(synonym)
            else:
                synonym_dict[representative_word] = []
                for synonym in synonym_list:
                    if synonym not in synonym_dict[representative_word]:
                        synonym_dict[representative_word].append(synonym)
        f = open(self.synonym_path, "w", encoding="utf-8")
        for representative_word, synonym_list in synonym_dict.items():
            synonym_line = ""
            if representative_word not in synonym_list:
                f.write(representative_word + "\t")
            for synonym in synonym_list:
                synonym_line += synonym + "\t"
            f.write(synonym_line.strip() + "\n")
        f.close()
        
    def remove_synonym(self, remove_list=[]):
        if type(remove_list) == type(""):
            remove_list = [remove_list]
        synonym_dict = self.get_synonym()
        for synonym in remove_list:
            if synonym in synonym_dict.keys():
                del synonym_dict[synonym]
            else:
                for representative_word, synonym_list in synonym_dict.items():
                    if synonym in synonym_list:
                        synonym_list.remove(synonym)
        f = open(self.synonym_path, "w", encoding="utf-8")
        for representative_word, synonym_list in synonym_dict.items():
            synonym_line = ""
            if representative_word not in synonym_list:
                f.write(representative_word + "\t")
            for synonym in synonym_list:
                synonym_line += synonym + "\t"
            f.write(synonym_line.strip() + "\n")
        f.close()
        
    def clear_synonym(self):
        f = open(self.synonym_path, "w", encoding="utf-8")
        f.close()
        
    def set_org_synonym(self):
        f = open(self.synonym_path, "w", encoding="utf-8")
        f_org = open(self.synonym_org_path, encoding="utf-8")
        for line in f_org:
            f.write(line)
        f_org.close()
        f.close()
        
    def is_synonym(self, synonym):
        synonym_dict = self.get_synonym()
        if synonym in synonym_dict.keys():
            return True
        for representative_word, synonym_list in synonym_dict.items():
            if representative_word == synonym or synonym in synonym_list:
                return True
        return False
        
    def get_cnoun(self):
        cnoun_list = []
        f = open(self.cnoun_path, encoding="utf-8")
        for line in f:
            cnoun_list.append(line.strip())
        f.close()
        return cnoun_list
    
    def add_cnoun(self, add_list=[]):
        cnoun_list = self.get_cnoun()
        f = open(self.cnoun_path, "a", encoding="utf-8")
        if type(add_list) == type(""):
            add_list = [add_list]
        for cnoun in add_list:
            if cnoun not in cnoun_list:
                f.write(cnoun + "\n")
        f.close()
        
    def remove_cnoun(self, remove_list=[]):
        cnoun_list = self.get_cnoun()
        f = open(self.cnoun_path, "w", encoding="utf-8")
        if type(remove_list) == type(""):
            remove_list = [remove_list]
        for cnoun in cnoun_list:
            if cnoun not in remove_list:
                f.write(cnoun + "\n")
        f.close()
        
    def clear_cnoun(self):
        f = open(self.cnoun_path, "w", encoding="utf-8")
        f.close()
        
    def set_org_cnoun(self):
        f = open(self.cnoun_path, "w", encoding="utf-8")
        f_org = open(self.cnoun_org_path, encoding="utf-8")
        for line in f_org:
            f.write(line)
        f_org.close()
        f.close()
        
    def is_cnoun(self, cnoun):
        cnoun_list = self.get_cnoun()
        if cnoun in cnoun_list:
            return True
        else:
            return False
    
    def get_stopword(self):
        stopword_list = []
        f = open(self.stopword_path, encoding="utf-8")
        for line in f:
            stopword_list.append(line.strip())
        f.close()
        return stopword_list
    
    def add_stopword(self, add_list=[]):
        stopword_list = self.get_stopword()
        f = open(self.stopword_path, "a", encoding="utf-8")
        if type(add_list) == type(""):
            add_list = [add_list]
        for stopword in add_list:
            if stopword not in stopword_list:
                f.write(stopword + "\n")
        f.close()
        
    def remove_stopword(self, remove_list=[]):
        stopword_list = self.get_stopword()
        f = open(self.stopword_path, "w", encoding="utf-8")
        if type(remove_list) == type(""):
            remove_list = [remove_list]
        for stopword in stopword_list:
            if stopword not in remove_list:
                f.write(stopword + "\n")
        f.close()
        
    def clear_stopword(self):
        f = open(self.stopword_path, "w", encoding="utf-8")
        f.close()
        
    def set_org_stopword(self):
        f = open(self.stopword_path, "w", encoding="utf-8")
        f_org = open(self.stopword_org_path, encoding="utf-8")
        for line in f_org:
            f.write(line)
        f_org.close()
        f.close()
        
    def is_stopword(self, stopword):
        stopword_list = self.get_stopword()
        if stopword in stopword_list:
            return True
        else:
            return False
    
    def start_timer(self):
        self.start = time.time()
        self.lab = []
        
    def lab_timer(self):
        self.lab.append((len(self.lab)+1, round(time.time() - self.start, 4)))
        return self.lab
    
    '''
    def get_spacing(self, sentence):
        if len(sentence) < 195:
            sentence = spacing(sentence)
        return sentence
    '''
    
    def get_token_position(self, sentence_org, tag_list):
        content_ = sentence_org
        position = 0
        loc_list = []
        for word, pos in tag_list:
            loc = content_.find(word)
            if loc != -1:
                position += loc
                content_ = content_[loc:]
                start = position
                end = position + len(word)
                org_word = sentence_org[start:end]
            else:
                start = 0
                end = 0
                org_word = word
            loc_list.append((org_word, pos, (start, end)))
        return loc_list
        
    def language_detector(self, sentence):
        len_ko = len(re.sub("[^가-힇]", "", sentence))
        len_en = len(re.sub("[^a-zA-Z]", "", sentence))
        return "ko" if len_ko >= len_en else "en"

    def iteration_remover(self, sentence, replace_char="."):
        pattern_list = [r'(.)\1{5,}', r'(..)\1{5,}', r'(...)\1{5,}']
        for pattern in pattern_list:
            matcher= re.compile(pattern)
            iteration_term_list = [match.group() for match in matcher.finditer(sentence)]
            for iteration_term in iteration_term_list:
                sentence = sentence.replace(iteration_term, 
                                            iteration_term[:pattern.count(".")] + replace_char*(len(iteration_term)-pattern.count(".")))
        return sentence
    
    def get_plain_text(self, sentence, pos_list=[], word_index=0, pos_index=1, tag_index=1, tag=True):
        plain_text_sentence = ""
        for token in sentence:
            if len(pos_list) > 0:
                if token[pos_index] in pos_list:
                    plain_text_sentence += token[word_index].replace(" ", "")
                    if tag:
                        plain_text_sentence += "/" + token[tag_index] + " "
                    else:
                        plain_text_sentence += " "
            else:
                plain_text_sentence += token[word_index].replace(" ", "")
                if tag:
                    plain_text_sentence += "/" + token[tag_index] + " "
                else:
                    plain_text_sentence += " "
        return plain_text_sentence.strip()
    
    def replacer(self, sentence):
        patterns = [
            (r'won\'t', 'will not'),
            (r'can\'t', 'cannot'),
            (r'i\'m', 'i am'),
            (r'ain\'t', 'is not'),
            (r'(\w+)\'ll', '\g<1> will'),
            (r'(\w+)n\'t', '\g<1> not'),
            (r'(\w+)\'ve', '\g<1> have'),
            (r'(\w+)\'s', '\g<1> is'),
            (r'(\w+)\'re', '\g<1> are'),
            (r'(\w+)\'d', '\g<1> would'),
        ]
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
        for (pattern, repl) in self.patterns:
            sentence = re.sub(pattern, repl, sentence)
        return sentence
    
    def masking(self, sentence, replace_char="*", replace_char_pattern = "", ner_tag_list=[], model_path=""):
        if model_path == "":
            ner = NamedEntityRecognizer()
        else:
            ner = NamedEntityRecognizer(model_path=model_path)
        ner_result = ner.parse(sentence)
        for word, ner_tag, loc in ner_result:
            if len(ner_tag_list) == 0 or ner_tag in ner_tag_list:
                if replace_char_pattern != "":
                    masked_word = ""
                    for w, r in zip(word, replace_char_pattern):
                        if w == r or r == "_":
                            masked_word += w
                        elif r == replace_char:
                            masked_word += r
                        else:
                            masked_word += w
                    if len(word) > len(replace_char_pattern):
                        masked_word += replace_char*len(word[len(replace_char_pattern):])
                    sentence = sentence[:loc[0]] + masked_word + sentence[loc[1]:]
                else:
                    sentence = sentence[:loc[0]] + replace_char*len(word) + sentence[loc[1]:]
                
        return sentence
    
    def sentence_splitter(self, paragraph):
        #sentence_list = self.kkma.sentences(paragraph)
        sentence_list = split_sentences(paragraph)
        return sentence_list
    