import requests

url = 'https://smart-answer-evaluator-api.onrender.com'
payload = {'ideal': 'Deom Ideal Answer', 'student': 'Demo Student Answer'}
headers = {'Content-Type': 'application/json'}

response = requests.post(url, json=payload, headers=headers)
data = response.json()
print(data)
print("Partial Correct Probablity : ",data['proba'][0])
print("Incorrect Probablity : ",data['proba'][1])
print("Correct Probablity : ",data['proba'][2])
print("Class : ",data['idx'])