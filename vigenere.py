from os import listdir, path
import logging
import threading
import time
import concurrent.futures

alphabet = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z, '.split(',')
words = [' the ', ' be ', ' to ', ' of ', ' and ']
lock = threading.Lock()
result = []

def threadDecipher(possibleKeys, ciphertext):
    textMatches = 0
    plaintext = ''
    key = ''
    for possibleKey in possibleKeys:
            possibleText = vigenere(ciphertext, possibleKey, False)
            
            matches = 0
            for word in words:
                matches += possibleText.count(word)

            if matches >= textMatches:
                textMatches = matches
                plaintext = possibleText
                key = possibleKey
    
    with lock:
        result.append( [key, textMatches, plaintext] )

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
    print('Vigenere\'s Cipher')
    print('------------------')
    print('1. Cipher a message')
    print('2. Decipher a message')
    print('3. Decrypt a message in a file')
    choice = input('\nYour Choice: ')

    if choice == '1':
        print('\nPlease input the plaintext you want to cipher and the key (key must be shorter than plaintext)')
        plaintext = input('Plain Text: ')
        key = input('Key: ')

        cipherText = vigenere(plaintext, key, True)
        print('\nYour ciphertext is: ', cipherText)
    elif choice == '2':
        print('\nPlease input the ciphertext you want to decipher and the key')
        ciphertext = input('Cipher Text: ')
        key = input('Key: ')

        plainText = vigenere(ciphertext, key, False)
        print('\nYour plaintext is: ', plainText)
    else:
        # Select input problem file
        print('Files in ./input/ directory:')
        fileArray = []
        count = 1
        for file in listdir('./input'):
            if file.endswith('.txt'):
                print(path.join(str(count) + '. ', file))
                fileArray.append(file)
                count += 1

        prompt = input(
            '\nWhich file number contains the ciphertext to decipher? ')
        selectedFile = fileArray[int(prompt)-1]
        file = open('./input/' + selectedFile,)

        # Save file line into string
        fileLine = file.read()
        file.close()

        # Divide text into groups of letters for which each key deciphers => ['a', 'z', 'k', ..., ' ', 'c'] (len: 5309)
        lettersByKey = [ 
            [letter for letter in fileLine[::4]],
            [letter for letter in fileLine[1::4]],
            [letter for letter in fileLine[2::4]],
            [letter for letter in fileLine[3::4]]
        ]

        # Count occurrence of letters per group => [151, 36, 100, 3, 114, 0, ..., 266, 389] (len: 27)
        occurrenceByKey = [
            [lettersByKey[0].count(letter) for letter in alphabet],
            [lettersByKey[1].count(letter) for letter in alphabet],
            [lettersByKey[2].count(letter) for letter in alphabet],
            [lettersByKey[3].count(letter) for letter in alphabet],
        ]

        # print(occurrenceByKey[0])
        
        # Order most occurring letters per group in dictionary => { 'g': 1092, 'l': 491, ' ': 389, ..., 'x': 2, 'f': 0 }
        s_occurrenceByKey = []
        for i in range(len(occurrenceByKey)):
            occurrence = {}
            for idx, letter in enumerate(alphabet):
                occurrence.update({ letter: occurrenceByKey[i][int(idx)] })
            s_occurrence = { key: value for key, value in sorted(occurrence.items(), key = lambda item: item[1], reverse=True ) }
            s_occurrenceByKey.append(s_occurrence)
        
        # print(s_occurrenceByKey[0])

        # Get top 4 letter occurrences by group => group1: ['g', 'l', ' ', 'v'], ..., group4: ['j', 'o', 'c', 'y']
        top4PerGroup = [
            [ list(s_occurrenceByKey[0].keys())[i] for i in range(4) ],
            [ list(s_occurrenceByKey[1].keys())[i] for i in range(4) ],
            [ list(s_occurrenceByKey[2].keys())[i] for i in range(4) ],
            [ list(s_occurrenceByKey[3].keys())[i] for i in range(4) ],
        ]

        # print(top4PerGroup)

        # Get possible keys by group, assuming ' ' is the most occuring character => for group1: ['g', 'l', ' ', 'v'] returns ['h', 'm', 'a', 'w']
        keysByGroup = [
            [ shiftLetter(top4PerGroup[0][i], 1) for i in range(len(top4PerGroup[0])) ],
            [ shiftLetter(top4PerGroup[1][i], 1) for i in range(len(top4PerGroup[1])) ],
            [ shiftLetter(top4PerGroup[2][i], 1) for i in range(len(top4PerGroup[2])) ],
            [ shiftLetter(top4PerGroup[3][i], 1) for i in range(len(top4PerGroup[3])) ],
        ]

        # print(keysByGroup)

        # Get all possible key combinations that deciphers text (in this case, 4^4, or 256 possible combinations with the assumption that ' ' is in the top 4 common characters in text)
        possibleKeys = []
        for i in range(len(keysByGroup[0])):
            for j in range(len(keysByGroup[1])):
                for k in range(len(keysByGroup[2])):
                    for l in range(len(keysByGroup[3])):
                        possibleKeys.append(keysByGroup[0][i] + keysByGroup[1][j] + keysByGroup[2][k] + keysByGroup[3][l])
        
        # print(len(possibleKeys))
        # print(possibleKeys)

        # Divide possible keys into groups of 4 for a threaded 'brute-force' attempt solution => [possibleKeys[0:64], possibleKeys[64:128], possibleKeys[128:192], possibleKeys[192:256]]
        threadKeys = [
            possibleKeys[0:int(len(possibleKeys)/4)],
            possibleKeys[int(len(possibleKeys)/4):int(len(possibleKeys)/4)*2],
            possibleKeys[int(len(possibleKeys)/4)*2:int(len(possibleKeys)/4)*3],
            possibleKeys[int(len(possibleKeys)/4)*3:int(len(possibleKeys))],
        ]

        # print(len(threadKeys[0]), len(threadKeys[1]), len(threadKeys[2]), len(threadKeys[3]))
        # print(threadKeys[0])
        # print(threadKeys)

        # Get possible plaintext with most common word matches through threaded brute force on generated keys
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for threadIndex in range(4):
                executor.submit(threadDecipher, threadKeys[threadIndex], fileLine)

        # Show user top 4 possible plaintexts with most matches
        for idx, possibleSolution in enumerate(result):
            print('Possible Key ' + str(idx) + ': ', possibleSolution[0])
            print('Common Word Matches: ', possibleSolution[1])
            print('Part of Possible Text:', possibleSolution[2][0:30])
            print()
        
        # Ask user to pick the plaintext that is actually deciphered and output it to a file
        choice = input('Which key deciphered the ciphertext? ')
        
        outputFile = open('./output/' + selectedFile.split('.')[0] + '_plaintext.' + selectedFile.split('.')[1], 'w')
        outputFile.write('Key: ' + result[int(choice)][0] + '\n')
        outputFile.write('---------------------------------------\n')
        outputFile.write(result[int(choice)][2])
        outputFile.close()

        print('Plaintext and key outputted to ./output/' + selectedFile.split('.')[0] + '_plaintext.' + selectedFile.split('.')[1])