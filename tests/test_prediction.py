import sys
sys.path.append('../') 
import pytest
from app.prediction import prediction 
from BertDataGenerator.data_generator import BertSemanticDataGenerator
import numpy as np

@pytest.fixture
def single_prediction():
    ideal = 'testing the ideal string'
    student ='testing the student string'
    answer_pair = np.array([[ideal,student]])
    query = BertSemanticDataGenerator(answer_pair, labels=None, batch_size=1, shuffle=False, include_targets=False,)
    query = query[0] 
    proba , idx = prediction(query)
    return proba[0][0] , idx

def test_single_prediction_not_none(single_prediction):
    assert single_prediction is not None

def test_idx_value(single_prediction):
    _, idx = single_prediction
    assert idx in [0, 1, 2], f"idx value {idx} is not in the expected range [0, 1, 2]"

def test_proba_shape(single_prediction):
    proba , _  = single_prediction
    assert proba.shape == (3,)

def test_proba_addition_is_one(single_prediction):
    proba,_ = single_prediction
    proba_p=proba[0]
    proba_i=proba[1]
    proba_c=proba[2]
    proba_total = proba_p+proba_i+proba_c
    assert proba_total == 1.0
