import concurrent.futures
import jpype

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