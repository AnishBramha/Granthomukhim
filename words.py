import json
import random
import unicodedata

def load_grammar(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data

    except FileNotFoundError:
        print('File not found')
        return None

    except json.JSONDecodeError as e:
        print(f'JSON error\n{e}')
        return None





def generate(symbol, data):
    grammar = data.get('grammar', {})
    lexicon = data.get('lexicon', {})

    if symbol in lexicon:
        return random.choice(lexicon[symbol])

    if symbol in grammar:

        options = grammar[symbol]
        if not options:
            return ''
        
        production = random.choice(options)
        
        word = ''
        for part in production:
            word += generate(part, data)
        return word

    return f'<{symbol}?>'



# SANDHI

def make_word(word1):

    if not isinstance(word1, str):
        word1 = ''.join(word1)

    word1 = unicodedata.normalize('NFC', word1)

    word = list(word1) + ['', '', '', '']

    i = 0

    while i < len(word) - 4:

        trigger = False

        j = i + 1
        k = i + 2
        l = i + 3

        if word[i] == 'n':

            if word[i] == 'n':
                if word[j] in ('k', 'g', 'ŋ'):
                    word[i] = 'ŋ'; trigger = True
                elif word[j] in ('c', 'j', 'ñ'):
                    word[i] = 'ñ'; trigger = True
                elif word[j] in ('ṭ', 'ḍ', 'ṇ'):
                    word[i] = 'ṇ'; trigger = True
                elif word[j] in ('t', 'd', 'n'):
                    word[i] = 'n'; trigger = True
                elif word[j] in ('p', 'b', 'm'):
                    word[i] = 'm'; trigger = True
                elif word[j] == 'r' and i > 0:
                    word[i] = 'ṇ'; word[j] = 'ḍr'; trigger = True
                elif word[j] in ('l', 'ḷ', 'ł'):
                    word[i] = word[j]; trigger = True
                elif word[j] in ('s', 'ś', 'ṣ'):
                    word[i] = 'm'; word[j] = ''; trigger = True
                elif word[j] == 'h':
                    word[j] = 'n'; trigger = True
            
            if trigger:
                if word[k] == 'h' and word[j] != '':
                    i = l
                else:
                    i = k


        elif word[i] in ('a', 'ā', 'i', 'ī', 'u', 'ū', 'ṛ', 'R', 'î', 'ǐ', 'e', 'ē', 'o', 'ō') and word[j] in ('a', 'ā', 'i', 'ī', 'u', 'ū', 'ṛ', 'R', 'î', 'ǐ', 'e', 'ē', 'o', 'ō'):

            word[i] = ''

            if word[j] == 'a': word[j] = 'ā'
            elif word[j] == 'i': word[j] = 'ī'
            elif word[j] == 'e': word[j] = 'ē'
            elif word[j] == 'u': word[j] = 'ū'
            elif word[j] == 'ṛ': word[j] = 'R'
            elif word[j] == 'o': word[j] = 'ō'

            i += 1
            trigger = True



        elif word[i] in ('k', 'g'):

            if word[j] == 'h':

                trigger = True

                if word[k] in ('c', 'j', 'ṭ', 'ḍ', 't', 'd', 'p', 'b'):
                    word[i] = word[k]; word[j] = ''
                elif word[k] == 'k':
                    word[j] = word[i]; word[k] = 'h'
                    if word[l] == 'h': word[l] = ''
                elif word[k] == 'g':
                    word[j] = 'g'; word[k] = 'h'
                    if word[l] == 'h': word[l] = ''
                elif word[k] in ('l', 'ḷ', 'ł'):
                    word[k] = 'l'
                
                i = l + 1 if word[l] == 'h' else l


            else:

                if word[j] == 'k':
                    word[j] = word[i]; trigger = True
                elif word[j] == 'g':
                    word[i] = 'g'; trigger = True
                elif word[j] in ('c', 'j', 'ṭ', 'ḍ', 't', 'd', 'p', 'b'):
                    word[i] = word[j]; trigger = True
                elif word[j] in ('l', 'ḷ', 'ł'):
                    word[j] = 'l'; trigger = True
                
                if trigger:
                    i = l if word[k] == 'h' else k

                         
            
        elif word[i] in ('c', 'j'):

            if word[j] == 'h':
                word[j] = ''; trigger = True

                if word[k] in ('g', 'j'): word[i] = 'j'
                elif word[k] in ('ṭ', 'ḍ', 'p', 'b'): word[i] = 'ṣ'
                elif word[k] in ('t', 'd'): word[i] = word[k]
                elif word[k] == 's': word[k] = word[i]
                elif word[k] in ('ś', 'ṣ'): word[i] = 'k'; word[k] = 'ṣ'
                
                i = l + 1 if word[l] == 'h' else l

            
            else:
                if word[j] in ('g', 'j'): 
                    word[i] = 'j'; trigger = True
                elif word[j] in ('ṭ', 'ḍ', 'p', 'b'): 
                    word[i] = 'ṣ'; trigger = True
                elif word[j] in ('t', 'd'): 
                    word[i] = word[j]; trigger = True
                elif word[j] == 's': 
                    word[j] = word[i]; trigger = True
                elif word[j] in ('ś', 'ṣ'): 
                    word[i] = 'k'; word[j] = 'ṣ'; trigger = True
                
                if trigger:
                    i = l if word[k] == 'h' else k



        elif word[i] in ('ṭ', 'ḍ'):

            if word[j] == 'h':
                word[j] = ''; trigger = True
                if word[k] in ('c', 'j'): word[k] = word[i]
                elif word[k] == 'ṭ': word[k] = word[i]
                elif word[k] == 'ḍ': word[i] = 'ḍ'
                elif word[k] in ('t', 'd'): word[i] = word[k]
                
                i = l + 1 if word[l] == 'h' else l

            else:
                if word[j] in ('c', 'j'): 
                    word[j] = word[i]; trigger = True
                elif word[j] == 'ṭ': 
                    word[j] = word[i]; trigger = True
                elif word[j] == 'ḍ': 
                    word[i] = 'ḍ'; trigger = True
                elif word[j] in ('t', 'd'): 
                    word[i] = word[j]; trigger = True
                
                if trigger:
                    i = l if word[k] == 'h' else k
        

        elif word[i] in ('t', 'd'):

            if word[j] == 'h':
                trigger = True
                if word[k] == 'g' or word[i] == 'd' and word[k] not in ('a', 'ā', 'i', 'ī', 'u', 'ū', 'ṛ', 'R', 'î', 'ǐ', 'e', 'ē', 'o', 'ō'): word[i] = 'd'; word[k] = 'g'
                elif word[k] in ('c', 'j'):
                    word[j] = ''; word[i] = word[k]
                    if word[l] != 'h': word[k] += 'h'
                
                i = l + 1 if word[l] == 'h' else l
            
            else:
                if word[j] == 'g' or word[i] == 'd' and word[j] not in ('a', 'ā', 'i', 'ī', 'u', 'ū', 'ṛ', 'R', 'î', 'ǐ', 'e', 'ē', 'o', 'ō'): 
                    word[i] = 'd'; word[j] = 'g'; trigger = True
                elif word[j] in ('c', 'j'): 
                    word[i] = word[j]; trigger = True
                    if word[k] != 'h': word[j] += 'h'
                
                if trigger:
                    i = l if word[k] == 'h' else k


        elif word[i] == ('p', 'b'):

            if word[j] == 'h':
                word[j] = ''; trigger = True
                if word[j] == 'g' or word[i] == 'b' and word[k] not in ('a', 'ā', 'i', 'ī', 'u', 'ū', 'ṛ', 'R', 'î', 'ǐ', 'e', 'ē', 'o', 'ō'): word[i] = 'b'; word[k] = 'g'
                elif word[j] == 'j' or word[i] == 'b': word[i] = 'b'; word[k] = 'j'
                
                i = l + 1 if word[l] == 'h' else l
            
            else:
                if word[j] == 'g' or word[i] == 'b' and word[j] not in ('a', 'ā', 'i', 'ī', 'u', 'ū', 'ṛ', 'R', 'î', 'ǐ', 'e', 'ē', 'o', 'ō'): 
                    word[i] = 'b'; word[j] = 'g'; trigger = True
                elif word[j] == 'j' or word[i] == 'b': 
                    word[i] = 'b'; word[j] = 'j'; trigger = True
                
                if trigger:
                    i = l if word[k] == 'h' else k



        elif word[i] in ('ŋ', 'ñ', 'ṇ', 'n', 'm'):

            if word[j] in ('k', 'g', 'ŋ'): word[i] = 'ŋ'; trigger = True
            elif word[j] in ('c', 'j', 'ñ'): word[i] = 'ñ'; trigger = True
            elif word[j] in ('ṭ', 'ḍ', 'ṇ'): word[i] = 'ṇ'; trigger = True
            elif word[j] in ('t', 'd', 'n'): word[i] = 'n'; trigger = True
            elif word[j] in ('p', 'b', 'm'): word[i] = 'm'; trigger = True

            elif word[j] in ('a', 'ā', 'i', 'ī', 'u', 'ū', 'ṛ', 'R', 'î', 'ǐ', 'e', 'ē', 'o', 'ō'):

                if word[i] not in ('m', 'n'):
                    word[i] = 'n'; trigger = True
            
            if trigger:
                i = l if word[k] == 'h' else k



        elif word[i] == 'ś':

            if word[j] in ('k', 'g', 'ṭ', 'ḍ', 'ṇ', 'p', 'b', 'm'):
                word[i] = 'ṣ'; trigger = True
            
            if trigger:
                i = l if word[k] == 'h' else k

        elif word[i] == 'ṣ':
            if word[j] in ('c', 'j', 't', 'd', 'n'):
                word[i] = 'ś'; trigger = True
            
            if trigger:
                i = l if word[k] == 'h' else k




        elif word[i] in ('l', 'ḷ', 'ł'):

            if word[j] in ('k', 'g', 't', 'd', 'n'): word[i] = 'l'; trigger = True
            elif word[j] in ('c', 'j'): word[i] = 'ł'; trigger = True
            elif word[j] in ('ṭ', 'ḍ'): word[i] = 'ḷ'; trigger = True
            
            if trigger:
                i = l if word[k] == 'h' else k



        if not trigger:
            i += 1

        j = i + 1
        k = i + 2
        l = i + 3


    return ''.join([char for char in word if char != ''])






def main():
    filename = 'cnf.json'
    cnf_data = load_grammar(filename)

    if cnf_data:
        print(f'Successfully loaded grammar from {filename}\n')
        print('--- GENERATED WORDS ---\n')

        print('VERBS (w_v):')
        for _ in range(5):
            raw = generate('w_v', cnf_data)
            print(raw)
            print(make_word(raw), end = '\n\n')

        print('\nNOUNS (Masculine - w_n_m):')
        for _ in range(3):
            raw = generate('w_n_m', cnf_data)
            print(raw)
            print(make_word(raw), end = '\n\n')

        print('\nNOUNS (Feminine - w_n_f):')
        for _ in range(3):
            raw = generate('w_n_f', cnf_data)
            print(raw)
            print(make_word(raw), end = '\n\n')
            
        print('\nADJECTIVES (w_adj):')
        for _ in range(4):
            raw = generate('w_adj', cnf_data)
            print(raw)
            print(make_word(raw), end = '\n\n')
            
        print('\nPRONOUNS (w_pro):')
        for _ in range(4):
            raw = generate('w_pro', cnf_data)
            print(raw)
            print(make_word(raw), end = '\n\n')


if __name__ == '__main__':
    main()









