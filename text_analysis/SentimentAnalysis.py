from teanaps import configure as con
from teanaps.visualization import GraphVisualizer

from gluonnlp.model import BERTModel, BERTEncoder
import gluonnlp as nlp
from mxnet.gluon import nn
import mxnet as mx
from mxnet import gluon

import numpy as np

class SentimentAnalysis():  
    def __init__(self, model_path=con.SENTIMENT_MODEL_PATH, kobert_path=con.SENTIMENT_UTIL_PATH["kobert"]):
        self.ctx = mx.cpu()
        self.kobert_path = kobert_path
        bert_base, vocab = self.__get_kobert_model()
        self.model = BERTClassifier(bert_base, num_classes=2, dropout=0.1)
        self.model.load_parameters(model_path, ctx=self.ctx)
        tokenizer_path = con.SENTIMENT_UTIL_PATH["tokenizer"]
        self.tok = nlp.data.BERTSPTokenizer(tokenizer_path, vocab, lower=False)
    
    def tag(self, sentence):
        sentence_list =  [[sentence, '0']]
        bert_sentence_list = BERTDataset(sentence_list, 0, 1, self.tok, 
                                         con.SENTIMENT_MODEL_CONFIG["max_len"], True, False)
        gluon_sentence_list = mx.gluon.data.DataLoader(bert_sentence_list, num_workers=5,
                                                       batch_size=int(con.SENTIMENT_MODEL_CONFIG["batch_size"]/2))
        for t, v, s, label in gluon_sentence_list:
            token_ids = t.as_in_context(self.ctx)
            valid_length = v.as_in_context(self.ctx)
            segment_ids = s.as_in_context(self.ctx)
            label = label.as_in_context(self.ctx)
            _, output = self.model(token_ids, segment_ids, valid_length.astype("float32"))
            for r in output:
                r = list(r)
                predict_value = r[0] if r[0] > r[1] else r[1]
                sentiment = r.index(predict_value)
                sentiment_label = "positive" if sentiment == 1 else "negative"
                return (r.index(predict_value), sentiment_label)
            
    def draw_sentence_weight(self, sentence):
        weight = self.get_weight(sentence)
        token_list = weight["token_list"]
        weight_list = [w**3 for w in weight["weight_list"]]
        gv = GraphVisualizer()
        return gv.draw_sentence_attention(token_list, weight_list)
        
    def draw_weight(self, sentence):
        attn_data = self.__get_attention(self.model, sentence)
        gv = GraphVisualizer()
        x = attn_data["text"]
        y = x
        x_data = []
        y_data = []
        z_data = []
        for x_index in range(len(x)):
            if x[x_index].strip() == "":
                continue
            x_data.append("("+str(x_index)+")"+x[x_index])
            z_data.append(attn_data["attn"][x_index])
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
            "title": "BERT SENTIMENT WEIGHT",
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
            if token_list[token_index].strip() == "":
                continue
            weight_list.append(attn_data["attn"][token_index])
        return {"token_list": token_list, "weight_list": weight_list}
    
    def __remove_char(self, tokens):
        return [t.replace('Ġ', ' ').replace('▁', ' ') for t in tokens]
    
    def __get_attention(self, model, sentence):
        sentence_list =  [[sentence, '0']]
        bert_sentence_list = BERTDataset(sentence_list, 0, 1, self.tok, 
                                         con.SENTIMENT_MODEL_CONFIG["max_len"], True, False)
        gluon_sentence_list = mx.gluon.data.DataLoader(bert_sentence_list, num_workers=5,
                                                       batch_size=int(con.SENTIMENT_MODEL_CONFIG["batch_size"]/2))
        for t, v, s, label in gluon_sentence_list:
            token_ids = t.as_in_context(self.ctx)
            valid_length = v.as_in_context(self.ctx)
            segment_ids = s.as_in_context(self.ctx)
            label = label.as_in_context(self.ctx)
            attn, _ = self.model(token_ids, segment_ids, valid_length.astype("float32"))
            attn_list = list(attn[11][0][0][11][127][:v.asnumpy()[0]].asnumpy())
        token_list = self.tok(sentence)
        token_list = self.__remove_char(token_list)
        results = {
            'attn': attn_list,
            'text': token_list,
        }
        return results
    
    def __get_kobert_model(self):
        use_pooler=True
        use_decoder=False
        use_classifier=False
        vocab_path = con.SENTIMENT_UTIL_PATH["tokenizer"]
        vocab_b_obj = nlp.vocab.BERTVocab.from_sentencepiece(vocab_path, padding_token="[PAD]")
        predefined_args = con.SENTIMENT_BERT_CONFIG
        encoder = BERTEncoder(attention_cell=predefined_args["attention_cell"],
                              num_layers=predefined_args["num_layers"],
                              units=predefined_args["units"],
                              hidden_size=predefined_args["hidden_size"],
                              max_length=predefined_args["max_length"],
                              num_heads=predefined_args["num_heads"],
                              scaled=predefined_args["scaled"],
                              dropout=predefined_args["dropout"],
                              #output_attention=False, output_all_encodings=False,
                              output_attention=True, output_all_encodings=False,
                              use_residual=predefined_args["use_residual"])
        net = BERTModel(encoder, len(vocab_b_obj.idx_to_token),
                        token_type_vocab_size=predefined_args["token_type_vocab_size"],
                        units=predefined_args["units"],
                        embed_size=predefined_args["embed_size"],
                        embed_dropout=predefined_args["embed_dropout"],
                        word_embed=predefined_args["word_embed"],
                        use_pooler=use_pooler, use_decoder=use_decoder, use_classifier=use_classifier)
        net.initialize(ctx=self.ctx)
        net.load_parameters(self.kobert_path, self.ctx, ignore_extra=True)
        return (net, vocab_b_obj)

class BERTClassifier(nn.Block):
    def __init__(self, bert, num_classes=2, dropout=None, prefix=None, params=None):
        super(BERTClassifier, self).__init__(prefix=prefix, params=params)
        self.bert = bert
        with self.name_scope():
            self.classifier = nn.HybridSequential(prefix=prefix)
            if dropout:
                self.classifier.add(nn.Dropout(rate=dropout))
            self.classifier.add(nn.Dense(units=num_classes))

    def forward(self, inputs, token_types, valid_length=None):
        _, attn, pooler = self.bert(inputs, token_types, valid_length)
        return attn, self.classifier(pooler)
    
class BERTDataset(mx.gluon.data.Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len, pad, pair):
        transform = nlp.data.BERTSentenceTransform(bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)
        sent_dataset = gluon.data.SimpleDataset([[i[sent_idx],] for i in dataset])
        self.sentences = sent_dataset.transform(transform)
        self.labels = gluon.data.SimpleDataset([np.array(np.int32(i[label_idx])) for i in dataset])

    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))

    def __len__(self):
        return (len(self.labels))