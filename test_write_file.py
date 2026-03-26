from functions.write_file import write_file

print("lorem.txt result:")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print("pkg/morelorem.txt result:")
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print("/tmp/temp.txt result:")
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
