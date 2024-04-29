import subprocess
import json
import pandas as pd
import ast
import datetime

# Get the current datetime
current_datetime = datetime.datetime.now()

# Format the datetime as a compact string
datetime_string = current_datetime.strftime('%Y%m%d_%H%M%S')



def load_instructions(instruction_file):
      with open(instruction_file) as f:
        data = json.load(f)
        return list(data)


instructions_file = "/Users/shararenorouzi/Library/CloudStorage/GoogleDrive-norouzi.sharare@gmail.com/My Drive/Thesis/Project/evaluation/samples/test_instructions.json"

instruction_list = load_instructions(instructions_file)
# print(list(instruction_list))
df = pd.DataFrame(instruction_list, columns=['instruction'])

# model = 'gpt-4'
model = 'gpt-3.5-turbo'

file_name = 'call_openai_retr.py'
def get_result(row):
    command = ['python', file_name, row['instruction'], model]

    result = subprocess.run(command, capture_output=True, text=True)  
    # print(result.stdout)

    try:
        res = ast.literal_eval(result.stdout)
        ser = pd.Series([res['RhinoScript'], res.get('description')])
    except:
        ser = pd.Series([result.stdout, None])

    return ser

    # print(ser)


df[[model, f'{model}_description']] = df.apply(get_result, axis=1)

output_file = f'./results/{file_name}instructions_output_{model}_{datetime_string}.csv'
df.to_csv(output_file)
# result = subprocess.run(command, capture_output=True, text=True)

# print('output', result)