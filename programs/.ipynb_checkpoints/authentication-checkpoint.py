import re

def authentication(password):
    f = open('../key/apikey.txt', 'r', encoding='UTF-8')
    key1 = f.read()
    f.close()
    f = open('../key/secretkey.txt', 'r', encoding='UTF-8')
    key2 = f.read()
    f.close()

    pattern = '(\d+)([a-z]*)(-?)'
    nums = re.findall(pattern, key1)
    key1 = ''.join([str(int(a[0])-password) + a[1] + a[2] for a in nums])
    
    pattern = '([a-z]*)(\d+)'
    nums = re.findall(pattern, key2)
    key2 = ''.join([a[0]+str(int(a[1])-password) for a in nums])
    return key1, key2

if __name__ == "__main__":
    a, b = authentication(123)
    print(a)
    print(b)