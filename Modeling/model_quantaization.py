import onnx
from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType, quantize_dynamic

# Define the path to the original and quantized ONNX models
onnx_model_path = "/content/drive/MyDrive/model.onnx"
quantized_model_path = "/content/drive/MyDrive/model_quantized.onnx"

# Perform dynamic quantization on the ONNX model
quantize_dynamic(
    model_input=onnx_model_path,        # Input model path
    model_output=quantized_model_path,  # Output model path
    weight_type=QuantType.QInt8         # Data type for quantization
)

print("Quantized model saved to:", quantized_model_path)