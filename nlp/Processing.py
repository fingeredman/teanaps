import re
from pykospacing import spacing

class Processing():  
    def __init__(self):
        self.a = 100
    
    def get_spacing(self, sentence):
        if len(sentence) < 195:
            sentence = spacing(sentence)
        return sentence
    
    def get_token_position(self, sentence_org, word_tagged_pos_list):
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
        
    def language_detector(self, sentence):
        len_ko = len(re.sub("[^가-힇]", "", sentence))
        len_en = len(re.sub("[^a-zA-Z]", "", sentence))
        return "ko" if len_ko >= len_en else "en"

    def iteration_remover(self, sentence):
        pattern_list = [r'(.)\1{5,}', r'(..)\1{5,}', r'(...)\1{5,}']
        for pattern in pattern_list:
            matcher= re.compile(pattern)
            iteration_term_list = [match.group() for match in matcher.finditer(sentence)]
            for iteration_term in iteration_term_list:
                sentence = sentence.replace(iteration_term, 
                                            iteration_term[:pattern.count(".")] + "."*(len(iteration_term)-pattern.count(".")))
        return sentence
    
    def get_plain_text(self, sentence, pos_list=[], word_index=0, tag_index=1, tag=True):
        plain_text_sentence_list = []
        plain_text_sentence = ""
        for token in sentence:
            if len(pos_list) > 0:
                if token[tag_index] in pos_list:
                    plain_text_sentence += token[word_index]
                    if tag:
                        plain_text_sentence += "/" + token[tag_index] + " "
                    else:
                        plain_text_sentence += " "
            else:
                plain_text_sentence += token[word_index]
                if tag:
                    plain_text_sentence += "/" + token[tag_index] + " "
                else:
                    plain_text_sentence += " "
        return plain_text_sentence
    
    def replacer(self, text):
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
        s = text
        for (pattern, repl) in self.patterns:
            s = re.sub(pattern, repl, s)
        return s
    
    