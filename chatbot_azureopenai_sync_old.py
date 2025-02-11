#--------------------------------------------------------------------------------
# Author:       Ahmed Aboulnaga
# Description:  Simple AI chatbot
#               - Tested on Python 3.12.9 and 3.13.2
#               - Uses the older openai.ChatCompletion which requires Python module openai==0.28
#               - Invokes the Azure OpenAI API synchronously
#--------------------------------------------------------------------------------

import openai

# Set up your Azure OpenAI endpoint and key
openai.api_type = "azure"
openai.api_base = "https://myahmedtest.openai.azure.com/" # Replace with your Azure OpenAI endpoint
openai.api_version = "2023-05-15"                         # Version may vary based on your Azure OpenAI setup
openai.api_key = "XXXXXXXXXX"                             # Replace with your Azure OpenAI API key

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
def fetch_messages(messages, model="gpt-4o", temperature=0):
    response = openai.ChatCompletion.create(
        engine=model,  # Use 'engine' instead of 'model' for Azure OpenAI
        messages=messages,
        temperature=temperature,
        max_tokens=200,
        n=1,
        stop=None,
    )
    return response.choices[0].message["content"]

# Function to refresh and update the conversation context based on user input
def refresh_conversation(chat):
    context.append({'role': 'user', 'content': f"{chat}"})
    response = fetch_messages(context, temperature=0.7)
    context.append({'role': 'assistant', 'content': f"{response}"})
    print(response)

# Main loop to engage users in conversation
def main():
    print("\n")
    print("--------------------------------------------------")
    print("Welcome to the Azure OpenAI Chatbot!")
    print("--------------------------------------------------")
    while True:
        message = input("\nPlease enter a message (or 'exit' to leave): ")
        if message.lower() == 'exit':
            break
        refresh_conversation(message)

if __name__ == '__main__':
    main()
