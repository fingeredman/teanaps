from teanaps import configure as con
from teanaps.visualization import GraphVisualizer
from teanaps.visualization import TextVisualizer
from teanaps.nlp import MorphologicalAnalyzer

import torch
from torch import nn
from torchcrf import CRF
#from transformers import BertModel, BertConfig
from pytorch_pretrained_bert import BertModel, BertConfig

from gluonnlp.data import SentencepieceTokenizer

import pickle
from collections import defaultdict

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
        
class KeywordExtractor():  
    def __init__(self, model_path=con.NER_MODEL_PATH, tagger="mecab"):
        with open(con.NER_UTIL_PATH["token_to_index"], 'rb') as f:
            self.token_to_index = pickle.load(f)
        with open(con.NER_UTIL_PATH["index_to_token"], 'rb') as f:
            self.index_to_token = pickle.load(f)
        with open(con.NER_UTIL_PATH["entity_to_index"], 'rb') as f:
            self.entity_to_index = pickle.load(f)
        with open(con.NER_UTIL_PATH["index_to_entity"], 'rb') as f:
            self.index_to_entity = pickle.load(f)
        self.tokenizer = SentencepieceTokenizer(con.NER_UTIL_PATH["tokenizer"])
        self.model_config = con.MODEL_CONFIG
        self.model_path = model_path
        self.vocab = con.VOCAB
        self.__load_ner_model()
        self.ma = MorphologicalAnalyzer()
        self.ma.set_tagger(tagger)
        
    def parse(self, input_text, max_keyword=5):
        input_text_lower = input_text.lower()
        list_of_input_ids = self.__sentence_to_token_index_list([input_text_lower])
        x_input = torch.tensor(list_of_input_ids).long()
        list_of_pred_ids, _ = self.model(x_input)
        list_of_ner_word, _ = self.__ner_decoder(input_text=input_text, input_text_lower=input_text_lower, 
                                                 list_of_input_ids=list_of_input_ids, 
                                                 list_of_pred_ids=list_of_pred_ids)
        list_of_ner_word.sort(key=lambda elem: elem[1], reverse=True)
        return [(word, round(weight, 5), loc) for word, weight, loc in list_of_ner_word if word != ""][:max_keyword]
    
    '''
    def parse_sentence(self, input_text):
        input_text_lower = input_text.lower()
        list_of_input_ids = self.__sentence_to_token_index_list([input_text_lower])
        x_input = torch.tensor(list_of_input_ids).long()
        list_of_pred_ids, _ = self.model(x_input)
        _, decoding_ner_sentence = self.__ner_decoder(input_text=input_text, input_text_lower=input_text_lower, 
                                                      list_of_input_ids=list_of_input_ids,
                                                      list_of_pred_ids=list_of_pred_ids)
        return decoding_ner_sentence
    '''
    def get_weight(self, sentence):
        attn_data = self.__get_attention(self.model, sentence)
        token_list = attn_data["text"]
        weight_list = []
        for token_index in range(len(token_list)):
            #weight_list.append(attn_data["attn"][11][11][token_index][token_index])
            weight_list.append(abs(attn_data["attn"][token_index]))
        return token_list[1:-1], weight_list[1:-1]
    '''
    def draw_sentence_weight(self, sentence):
        token_list, weight_list = self.get_weight(sentence)
        tv = TextVisualizer()
        tv.set_plotly()
        return tv.draw_sentence_attention(token_list, weight_list)
    
    def draw_weight(self, sentence):
        gv = GraphVisualizer()
        gv.set_plotly()
        token_list, weight_list = self.get_weight(sentence)
        x_data = ["(" + str(token_index) + ")" + token for token_index, token in enumerate(token_list)]
        z_data = [weight for weight in weight_list]
        data_meta_list = []
        data_meta = {
            "graph_type": "histogram",
            "data_name": "Y",
            "x_data": x_data,
            "y_data": z_data,
            "y_axis": "y2"
        }
        data_meta_list.append(data_meta)
        graph_meta = {
            "title": "NER WEIGHT",
            "x_tickangle": -45,
            "y1_tickangle": 0,
            "y2_tickangle": 0,
            "x_name": "TOKEN",
            "y1_name": "WEIGHT",
            "y2_name": "WEIGHT",
        }
        return gv.draw_histogram(data_meta_list, graph_meta)
    '''
    
    def __token_list_to_index_list(self, token_list):
        index_list = []
        for token in token_list:
            index_list.append([self.__token_to_index(t) for t in token])
        return index_list

    def __sentence_to_token_list(self, sentence):
        token_list = [self.tokenizer(char) for char in sentence]
        token_list_ = []
        for token in token_list[0]:
            if len(token) > 1 and token[-1] in ["은", "는", "로", "를", "을"]:
                token_list_.append(token[:-1])
                token_list_.append(token[-1])
            else:
                token_list_.append(token)
        return [token_list_]

    def __token_list_to_token_index_list(self, token_list):
        index_list = []
        for token in token_list:
            token = [self.vocab["cls_token"]] + token + [self.vocab["sep_token"]]
            index_list.append([self.__token_to_index(t) for t in token])
        return index_list

    def __sentence_to_token_index_list(self, sentence):
        token_list = self.__sentence_to_token_list(sentence)
        token_index_list = self.__token_list_to_token_index_list(token_list)
        return token_index_list

    def __index_list_to_token_list(self, index_list):
        token_list = []
        for index in index_list:
            token = [self.__index_to_token(i) for i in index]
            token_list.append(token)
        return token_list

    def __token_to_index(self, token):
        if token in self.token_to_index.keys():
            return self.token_to_index[token]
        else:
            token = self.vocab["unk_token"]
            return self.token_to_index[token]            

    def __index_to_token(self, index):
        if index in self.index_to_token.keys():
            return self.index_to_token[index]
        else:
            index = self.token_to_index[self.vocab["unk_token"]]
            return self.index_to_token[index]

    def __get_token_position(self, sentence_org, token_list):
        token_list = [token.replace("▁", "") for token in token_list[1:-1]]
        content_org = sentence_org.lower()
        content_ = sentence_org.lower()
        position = 0
        end = 0
        token_loc_list = []
        for i, token in enumerate(token_list):
            if token == "":
                loc = content_.find(token_list[i+1])
            else:
                loc = content_.find(token)
            if loc != -1:
                start = end+loc
                end += loc + len(token)
                content_ = content_org[end:]
            else:
                start = end
                end += len(token)

            token_loc_list.append((token, (start, end)))
        return [('[CLS]', (0, 0))] + token_loc_list + [('[SEP]', (0, 0))]
        
    def __load_ner_model(self):
        self.model = KobertCRF(config=self.model_config, num_classes=len(self.entity_to_index), vocab=self.vocab)
        model_dict = self.model.state_dict()
        checkpoint = torch.load(self.model_path, map_location=torch.device('cpu'))
        convert_keys = {}
        for k, v in checkpoint['model_state_dict'].items():
            new_key_name = k.replace("module.", '')
            if new_key_name not in model_dict:
                print("{} is not int model_dict".format(new_key_name))
                continue
            convert_keys[new_key_name] = v
        self.model.load_state_dict(convert_keys)
        self.model.eval()
        device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.model.to(device)
    
    def __get_attention(self, model, sentence):
        token_list = [self.vocab["cls_token"]] + self.__sentence_to_token_list([sentence])[0] + [self.vocab["sep_token"]]
        token_ids = self.__token_list_to_index_list([token_list])[0]
        tokens_tensor = torch.tensor(token_ids).unsqueeze(0)
        model.eval()
        _, output = model(tokens_tensor)
        attn_data_list = output[0][0]
        attn_dict = defaultdict(list)
        for attn_data in attn_data_list:
            attn = attn_data[0]
            attn_dict["all"].append(attn.tolist())
        token_list = self.__remove_char(token_list)
        token_list = self.__set_delimiter(token_list, self.vocab["cls_token"], self.vocab["sep_token"])
        results = {
            "attn": attn_dict["all"],
            "text": token_list,
        }
        return results

    def __remove_char(self, tokens):
        return [t.replace("Ġ", " ").replace("▁", " ") for t in tokens]

    def __set_delimiter(self, tokens, cls_token, sep_token):
        formatted_tokens = []
        for t in tokens:
            if sep_token:
                t = t.replace(sep_token, "[SEP]")
            if cls_token:
                t = t.replace(cls_token, "[CLS]")
            formatted_tokens.append(t)
        return formatted_tokens
    
    def __get_stopwords(self):
        stopword_list = open(con.STOPWORD_PATH, encoding="utf-8").read().strip().split("\n")
        return stopword_list
    
    def __ner_decoder(self, input_text, input_text_lower, list_of_input_ids, list_of_pred_ids):
        nn_dict = {}
        pos_list = self.ma.parse(input_text_lower)
        #print(pos_list)
        for word, pos, loc in pos_list:
            if pos in ["NNG", "NNP"] and word not in self.__get_stopwords():
                nn_dict[word] = (word, pos, loc)
        #print(nn_dict)
        list_of_tokens = self.__sentence_to_token_list([input_text_lower])
        #print(list_of_tokens)
        input_token = []
        for i, token in enumerate(self.__index_list_to_token_list(list_of_input_ids)[0]):
            if token == "[UNK]":
                input_token.append(list_of_tokens[0][i-1])
            else:
                input_token.append(token)
        pred_ner_tag = [self.index_to_entity[pred_id] for pred_id in list_of_pred_ids[0]]
        loc_list = self.__get_token_position(input_text_lower, input_token)
        _, weight_list = self.get_weight(input_text_lower)
        #print(weight_list)
        list_of_ner_word = []  
        temp_weight = 0
        temp_loc_a = loc_list[1][1][0]
        temp_loc_b = loc_list[1][1][1]
        temp_entity = ""
        temp_ner_tag = ""
        temp_sentence = ""
        for token, ner_tag, loc, weight in zip(input_token, pred_ner_tag, loc_list, weight_list):
            if ner_tag[:2] == "B-":
                if temp_entity != "":
                    list_of_ner_word.append((input_text[temp_loc_a:temp_loc_b], 
                                             temp_weight, (temp_loc_a, temp_loc_b)))
                                             #temp_ner_tag, temp_weight, (temp_loc_a, temp_loc_b)))
                    if temp_entity[0] == "▁":
                        temp_sentence += " "
                    temp_sentence += "<" + input_text[temp_loc_a:temp_loc_b] + ":" + temp_ner_tag + ">"
                temp_entity = ""
                temp_weight = 0
                temp_loc_a = loc[1][0]
                temp_loc_b = loc[1][1]
                temp_ner_tag = ner_tag[2:]
                temp_entity += token
                temp_weight += weight
            elif ner_tag[:2] == "I-":
                temp_weight += weight
                temp_loc_b = loc[1][1]
                temp_ner_tag = ner_tag[2:]
                if temp_entity != "":
                    temp_entity += token
                    temp_weight += weight
                if token not in ["[CLS]", "[SEP]"]:
                    if temp_entity == "":
                        temp_sentence += input_text[loc[1][0]:loc[1][1]]
            else:
                if temp_entity != "":
                    list_of_ner_word.append((input_text[temp_loc_a:temp_loc_b], 
                                             temp_weight, (temp_loc_a, temp_loc_b)))
                                             #temp_ner_tag, temp_weight, (temp_loc_a, temp_loc_b)))
                    if temp_entity[0] == "▁":
                        temp_sentence += " "
                    temp_sentence += "<" + input_text[temp_loc_a:temp_loc_b] + ":" + temp_ner_tag + ">"
                if token not in ["[CLS]", "[SEP]"]:
                    if token == "▁":
                        temp_sentence += " "
                    elif token[0] == "▁":
                        temp_sentence += " " + input_text[loc[1][0]:loc[1][1]]
                    elif token[-1] == "▁":
                        temp_sentence += input_text[loc[1][0]:loc[1][1]] + " "
                    else:
                        temp_sentence += input_text[loc[1][0]:loc[1][1]]
                temp_entity = ""
                temp_weight = 0
        #print(list_of_ner_word)
        window_size = 3
        list_of_tokens = list_of_tokens[0]
        for token_index in range(len(list_of_tokens)):
            #print(list_of_tokens[token_index])
            candidate_list = []
            for window in range(1, window_size+1):
                candidate = list_of_tokens[token_index:token_index+window]
                candidate_weight_list = weight_list[token_index:token_index+window]
                candidate_list.append((candidate, candidate_weight_list))
            #print(candidate_list)
            for candidate, candidate_weight_list in candidate_list:
                candidate_word = ""
                candidate_weight = 0
                for token, weight in zip(candidate, candidate_weight_list):
                    #print(candidate)
                    candidate_word += token
                    candidate_weight += weight
                candidate_word = candidate_word.replace("▁", " ").strip()
                if candidate_word in nn_dict.keys() and candidate_word not in [word for word, _, _ in list_of_ner_word]:
                    #print(candidate_word, candidate_weight, nn_dict[candidate_word][2])
                    list_of_ner_word.append((candidate_word, candidate_weight, nn_dict[candidate_word][2]))
        return list_of_ner_word, temp_sentence.strip()
        
