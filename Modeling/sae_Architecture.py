import tensorflow as tf
import transformers 

# Define input layers
input_ids = tf.keras.layers.Input(shape=(max_length,), dtype=tf.int32, name="input_ids")
attention_masks = tf.keras.layers.Input(shape=(max_length,), dtype=tf.int32, name="attention_masks")
token_type_ids = tf.keras.layers.Input(shape=(max_length,), dtype=tf.int32, name="token_type_ids")

# Loading pretrained BERT model
bert_model = transformers.TFBertModel.from_pretrained("bert-base-uncased")

# Connect inputs to the BERT model
bert_output = bert_model(input_ids, attention_mask=attention_masks, token_type_ids=token_type_ids)

# Bidirectional LSTM with batch normalization and dropout
bi_lstm = tf.keras.layers.Bidirectional(
    tf.keras.layers.LSTM(64, return_sequences=True, dropout=0.3)
)(bert_output.last_hidden_state)
bi_lstm = tf.keras.layers.BatchNormalization()(bi_lstm)

# Applying hybrid pooling approach to bi_lstm sequence output
avg_pool = tf.keras.layers.GlobalAveragePooling1D()(bi_lstm)
max_pool = tf.keras.layers.GlobalMaxPooling1D()(bi_lstm)
concat = tf.keras.layers.concatenate([avg_pool, max_pool])

# Additional dropout layer
dropout = tf.keras.layers.Dropout(0.5)(concat)

# Dense layer with softmax activation
output = tf.keras.layers.Dense(3, activation="softmax")(dropout)

# Model definition
model = tf.keras.models.Model(inputs=[input_ids, attention_masks, token_type_ids], outputs=output)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

model.summary()
