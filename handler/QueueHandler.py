import concurrent.futures
import jpype

'''
class MyFunction():
    def __init__(self):
        #jpype.attachThreadToJVM()
        None
        
    def test_function(self, parm_dict):
        #jpype.attachThreadToJVM()
        print_list = parm_dict["print_list"]
        for i in print_list:
            print(i)
            time.sleep(1)
        result = {
            "request_id": parm_dict["request_id"], 
            "result": "complete."
        }
        return result
        
from teanaps.handler.QueueHandler import QueueHandler

qh = QueueHandler(3)
for i in range(10):
    mf = MyFunction()
    input_function = mf.test_function
    parm_dict = {
        "request_id" : i,
        "print_list": ["aaa", "bbb", "ccc", "ddd"]
    }
    qh.add_lambda(input_function, parm_dict)
'''

class QueueHandler():
    def __init__(self, thread_count):
        self.lambda_count = 0
        self.pool = concurrent.futures.ThreadPoolExecutor(thread_count)
        self.result_dict = {}
        
    def add_lambda(self, input_function, parm_dict):
        self.lambda_count += 1
        self.call_lambda(input_function, parm_dict)
        
    def call_lambda(self, input_function, parm_dict):
        future = self.pool.submit(input_function, parm_dict)
        future.add_done_callback(self.done)
    
    def done(self, f):
        f.cancel()
        self.lambda_count -= 1
        result = f.result()
        self.result_dict[result["request_id"]] = result["result"]
        if self.lambda_count == 0:
            print("done")
        else:
            print(self.lambda_count)
    
    def get_result(self):
        return self.result_dict