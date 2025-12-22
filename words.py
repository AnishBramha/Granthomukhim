import json
import random
from sandhi import *

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




def main():

    filename = 'cnf.json'
    cnf_data = load_grammar(filename)

    if cnf_data:
        print(f'Successfully loaded grammar from {filename}\n')
        print('--- GENERATED WORDS ---\n')

        print('VERBS:')
        for _ in range(5):
            raw = generate('w_v', cnf_data)
            print(raw)
            print(make_word(raw), end = '\n\n')

        print('\nNOUNS (Masculine):')
        for _ in range(5):
            raw = generate('w_n_m', cnf_data)
            print(raw)
            print(make_word(raw), end = '\n\n')

        print('\nNOUNS (Feminine):')
        for _ in range(5):
            raw = generate('w_n_f', cnf_data)
            print(raw)
            print(make_word(raw), end = '\n\n')
            
        print('\nADJECTIVES:')
        for _ in range(5):
            raw = generate('w_adj', cnf_data)
            print(raw)
            print(make_word(raw), end = '\n\n')
            
        print('\nPRONOUNS:')
        for _ in range(5):
            raw = generate('w_pro', cnf_data)
            print(raw)
            print(make_word(raw), end = '\n\n')


if __name__ == '__main__':
    main()









