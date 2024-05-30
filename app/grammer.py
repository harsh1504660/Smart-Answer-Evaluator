import openai
import re
import time
import random
import os
# Set your OpenAI API key
api_key = os.getenv('gpt_key')
openai.api_key = api_key
std_prompt = 'correct the grammer\n'

def correct_grammar(sentence):
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": "{}+{}".format(std_prompt,sentence)}
        ]
        )
        print("request sent")

        print("fetching the results")
        text = response.choices[0].message['content']
        text = text.replace('*'," ")
        print(text)
        print('\n')
    except Exception as e:
        print(e)
        exit()