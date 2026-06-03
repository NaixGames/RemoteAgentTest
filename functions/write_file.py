import os
from google.genai import types

import sys
sys.path.append(".")
from config import MAX_CHARS

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))

        is_valid_target_directory = os.path.commonpath([abs_working_directory, target_file_path]) == abs_working_directory

        result = f'Results for writting "{file_path}" filepatb:\n'

        if not is_valid_target_directory:
            result += f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
            return result
        
        if os.path.isdir(target_file_path):
            result += f'Error: "{target_file_path}" is actually a directory and not a filepath'
            return result
        
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        with open(target_file_path, "w") as f:
            f.write(content)

        result += f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        return result

    except BaseException as e:
        return f'Error: {e}'
    


schema_write_file= types.FunctionDeclaration(
    name = "write_file",
    description="Creates a file with the given content on disk",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file we create, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content the created file will have",
            )
        },
        required=["file_path", "content"]
    ),
)