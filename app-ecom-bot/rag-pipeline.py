#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('head Ecommerce_FAQ_Chatbot_dataset.json')


# ## Generating unique ID's

# In[2]:


# Re-load the document since it was not defined in this new code execution.
import json
import hashlib

with open('Ecommerce_FAQ_Chatbot_dataset.json', 'rt') as f_in:
    documents= json.load(f_in)

def generate_document_id(doc):
    combined = f"{doc['question']}-{doc['answer'][:10]}"
    hash_object = hashlib.md5(combined.encode())
    hash_hex = hash_object.hexdigest()
    document_id = hash_hex[:8]
    return document_id

for qa_pair in documents['questions']:
    doc_id = generate_document_id(qa_pair)
    qa_pair['id'] = doc_id  # Add the generated ID to the question-answer pair


# In[3]:


hashes = []

for doc in documents['questions']:
    hashes.append(doc)


# In[4]:


hashes[0]


# In[6]:


# check if hash unique hash id count and len of questions ar equal
len(hashes) == len(documents['questions'])


# In[7]:


with open('documents-with-ids.json', 'wt') as f_out:
    json.dump(hashes, f_out, indent=2)


# In[8]:


get_ipython().system('head documents-with-ids.json')


# ## Chunking

# In[9]:


from openai import OpenAI
from dotenv import load_dotenv


# In[10]:


load_dotenv()


# In[11]:


import json
with open("documents-with-ids.json",'rt') as f_out:
    documents= json.load(f_out)


# In[12]:


documents[0]


# In[13]:


prompt=f"""Review {documents} and create output a new .json file that contains a key which categorises the type of question
            based on the topics they belong to, some high level topics are:
                1. Account & Registration
                2. Payments & Pricing
                3. Shipping & Delivery
                4. Returns & Refunds
                5. Order Management
                6. Customer Support & Services
                7. Product Information
                
            The topics above must be introduced as a new key "topic" for each question, answer pair.
            
            return only the contents found in between ```json``` nothing else.
"""


# In[16]:


client= OpenAI()
model= "gpt-4o-mini"
response= client.chat.completions.create(
        model=model,
       messages=[
        # {"role": "system", "content": "You are a helpful assistant."},
        {"role":"user", "content": prompt}
    ],
)


# In[17]:


def format_output(response):
    data_to_view = {
        "response": response.choices[0].message.content.replace("```json",'').replace('```','')
    }
    return data_to_view['response']

response_string = format_output(response)


# In[18]:


dat = json.loads(response_string)


# In[20]:


import pandas as pd
dat_df = pd.DataFrame(dat)

dat_df.head()


# In[21]:


dat_df.to_csv('chunked_data.csv', index=False)


# ## Indexing

# In[227]:


dat_df.columns


# In[229]:


import minsearch


# In[234]:


index= minsearch.Index(
    text_fields = ['question', 'answer', 'id', 'topic'],
    keyword_fields = []
)


# In[244]:


query = "How can I track an order"


# In[239]:


dco = dat_df.to_dict(orient='records')


# In[240]:


index.fit(dco)


# In[245]:


index.search(query, num_results=3)


# ## RAG Flow

# In[253]:


entry_template= """
question:{question}
answer:{answer}
topic:{topic}
""".strip()

prompt_template = """You are a customer service representative for an e-commerce website. Answer the QUESTION based on the CONTEXT from our frequently asked queries database.
Use only facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT: {context}
""".strip()


# In[252]:


def search(query):
    boost = {'question': 3.0, "topic":0.5}
    
    results = index.search(query=query,
                           boost_dict=boost,
                           num_results=10)
    return results

def build_prompt(query, search_results):
    context= ""
    
    for doc in search_results:
        context= context + entry_template.format(**doc) + "\n\n"
        
    prompt= prompt_template.format(question=query, context= context).strip()
    
    return prompt

def llm(prompt):
    
    reponse= client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role":"user","content":prompt}]
    )
    
    return reponse.choices[0].message.content

def rag(query):
    results= search(query)
    prompt= build_prompt(query=query,search_results=results)
    response= llm(prompt=prompt)
    return response


# In[258]:


query= "I don't understand how to track my order"
answer= rag(query)
print(answer)

