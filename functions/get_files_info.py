import os
from google.genai import types

def get_directory_info(directory: str) -> str:
    #atm I will hope and pray the directory is a real directory (which should be with the checks below)
    result = ""
    for element in os.listdir(directory):
        if (result != ""):
            result += "\n"
        element_dir = directory+"/" + element
       
        result += f"- {element}: file_size={os.path.getsize(element_dir)} bytes, is_dir={os.path.isdir(element_dir)}"
    return result

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(abs_working_directory, directory))

        is_valid_target_directory = os.path.commonpath([abs_working_directory, target_directory]) == abs_working_directory

        result = f'Results for "{directory}" directory:\n'

        if not is_valid_target_directory:
            result += f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            return result
        
        if not os.path.isdir(target_directory):
            result += f'Error: "{directory}" is not a directory'
            return result

        result += get_directory_info(target_directory)
        return result

    except BaseException as e:
        return f'Error: {e}'
    


schema_get_files_info = types.FunctionDeclaration(
    name = "get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)