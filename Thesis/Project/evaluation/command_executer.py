import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import json

def execute_command(command_list):
    for command in command_list:

        try:
            # Assuming the command is a valid RhinoScriptSyntax command
            eval(command)
        except Exception as e:
            return "Error", str(e)
        
    return "Success", None
    

def main(commands_file):
    # Read commands and descriptions from a file or list
    with open(commands_file, 'r') as file:
        commands = json.load(file)
    
    for instruction, command in commands:
        # command = line.strip()
        command_list = command['RhinoScript']
        if command:
            output, error = execute_command(command)
            # Here you should implement logic to create an image with the command and output/error
            print(f"Command: {command}\nResult: {output if output else error}\n")

if __name__ == "__main__":
    commands_file = "../prompts/6_gpt-3.5-turbo_responses_small.json"
    main(commands_file)