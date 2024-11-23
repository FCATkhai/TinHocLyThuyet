import re

with (open('test.txt') as file):
    for line in file.readlines():
        line = line.strip()
        # 1)
        # result = re.match(r'^[th].*re', line)
        # 2)
        # result = re.match(r'.{20,}', line)
        # 3)
        # result = re.search(r'\?!$', line)
        # 4)
        # co thu tu
        # result = re.search(r'a.*r.*s.*m.*l', line)
        # bat ke thu tu
        # result = re.search(r'^(?=.*a)(?=.*r)(?=.*s)(?=.*m)(?=.*l).*', line)
        # 5)
        # result = re.search(r'(?=.*,)(?=.*\.).*', line)
        # 6)
        # result = re.search(r'mouse', line)
        # 7)
        # result = re.search(r'a+b', line)
        # 8)
        # result = re.search(r'@([\w.-]+\.[a-zA-Z]{2,})\b', line)
        
        if result:
            print(line)



# 9)
test_str = "<head>This is a sample text within head tags.</head>"
result = re.search(r'<head>(.*?)</head>', test_str)
print(result.group(1))


        
# content = re.findall(r"<head>([^<]+)</head>", line) 