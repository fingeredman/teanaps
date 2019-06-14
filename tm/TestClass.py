import mecab

class TextClass():  
    def __init__(self):
        self.result = [1, 2, 3, 4]
        
    def get_result(self):
        mc = mecab.MeCab()
        return mc.pos("아버지가 방에 들어가신다.")