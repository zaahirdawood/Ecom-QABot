from time import time
import ingest
from openai import OpenAI
from dotenv import load_dotenv



load_dotenv()
client= OpenAI()
index= ingest.load_index()


def search(query):
    boost = {}
    
    results = index.search(query=query,
                           boost_dict=boost,
                           num_results=10)
    return results

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
    t0= time()
    results= search(query)
    prompt= build_prompt(query=query,search_results=results)
    response= llm(prompt=prompt)
    t1= time()
    
    took= t1 - t0
    
    answer_data= { "answer": response,
                  "model_used": 'gpt-4o-mini',
                  "response_time": took,
                  "relevance": 0, 
                  "relevance_explanation": "RELEVANT",
                  "prompt_tokens": len(prompt.split()),  
                  "completion_tokens": len(response.split()),  
                  "total_tokens": len(prompt.split()) + len(response.split()),  
                  "eval_prompt_tokens": 0,  
                  "eval_completion_tokens": 0,  
                  "eval_total_tokens": 0,  
                 "openai_cost": 0 
    }
    
    
    return answer_data