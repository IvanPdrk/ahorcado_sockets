import random
words=['acosadores', 'justiciera', 'eclipsante', 'danzadores',
       'cabelleras', 'babilonias', 'obscuridad', 'ochenteros',
       'efectuamos', 'educativas'
       ]

def ahorcado():
    tries=0
    indexes = []
    ran = random.randrange(9)
    word = words[ran]
    hidden_word = ['_'] * len(word)
    while True:
        new_letter=input('Ingresa una letra:\n')
        for letter in word:
            if letter == new_letter:
                indexes.append(new_letter)
        if len(indexes) == 0:
            tries+=1
        else:
            for idx in word:
                if idx is new_letter:
                    hidden_word.append(idx)
                print('Correcto')

print("W E L C O M E")
ahorcado()

