from route import app
from model_singleton import ModelSingleton 

if __name__=="__main__": 
    ModelSingleton()
    app.run(host="0.0.0.0", port=5000)

