# -----------------------------------------
# * Env Check *
# -----------------------------------------
import os
path_str = os.environ["PATH"]
path_list = path_str.split(":")
path_check = len([path for path in path_list if "/home/teanaps_home" in path])
if path_check == 0:
    TEANAPS_PATH = ""
else:
    TEANAPS_PATH = "/home/teanaps_home/anaconda3/lib/python3.7/site-packages/"
    
# -----------------------------------------
# * Version *
# -----------------------------------------
VERSION = "0.9.700"

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
STOPWORD_PATH = TEANAPS_PATH + "teanaps/data/corpus/stopword.txt"
STOPWORD_ORG_PATH = TEANAPS_PATH + "teanaps/data/corpus/stopword_org.txt"
CNOUN_PATH = TEANAPS_PATH + "teanaps/data/corpus/cnoun.txt"
CNOUN_ORG_PATH = TEANAPS_PATH + "teanaps/data/corpus/cnoun_org.txt"
SYNONYM_PATH = TEANAPS_PATH + "teanaps/data/corpus/synonym.txt"
SYNONYM_ORG_PATH = TEANAPS_PATH + "teanaps/data/corpus/synonym_org.txt"

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
NER_MODEL_PATH = TEANAPS_PATH + "teanaps/model/ner/ner_model.bin"
NER_UTIL_PATH = {
    "token_to_index": TEANAPS_PATH + "teanaps/model/ner/token_to_index",
    "index_to_token": TEANAPS_PATH + "teanaps/model/ner/index_to_token",
    "entity_to_index": TEANAPS_PATH + "teanaps/model/ner/entity_to_index",
    "index_to_entity": TEANAPS_PATH + "teanaps/model/ner/index_to_entity",
    "tokenizer": TEANAPS_PATH + "teanaps/model/ner/tokenizer"
}
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
# teanaps.text_analysis.TfidfCalculator
# -----------------------------------------
TFIDF_VECTORIZER_PATH = "tfidf_vectorizer"
TF_VECTORIZER_PATH = "tf_vectorizer"

# -----------------------------------------
# teanaps.text_analysis.SentimentAnalysis
# -----------------------------------------
SENTIMENT_MODEL_PATH = TEANAPS_PATH + "teanaps/model/sentiment/senti_model"
SENTIMENT_UTIL_PATH = {
    "tokenizer": TEANAPS_PATH + "teanaps/model/sentiment/tokenizer",
    "kobert": TEANAPS_PATH + "teanaps/model/sentiment/mxnet_kobert",
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
WINDOW_SIZE = 5
MAX_WORKERS = 5

# -----------------------------------------
# * Visualization *
# -----------------------------------------
COLOR_CODE_LIST = [
    #"#1D1E23",
    #"#FFFFFF",
    #"#A4AAA7",
    #"#959EA2",
    #"#616264",
    #"#6F606E",
    #"#DDE7E7",
    #"#E7E6D2",
    #"#E3DDCB",
    #"#D8C8B2",
    "#B82647",
    "#F15B5B",
    "#9F494C",
    "#683235",
    "#966147",
    "#BD7F41",
    #"#C38866",
    "#D77964",
    #"#CA5E59",
    "#C23352",
    "#EA8474",
    "#BF2F7B",
    "#CE5A9E",
    "#BE577B",
    "#D97793",
    "#DB4E9C",
    "#E2A6B4",
    "#E0709B",
    "#E16350",
    "#8A4C44",
    "#8E6F80",
    "#F9D537",
    "#EBBC6B",
    "#FEE134",
    "#F5F0C5",
    "#F8E77F",
    "#F7B938",
    "#F1A55A",
    "#E5B98F",
    "#ED9149",
    "#C8852C",
    "#D6B038",
    "#9A6B31",
    "#F6FC7A",
    "#DDA28F",
    "#BB9E8B",
    "#0B6DB7",
    "#00B5E3",
    "#5AC6D0",
    "#00A6A9",
    "#5DC19B",
    "#6C71B5",
    "#448CCB",
    "#006494",
    "#026892",
    "#6A5BA8",
    "#7963AB",
    "#6979BB",
    "#45436C",
    "#4F599F",
    "#417141",
    "#16AA52",
    "#6AB048",
    "#569A49",
    "#C0D84D",
    "#CBDD61",
    "#009770",
    "#0A8D5E",
    "#1C9249",
    "#2E674E",
    "#72C6A5",
    "#9ED6C0",
    "#5C6EB4",
    "#397664",
    "#31B675",
    "#245441",
    "#1583AF",
    "#18B4E9",
    "#6D1B43",
    "#89236A",
    "#9C4998",
    "#733E7F",
    "#5D3462",
    "#403F95",
    "#84A7D3",
    "#B3A7DC",
    "#BEA3C9",
    "#47302E",
    "#BA4160"]

# -----------------------------------------
# teanaps.visualization.GraphVisualizer
# -----------------------------------------
WATERMARK_URL = "https://raw.githubusercontent.com/fingeredman/teanaps-documents/main/data/logo/teanaps_logo_nbg_1600x400.png"
WORDCLOUD_FONT_PATH = TEANAPS_PATH + "teanaps/data/font/NanumSquareB.otf"
WORDCLOUD_MASK_PATH = TEANAPS_PATH + "teanaps/data/image/wordcloud_mask_type_01.png"
WORDCLOUD_WATERMARK_PATH = TEANAPS_PATH + "teanaps/data/image/wordcloud_mask_type_02.png"

# -----------------------------------------
# * Handler *
# -----------------------------------------

# -----------------------------------------
# teanaps.handler.MESSAGE HANDLER
# -----------------------------------------
# For SLACK
#WEBHOOK_URL = "https://hooks.slack.com/services/TNLDWA5B7/BN-----JS/GZ0f--------------FIaug7"