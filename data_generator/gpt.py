import openai
import pandas as pd
import re
import time
import pygame
from questions import history_sa_9
import random
# Set your OpenAI API key
api_key = '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' ### harsh
#api_key = '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' ### monita


# Initialize the OpenAI API client
def play_music(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
openai.api_key = api_key
""" diff = ['\ngive long answer , while giving the partial correct answers and incorrect answers make sure to miss some important information , all the naswers must more than 200 words and lenght of all the answrs must be close to equal\n\n',
  '\nmake sure every answer must be the lenght of 100 to 150 words , include all relevent information like important names , dates or incidents \n\n',
  '\nall answers must be more than 100 words , lenght of incorect answer must be equal to the ideal answer\n\n',
  '\nall answers must be more than 100 words ,include all relevent information like important names , dates or incidents and for partial correct and incorrect change or use the wrong name and wrong dates \n\n',
  '\nin incorrect and partial correct answer manipulate the dates and name which occured in ideal and correct answrs , add all relevent information can make the ansers long.\n\n',
  '\nmarks for the answers is 5 so give the answers like that , vary the lenngth of answers , you can give the long answers as well \n\n',
  '\nall answers must be more than 100 words , for correct answer give most of the information correct from ideal one and for the partial correct and incorrect give all the information from ideal answer but manipulate it the important things , names , placses , scenes and information \n\n']
"""
def diffrentiator():
  diff = ['\nall answers must be long answer and contain minimum of 200 words ,include all relevent information like important names , dates or incidents',
  '\nall answers should be long answers and length of incorect answer must be equal to the ideal answer ',
  '\nall answers must be long answers containing 150 to 200 words, consider the relevent dates and name for ideal and correct answer and for partial and incorrect answer manipulate these names and dates',
  '\nanswers must be long answers containing 200 to 250 words , in incorrect and partial correct answer manipulate the dates and name which occured in ideal and correct answrs , also change the length of ideal and correct answers ',
  '\nanswers must contain 200 to 250 words as they have marks weightage of 10 marks , vary the length of answers']
  rand = random.randint(0,4)
  return diff[rand]
# Define a prompt
std_prompt = 'Generate four responses to the question given below. The first response should be the ideal answer, named "ideal answer". The second response should be the correct answer with variation, named "correct answer". The third response should contain partially correct information, named "partial correct answer". Finally, the fourth response should be entirely incorrect, named "incorrect answer".'
columns = ['ideal answer','students answer','lable']
#data = pd.DataFrame(columns=columns)
data = pd.read_csv('data_history_p4.csv',usecols=['ideal answer','students answer','lable'])
print(data.shape)
count = 0

t_time = time.time()
for q in history_sa_9:

  start = time.time()
  count=count +1
  extention = diffrentiator()
  try:
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "user", "content": "{}+{}+{}".format(std_prompt,extention,q)}
      ]
      )
    print("request sent")

    print("fetching the results")
    text = response.choices[0].message['content']
    text = text.replace('*'," ")
    print(text)
    print('\n')
    print("fetching the results.....complete")
    ideal_regex = r"Ideal\s*answer:\s*(.*?)\s*Correct\s*answer:"
    correct_regex = r"Correct\s*answer:\s*(.*?)\s*Partial\s*correct\s*answer:"
    partial_regex = r"Partial\s*correct\s*answer:\s*(.*?)\s*Incorrect\s*answer:"
    incorrect_regex = r"Incorrect\s*answer:\s*(.*?)$"

  # Extract responses using regular expressions
    ideal_match = re.search(ideal_regex, text,re.IGNORECASE | re.DOTALL)
    correct_match  = re.search(correct_regex, text,re.IGNORECASE | re.DOTALL)
    partial_match= re.search(partial_regex, text,re.IGNORECASE | re.DOTALL)
    incorrect_match = re.search(incorrect_regex, text,re.IGNORECASE | re.DOTALL)

    ideal_answer = ideal_match.group(1) if ideal_match else None
    correct_answer = correct_match.group(1) if correct_match else None
    partial_answer = partial_match.group(1) if partial_match else None
    incorrect_answer = incorrect_match.group(1) if incorrect_match else None
    row1 = [ideal_answer, correct_answer, 'correct']
    row2 = [ideal_answer, partial_answer, 'partially correct']
    row3 = [ideal_answer, incorrect_answer, 'incorrect']

    data = data._append(pd.Series(row1, index=data.columns), ignore_index=True)
    data = data._append(pd.Series(row2, index=data.columns), ignore_index=True)
    data = data._append(pd.Series(row3, index=data.columns), ignore_index=True)
    print("time taken : ",float(time.time() - start)," S")
    print('Entry no. {} added sucessfully'.format(count))
    print("Cool Down period starts")
    time.sleep(20)
    print('cool down period ended')
  except Exception as e:
    data.to_csv('data_history_p4.csv')
    print("error occured",e,'\n\n data stored succesully until : {}'.format(count))
    print("current question : {}".format(q))
    play_music('brass-fail-1-b-185075.mp3')
    pygame.time.wait(5000)
    exit()


data.to_csv('data_history_p4.csv')
e_time = int((time.time() - t_time) / 60)
print("DATA EXTRACTION COMPLETED !!!")
print("TIME TAKEN : {} Min".format(e_time))
play_music('i-see-money-181273.mp3')
pygame.time.wait(5000)

