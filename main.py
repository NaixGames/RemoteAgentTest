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

from prompts import system_prompt
from config import GLOBAL_TEMPERATURE

from functions.call_function import available_functions, call_function

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


def process_response(response, parser_args, result_history):
    if (response.function_calls != None and len(response.function_calls) > 0):
        func_res = call_function(response.function_calls, parser_args.verbose)
        
        if (func_res.parts == None):
            raise Exception("function call result has empty parts. This is a bug")
        
        if (func_res.parts[0].function_response == None):
            raise Exception("function call result has empty function response. This is a bug.")
        
        if (func_res.parts[0].function_response.response == None):
            raise Exception("function call result has empty response field. This is a bug.")
        
        if (parser_args.verbose):
            print(f"-> {func_res.parts[0].function_response.response}")

        result_history.append(func_res.parts[0])
        return "Function call processed"
        
    return response.text



def main():
    print("Hello from our AIAgent!")

    parser_args = get_user_input()

    question = parser_args.user_prompt

    messages = parse_question_with_context(question)

    result_history = []

    if (question == None or question == ""):
        raise Exception("No question Given")
    
    config = types.GenerateContentConfig(
        system_instruction=system_prompt, 
        temperature=GLOBAL_TEMPERATURE,
        tools = [available_functions]
    )
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=config
    )
    
    get_usage_info(response, parser_args)
    print(process_response(response, parser_args, result_history))


if __name__ == "__main__":
    main()
