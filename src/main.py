from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
#import openai  # For OpenAI API integration

# Define your OpenAI API key
#openai.api_key = None



import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = "https://models.inference.ai.azure.com"
model_name = "Phi-3-small-8k-instruct"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

app = FastAPI()


class ContractData(BaseModel):
    text: str
    communication: str

def extract_contract_details(text):
    """Use an LLM model to extract contract details."""
    prompt = f"""
    Extract the following details from the contract text below:
    1. Supplier Name
    2. Buyer Name
    3. Effective Date
    4. Payment Terms
    5. Warranty Terms
    6. Pricing
    7. Delivery Time
    8. Governing Law

    Contract Text:
    {text}
    """


    response = client.complete(
        messages=[
            SystemMessage(content="You are a expert in legal contract analysis."),
            UserMessage(content=prompt),
        ],
        model=model_name,
        temperature=0.7,
        max_tokens=4000,
        top_p=1.
    )

    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": "You are an expert in legal contract analysis."},
    #         {"role": "user", "content": prompt}
    #     ]
    # )

    extracted_details = response.choices[0].message.content
    #print(extracted_details)
    return extracted_details

def sentiment_analysis(text):
    """Use an LLM model to perform sentiment analysis on communication."""
    prompt = f"""
    Analyze the sentiment of the following communication text and provide a sentiment score (e.g., Positive, Neutral, Negative):

    Communication Text:
    {text}
    """

    response = client.complete(
        messages=[
            SystemMessage(content="You are an expert in sentiment analysis."),
            UserMessage(content=prompt),
        ],
        model=model_name,
        temperature=0.7,
        max_tokens=4000,
        top_p=1.
    )

    sentiment_score = response.choices[0].message.content
    return sentiment_score

@app.post("/analyze")
def analyze_contract(data: ContractData):
    """Endpoint to analyze contract and communication text."""
    try:
        contract_details = extract_contract_details(data.text)
        print(contract_details)
        sentiment_score = sentiment_analysis(data.communication)

        # Prepare response
        response = {
            "Contract Details": contract_details,
            "Sentiment Score": sentiment_score
        }

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
