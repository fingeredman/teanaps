import pickle

class FileHandler():  
    def __init__(self):
        None
        
    def save_data(self, file_name, data):
        with open(file_name, "wb") as f:
            pickle.dump(data, f, -1)
        
    def load_data(self, file_name):
        with open(file_name, "rb") as f:
            data = pickle.load(f)
        return data
    
    def save_txt(self, file_name, line_list, encoding="utf-8", separator="\t"):
        f = open(file_name, "w", encoding=encoding)
        for line in line_list:
            if type(line) == "str":
                f.write(line.replace("\n", " "))
            else:
                new_line = ""
                for col in line:
                    new_line += col.replace("\n", " ") + separator
                f.write(new_line.strip())
            f.write("\n")
        f.close()
    
    def load_txt(self, file_name, encoding="utf-8", separator="\t"):
        line_list = []
        f = open(file_name, encoding=encoding)
        for line in f:
            line = line.replace("\n", " ").split(separator)
            line_list.append(line)
        return line_list