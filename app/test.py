import re
regex1 = 'nan'
regex1 = re.compile(regex1)
data = ' 2 T: nan'

if re.search(regex1, data):
    print('ole')

string = '(112, "Host is down")'
string = string.replace('(', '')
string = string.replace(')', '')
string = string.split(',')
print(string[0])
print(string[1])
print(string[0])
