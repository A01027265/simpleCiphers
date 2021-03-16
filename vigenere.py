from os import listdir, path
import logging
import threading
import time
import concurrent.futures

alphabet = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z, '.split(',')
words = [' the ', ' be ', ' to ', ' of ', ' and ']

def threadDecipher(possibleKeyShifts, possibleKeyLetters, lettersByKey):
    textMatches = 0
    text = ''
    key = ''
    for idx, shift in enumerate(possibleKeyShifts):
            # Shift every letter in every group by appropriate shift
            shiftedGroups = []
            for i in range(4):
                shiftedGroup = []
                for letter in lettersByKey[i]:
                    shiftedGroup.append(shiftLetter(letter, shift[i] * -1))
                    shiftedGroups.append(shiftedGroup)
            
            test = [None] * (len(shiftedGroups[0])+len(shiftedGroups[1])+len(shiftedGroups[2])+len(shiftedGroups[3]))
            for i in range(4):
                test[i::4] = shiftedGroups[i]
            
            possibleText = ''.join(test)
            possibleKey = possibleKeyLetters[idx]
            
            matches = 0
            for word in words:
                matches += possibleText.count(word)
            
            print('Possible Shift: ', possibleKey)
            print(lettersByKey[0][0:10])
            print(shiftedGroups[0][0:10])
            # print(shift[1])
            # print(possibleKey)
            # print(idx)

            if matches >= textMatches:
                textMatches = matches
                text = possibleText
                key = possibleKey
    
    return [key, textMatches, text]

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

        # # Save all lines in selected file into array
        # fileLines = []
        # for line in file:
        #     fileLines.append(line)

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
        for i in range(4):
            occurrence = {}
            for idx, letter in enumerate(alphabet):
                occurrence.update({ letter: occurrenceByKey[i][int(idx)] })
            s_occurrence = { key: value for key, value in sorted(occurrence.items(), key = lambda item: item[1], reverse=True ) }
            s_occurrenceByKey.append(s_occurrence)
        
        # print(len(lettersByKey[0]))
        # print(len(lettersByKey[1]))
        # print(len(lettersByKey[2]))
        # print(len(lettersByKey[3]))
        # print(s_occurrenceByKey[0])
        # print(s_occurrenceByKey[1])
        # print(s_occurrenceByKey[2])
        # print(s_occurrenceByKey[3])

        # Get top 4 letter occurrences by group => group1: ['g', 'l', ' ', 'v'], ..., group4: ['j', 'o', 'c', 'y']
        top4PerGroup = [
            [ list(s_occurrenceByKey[0].keys())[i] for i in range(4) ],
            [ list(s_occurrenceByKey[1].keys())[i] for i in range(4) ],
            [ list(s_occurrenceByKey[2].keys())[i] for i in range(4) ],
            [ list(s_occurrenceByKey[3].keys())[i] for i in range(4) ],
        ]

        # print(top4PerGroup)

        # Get possible keys by group, assuming ' ' is the most occuring character => for group1: ['g', 'l', ' ', 'v'] returns ['u', 'p', 'a', 'f']
        keysByGroup = [
            [ alphabet[ alphabet.index(' ') - alphabet.index(top4PerGroup[0][i])] for i in range(4) ],
            [ alphabet[ alphabet.index(' ') - alphabet.index(top4PerGroup[1][i])] for i in range(4) ],
            [ alphabet[ alphabet.index(' ') - alphabet.index(top4PerGroup[2][i])] for i in range(4) ],
            [ alphabet[ alphabet.index(' ') - alphabet.index(top4PerGroup[3][i])] for i in range(4) ],
        ]

        # print(keysByGroup)

        # Convert possible keys by group to shifts => for group1: ['u', 'p', 'a', 'f'] returns [20, 15, 0, 5]
        shiftsByGroup = [
            [ alphabet.index(keysByGroup[0][i]) for i in range(len(keysByGroup[0])) ],
            [ alphabet.index(keysByGroup[1][i]) for i in range(len(keysByGroup[1])) ],
            [ alphabet.index(keysByGroup[2][i]) for i in range(len(keysByGroup[2])) ],
            [ alphabet.index(keysByGroup[3][i]) for i in range(len(keysByGroup[3])) ],
        ]

        # print(shiftsByGroup)

        # Get all possible key combinations that deciphers text (in this case, 4^4, or 256 possible combinations with the assumption that ' ' is in the top 4 common characters in text)
        possibleKeyLetters = []
        possibleKeyShifts = []
        for i in range(len(keysByGroup[0])):
            for j in range(len(keysByGroup[1])):
                for k in range(len(keysByGroup[2])):
                    for l in range(len(keysByGroup[3])):
                        possibleKeyLetters.append(keysByGroup[0][i] + keysByGroup[1][j] + keysByGroup[2][k] + keysByGroup[3][l])
                        possibleKeyShifts.append( [ shiftsByGroup[0][i], shiftsByGroup[1][j], shiftsByGroup[2][k], shiftsByGroup[3][l] ] )
        
        # print(len(possibleKeyLetters))
        # print(len(possibleKeyShifts))
        # print(possibleKeyLetters)
        # print(possibleKeyShifts)

        # Divide possible keys into groups of 4 for a threaded 'brute-force' attempt solution => [possibleKeyLetters[0:64], possibleKeyLetters[64:128], possibleKeyLetters[128:192], possibleKeyLetters[192:256]]
        threadKeyLetters = [
            possibleKeyLetters[0:int(len(possibleKeyLetters)/4)],
            possibleKeyLetters[int(len(possibleKeyLetters)/4):int(len(possibleKeyLetters)/4)*2],
            possibleKeyLetters[int(len(possibleKeyLetters)/4)*2:int(len(possibleKeyLetters)/4)*3],
            possibleKeyLetters[int(len(possibleKeyLetters)/4)*3:int(len(possibleKeyLetters))],
        ]

        # print(len(threadKeyLetters[0]), len(threadKeyLetters[1]), len(threadKeyLetters[2]), len(threadKeyLetters[3]))
        # print(threadKeyLetters[0])
        # print(threadKeyLetters)
        
        # Divide possible keys into groups of 4 for a threaded 'brute-force' attempt solution => [possibleKeyShifts[0:64], possibleKeyShifts[64:128], possibleKeyShifts[128:192], possibleKeyShifts[192:256]]
        threadKeyShifts = [
            possibleKeyShifts[0:int(len(possibleKeyShifts)/4)],
            possibleKeyShifts[int(len(possibleKeyShifts)/4):int(len(possibleKeyShifts)/4)*2],
            possibleKeyShifts[int(len(possibleKeyShifts)/4)*2:int(len(possibleKeyShifts)/4)*3],
            possibleKeyShifts[int(len(possibleKeyShifts)/4)*3:int(len(possibleKeyShifts))],
        ]
        
        # print(len(threadKeyShifts[0]), len(threadKeyShifts[1]), len(threadKeyShifts[2]), len(threadKeyShifts[3]))
        # print(threadKeyShifts[0])
        # print(threadKeyShifts)

        test = threadDecipher(threadKeyShifts[0], threadKeyLetters[0], lettersByKey)
        test1 = threadDecipher(threadKeyShifts[1], threadKeyLetters[1], lettersByKey)
        test2 = threadDecipher(threadKeyShifts[2], threadKeyLetters[2], lettersByKey)
        test3 = threadDecipher(threadKeyShifts[3], threadKeyLetters[3], lettersByKey)
        print(test[0], test[1])
        print(test1[0], test1[1])
        print(test2[0], test2[1])
        print(test3[0], test3[1])

        # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        #     for threadIndex in range(4):
        #         executor.submit(query.threadedData, threadIndex)

        '''
        # Get key by group, assuming ' ' is the most occurring character => for ['g', ' ', 'b', 'j'] returns ['u', 'a', 'z', 'r']
        # keyByGroup = [
        #     alphabet[alphabet.index(' ') - ( alphabet.index(list(s_occurrenceByKey[0].keys())[0]) - alphabet.index('a') )],
        #     alphabet[alphabet.index(' ') - ( alphabet.index(list(s_occurrenceByKey[1].keys())[0]) - alphabet.index('a') )],
        #     alphabet[alphabet.index(' ') - ( alphabet.index(list(s_occurrenceByKey[2].keys())[0]) - alphabet.index('a') )],
        #     alphabet[alphabet.index(' ') - ( alphabet.index(list(s_occurrenceByKey[3].keys())[0]) - alphabet.index('a') )],
        # ]
        '''

        '''
        # Turn key for every group into shifts => for ['u', 'a', 'z', 'r'] returns [20, 0, 25, 17]
        shiftsByGroup = [
            (alphabet.index(keyByGroup[i]) - alphabet.index('a')) for i in range(len(keyByGroup))
        ]

        # print(keyByGroup)
        # print(shiftsByGroup)

        # Shift every letter in every group by appropriate shift
        shiftedGroups = []
        for i in range(4):
            shiftedGroup = []
            for letter in lettersByKey[i]:
                shiftedGroup.append(shiftLetter(letter, shiftsByGroup[i] * -1))
            shiftedGroups.append(shiftedGroup)
        
        # print(lettersByKey[0][0])
        # print(shiftedGroups[0][0])

        # print(shiftedGroups[1][0])
        # print(shiftedGroups[2][0])
        # print(shiftedGroups[3][0])

        # print(len(shiftedGroups[0]))
        # print(len(shiftedGroups[1]))
        # print(len(shiftedGroups[2]))
        # print(len(shiftedGroups[3]))
        '''

        '''
        # --------------------------------------- JOIN ALL GROUPS WITH KEY SHIFTS
        test = [None] * (len(shiftedGroups[0])+len(shiftedGroups[1])+len(shiftedGroups[2])+len(shiftedGroups[3]))

        for i in range(4):
            test[i::4] = shiftedGroups[i]
        
        # print(''.join(test))
        '''

        # --------------------------------------------------- CAESAR SOLUTION
        # fL = [ fileLine[i] for i in range(len(fileLine)) ]
        # test = ''.join([ shiftLetter(letter, -10) for letter in fL ])
        # print(fL)
        # print(test)


        
    
'''
a b c d e f g h i j k l m n o p q r s t u v w x y z _
g h i j k l m n o p q r s t u v w x y z _ a b c d e f
k l m n o p q r s t u v w x y z _ a b c d e f g h i j
o p q r s t u v w x y z _ a b c d e f g h i j k l m n
y z _ a b c d e f g h i j k l m n o p q r s t u v w x

gcgyiunyzjrybx
gcgyiunyzjrybx

gzzgiqfgzfjgbt

a b c d e f g h i j k l m n o p q r s t u v w x y z _
l m n o p q r s t u v w x y z _ a b c d e f g h i j k

a b c d e f g h i j k l m n o p q r s t u v w x y z _
------------------------------------------------------
_ a b c d e f g h i j k l m n o p q r s t u v w x y z
e f g h i j k l m n o p q r s t u v w x y z _ a b c d

'''
