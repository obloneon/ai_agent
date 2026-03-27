import sys
import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("API key not found")

client = genai.Client(api_key=api_key)

def main():
    print("Hello from ai-agent!")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            ),
        )
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        if response.usage_metadata == None:
            raise RuntimeError("API request failed")
        if args.verbose:
            print("System prompt: " + system_prompt)
            print("User prompt: " + args.user_prompt)
            print("Prompt tokens: "  + str(response.usage_metadata.prompt_token_count))
            print("Response tokens: "  + str(response.usage_metadata.candidates_token_count))
        if not response.function_calls == None:
            function_responses = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call)
                if len(function_call_result.parts) == 0:
                    raise Exception("function_call_result.parts is empty")
                if function_call_result.parts[0].function_response == None:
                    raise Exception("function_call_result.parts[0].function_response is None")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("The result of the called function is None")
                function_responses.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            print("Response:\n" + response.text)
            return
    sys.exit("maximum number of iterations is reached and the model still hasn't produced a final response")
if __name__ == "__main__":
    main()
