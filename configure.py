# -----------------------------------------
# * API *
# -----------------------------------------
ENTITY_API_URL = "http://api.teanaps.com/v1/lexicon/entity"

# -----------------------------------------
# * Plotly *
# -----------------------------------------
PLOTLY_USERNAME = "fingeredman"
PLOTLY_API_KEY = "7xQjXPiDYPi1iIrrT3ID"

# -----------------------------------------
# * NLP *
# -----------------------------------------

# -----------------------------------------
# teanaps.nlp.Processing
# -----------------------------------------
STOPWORD_PATH = "teanaps/data/stopword/stopword.txt"
STOPWORD_ORG_PATH = "teanaps/data/stopword/stopword_org.txt"

# -----------------------------------------
# teanaps.nlp.MorphologicalAnalyzer
# -----------------------------------------
# Select Part of Speech Tagger
#POS_TAGGER = "mecab"
#POS_TAGGER = "mecab-ko"
#POS_TAGGER = "kkma"
POS_TAGGER = "okt"
POS_TAG_MAP = {
    "NNG": "NNG", "NNB": "NNB", "NNP": "NNP", "NP": "NP", "NR": "NR", 
    "VV": "VV", "VX": "VX", "VA": "VA", "VCN": "VCN", "VCP": "VCP",
    "MM": "MM", "MAG": "MAG","MAJ": "MAJ", "IC": "IC", 
    "DT": "DT", "EX": "EX", "IN": "IN", "MD": "MD", "PDT": "PDT", "RP": "RP", "TO": "TO",
    "WDT": "WDT", "WP": "WP", "WP$": "WP$", "WRB": "WRB",
    "JKB": "JKB", "JKC": "JKC","JKG": "JKG", "JKO": "JKO", "JKQ": "JKQ", "JKS": "JKS", "JKV": "JKV", 
    "JC": "JC", "JX": "JX", 
    "EC": "EC", "EP": "EP", "EF": "EF", "ETN": "ETN", "ETM": "ETM", 
    "XPN": "XPN", "XSN": "XSN", "XSV": "XSV", "XSA": "XSA", 
    "XR": "XR", "SE": "SW", "SF": "SW", "SH": "OL", "SL": "OL", "SN": "SN", 
    "SS": "SW", "SW": "SW", "SP": "SW", "UN": "UN", "SO": "SW", 
    # For MeCab
    "NNBC": "NNB", "NN": "NNG", "NNS": "NNG", "NNPS": "NNP", "PRP": "NP", "PRP$": "NP", 
    "JJ": "VA", "JJR": "VA", "JJS": "VA", "VB": "VV", "VBG": "VV", "VBN": "VV", "VBZ": "VV", 
    "RB": "MAG", "RBS": "MAG", "RBR": "MAG",
    "UH": "IC", "CC": "JC", "FW": "OL", "CD": "SN",
    "SSO": "SW", "SSC": "SW", "SC": "SW", "SY": "SW", "LS": "SW",
    "UNKNOWN": "UN", "UNT": "UN", "UNA": "UN", "NA": "UN", "E": "UN",
    # For KKMA
    "NNM": "NNB", "VXV": "VX", "VXA": "VX", "VXN": "VX", "MDT": "MM", "MDN": "MM", "MAC": "MAJ",
    "JKM": "JKB", "EPH": "EP", "EPT": "EP", "EPP": "EP", "ECE": "EC", "ECD": "EC", "ECS": "EC",
    "EFN": "EF", "EFQ": "EF", "EFO": "EF", "EFA": "EF", "EFI": "EF", "EFR": "EF", "ETD": "ETM",
    "XPV": "XPN", "OH": "OL", "SL": "OL", "OL": "OL", "ON": "SN", "UV": "UN", "UE": "UN", 
    # For Okt
    "Noun": "NNG", "Adjective": "VA", "Verb": "VV", "Determiner": "MM", "Adverb": "MAG",
    "Conjunction": "MAJ", "Exclamation": "IC", "Josa": "JC", "PreEomi": "EP", "Eomi": "EC",
    "Suffix": "XPN", "Unknown": "UN", "Punctuation": "SW", "Alpha": "OL", "Number": "SN",
    "Foreign": "OL", "Modifier": "MM", "Hashtag": "SW", "KoreanParticle": "SW", "ScreenName": "SW",
    "Email": "SW", "VerbPrefix": "XPN", "URL": "SW", "CashTag": "SW"
}
LEMMATIZER_POS_MAP = {'J': 'a', 'N': 'n', 'R': 'r', 'V': 'v'}
SYMBOLS_POS_MAP = {
    "...": "SW", ".": "SW", "?": "SW", "!": "SW",
    "-": "SW", ",": "SW", "·": "SW", ";": "SW", ":": "SW", "/": "SW",
    "'": "SW", "\"": "SW", "(": "SW", ")": "SW", "<": "SW", ">": "SW",     
}
SKIP_WORD_LIST = ["/"]

