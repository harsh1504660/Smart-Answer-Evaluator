import openai 
import anthropic
import pandas as pd

data = pd.read_csv('testing.csv')
std_prompt = "Generate four responses to the question given below. The first response should be the ideal answer, named 'ideal answer'. The second response should be the correct answer with variation, named 'correct answer'. The third response should contain partially correct information, named 'partial correct answer''. Finally, the fourth response should be entirely incorrect, named 'incorrect answer'."
extension = "\n answers must be long answers containing 200 to 250 words , in incorrect and partial correct answer manipulate the dates and name which occured in ideal and correct answrs , also change the length of ideal and correct answers "
q = "Evaluate the administrative policies implemented by Sambhaji Maharaj and how they reflected the legacy of Shivaji Maharaj's rule, considering justice, revenue systems, and punishment for rebellious landlords."
api_key = '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'
openai.api_key = api_key
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "user", "content": "{}+{}+{}".format(std_prompt,extension,q)
      }
      ],max_tokens=4000
      )
print("request sent")

print("fetching the results")
text = response.choices[0].message['content']
text = text.replace('*'," ")
print("TEXT FROM GPT-3.5 : {}".format(text))
data = data._append(pd.Series(text, index=data.columns), ignore_index=True)

print("\n\n\n\n\n")


client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)

MODEL_H = "claude-3-haiku-20240307"
MODEL_S = "claude-3-sonnet-20240229"
message = client.messages.create(
        model=MODEL_S,
        max_tokens=3000,
        messages=[
            {"role": "user", "content": "{}+{}+{}".format(std_prompt,extension,q)}
        ]
    )


print("request sent")

print("fetching the results")
texT_0 = message.content[0].text
text_0 = text.replace('*'," ")
print("TEXT FROM CLAUDE-H : {}".format(text))
data = data._append(pd.Series(text, index=data.columns), ignore_index=True)


data.to_csv('testing.csv')