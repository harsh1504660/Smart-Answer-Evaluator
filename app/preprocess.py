import tensorflow as tf
from transformers import TFBertModel
import re
import numpy as np
from app.stopwords import STOPWORDS
import transformers
from app.grammer import correct_grammar
#nltk.download('stopwords')

# Register the custom object (TFBertModel) with TensorFlow
print("stop words is removeed")
def remove_stopwords(text):
    words = text.split()
    filtered_text = [word for word in words if word.lower() not in STOPWORDS]
    return ' '.join(filtered_text)
def prep(text):

    text = text.replace('\n',' ')
    text = text.replace('/n',' ')
    processed_text = correct_grammar(text)
    text = processed_text.lower()
    text = re.sub(r'[^\w\s]', '',text)
    text = remove_stopwords(text)
    # Join filtered tokens back into a string
    return text

def dataloader(ideal , student):
    #tf.keras.utils.get_custom_objects()['TFBertModel'] = TFBertModel

    #model =tf.keras.models.load_model(r'E:\NLP\6-Projects\11-Smart_Answer_Checker\Modeling\models\model2.h5')
    answer_pair = np.array([[str(ideal),str(student)]])
    query = BertSemanticDataGenerator(
        answer_pair , labels=None,batch_size=1,shuffle=False,include_targets=False)
    query_data = query[0] 
    return query_data

class BertSemanticDataGenerator(tf.keras.utils.Sequence):
    """Generates batches of data.

    Args:
        sentence_pairs: Array of premise and hypothesis input sentences.
        labels: Array of labels.
        batch_size: Integer batch size.
        shuffle: boolean, whether to shuffle the data.
        include_targets: boolean, whether to incude the labels.

    Returns:
        Tuples `([input_ids, attention_mask, `token_type_ids], labels)`
        (or just `[input_ids, attention_mask, `token_type_ids]`
         if `include_targets=False`)
    """

    def __init__(
        self,
        sentence_pairs,
        labels,
        batch_size=32,
        shuffle=True,
        include_targets=True,
    ):
        self.sentence_pairs = sentence_pairs
        self.labels = labels
        self.shuffle = shuffle
        self.batch_size = batch_size
        self.include_targets = include_targets

        # Load our BERT Tokenizer to encode the text.
        # We will use base-base-uncased pretrained model.
        self.tokenizer = transformers.BertTokenizer.from_pretrained(
            "bert-base-uncased", do_lower_case=True
        )
        self.indexes = np.arange(len(self.sentence_pairs))
        self.on_epoch_end()

    def __len__(self):
        # Denotes the number of batches per epoch.
        return len(self.sentence_pairs) // self.batch_size

    def __getitem__(self, idx):
        # Retrieves the batch of index.
        indexes = self.indexes[idx * self.batch_size : (idx + 1) * self.batch_size]
        sentence_pairs = self.sentence_pairs[indexes]

        # With BERT tokenizer's batch_encode_plus batch of both the sentences are
        # encoded together and separated by [SEP] token.
        encoded = self.tokenizer.batch_encode_plus(
            sentence_pairs.tolist(),
            add_special_tokens=True,
            max_length=512,
            return_attention_mask=True,
            return_token_type_ids=True,
            pad_to_max_length=True,
            return_tensors="tf",
            truncation=True
        )

        # Convert batch of encoded features to numpy array.
        input_ids = np.array(encoded["input_ids"], dtype="int32")
        attention_masks = np.array(encoded["attention_mask"], dtype="int32")
        token_type_ids = np.array(encoded["token_type_ids"], dtype="int32")

        # Set to true if data generator is used for training/validation.
        if self.include_targets:
            labels = np.array(self.labels[indexes], dtype="int32")
            return [input_ids, attention_masks, token_type_ids], labels
        else:
            return [input_ids, attention_masks, token_type_ids]

    def on_epoch_end(self):
        # Shuffle indexes after each epoch if shuffle is set to True.
        if self.shuffle:
            np.random.RandomState(42).shuffle(self.indexes)
