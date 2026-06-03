import os
from google.genai import types

import sys
sys.path.append(".")
from config import MAX_CHARS

def get_file_info(abs_file_path : str, file_path: str) -> str:
    with open(abs_file_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if f.read(1):
            file_content_string += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string

def get_file_content(working_directory : str, file_path : str):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))

        is_valid_target_directory = os.path.commonpath([abs_working_directory, target_file_path]) == abs_working_directory

        result = f'Results for "{file_path}" file:\n'

        if not is_valid_target_directory:
            result += f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
            return result
        
        if not os.path.isfile(target_file_path):
            result += f'Error: File not found or is not a regular file: "{file_path}"'
            return result

        result += get_file_info(target_file_path, file_path)
        return result

    except BaseException as e:
        return f'Error: {e}' 


schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description="Provides the first 10000 characters of a file, when seen as a string.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file we want the content, relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)