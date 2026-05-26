import os
from dotenv import load_dotenv
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if (api_key == None):
    raise Exception("API KEY NOT FOUND")

from google import genai
from google.genai import types

client = genai.Client(api_key = api_key)

def get_user_input():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()

def parse_question_with_context(question):
    #Need to do a real thing later, but for now we just parse the single prompt as context
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=question)])
    ]  
    return messages


def get_usage_info(response, parser_args):
    if (not parser_args.verbose):
        return
    
    usage_data = response.usage_metadata
    if (usage_data == None):
        raise RuntimeError("Failed to get usage metadata")

    print(f"User prompt: {parser_args.user_prompt}")
    print(f"Prompt tokens: {usage_data.prompt_token_count}")
    print(f"Response tokens: {usage_data.candidates_token_count}")


def get_response_text(response):
    print(response.text)



def main():
    print("Hello from our AIAgent!")

    parser_args = get_user_input()

    question = parser_args.user_prompt

    messages = parse_question_with_context(question)

    if (question == None or question == ""):
        raise Exception("No question Given")
    
    response = client.models.generate_content(model='gemini-2.5-flash', contents=messages)
    
    get_usage_info(response, parser_args)
    get_response_text(response)


if __name__ == "__main__":
    main()
