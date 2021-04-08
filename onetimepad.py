from os import listdir, path
from random import seed, randint

alphabet = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z, '.split(',')

def shiftLetter(letter, shift):
    newIdx = alphabet.index(letter) + shift
    if newIdx >= 27:
        return alphabet[newIdx-27]
    elif newIdx >= 0 and newIdx < 27:
       return alphabet[newIdx]
    else:
        return alphabet[27+newIdx]

def vigenere(text, key, cipher):
    keyShifts = []
    if cipher:
        # keyShifts = all shifts in key ('gkoy' becomes [6, 10, 14, 24] for each letter respectively) (encryption)
        keyShifts = [ (alphabet.index(key[i]) - alphabet.index('a')) for i in range(len(key)) ]
    else:
        # keyShifts = all shifts in key, but negative ('gkoy' becomes [-6, -10, -14, -24] for each letter respectively) (decryption)
        keyShifts = [ ((alphabet.index(key[i]) - alphabet.index('a')) * -1) for i in range(len(key)) ]
    
    textLetters = [ text[i] for i in range(len(text)) ] # parse all characters in text into an array
    cipherKey = [ keyShifts[i % len(keyShifts)] for i in range(len(textLetters)) ]  # repeat keyShifts to match textLetters length ('hello' with key 'gk' will output [6, 10, 6, 10, 6])
    vigenereText = [ shiftLetter(textLetters[i], cipherKey[i]) for i in range(len(textLetters)) ]   # shift every letter to encrypt/decrypt text

    return ''.join(vigenereText)


if __name__ == "__main__":
    print('One Time Pad')
    print('------------------')
    print('1. Cipher a message')
    print('2. Decipher a message')
    choice = input('\nYour Choice: ')

    if choice == '1':
        print('\nPlease input the plaintext you want to cipher')
        plaintext = input('Plain Text: ')

        key = ''
        for i in range(len(plaintext)):
            seed()
            key += alphabet[randint(0,26)]

        cipherText = vigenere(plaintext, key, True)
        print('\nYour ciphertext is: ', cipherText)
        print('Your key is: ', key)
    else:
        print('\nPlease input the ciphertext you want to decipher and the key')
        ciphertext = input('Cipher Text: ')
        key = input('Key: ')

        plainText = vigenere(ciphertext, key, False)
        print('\nYour plaintext is: ', plainText)