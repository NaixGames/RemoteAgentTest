import os
import subprocess

from google.genai import types


import sys
sys.path.append(".")
from config import EXECUTION_TIMEOUT


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str: 
    try:
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        abs_working_directory = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))

        is_valid_target_directory = os.path.commonpath([abs_working_directory, absolute_file_path]) == abs_working_directory

        result = f'Results for running "{file_path}" directory:\n'

        if not is_valid_target_directory:
            result += f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            return result
        
        if not os.path.isfile(absolute_file_path):
            result += f'Error: "{file_path}" does not exist or is not a regular file'
            return result

        #if all checks pass, run the file
        command = ["python3", absolute_file_path]
        if (args != None):
            command.extend(args)

        sub_result = subprocess.run(command, capture_output=True, text=True, timeout=EXECUTION_TIMEOUT)

        if (sub_result.returncode != 0):
            result += f"Process exited with code {sub_result.returncode}\n"

        if (sub_result.stderr == "" and sub_result.stdout == ""):
            result += f"No output produced\n"
        else:
            result += f"STDOUT:{sub_result.stdout}\nSTDERR:{sub_result.stderr}\n"

        return result

    except BaseException as e:
        return f'Error: {e}'
    

schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description="Runs a python script, allowing to pass arguments in an array." ,
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the python script we want to run, relative to the working directory",
            ),
            "args" : types.Schema(
                type=types.Type.ARRAY,
                description = "An array of arguments that can be used to run the python script",
                items = types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"]
    ),
)