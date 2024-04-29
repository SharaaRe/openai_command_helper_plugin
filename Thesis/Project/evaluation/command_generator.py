#imports

import pandas
import openai 
from openai import AsyncOpenAI as OpenAI
import os
import sys
import dotenv
import json
import asyncio
import time


import os
from dotenv import load_dotenv



def load_openai_key():
       # Specify the path to your .env file
        env_file_path = '/Users/shararenorouzi/Library/CloudStorage/GoogleDrive-norouzi.sharare@gmail.com/My Drive/Thesis/Project/.env'  # Update this with the correct path
        load_dotenv(env_file_path)
                # Access your API key by referencing the environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        print(api_key)
        openai.api_key = api_key
        client = OpenAI()
        return client


#completion async 

#completion async 

async def get_completion(client, model, user_instruction, prompt):
        print('th')
        messages = [{"role": "user", "content": prompt.format(user_instruction=user_instruction)}]
        wait_time = 1

        try:
                response =  await client.chat.completions.create(
                                        model=model,
                                        messages=messages,
                                        temperature=0, # this is the degree of randomness of the model's output
                                )
                return {user_instruction: json.loads(response.choices[0].message.content)}
                
        except openai.APIError as e:
                #Handle API error here, e.g. retry or log
                print(f"OpenAI API returned an API Error: {e}")
                return user_instruction, 'APIError'
        except openai.APIConnectionError as e:
                #Handle connection error here
                print(f"Failed to connect to OpenAI API: {e}")
                return user_instruction, 'APIConnectionError'

        except openai.RateLimitError as e:
                #Handle rate limit error (we recommend using exponential backoff)
                print(f"OpenAI API request exceeded rate limit: {e}")
                return user_instruction, 'RateLimitError'
                
def load_prompt(prompt_file):

        with open(prompt_file, 'r') as file:
                prompt = file.read().replace('\n', '')
                return prompt
        


def load_instructions(instruction_file):
      with open(instruction_file) as f:
        data = json.load(f)
        return data
        
# Project/prompts/5.txt
      
def get_gpt_response(data, prompt):

        pass

async def async_get_gpt_response(client, model, data, prompt):
        print('here')
        commands = []
        tasks = []
        for instruction in data:

                task = asyncio.create_task(get_completion(client, model, instruction, prompt))
                # time.sleep(1)
                tasks.append(task)
                print('there')
        
        commands = await asyncio.gather(*tasks)

        return commands



async def run_script(client, model, prompt_file, instructions_file):
        results = []

        # try:
        prompt = load_prompt(prompt_file)
        print(f"Prompt loaded! '{prompt}'")
        instructions = load_instructions(instructions_file)
        print(f"{len(instructions)} instructions loaded")
        # print(instructions)
        chunk_size = 10
        instruction_chunks = [instructions[i:i + chunk_size] for i in range(0, len(instructions), chunk_size)]
        for i, chunk in enumerate(instruction_chunks): 
                print(f'Chunk number {i}')
                responses = await async_get_gpt_response(client,model, chunk, prompt)
                print('here')
                print(responses)
                results += responses

        # except Exception as e:
        #        print('failed!', e)

        # finally:
        output_path = f'{prompt_file[:-4]}_{model}_responses.json'
        print(output_path)
        with open(output_path, 'w') as f:
                print(f)
                # results = dict(ChainMap(*results))
                json.dump(results, f)
                                # res = json.l






client = load_openai_key()
print(client)
model = 'gpt-3.5-turbo'
# model = 'gpt-4-turbo-preview'
# model = 'gpt-4'
prompt_file = "/Users/shararenorouzi/Library/CloudStorage/GoogleDrive-norouzi.sharare@gmail.com/My Drive/Thesis/Project/prompts/6.txt"
instructions_file = "/Users/shararenorouzi/Library/CloudStorage/GoogleDrive-norouzi.sharare@gmail.com/My Drive/Thesis/Project/evaluation/samples/test_instructions_small.json"
# instructions_file = "./samples/test_instructions.json"
print(prompt_file, instructions_file)


loop = asyncio.get_event_loop()
asyncio.run(run_script(client, model, prompt_file, instructions_file))
