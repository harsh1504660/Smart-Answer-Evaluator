from BertDataGenerator.data_generator import BertSemanticDataGenerator
from huggingface_hub import hf_hub_download
import onnxruntime
import numpy as np

model_name='harshai1504/sae'
model = hf_hub_download(repo_id=model_name, filename="sae_quantized_8000.onnx",use_auth_token='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')
session = onnxruntime.InferenceSession(model)

answer_pair = np.array([["ideal string", "student string "]])
query_generator = BertSemanticDataGenerator(answer_pair, labels=None, batch_size=1, shuffle=False, include_targets=False,)
query_data = query_generator[0]
output = session.run(None, {'input_ids': query_data[0], 'attention_masks': query_data[1], 'token_type_ids': query_data[2]})
print(output)
print(output[0][0][0])