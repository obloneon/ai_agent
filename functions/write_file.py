import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content into a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Name of the file"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="A string with the content to write into the file"
            ),

        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
	try:
		working_dir_abspath = os.path.abspath(working_directory)
		target_file = os.path.normpath(os.path.join(working_dir_abspath, file_path))
		valid_target_file = os.path.commonpath([working_dir_abspath, target_file]) == working_dir_abspath
		if not valid_target_file:
			return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
		if os.path.isdir(target_file):
			return f'Error: Cannot write to "{file_path}" as it is a directory'
		os.makedirs(os.path.dirname(target_file), exist_ok=True)
		with open(target_file, "w") as f:
			f.contents = content
			return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

	except Exception as e:
		return f"Error: {e}"
