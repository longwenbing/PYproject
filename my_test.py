import re

str_numbers='123550asfdlaskf'
numbers = re.findall(r'([1-9]\d*)', str_numbers)[0]
print(numbers)