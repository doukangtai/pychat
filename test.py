import re
# content = "@aaa@"
# ret = re.match(r"(?<=@).*?(?=@)", content)
# ret = re.match(r"@(.*)@", content)
# print(ret is None)
# print(ret.group(0))
# print(ret.group(1))

x = '@姜富超aaa'
autor = re.split('@', x)
print(autor[0])
print(len(autor))
# print(autor[2])

