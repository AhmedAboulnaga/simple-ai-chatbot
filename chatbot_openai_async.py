#--------------------------------------------------------------------------------
# Author:       Ahmed Aboulnaga
# Description:  Simple AI chatbot
#               - Tested on Python 3.12.9 and 3.13.2
#               - Requires Python module openai==1.61.1
#               - Invokes the OpenAI API asynchronously
#--------------------------------------------------------------------------------

import openai
import asyncio

# Initialize OpenAI client
client = openai.AsyncClient(api_key='<your-api-key>')

# Load knowledge base
with open("mydata.txt") as file:
    my_data = file.read()

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
context.append({'role': 'system', 'content': f"""{rules} {my_data}"""})

# Function to fetch messages from the OpenAI Chat model
async def fetch_messages_async(messages, model="gpt-3.5-turbo", temperature=0):
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=4000,
        n=1,
        stop=None,
    )
    return response.choices[0].message.content

# Function to refresh and update the conversation context based on user input
async def refresh_conversation(chat):
    context.append({'role': 'user', 'content': chat})
    response = await fetch_messages_async(context, temperature=0.7)
    context.append({'role': 'assistant', 'content': response})
    print(response)

# Main loop to engage users in conversation
async def main():
    print("\n")
    print("--------------------------------------------------")
    print("Welcome to the OpenAI AI Chatbot!")
    print("--------------------------------------------------")
    while True:
        message = input("\nPlease enter a message (or 'exit' to leave): ")
        if message.lower() == 'exit':
            break
        await refresh_conversation(message)

if __name__ == '__main__':
    #main()
    asyncio.run(main())