class KobertCRF(nn.Module):
    def __init__(self, config, num_classes, vocab=None):
        super(KobertCRF, self).__init__()
        self.bert_config = con.BERT_CONFIG
        self.bert_config['output_attentions'] = True
        self.bert = BertModel(config=BertConfig.from_dict(self.bert_config))
        self.vocab = vocab
        self.dropout = nn.Dropout(config["dropout"])
        self.position_wise_ff = nn.Linear(config["hidden_size"], num_classes)
        self.crf = CRF(num_tags=num_classes, batch_first=True)
        with open(con.NER_UTIL_PATH["token_to_index"], 'rb') as f:
            self.token_to_index = pickle.load(f)

    def forward(self, input_ids, token_type_ids=None, tags=None):
        attention_mask = input_ids.ne(self.token_to_index[self.vocab["padding_token"]]).float()
        #outputs = self.bert(input_ids=input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask)
        outputs = self.bert(input_ids=input_ids, token_type_ids=token_type_ids, 
                            #attention_mask=attention_mask, output_all_encoded_layers=True)
                            attention_mask=attention_mask, output_all_encoded_layers=False)
        last_encoder_layer = outputs[0]
        last_encoder_layer = self.dropout(last_encoder_layer)
        emissions = self.position_wise_ff(last_encoder_layer)        
        if tags is not None:
            log_likelihood, sequence_of_tags = self.crf(emissions, tags), self.crf.decode(emissions)
            return log_likelihood, sequence_of_tags
        else:
            sequence_of_tags = self.crf.decode(emissions)
            return sequence_of_tags, outputs