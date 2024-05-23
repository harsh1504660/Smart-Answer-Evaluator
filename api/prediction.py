#import tensorflow as tf
#import transformers
#from transformers import TFBertModel
import onnxruntime
import numpy as np
import time
from huggingface_hub import hf_hub_download
#from preprocess import BertSemanticDataGenerator


def prediction(query):
    start = time.time()
    #tf.keras.utils.get_custom_objects()['TFBertModel'] = TFBertModel

    #model =tf.keras.models.load_model(r'E:\NLP\6-Projects\11-Smart_Answer_Checker\Modeling\models\model2.h5')

    #proba = model.predict(query)[0]  # Assuming you want predictions for the first sample in the batch
    #idx = np.argmax(proba)
    #proba_ = f"{proba[idx]: .2f}%" 
    
 
    model_name='harshai1504/sae'
    model = hf_hub_download(repo_id=model_name, filename="model_quantized_8000.onnx", use_auth_token='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')
    print("model is loaded")
    session = onnxruntime.InferenceSession(model)
    print("model is loaded")
    # Load the model

    # Prepare data for predictio

    # Retrieve a batch of data
    #query_data = query[0]  # Assuming you want to predict for the first batch only

    # Perform prediction
    output = session.run(None, {'input_ids': query[0], 'attention_masks': query[1], 'token_type_ids': query[2]})
    print('prediction success')
    idx = np.argmax(output)
    e_time = time.time()
    print("time taken : {}".format(e_time-start))
    print(output[0][0])
    print(idx)
    return output, idx
   # return proba ,idx