# -----------------------------------------
# teanaps.nlp.NamedEntityRecognizer
# -----------------------------------------
NER_MODEL_PATH = "teanaps/model/ner/ner_model.bin"
NER_UTIL_PATH = {
    "token_to_index": "teanaps/model/ner/token_to_index",
    "index_to_token": "teanaps/model/ner/index_to_token",
    "entity_to_index": "teanaps/model/ner/entity_to_index",
    "index_to_entity": "teanaps/model/ner/index_to_entity",
    "tokenizer": "teanaps/model/ner/tokenizer"
}
'''
NER_MODEL_PATH = "teanaps/model/ner_article/ner_article_model_20191215.bin"
NER_UTIL_PATH = {
    "token_to_index": "teanaps/model/ner_article/token_to_index",
    "index_to_token": "teanaps/model/ner_article/index_to_token",
    "entity_to_index": "teanaps/model/ner_article/entity_to_index",
    "index_to_entity": "teanaps/model/ner_article/index_to_entity",
    "tokenizer": "teanaps/model/ner_article/tokenizer"
}
'''
BERT_CONFIG = {
    "attention_probs_dropout_prob": 0.1,
    "hidden_act": "gelu",
    "hidden_dropout_prob": 0.1,
    "hidden_size": 768,
    "initializer_range": 0.02,
    "intermediate_size": 3072,
    "max_position_embeddings": 512,
    "num_attention_heads": 12,
    "num_hidden_layers": 12,
    "type_vocab_size": 2,
    "vocab_size": 8002
}

MODEL_CONFIG = {
    "hidden_size": 768,
    "dropout": 0.1,
}
VOCAB = {
    "padding_token": "[PAD]",
    "cls_token": "[CLS]",
    "sep_token": "[SEP]",
    "unk_token": "[UNK]"
}

# -----------------------------------------
# * Text Analysis *
# -----------------------------------------

# -----------------------------------------
# teanaps.text_analysis.SentimentAnalysis
# -----------------------------------------
SENTIMENT_MODEL_PATH = "teanaps/model/sentiment/senti_model"
SENTIMENT_UTIL_PATH = {
    "tokenizer": "teanaps/model/sentiment/tokenizer",
    "kobert": "teanaps/model/sentiment/mxnet_kobert",
}
SENTIMENT_MODEL_CONFIG = {
    "max_len": 128,
    "batch_size": 32
}
SENTIMENT_BERT_CONFIG = {
    "attention_cell": 'multi_head',
    "num_layers": 12,
    "units": 768,
    "hidden_size": 3072,
    "max_length": 512,
    "num_heads": 12,
    "scaled": True,
    "dropout": 0.1,
    "use_residual": True,
    "embed_size": 768,
    "embed_dropout": 0.1,
    "token_type_vocab_size": 2,
    "word_embed": None,
}

# -----------------------------------------
# teanaps.text_analysis.CoWordCalculator
# -----------------------------------------
WINDOW_SIZE = 2
MAX_WORKERS = 5

# -----------------------------------------
# * Visualization *
# -----------------------------------------

# -----------------------------------------
# teanaps.visualization.GraphVisualizer
# -----------------------------------------
WATERMARK_URL = "https://raw.githubusercontent.com/fingeredman/teanaps/master/data/logo/teanaps_logo_no-bg.png"
WORDCLOUD_FONT_PATH = "teanaps/data/font/NanumSquareB.otf"

# -----------------------------------------
# * Handler *
# -----------------------------------------

# -----------------------------------------
# teanaps.handler.MESSAGE HANDLER
# -----------------------------------------
# For SLACK
#WEBHOOK_URL = "https://hooks.slack.com/services/TNLDWA5B7/BN-----JS/GZ0f--------------FIaug7"