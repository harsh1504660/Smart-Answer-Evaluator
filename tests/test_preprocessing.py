import sys
sys.path.append('../')
import pytest
import numpy as np
from app.preprocess import prep, dataloader,remove_stopwords
from app.stopwords import STOPWORDS
from app.grammer import correct_grammar
from app.ocr import ocr


def test_correct_grammar():
    text = 'tis is an ideal exaple'
    expected = 'This is an ideal example.'
    result = correct_grammar(text)
    assert result == expected 

def test_ocr_for_image():
    img = r'image_test\image.png'
    result = ocr(img)
    assert isinstance(result, str)


def test_remove_stopwords():
    text = "This is a test sentence and it has stopwords."
    expected = "test sentence stopwords."
    result = remove_stopwords(text)
    assert result == expected, f"Expected '{expected}', but got '{result}'"


def test_dataloader():
    ideal = "Ideal answer text."
    student = "Student answer text."
    query_data = dataloader(ideal, student)
    
    assert len(query_data) == 3, f"Expected length of 3, but got {len(query_data)}"
    

    assert all(isinstance(q, np.ndarray) for q in query_data), "Not all elements are numpy arrays"
    

    input_ids, attention_masks, token_type_ids = query_data
    expected_shape = (1, 512)
    assert input_ids.shape == expected_shape, f"Expected shape {expected_shape}, but got {input_ids.shape}"
    assert attention_masks.shape == expected_shape, f"Expected shape {expected_shape}, but got {attention_masks.shape}"
    assert token_type_ids.shape == expected_shape, f"Expected shape {expected_shape}, but got {token_type_ids.shape}"