#!/usr/bin/env python
# coding: utf-8

# ## Retrieval Evaluation

# In[1]:


import pandas as pd
from helper import get_data_path, get_openai_api_key

data_path = get_data_path()
df = pd.read_csv(data_path)

df.head()


# In[2]:


documents= df.to_dict(orient='records')
documents[0]


# In[3]:


prompt_template="""
You emulate a user of our fitness assistant.

Formulate 5 questions this user might ask based on a provided topic.
The records should contain the answer to the questions, and the questions should.
be complete and not too short. If possible, use as fewer words as possible from the record.

The record:

question: {question}
answer: {answer}
topic: {topic}

Provide the output in parsable JSON without using code blocks:

{{"question": ["question1", "question2", "question3", ..., "question5"]}}            
""".strip()

prompt = prompt_template.format(**documents[0])


# In[8]:


from openai import OpenAI

openai_api_key = get_openai_api_key()
client= OpenAI(api_key=openai_api_key)
model= "gpt-4o-mini"
response= client.chat.completions.create(
        model=model,
       messages=[
        {"role":"user", "content": prompt}
    ],
)


# In[12]:


import json

questions= json.loads(response.choices[0].message.content)


# In[6]:


def generate_questions(doc):
    prompt = prompt_template.format(**doc)

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": prompt}]
    )

    json_response = response.choices[0].message.content
    return json_response


# In[5]:


from tqdm.auto import tqdm


# In[14]:


import json
results = {}

for doc in tqdm(documents):
     doc_id = doc['id']
     if doc_id in results:
         continue
     questions_raw = generate_questions(doc)
     questions = json.loads(questions_raw)
     results[doc_id] = questions['question']


# In[18]:


final_results = []

for doc_id, questions in results.items():

    for q in questions:
        final_results.append(( doc_id,q))


# In[20]:


new_df= pd.DataFrame(final_results, columns=['id','question'])


# In[21]:


new_df.to_csv('ground-truth-retrieval.csv', index=False)


# In[22]:


get_ipython().system('head ground-truth-retrieval.csv')


# In[27]:


ground_truth = new_df.to_dict(orient='records')


# In[29]:


import minsearch
index= minsearch.Index(
    text_fields = ['question', 'answer', 'id', 'topic'],
    keyword_fields = ['id']
)


# In[30]:


index.fit(documents)


# In[31]:


def hit_rate(relevance_total):
    cnt = 0
    
    for line in relevance_total:
        if True in line:
            cnt = cnt + 1
    
    return cnt / len(relevance_total)

def mrr(relevance_total):
    total_score = 0.0
    
    for line in relevance_total:
        for rank in range(len(line)):
            if line[rank] == True:
                total_score = total_score + 1 / (rank + 1)
                break
    
    return total_score / len(relevance_total)


# In[32]:


def minsearch_search(query):
    boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results


# In[33]:


def evaluate(ground_truth, search_function):
    relevance_total = []

    for q in tqdm(ground_truth):
        doc_id = q['id']
        results = search_function(q)
        relevance = [d['id'] == doc_id for d in results]
        relevance_total.append(relevance)

    return {
        'hit_rate': hit_rate(relevance_total),
        'mrr': mrr(relevance_total),
    }


# In[34]:


from tqdm.auto import tqdm

evaluate(ground_truth, lambda q: minsearch_search(q['question']))


# ## Optimise parameters for retrieval

# In[38]:


# # Import optimisation libraries
# from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
# from hyperopt.pyll import scope

# split data into train, validation and test sets
df_validation= new_df[:100]
df_test = new_df[100:]


# In[49]:


import random

def simple_optimize(param_ranges, objective_function, n_iterations=10):
    best_params = None
    best_score = float('-inf')  # Assuming we're minimizing. Use float('-inf') if maximizing.

    for _ in range(n_iterations):
        # Generate random parameters
        current_params = {}
        for param, (min_val, max_val) in param_ranges.items():
            if isinstance(min_val, int) and isinstance(max_val, int):
                current_params[param] = random.randint(min_val, max_val)
            else:
                current_params[param] = random.uniform(min_val, max_val)
        
        # Evaluate the objective function
        current_score = objective_function(current_params)
        
        # Update best if current is better
        if current_score > best_score:  # Change to > if maximizing
            best_score = current_score
            best_params = current_params
    
    return best_params, best_score


# In[51]:


gt_val = new_df.to_dict(orient='records')


# In[46]:


def minsearch_search(query, boost=None):
    if boost is None:
        boost = {}

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=10
    )

    return results


# In[47]:


param_ranges = {
    'question': (0.0, 3.0),
    'topic': (0.0, 3.0)
}

def objective(boost_params):
    def search_function(q):
        return minsearch_search(q['question'], boost_params)

    results = evaluate(gt_val, search_function)
    return results['mrr']


# In[55]:


simple_optimize(param_ranges, objective, n_iterations=30)


# In[ ]:




