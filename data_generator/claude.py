import anthropic
from IPython.display import display
from IPython.display import Markdown
import random
import pandas as pd
import re
import pygame
import time
from questions import history_sa_9


client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)

MODEL_S = "claude-3-sonnet-20240229"
MODEL_H = "claude-3-haiku-20240307"
MODEL_O = "claude-3-opus-20240229"


def play_music(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

"""\nall answers must be long answer and contain minimum of 200 words ,include all relevent information like important names , dates or incidents',
  '\nall answers should be long answers and length of incorect answer must be equal to the ideal answer ',
  '\nall answers must be long answers containing 150 to 200 words, consider the relevent dates and name for ideal and correct answer and for partial and incorrect answer manipulate these names and dates',
  '\nanswers must be long answers containing 200 to 250 words , in incorrect and partial correct answer manipulate the dates and name which occured in ideal and correct answrs , also change the length of ideal and correct answers ',
  '\nanswers must contain 200 to 250 words as they have marks weightage of 10 marks , vary the length of answers'"""
def diffrentiator():
  diff = ["\n all answers should be upto 100 words and don't mention the word count",
  "",
  "",
  "\nanswers must contain 100 to 200 words as they have marks weightage of 10 marks , vary the length of answers , don't mention the word count",
  "\nthe lenght of all the answers should be same or close to equal , don't need to mention the word count"
  ]
  rand = random.randint(0,4)
  return diff[rand]
# Define a prompt
std_prompt = 'Generate four responses to the question given below. The first response should be the ideal answer, named "ideal answer". The second response should be the correct answer with variation, named "correct answer". The third response should contain partially correct information, named "partial correct answer". Finally, the fourth response should be entirely incorrect, named "incorrect answer".do not compromise with the name of answer its essential for me toextract the text'
columns = ['ideal answer','students answer','lable']
#data = pd.DataFrame(columns=columns)
data = pd.read_csv('data_history_p3.csv',usecols=['ideal answer','students answer','lable'])
print(data.shape)
count = 0

t_time = time.time()
for q in history_a_9:

  start = time.time()
  count=count +1
  extention = diffrentiator()
  try:
    message = client.messages.create(
        model=MODEL_S,
        max_tokens=3500,
        messages=[
            {"role": "user", "content": "{}+{}+{}".format(std_prompt,extention,q)}
        ]
    )
    print("request sent")

    print("fetching the results")
    text = message.content[0].text
    text = text.replace('*'," ")
    text = text.replace('"','')
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
    time.sleep(6)
    print('cool down period ended')
  except Exception as e:
    data.to_csv('data_history_p3.csv')
    print("error occured",e,'\n\n data stored succesully until : {}'.format(count))
    print("current question : {}".format(q))
    play_music('brass-fail-1-b-185075.mp3')
    pygame.time.wait(5000)
    exit()


data.to_csv('data_history_p3.csv')
e_time = int((time.time() - t_time) / 60)
print("DATA EXTRACTION COMPLETED !!!")
print("TIME TAKEN : {} Min".format(e_time))
play_music('i-see-money-181273.mp3')
pygame.time.wait(5000)

