from time import time
import ingest
from openai import OpenAI
from dotenv import load_dotenv
import json



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
    
    answer= reponse.choices[0].message.content
    
    token_stats = {
        "prompt_tokens": reponse.usage.prompt_tokens,
        "completion_tokens": reponse.usage.completion_tokens,
        "total_tokens": reponse.usage.total_tokens,
    }
    
    return answer, token_stats

evaluation_prompt_template = """
You are an expert evaluator for a RAG system.
Your task is to analyze the relevance of the generated answer to the given question.
Based on the relevance of the generated answer, you will classify it
as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

Here is the data for evaluation:

Question: {question}
Generated Answer: {answer}

Please analyze the content and context of the generated answer in relation to the question
and provide your evaluation in parsable JSON without using code blocks:

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
  "Explanation": "[Provide a brief explanation for your evaluation]"
}}
""".strip()


def evaluate_relevance(query, answer):
    prompt_answer = evaluation_prompt_template.format(question=query, answer=answer)
    evaluation, tokens = llm(prompt_answer)

    try:
        json_eval = json.loads(evaluation)
        return json_eval, tokens
    
    except json.JSONDecodeError:
        
        result={
            "Relevance":"Unknown",
            "Explanation":"Failed to parse evaluation"
        }
        return result, tokens

# def calculate_openai_cost(model="gpt-4o-mini", tokens):
#     openai_cost = 0

#     if model == "gpt-4o-mini":
#         openai_cost = (
#             tokens["prompt_tokens"] * 0.00015 + tokens["completion_tokens"] * 0.0006
#         ) / 1000
#     else:
#         print("Model not recognized. OpenAI cost calculation failed.")

#     return openai_cost
    

def rag(query): 
    t0= time()
    
    results= search(query)
    prompt= build_prompt(query=query,search_results=results)
    response, token_stats = llm(prompt=prompt)
    relevance, rel_token_stats= evaluate_relevance(query, response)
    
    # openai_cost_rag = calculate_openai_cost("gpt-4o-mini", token_stats)
    # openai_cost_eval = calculate_openai_cost("gpt-4o-mini", rel_token_stats)
    
    # openai_cost= openai_cost_rag + openai_cost_eval
    t1= time()
    
    took= t1 - t0
    
    answer_data= { "answer": response,
                  "model_used": 'gpt-4o-mini',
                  "response_time": took,
                  "relevance": relevance.get("Relevance","UNKNOWN"), 
                  "relevance_explanation": relevance.get("Explanation","Failed to parse evaluation"),
                  "prompt_tokens": token_stats['prompt_tokens'],  
                  "completion_tokens": token_stats['completion_tokens'],  
                  "total_tokens": rel_token_stats['total_tokens'],  
                  "eval_prompt_tokens": rel_token_stats["prompt_tokens"],  
                  "eval_completion_tokens": rel_token_stats["completion_tokens"],  
                  "eval_total_tokens": token_stats["total_tokens"],  
                 "openai_cost": 0
    }
    
    
    return answer_data