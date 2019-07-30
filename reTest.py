import re

str = "hi My name is 'apple', apple is .. what? "
print(re.findall(r'\W+', str))