from functions.get_file_content import get_file_content
from config import MAX_CHARS


print("Result for lorem.txt:")
result = get_file_content("calculator", "lorem.txt")
assert len(result) > MAX_CHARS
assert 'truncated at' in result
print(len(result))
print("Result for main.py:")
print(get_file_content("calculator", "main.py"))
print("Result for pkg/calculator.py:")
print(get_file_content("calculator", "pkg/calculator.py"))
print("Result for /bin/cat:")
print(get_file_content("calculator", "/bin/cat"))
print("Result for pkg/does_not_exist.py:")
print(get_file_content("calculator", "pkg/does_not_exist.py"))
