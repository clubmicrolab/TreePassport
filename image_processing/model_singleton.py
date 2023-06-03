
from deepforest import main


class ModelSingleton:
    
    __shared_MODEL_instance = None
 
    @staticmethod
    def getInstance():
        if ModelSingleton.__shared_MODEL_instance == None:
            ModelSingleton()
        return ModelSingleton.__shared_MODEL_instance
 
    def __init__(self):
        """virtual private constructor"""
        if ModelSingleton.__shared_MODEL_instance != None:  
            raise Exception("This class is a singleton class !")
        else:
            ModelSingleton.__shared_MODEL_instance =  main.deepforest()
            ModelSingleton.__shared_MODEL_instance.use_release(check_release=True)  
            