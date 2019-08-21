# Database


# Plotly
PLOTLY_USERNAME = "fingeredman"
PLOTLY_API_KEY = "7xQjXPiDYPi1iIrrT3ID"

# Text Pre-processing
STOPWORD_PATH = "data/stopword.txt"

# CoWordCalculator
WINDOW_SIZE = 2
MAX_WORKERS = 5

# SyntaxAnalyzer
POS_TAG_MAP = {
    #For MeCab
    'NNG': 'NNG','NNB': 'NNB', 'NNBC': 'NNB', 'NNP': 'NNP', 
    'NN': 'NNG', 'NNS': 'NNG', 'NNPS': 'NNP',
    'NP': 'NP', 'NR': 'NR', 'PRP': 'NP', 'PRP$': 'NP',
    'VV': 'VV', 'VX': 'VX', 'VA': 'VA', 'VCN': 'VCN', 'VCP': 'VCP', 
    'JJ': 'VA', 'JJR': 'VA', 'JJS': 'VA', 'VB': 'VV', 'VBG': 'VV', 'VBN': 'VV', 'VBZ': 'VV', 
    'MM': 'MM', 'MAG': 'MAG','MAJ': 'MAJ', 'RB': 'MAG', 'RBS': 'MAG', 'RBR': 'MAG',
    'IC': 'IC', 'UH': 'IC', 'CC': 'JC', 'FW': 'SL', 'CD': 'SN',
    'DT': 'DT', 'EX': 'EX', 'IN': 'IN',
    'MD': 'MD', 'PDT': 'PDT', 'RP': 'RP', 'TO': 'TO',
    'WDT': 'WDT', 'WP': 'WP', 'WP$': 'WP$', 'WRB': 'WRB',
    'JKB': 'JKB', 'JKC': 'JKC','JKG': 'JKG', 'JKO': 'JKO', 'JKQ': 'JKQ', 'JKS': 'JKS', 'JKV': 'JKV', 
    'JC': 'JC', 'JX': 'JX', 
    'EC': 'EC', 'EP': 'EP', 'EF': 'EF', 'ETN': 'ETN', 'ETM': 'ETM', 
    'XPN': 'XPN', 'XSN': 'XSN', 'XSV': 'XSV', 'XSA': 'XSA', 
    'XR': 'XR', 'SE': 'SE', 'SF': 'SF', 'SSO': 'SS', 'SSC': 'SS', 'SC': 'SP', 
    'SY': 'SO', 
    'SH': 'SH', 'SL': 'SL', 'SN': 'SN', 'LS': 'SW',
    'UNKNOWN': "UN", 'UNT': "UN", 'UNA': "UN", 'NA': "UN", 'E': "UN",
    #For KKMA
    "NNM": "NNB", "VXV": "VX", "VXA": "VX", "VXN": "VX", "MDT": "MM", "MDN": "MM", "MAC": "MAJ",
    "JKM": "JKB", "EPH": "EP", "EPT": "EP", "EPP": "EP", "ECE": "EC", "ECD": "EC", "ECS": "EC",
    "EFN": "EF", "EFQ": "EF", "EFO": "EF", "EFA": "EF", "EFI": "EF", "EFR": "EF", "ETD": "ETM",
    "XPV": "XPN", "OH": "SH", "OL": "SL", "ON": "SN", "UV": "UN", "UE": "UN", "SS": "SS", "SW": "SW",
    "SP": "SP", "UN": "UN", "SO": "SO", 
    #For Okt
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

# DocumentClustering
