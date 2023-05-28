import requests
d = {'state':'Orissa','district':'Gajapati','date':'2023-02-01'}
r = requests.post('http://0728-202-160-145-20.ngrok-free.app/predict',json=d)
print('Connection Established Succesfully')
print(r.json())
d1 = {'state':'Meghalaya','district':'East Garo Hills','date':'2024-05-06'}
r1 = requests.post('http://0728-202-160-145-20.ngrok-free.app/predict',json=d1)
print(r1.json())
d2 = {'state':'Gujarat','district':'Ahmedabad','date':'2024-09-01'}
r2 = requests.post('http://0728-202-160-145-20.ngrok-free.app/predict',json=d2)
print(r2.json()) 