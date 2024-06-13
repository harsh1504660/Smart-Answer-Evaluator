import tensorflow as tf
import tf2onnx
import onnx

# Load your TensorFlow Keras model
tf.keras.utils.get_custom_objects()['TFBertModel'] = TFBertModel
model = tf.keras.models.load_model('/content/drive/MyDrive/model.h5')

# Convert the TensorFlow Keras model to ONNX format
onnx_model, _ = tf2onnx.convert.from_keras(model)

# Save the ONNX model to a file
onnx_file_path = "/content/drive/MyDrive/model.onnx"
onnx.save(onnx_model, onnx_file_path)
