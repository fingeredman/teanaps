# -----------------------------------------
# * API *
# -----------------------------------------
ENTITY_API_URL = "http://api.teanaps.com/v1/entity"

# -----------------------------------------
# * Plotly *
# -----------------------------------------
PLOTLY_USERNAME = "fingeredman"
PLOTLY_API_KEY = "7xQjXPiDYPi1iIrrT3ID"

# -----------------------------------------
# * Text Pre-processing *
# -----------------------------------------
STOPWORD_PATH = "teanaps/data/stopword.txt"

# Select Part of Speech Tagger
#POS_TAGGER = "mecab"
#POS_TAGGER = "mecab-ko"
#POS_TAGGER = "kkma"
POS_TAGGER = "okt"
#

# -----------------------------------------
# CoWordCalculator
# -----------------------------------------
WINDOW_SIZE = 2
MAX_WORKERS = 5

# -----------------------------------------
# SyntaxAnalyzer
# -----------------------------------------
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
    "XR": "XR", "SE": "SE", "SF": "SF", "SH": "SH", "SL": "SL", "SN": "SN", 
    "SS": "SS", "SW": "SW", "SP": "SP", "UN": "UN", "SO": "SO", 
    # For MeCab
    "NNBC": "NNB", "NN": "NNG", "NNS": "NNG", "NNPS": "NNP", "PRP": "NP", "PRP$": "NP", 
    "JJ": "VA", "JJR": "VA", "JJS": "VA", "VB": "VV", "VBG": "VV", "VBN": "VV", "VBZ": "VV", 
    "RB": "MAG", "RBS": "MAG", "RBR": "MAG",
    "UH": "IC", "CC": "JC", "FW": "SL", "CD": "SN",
    "SSO": "SS", "SSC": "SS", "SC": "SP", "SY": "SO", "LS": "SW",
    "UNKNOWN": "UN", "UNT": "UN", "UNA": "UN", "NA": "UN", "E": "UN",
    # For KKMA
    "NNM": "NNB", "VXV": "VX", "VXA": "VX", "VXN": "VX", "MDT": "MM", "MDN": "MM", "MAC": "MAJ",
    "JKM": "JKB", "EPH": "EP", "EPT": "EP", "EPP": "EP", "ECE": "EC", "ECD": "EC", "ECS": "EC",
    "EFN": "EF", "EFQ": "EF", "EFO": "EF", "EFA": "EF", "EFI": "EF", "EFR": "EF", "ETD": "ETM",
    "XPV": "XPN", "OH": "SH", "OL": "SL", "ON": "SN", "UV": "UN", "UE": "UN", 
    # For Okt
    "Noun": "NNG", "Adjective": "VA", "Verb": "VV", "Determiner": "MM", "Adverb": "MAG",
    "Conjunction": "MAJ", "Exclamation": "IC", "Josa": "JC", "PreEomi": "EP", "Eomi": "EC",
    "Suffix": "XPN", "Unknown": "UN", "Punctuation": "SW", "Alpha": "SL", "Number": "SN",
    "Foreign": "SL", "Modifier": "MM", "Hashtag": "SW", "KoreanParticle": "SW", "ScreenName": "SW",
    "Email": "SW", "VerbPrefix": "XPN", "URL": "SW",
}
LEMMATIZER_POS_MAP = {'J': 'a', 'N': 'n', 'R': 'r', 'V': 'v'}
SYMBOLS_POS_MAP = {
    "...": "SE", ".": "SF", "?": "SF", "!": "SF",
    "-": "SO", ",": "SP", "·": "SP", ";": "SP", ":": "SP", "/": "SP",
    "'": "SS", "\"": "SS", "(": "SS", ")": "SS", "<": "SS", ">": "SS",     
}
SKIP_WORD_LIST = ["/"]

# -----------------------------------------
# MESSAGE HANDLER
# -----------------------------------------
# For SLACK
WEBHOOK_URL = "https://hooks.slack.com/services/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"