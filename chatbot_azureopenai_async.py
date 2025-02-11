#--------------------------------------------------------------------------------
# Author:       Ahmed Aboulnaga
# Description:  Simple AI chatbot
#               - Tested on Python 3.12.9 and 3.13.2
#               - Uses Python module openai==1.61.1
#               - Invokes the Azure OpenAI API asynchronously
#--------------------------------------------------------------------------------

from openai import AzureOpenAI
import asyncio

# Set up your Azure OpenAI client
client = AzureOpenAI(
    api_key="XXXXXXXXXX",                                  # Replace with your Azure OpenAI API key
    api_version="2023-05-15",                              # Azure OpenAI API version
    azure_endpoint="https://myahmedtest.openai.azure.com/" # Your Azure OpenAI endpoint
)

# Load knowledge base
with open("mydata.txt", "r") as f1:
    my_data = f1.read()

# Initialize the context with interaction rules and my data
context = []

# Define the chatbot interaction rules here, including how it should greet users and provides information
rules = """
Your name is Ahmed and you are an AI clone of the real Ahmed Aboulnaga. \
When responding, be more informal than formal. \
When asked about the content of the data, mimic someone with a personality that is honest, but can be sarcastic at times. \
In the responses, keep the answers brief but engaging. \
"""

# Combine contents from both files
context.append({'role': 'system', 'content': f"""{rules}\n\n{my_data}"""})

# Function to fetch messages from the Azure OpenAI Chat model
async def fetch_messages(messages, model="gpt-4o", temperature=0):
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=200,
        n=1,
        stop=None,
    )
    return response.choices[0].message.content

# Function to refresh and update the conversation context based on user input
async def refresh_conversation(chat):
    context.append({'role': 'user', 'content': chat})
    response = fetch_messages(context, temperature=0.7)
    context.append({'role': 'assistant', 'content': response})
    print(response)

# Main loop to engage users in conversation
async def main():
    print("\n")
    print("--------------------------------------------------")
    print("Welcome to the Azure OpenAI Chatbot!")
    print("--------------------------------------------------")
    while True:
        message = input("\nPlease enter a message (or 'exit' to leave): ")
        if message.lower() == 'exit':
            break
        await refresh_conversation(message)

if __name__ == '__main__':
    asyncio.run(main())
