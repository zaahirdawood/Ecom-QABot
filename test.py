import requests

url='http://127.0.0.1:5000/question'

#'http://0.0.0.0:5001/question'
#or
#'http://127.0.0.1:5000/question'

question= (
    "How can I find out where is my order?"
)

data= {'question':question}


response= requests.post(url=url, json=data).json()


print(response)