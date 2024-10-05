# Ecom-QABot

E-commerce Chatbot with Retrieval-Augmented Generation (RAG)

## Problem Statement

Creating responsive and engaging chatbots has traditionally involved manually labeling responses to predefined questions. This approach often results in robotic interactions, causing users to feel frustrated and prompting them to seek human assistance. In the rapidly evolving landscape of E-commerce, there is a pressing need for chatbots that can engage customers organically, enhancing their experience and streamlining support.

## Data Description

Link to dataset: [E-commerce-faq](https://www.kaggle.com/datasets/saadmakhdoom/ecommerce-faq-chatbot-dataset)

To tackle the problem, we utilize the following datasets:

	1.	E-commerce Product Data: This dataset includes information about products, such as names, descriptions, prices, and categories. This information will help the chatbot retrieve relevant product details based on customer queries.
	2.	Customer Inquiry Logs: A collection of previous customer interactions, including questions and responses. This dataset serves as a training resource to enhance the chatbot’s understanding of common inquiries and effective responses.
	3.	Feedback Data: Data from customer feedback and ratings on interactions. This will help evaluate the chatbot’s performance and guide future improvements.

## Technologies

Python 3.11.6
Minsearch for full-text search
Flask as the API interface 
OpenAI (gpt-4o-mini) as an LLM

## Implementation

The project employs a Retrieval-Augmented Generation (RAG) flow to combine retrieval of relevant information from the datasets with generative language models. This approach allows the chatbot to provide accurate answers while maintaining a conversational tone.

## Getting Started

To get started with this project, follow these steps:

1.	Clone this repository.
   
2.	Install the necessary dependencies.

Running it

We use poetry to manage our dependencies and python 3.11.6

if you don't have poetry run:

```bash
pip install poetry
```

once the repository is copied run to test the llm application 

```bash
poetry install
```

running the application

```bash
poetry run python src/ecom_bot/app.py
```

testing the application

```bash
URL=http://127.0.0.1:5000
QUESTION="How can I find out where is my order?"
DATA='{
    "question": "'${QUESTION}'"
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${DATA}" \
    ${URL}/question
```

llm answer results:

```json
{
  "answer": "You can find out where your order is by tracking it. To track your order, log into your account and navigate to the 'Order History' section. There, you will find the tracking information for your shipment.",
  "conversation_id": "a3572aaa-d725-4408-a2e1-d17fc78ad5b6",
  "question": "How can I find out where is my order?"
}
```

Sending feedback:

```bash
ID='a3572aaa-d725-4408-a2e1-d17fc78ad5b6'

FEEDBACK_DATA='{
    "conversation_id": "'${ID}'",
    "feedback": 1
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${FEEDBACK_DATA}" \
    ${URL}/feedback

```

feedback results:

```json
{
  "message": "Feedback received for conversation a3572aaa-d725-4408-a2e1-d17fc78ad5b6: 1"
}
```

alternatively to test the app try:

```bash
poetry run python test.py
```

3.	Load the datasets and start the chatbot.

For detailed instructions, refer to the Installation Guide.

## Evaluation

for the code for the evaluation please refer to the [retrieval-eval.ipynb](./retrieval-eval.ipynb)

basic retrieval evaluation results in without any boosting:

`Hit rate`: 89%

`MRR`: 64%

after optimisation using a variation of weight on question and topic

these were the parameters : 

```
{'question': 0.32661063225044673, 'topic': 0.1000480066922591}
```

`Hit rate`: 91%

`MRR`: 71%

## Retrival

## The RAG flow

## Monitoring

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.



