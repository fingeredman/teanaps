from teanaps import configure as con
from teanaps.visualization import GraphVisualizer

import torch
from torch import nn
from torchcrf import CRF
from transformers import BertModel, BertConfig
from gluonnlp.data import SentencepieceTokenizer

import pickle
import json
from collections import defaultdict

from IPython.core.display import display, HTML, Javascript

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
        
class NamedEntityRecognizer():  
    def __init__(self, model_path=con.NER_MODEL_PATH):
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
        
    def ner(self, input_text):
        list_of_input_ids = self.__sentence_to_token_index_list([input_text])
        x_input = torch.tensor(list_of_input_ids).long()
        list_of_pred_ids, _ = self.model(x_input)
        list_of_ner_word, decoding_ner_sentence = self.__ner_decoder(input_text=input_text, 
                                                                     list_of_input_ids=list_of_input_ids, 
                                                                     list_of_pred_ids=list_of_pred_ids)
        return list_of_ner_word
    
    def draw_weight(self, sentence):
        attn_data = self.__get_attention(self.model, sentence)
        gv = GraphVisualizer()
        x = attn_data["text"]
        y = x
        x_data = []
        y_data = []
        z_data = []
        for x_index in range(len(x)):
            x_data.append("("+str(x_index)+")"+x[x_index])
            z_data.append(attn_data["attn"][11][11][x_index][x_index])
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
            "title": "BERT NER WEIGHT",
            "x_tickangle": -45,
            "y1_tickangle": 0,
            "y2_tickangle": 0,
            "x_name": "TOKEN",
            "y1_name": "WEIGHT",
            "y2_name": "WEIGHT",
        }
        return gv.draw_histogram(data_meta_list, graph_meta)
    
    def get_weight(self, sentence):
        attn_data = self.__get_attention(self.model, sentence)
        gv = GraphVisualizer()
        token_list = attn_data["text"]
        weight_list = []
        for token_index in range(len(token_list)):
            weight_list.append(attn_data["attn"][11][11][token_index][token_index])
        return {"token_list": token_list, "weight_list": weight_list}
    
    def __token_list_to_index_list(self, token_list):
        index_list = []
        for token in token_list:
            index_list.append([self.__token_to_index(t) for t in token])
        return index_list

    def __sentence_to_token_list(self, sentence):
        token_list = [self.tokenizer(char) for char in sentence]
        return token_list

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
        content_ = sentence_org
        position = 0
        token_loc_list = []
        for token in token_list:
            token = token.replace("▁", "")
            loc = content_.find(token)
            if loc != -1:
                position += loc
                content_ = content_[loc:]
                start = position
                end = position + len(token)
            else:
                start = 0
                end = 0
            token_loc_list.append((token, (start, end)))
        return token_loc_list

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
        attn_data_list = output[-1]
        attn_dict = defaultdict(list)
        for layer, attn_data in enumerate(attn_data_list):
            attn = attn_data[0]
            attn_dict['all'].append(attn.tolist())
        token_list = self.__remove_char(token_list)
        token_list = self.__set_delimiter(token_list, self.vocab["cls_token"], self.vocab["sep_token"])
        results = {
            'attn': attn_dict['all'],
            'text': token_list,
        }
        return results

    def __remove_char(self, tokens):
        return [t.replace('Ġ', ' ').replace('▁', ' ') for t in tokens]

    def __set_delimiter(self, tokens, cls_token, sep_token):
        formatted_tokens = []
        for t in tokens:
            if sep_token:
                t = t.replace(sep_token, '[SEP]')
            if cls_token:
                t = t.replace(cls_token, '[CLS]')
            formatted_tokens.append(t)
        return formatted_tokens
    
    def __ner_decoder(self, input_text, list_of_input_ids, list_of_pred_ids):
        input_token = self.__index_list_to_token_list(list_of_input_ids)[0]
        pred_ner_tag = [self.index_to_entity[pred_id] for pred_id in list_of_pred_ids[0]]
        list_of_ner_word = []
        entity_word, entity_tag, prev_entity_tag = "", "", ""
        loc_list = self.__get_token_position(input_text, input_token)
        for i, pred_ner_tag_str in enumerate(pred_ner_tag):
            if "B-" in pred_ner_tag_str:
                if input_token[i] == "▁":
                    entity_word_index_a = loc_list[i+1][1][0]
                    entity_word_index_b = loc_list[i+1][1][1]
                else:
                    entity_word_index_a = loc_list[i][1][0]
                    entity_word_index_b = loc_list[i][1][1]
                entity_tag = pred_ner_tag_str[-3:]
                if prev_entity_tag != entity_tag and prev_entity_tag != "":
                    list_of_ner_word.append((entity_word.replace("▁", ""), 
                                             prev_entity_tag, 
                                             (entity_word_index_a, entity_word_index_b)))
                entity_word = input_token[i]
                prev_entity_tag = entity_tag
            elif "I-"+entity_tag in pred_ner_tag_str:
                entity_word += input_token[i]
                entity_word_index_b = loc_list[i][1][1]
            else:
                if entity_word != "" and entity_tag != "":
                    list_of_ner_word.append((entity_word.replace("▁", " ").strip(), 
                                             entity_tag, (entity_word_index_a, entity_word_index_b)))
                entity_word, entity_tag, prev_entity_tag = "", "", ""
        decoding_ner_sentence = ""
        is_prev_entity = False
        prev_entity_tag = ""
        is_there_B_before_I = False        
        for i, (token_str, pred_ner_tag_str) in enumerate(zip(input_token, pred_ner_tag)):
            if i == 0 or i == len(pred_ner_tag)-1:
                continue
            token_str = token_str.replace('▁', ' ')
            if 'B-' in pred_ner_tag_str:
                if is_prev_entity is True:
                    decoding_ner_sentence += '/' + prev_entity_tag+ ']'
                if token_str[0] == ' ':
                    token_str = list(token_str)
                    token_str[0] = ' ['
                    token_str = ''.join(token_str)
                    decoding_ner_sentence += token_str
                else:
                    decoding_ner_sentence += '[' + token_str
                is_prev_entity = True
                prev_entity_tag = pred_ner_tag_str[-3:]
                is_there_B_before_I = True
            elif 'I-' in pred_ner_tag_str:
                decoding_ner_sentence += token_str

                if is_there_B_before_I is True:
                    is_prev_entity = True
            else:
                if is_prev_entity is True:
                    decoding_ner_sentence += '/' + prev_entity_tag+ ']' + token_str
                    is_prev_entity = False
                    is_there_B_before_I = False
                else:
                    decoding_ner_sentence += token_str
        return list_of_ner_word, decoding_ner_sentence
        
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
        outputs = self.bert(input_ids=input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask)
        last_encoder_layer = outputs[0]
        last_encoder_layer = self.dropout(last_encoder_layer)
        emissions = self.position_wise_ff(last_encoder_layer)        
        if tags is not None:
            log_likelihood, sequence_of_tags = self.crf(emissions, tags), self.crf.decode(emissions)
            return log_likelihood, sequence_of_tags
        else:
            sequence_of_tags = self.crf.decode(emissions)
            return sequence_of_tags, outputs