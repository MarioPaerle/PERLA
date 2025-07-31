import pyphen
with open('datas/parole_sillabate_1.txt', 'r') as f:
    words = f.readlines()
print('it_IT' in pyphen.LANGUAGES)

dic = pyphen.Pyphen(lang='nl_NL')
with open('datas/parole_sillabate_2.txt', 'w') as f:
    for word in words:
        sep = dic.inserted(word).replace('-', ' ')
        f.write(sep)