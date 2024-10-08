# Ecom-QABot

E-commerce Chatbot with Retrieval-Augmented Generation (RAG)

## Project Overview

The Ecom-QABot is a RAG application designed to assist users with their E-commerce inquiries.

The main use cases include:

- **Product Information**: Providing detailed information about products based on user queries.
- **Order Status**: Assisting users in tracking their orders and providing updates.
- **FAQ Assistance**: Offering answers to frequently asked questions related to E-commerce.
- **Conversational Interaction**: Engaging users in a natural conversation, enhancing their shopping experience.

## Data Description

Link to dataset: [E-commerce FAQ Dataset](https://www.kaggle.com/datasets/saadmakhdoom/ecommerce-faq-chatbot-dataset)

To tackle the problem, we utilize the following datasets:

1. **E-commerce Product Data**: This dataset includes information about products, such as names, descriptions, prices, and categories. This information helps the chatbot retrieve relevant product details based on customer queries.
2. **Customer Inquiry Logs**: A collection of previous customer interactions, including questions and responses. This dataset serves as a training resource to enhance the chatbot’s understanding of common inquiries and effective responses.
3. **Feedback Data**: Data from customer feedback and ratings on interactions. This will help evaluate the chatbot’s performance and guide future improvements.

## Technologies

- Python 3.11.6
- Minsearch for full-text search
- Flask as the API interface
- OpenAI (gpt-4o-mini) as an LLM

## Implementation

The project employs a Retrieval-Augmented Generation (RAG) flow to combine retrieval of relevant information from the datasets with generative language models. This approach allows the chatbot to provide accurate answers while maintaining a conversational tone.

## Getting Started

To get started with this project, follow these steps:

1. Clone this repository.
   
2. Install the necessary dependencies.

### Running it

We use Poetry to manage our dependencies with Python 3.11.6.

If you don't have Poetry, run:

```bash
pip install poetry
```

Once the repository is copied, run to test the LLM application:

```bash
poetry install
```

```bash
poetry shell
```
Running the Application

```bash
poetry run python src/ecom_bot/app.py
```

Testing the Application


```bash
URL=http://127.0.0.1:5000
QUESTION="How can I find out where my order is?"
DATA='{
    "question": "'${QUESTION}'"
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${DATA}" \
    ${URL}/question
```

LLM Answer Results:

```bash
{
  "answer": "You can find out where your order is by tracking it. To track your order, log into your account and navigate to the 'Order History' section. There, you will find the tracking information for your shipment.",
  "conversation_id": "a3572aaa-d725-4408-a2e1-d17fc78ad5b6",
  "question": "How can I find out where my order is?"
}
```

Sending Feedback:

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

Feedback Results:

```bash
{
  "message": "Feedback received for conversation a3572aaa-d725-4408-a2e1-d17fc78ad5b6: 1"
}
```

Alternatively, to test the app, try:

```bash
poetry run python test.py
```


3.	Load the datasets and start the chatbot.

For detailed instructions, refer to the Installation Guide.

Evaluation

For the code for the evaluation, please refer to the retrieval-eval.ipynb.

Basic retrieval evaluation results without any boosting:

	•	Hit rate: 89%
	•	MRR: 64%

After optimization using a variation of weight on question and topic, these were the parameters:

```json
{'question': 0.32661063225044673, 'topic': 0.1000480066922591}
```

	•	Hit rate: 91%
	•	MRR: 71%


The RAG Flow

**develped the RAG Flow, due to time constraints did not manage to complete for project deadline**

Monitoring

**Monitoring is functional, the grafana UI is accesible, the dashboard was not completed for project deadline**

Running it with Docker

The more straightforward method to run this application is Docker.


```bash
docker-compose up
```

```bash
export POSTGRES_HOST=localhost
```

```bash
docker build -t ecom-bot .

docker run -it --rm \
    -e OPENAI_API_KEY=${OPENAI_API_KEY} \
    -e DATA_PATH="data/chunked_data.csv" \
    -p 5001:5000 \
    ecom-bot
```

test the docker version using the test.py file.

```bash
poetry run python test.py
```
