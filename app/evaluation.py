CORRECT_THRESHOLD_SOFT = 0.9
PARTIAL_THRESHOLD_SOFT = 0.6
INCORRECT_THRESHOLD_SOFT = 0.75
CORRECT_THRESHOLD_HARD = 0.95
PARTIAL_THRESHOLD_HARD = 0.65
INCORRECT_THRESHOLD_HARD = 0.7
REDUCTION_STEP = 0.05
#0 parrtil , 1 incorrect , 2 correct 
def custom_round(value):
    # Calculate the integer part and the fractional part
    integer_part = int(value)
    fractional_part = value - integer_part

    if fractional_part <= 0.3:
        return integer_part
    elif 0.4 <= fractional_part <= 0.7:
        return integer_part + 0.5
    else:
        return integer_part + 1
def calculate_ranges(max_marks):
    max_marks = float(max_marks)
    correct_start = int(max_marks * 0.50)
    correct_end = int(max_marks)

    partial_start = int(max_marks * 0.40)
    partial_end = int(max_marks * 0.60)

    incorrect_start = 0
    incorrect_end = int(max_marks * 0.40)

    correct_r = list(range(correct_start, correct_end + 1))[::-1]
    partial_r = list(range(partial_start, partial_end + 1))[::-1]
    incorrect_r = list(range(incorrect_start, incorrect_end+1))

    return correct_r, partial_r, incorrect_r

def calculate_marks_soft(max_marks , p_correct,p_incorrect,p_partial,idx,correct_r, partial_r, incorrect_r):
    print('correct:',correct_r)
    print('incorrect:',incorrect_r)
    print('partial:',partial_r)
    max_marks=float(max_marks)
    if idx ==0:
        if p_partial >=PARTIAL_THRESHOLD_SOFT:    ### for maximum marsk
            marks = partial_r[0]
            return marks
        else :
            
            diffrence = PARTIAL_THRESHOLD_SOFT - p_partial
            distance = round(diffrence / REDUCTION_STEP)
            reduction_factor = max_marks*0.1            ### reduction marks
            total_reduction = distance*reduction_factor
            marks = custom_round(partial_r[0] - total_reduction)
            if marks >= partial_r[-1]:
                return marks
            else :
                marks = partial_r[-1]
                return marks
    elif idx ==2:
        partial_contrib = 0
        if p_correct >=CORRECT_THRESHOLD_SOFT:    ### for maximum marsk
            marks = correct_r[0]
            return marks

        else :
            if p_partial >=0.10:
                partial_contrib = p_partial*max_marks*0.05
            diffrence = CORRECT_THRESHOLD_SOFT - p_correct
            distance = round(diffrence / REDUCTION_STEP)
            reduction_factor = max_marks*0.1            ### reduction marks
            total_reduction = distance*reduction_factor
            marks = custom_round(correct_r[0] - total_reduction - partial_contrib)
            if marks >= correct_r[-1]:
                return marks
            else :
                marks = correct_r[-1]
                return marks
    else :
        print("in the incorrect section")
        partital_contrib=0
        if p_incorrect >= INCORRECT_THRESHOLD_SOFT:
            marks = incorrect_r[0]
            return marks
        else :
            if p_partial >= 0.10:
                print("in the new section")
                partial_contrib = p_partial*max_marks*0.05
                print(max_marks)
                print(partial_contrib)
            diffrence =INCORRECT_THRESHOLD_SOFT - p_incorrect
            print("probab of incorrect : ", p_incorrect )
            print(diffrence)
            distance = round(diffrence/REDUCTION_STEP)
            print(distance)
            reduction_factor = max_marks*0.1
            print(reduction_factor)
            total_reduction = distance*reduction_factor
            print(total_reduction)
            marks = custom_round(incorrect_r[0] + total_reduction +partial_contrib)
            if marks <=incorrect_r[-1]:
                return marks
            else :
                marks = incorrect_r[-1]
                return marks

def calculate_marks_hard(max_marks , p_correct,p_incorrect,p_partial,idx,correct_r, partial_r, incorrect_r):
    max_marks = float(max_marks)
    if idx ==0:
        if p_partial >=PARTIAL_THRESHOLD_HARD:    ### for maximum marsk
            marks = partial_r[0]
            return marks
        else :
            diffrence = PARTIAL_THRESHOLD_HARD - p_partial
            distance = round(diffrence / REDUCTION_STEP)
            reduction_factor = max_marks*0.1           ### reduction marks
            total_reduction = distance*reduction_factor
            marks = custom_round(partial_r[0] - total_reduction)
            if marks >= partial_r[-1]:
                return marks
            else :
                marks = partial_r[-1]
                return marks
    elif idx ==2:
        if p_correct >=CORRECT_THRESHOLD_HARD:    ### for maximum marsk
            marks = correct_r[0]
            return marks
        else :
            diffrence = CORRECT_THRESHOLD_HARD - p_correct
            distance = round(diffrence / REDUCTION_STEP)
            reduction_factor = max_marks*0.1          ### reduction marks
            total_reduction = distance*reduction_factor
            marks = custom_round(correct_r[0] - total_reduction)
            if marks >= correct_r[-1]:
                return marks
            else :
                marks = correct_r[-1]
                return marks
    else :
        if p_incorrect >= INCORRECT_THRESHOLD_HARD:
            marks = incorrect_r[0]
            return marks
        else :
            diffrence =INCORRECT_THRESHOLD_HARD - p_incorrect
            distance = round(diffrence/REDUCTION_STEP)
            reduction_factor = max_marks*0.1
            total_reductin = distance*reduction_facotr
            marks = custom_round(incorrect_r[0] + total_reduction)
            if marks <=incorrect_r[-1]:
                return marks
            else :
                marks = incorrect_r[-1]
                return marks

def evaluation(checking_type,max_marks , p_correct,p_incorrect,p_partial,idx):
    correct_r, partial_r, incorrect_r = calculate_ranges(max_marks=max_marks)
    p_correct = custom_round(p_correct*10)/10
    p_incorrect = custom_round(p_incorrect*10)/10
    p_partial = custom_round(p_partial*10)/10
    if checking_type =='soft':
        marks = calculate_marks_soft(max_marks , p_correct,p_incorrect,p_partial,idx,correct_r, partial_r, incorrect_r)
        return marks
    else:
        marks = calculate_marks_hard(max_marks , p_correct,p_incorrect,p_partial,idx,correct_r, partial_r, incorrect_r)
        return marks 
print(evaluation('hard',15,0.4,0.3,0.5,0))