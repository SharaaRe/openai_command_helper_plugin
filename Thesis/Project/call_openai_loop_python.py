
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
            prompt = f"""Generate a Python script using RhinoScriptSyntax suitable for the Rhino Python scripting environment. The script should be designed to create customizable 3D models in Rhino 3D based on user-defined parameters. The function should take necessary parameters (such as shape, dimensions, location, etc.) as arguments and add the specified model to the Rhino document. The script should be flexible enough to accommodate a variety of shapes and sizes based on user input.
            Here is an example function that creates a sphere in Rhino 3D:
            <<< 
            import rhinoscriptsyntax as rs

            def create_sphere(center, radius):
                # Creates a sphere at the specified center with the given radius
                sphere_id = rs.AddSphere(center, radius)
                return sphere_id

            # Example usage
            center_point = (0, 0, 0)  # Center of the sphere at the world origin
            radius = 5  # Radius of the sphere
            sphere = create_sphere(center_point, radius)
            >>>
            Using this example as a guide, generate a similar Python script function that is adaptable for creating 3D model or operate an action based on the parameters provided by the user. The function should take arguments for the shape type, dimensions, and location, and then construct the model accordingly in Rhino and operate it.

            """
            # print(prompt_5)
            messages = [{"role": "user", "content": prompt}]
            response = openai.ChatCompletion.create(
                model='gpt-4',
                messages=messages,
                temperature=0, # this is the degree of randomness of the model's output
            )
            print(response.choices[0]["message"]["content"])

        except Exception as e:
            print('ERROR', e)
            # print('there')
            # print('this is an error', e)
        #   Print the generate`d translation
    # print('fake response')