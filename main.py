print("Hello World")
import openai

'''
* code provided by Nessie from CapitalOne

import requests
import json 

customerId = 'your customerId here'
apiKey = 'your apiKey here'

url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId,apiKey)
payload = {
  "type": "Savings",
  "nickname": "test",
  "rewards": 10000,
  "balance": 10000,	
}
# Create a Savings Account
response = requests.post( 
	url, 
	data=json.dumps(payload),
	headers={'content-type':'application/json'},
	)

if response.status_code == 201:
	print('account created')
view raw
'''