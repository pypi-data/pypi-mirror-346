from ..modules import run_test

def count_coins(coins):
    coins = coins.split(",")
    coin200 = float(coins[0])*200
    coin100 = float(coins[1])*100
    coin50 = float(coins[2])*50
    coin20 = float(coins[3])*20
    coin10 = float(coins[4])*10
    coin5 = float(coins[5])*5
    coin2 = float(coins[6])*2
    coin1 = float(coins[7])
    coin05 = float(coins[8])*0.5
    coin025 = float(coins[9])*0.25
    coin01 = float(coins[10])*0.1
    coin005 = float(coins[11])*0.05

    return f"Total: R$ {coin200 + coin100 + coin50 + coin20 + coin10 + coin5 + coin2 + coin1 + coin05 + coin025 + coin01 + coin005:.2f}"

def random_password(length: int = 8, use_special: bool = False) -> str:
    import random
    import string

    if use_special:
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        characters = string.ascii_letters + string.digits

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def morse_code(text: str) -> str:
    MORSE_CODE_DICT = {
    #--- Letras A–Z ---
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',
    'E': '.',     'F': '..-.',  'G': '--.',   'H': '....',
    'I': '..',    'J': '.---',  'K': '-.-',   'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',   'P': '.--.',
    'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',
    'Y': '-.--',  'Z': '--..',

    #--- Dígitos 0–9 ---
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',

    #--- Pontuação e símbolos básicos ---
    '.': '.-.-.-',   ',': '--..--',  '?': '..--..',  "'": '.----.',
    '!': '-.-.--',   '/': '-..-.',   '(': '-.--.',   ')': '-.--.-',
    '&': '.-...',    ':': '---...',  ';': '-.-.-.',  '=': '-...-',
    '+': '.-.-.',    '-': '-....-',  '_': '..--.-',  '"': '.-..-.',
    '$': '...-..-',  '@': '.--.-.',

    #--- Letras acentuadas / variantes internacionais ---
    'Á': '.-.-',    # igual a Ä
    'À': '.--.-',
    'Â': '.--.-',
    'Ã': '.--.-',
    'É': '..-..',
    'È': '.-..-',
    'Ê': '..-..',   # pode usar mesmo código de É
    'Í': '..--.',
    'Ó': '---.',
    'Ô': '---.-',
    'Õ': '---.-',
    'Ú': '..--',
    'Û': '..--',
    'Ç': '-.-..',
}

# inversão para decode automático
    INVERSE_MORSE = {v: k for k, v in MORSE_CODE_DICT.items()}
    """
    Se `text` for composto apenas de '.', '-', ' ' e '/',
    faz decode para ASCII; senão, faz encode para Morse.
    
    Usa ' ' para separar letras e ' / ' para separar palavras.
    """
    # conjunto de caracteres válidos em Morse
    morse_chars = set('.- /')
    if set(text) <= morse_chars:
        # DECODE
        words = text.strip().split(' / ')
        decoded = []
        for word in words:
            letters = word.split()
            decoded.append(''.join(INVERSE_MORSE.get(code, '?') for code in letters))
        return ' '.join(decoded)
    else:
        # ENCODE
        encoded_words = []
        for word in text.upper().split():
            codes = []
            for ch in word:
                code = MORSE_CODE_DICT.get(ch)
                if code is None:
                    # ignora caractere sem mapeamento
                    continue
                codes.append(code)
            encoded_words.append(' '.join(codes))
        return ' / '.join(encoded_words)



if __name__ == "__main__":
    run_test(count_coins, "1,2,3,4,5,6,7,8,9,10,11,12")
    run_test(random_password, 100, True)
    run_test(random_password)
    run_test(morse_code, "HELLO WORLD")
    run_test(morse_code, ".... . .-.. .-.. --- / .-- --- .-. .-.. -..")
    run_test(morse_code, "Coisas? Coisas... Coisas que me levaram a crer que toda a humanidade está MORTA, o sangue é combustível, o inferno está cheio.")
    run_test(morse_code, "-.-. --- .. ... .- ... ..--.. / -.-. --- .. ... .- ... .-.-.- .-.-.- .-.-.- / -.-. --- .. ... .- ... / --.- ..- . / -- . / .-.. . ...- .- .-. .- -- / .- / -.-. .-. . .-. / --.- ..- . / - --- -.. .- / .- / .... ..- -- .- -. .. -.. .- -.. . / . ... - .-.- / -- --- .-. - .- --..-- / --- / ... .- -. --. ..- . / ..-.. / -.-. --- -- -... ..- ... - ..--. ...- . .-.. --..-- / --- / .. -. ..-. . .-. -. --- / . ... - .-.- / -.-. .... . .. --- .-.-.-")