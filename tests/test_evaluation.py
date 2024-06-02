import sys 
sys.path.append('../')
import pytest
from app.evaluation import evaluation , custom_round , calculate_ranges ,calculate_marks_soft,calculate_marks_hard

def test_custom_round():
    t1 , t2 , t3 = 8.1,8.4,8.8
    et1 = 8.0
    et2 = 8.5
    et3 = 9.0
    rt1 = custom_round(t1)
    rt2 = custom_round(t2)
    rt3 = custom_round(t3)
    assert et1 ==rt1
    assert et2 ==rt2
    assert et3 ==rt3

def test_calculate_ranges_for_finitness_and_correctness():
    cr ,pr, ir = calculate_ranges(10)
    ecr = [10,9,8,7,6,5]
    epr = [6,5,4]
    eir = [0,1,2,3,4]
    assert cr ==ecr
    assert pr ==epr
    assert ir ==eir

def test_calcuate_marks_soft_for_none():
    m = calculate_marks_soft(15,0.8,0.1,0.1,2,[10,9,8,7,6,5],[4,5,6],[0,1,2,3,4])
    assert m is not None

def test_calcuate_marks_hard_for_none():
    m = calculate_marks_hard(15,0.8,0.1,0.1,2,[10,9,8,7,6,5],[4,5,6],[0,1,2,3,4])
    assert m is not None

def test_calculate_marks_soft_for_correctness():
    m = calculate_marks_soft(15,0.8,0.1,0.1,2,[10,9,8,7,6,5],[4,5,6],[0,1,2,3,4])
    em = 7
    assert m==em

def test_calculate_marks_hard_for_correctness():
    m = calculate_marks_hard(15,0.8,0.1,0.1,2,[10,9,8,7,6,5],[4,5,6],[0,1,2,3,4])
    em = 5
    assert m==em

def test_evaluation_for_none():
    ms = evaluation('soft',10,0.6,0.3,0.1,2)
    mh = evaluation('hard',10,0.6,0.3,0.1,2)
    assert ms is not None
    assert mh is not None
def test_evaluation_for_correctness():
    ms = evaluation('soft',10,0.6,0.3,0.1,2)
    mh = evaluation('hard',10,0.6,0.3,0.1,2)
    es = 5
    eh = 5
    assert ms==es
    assert mh == eh