import os
import subprocess
import json

def get_user_input(prompt):
    """ Function to get user input """
    return input(prompt)

def main():
    # Fetch the API key from the system environment
    api_key = os.environ.get('OPEN_API_KEY')

    if not api_key:
        print("API key not found in environment. Please set OPEN_API_KEY.")
        return

    while True:
        # Prompt user for input
        user_prompt = get_user_input("Enter your DALLE3 prompt or c to cancel: ")

        # Check if user wants to cancel
        if user_prompt.lower() == "c":
            print("Script cancelled.")
            break

        # Confirm the prompt
        confirm = get_user_input("Are you sure you want to submit this prompt? Enter y for Yes or n to cancel: ")

        # If confirmed, construct and make the request
        if confirm.lower() == "y":
            print(f"Authorization Header: Bearer {api_key}")
            print(f"Prompt: {user_prompt}")

            # JSON data for the API request
            data = json.dumps({
                "model": "dall-e-3",          # Specifies the model to be used
                "prompt": user_prompt,        # The user-provided prompt
                "n": 1,                       # Number of images to generate
                "size": "1024x1024"           # Size of the generated images
            })

            # Constructing the cURL command for the API request
            curl_command = [
                "curl", "-X", "POST", "https://api.openai.com/v1/images/generations",
                "-H", "Content-Type: application/json",
                "-H", f"Authorization: Bearer {api_key}",
                "-d", data
            ]

            print("cURL Command:", " ".join(curl_command))
            
            # Executing the cURL command and capturing the response
            try:
                response = subprocess.run(curl_command, capture_output=True, text=True, check=True)
                print("Response:\n", response.stdout)
            except subprocess.CalledProcessError as e:
                # Handling errors during the API request
                print("Error occurred:")
                print(e.stderr)

            break

if __name__ == "__main__":
    main()
