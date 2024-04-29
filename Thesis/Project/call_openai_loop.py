
import os
import openai
from dotenv import load_dotenv
import time
import sys

# Specify the path to your .env file
env_file_path = '.env'  # Update this with the correct path

# Load the environment variables from the .env file
load_dotenv(env_file_path)

# Access your API key by referencing the environment variable
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key
# print(api_key)

def get_completion(prompt, model="gpt-4"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]




# time.sleep(5)
# print("here")
# response = get_completion(prompt_5)

if __name__ == '__main__':
    while True:
        try:
            # user_instructions = sys.argv[1]
            user_instructions = input("Please Enter the Instruction!")
            user_request = 'I want a 2d array of boxes'
            prompt_5 = f"""
            You are an expert rhino3d designer who can work with rhino3d api,
            the user will give you instructions about an action in rhino and you should give a list of 'RhinoScrip' for
            running in RhinoCommon framework 'RunScript' method, list the commands in a json.
            RhinoScripts are like this <<
            '_Sphere 0,0,0 1' for creating a sphere or
            '_ArrayPolar _Copy=_Yes _DeleteInput=_No _AngleBetweenCopies=90 _Center=0,0,0 _Count=4 _DeleteInput=No' for array the object
            <<
            This is users request: << {user_instructions} >>

            Please make sure it is a valid syntax and works if I feed it to the rhino command line!
            """

            prompt_gpt_created = f"""
            Generate two commands for creating a 3D model in Rhino 3D software based on user-defined parameters. The first command should be a Python script using RhinoScriptSyntax, suitable for the Rhino Python scripting environment. The second should be a command line instruction for direct use in Rhino's command interface.
            The actipn to be done is {user_instructions}.
            For the Python script, provide a function that takes necessary parameters (such as dimensions, location, etc.) as arguments and adds the specified model to the Rhino document. The function should be versatile enough to accommodate different shapes and sizes based on user input.
            For the Rhino command line, provide a step-by-step sequence of inputs that a user would follow to create the same model using Rhino's built-in commands. The instructions should be clear and easy to adapt to different user-specified parameters.
            Please ensure that both the Python script and the Rhino command line instructions are detailed, accurate, and easy to customize based on user inputs."""
            # print(prompt_5)
            messages = [{"role": "user", "content": prompt_5}]
            response = openai.ChatCompletion.create(
                model='gpt-4',
                messages=messages,
                temperature=0, # this is the degree of randomness of the model's output
            )
            print(response.choices[0]["message"]["content"])
            messages_2 = [{"role": "user", "content": prompt_gpt_created}]
            response_2 = openai.ChatCompletion.create(
                model='gpt-4',
                messages=messages_2,
                temperature=0, # this is the degree of randomness of the model's output
            )
            print("_______________________________")
            print(response_2.choices[0]["message"]["content"])

        except Exception as e:
            print('ERROR', e)
            # print('there')
            # print('this is an error', e)
        #   Print the generate`d translation
    # print('fake response')