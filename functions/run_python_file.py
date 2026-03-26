import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Name of the file (needs to end with .py"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="A list of strings with additional arguments to run the file with",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A string representing an argument to run the file with",
                ),
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory, file_path, args=None):
	try:
		working_dir_abspath = os.path.abspath(working_directory)
		target_file = os.path.normpath(os.path.join(working_dir_abspath, file_path))
		valid_target_file = os.path.commonpath([working_dir_abspath, target_file]) == working_dir_abspath
		if not valid_target_file:
			return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
		if not os.path.isfile(target_file):
			return f'Error: "{file_path}" does not exist or is not a regular file'
		if not target_file.endswith(".py"):
			return f'Error: "{file_path}" is not a Python file'
		command = ["python", target_file]
		if args:
			command.extend(args)
		completed_process = subprocess.run(command, cwd= working_dir_abspath, capture_output=True, text=True, timeout=30)
		outputs = []
		if completed_process.returncode != 0:
			outputs.append(f'Process exited with code {completed_process.returncode}')
		if not completed_process.stdout and not completed_process.stderr:
			outputs.append("No output produced")
		else:
			if completed_process.stdout:
				outputs.append(f"STDOUT: {completed_process.stdout}")
			if completed_process.stderr:
				outputs.append(f"STDERR: {completed_process.stderr}")
		return "\n".join(outputs)
	except Exception as e:
		return f"Error: {e}"
