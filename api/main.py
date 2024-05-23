from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api.preprocess import prep, dataloader
from api.prediction import prediction
import numpy as np
import uvicorn

app = FastAPI()

class PredictRequest(BaseModel):
    ideal: str
    student: str

@app.get('/')
def hello():
    print('hello world')
    return {"hello": "world"}

@app.post('/pred')
def predict(request: PredictRequest):
    try:
        print(request.ideal)
        print(request.student)
        
        ideal = prep(request.ideal)
        student = prep(request.student)
        
        print(ideal)
        print(student)
        
        query = dataloader(ideal, student)
        print("query sent")
        
        proba, idx = prediction(query)
        
        # Convert numpy array to a list
        if isinstance(proba, np.ndarray):
            proba = proba.tolist()
        elif isinstance(proba, list):
            proba = [p.tolist() for p in proba if isinstance(p, np.ndarray)]

        # Convert idx to Python int if it's a numpy int
        if isinstance(idx, np.integer):
            idx = int(idx)
        
        # Create the response
        response = {
            "proba": proba[0][0],
            "idx": idx
        }
        
        print(f"Response: {response}")
        return response

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

