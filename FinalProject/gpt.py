#This code was taken from the GPT documentation
from openai import OpenAI
from config import api_gpt_key

def fetch_gpt_data(ticker):
    '''
    Initialize the client with the API key
    '''
    client = OpenAI(api_key=api_gpt_key)

    # Making a request to the API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"In a small paragraph tell me basic company information about {ticker}"}],
        stream=False
    )

    return response.choices[0].message.content #Return the response content
