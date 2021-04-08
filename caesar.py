from os import listdir, path

alphabet = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z, '.split(',')
words = [' the ', ' be ', ' to ', ' of ', ' and ']

def shiftLetter(letter, shift):
    newIdx = alphabet.index(letter) + shift
    if newIdx >= 27:
        return alphabet[newIdx-27]
    elif newIdx >= 0 and newIdx < 27:
       return alphabet[newIdx]
    else:
        return alphabet[27+newIdx]

def caesar(text, key, cipher):
    keyShift = None
    if cipher:
        # keyShift = shift in key ('g' becomes 6) (encryption)
        keyShift = alphabet.index(key)
    else:
        # keyShift = shift in key, but negative ('g' becomes -6) (decryption)
        keyShift = alphabet.index(key) * -1
    
    textLetters = [ text[i] for i in range(len(text)) ] # parse all characters in text into an array
    caesarText = [ shiftLetter(textLetters[i], keyShift) for i in range(len(textLetters)) ]   # shift every letter to encrypt/decrypt text

    return ''.join(caesarText)

if __name__ == "__main__":
    print('Caesar\'s Cipher')
    print('------------------')
    print('1. Cipher a message')
    print('2. Decipher a message')
    print('3. Decrypt a message in a file')
    choice = input('\nYour Choice: ')

    if choice == '1':
        print('\nPlease input the plaintext you want to cipher and the key (key must be one character long)')
        plaintext = input('Plain Text: ')
        key = input('Key: ')

        cipherText = caesar(plaintext, key, True)
        print('\nYour ciphertext is: ', cipherText)
    elif choice == '2':
        print('\nPlease input the ciphertext you want to decipher and the key')
        ciphertext = input('Cipher Text: ')
        key = input('Key: ')

        plainText = caesar(ciphertext, key, False)
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

        # Count occurrence of letters in text => [151, 36, 100, 3, 114, 0, ..., 266, 389] (len: 27)
        occurrence = [ fileLine.count(letter) for letter in alphabet ]

        # print(occurrence, len(occurrence))

        # Order most occurring letters in text in dictionary => { 'g': 1092, 'l': 491, ' ': 389, ..., 'x': 2, 'f': 0 }
        occurrenceDict = {}
        for idx, letter in enumerate(alphabet):
            occurrenceDict.update({ letter: occurrence[int(idx)] })
        s_occurrence = { key: value for key, value in sorted(occurrenceDict.items(), key = lambda item: item[1], reverse=True ) }
        
        # print(s_occurrence)

        # Get top 4 letter occurrences in dictionary => ['g', 'l', ' ', 'v']
        top4Letters = [ list(s_occurrence.keys())[i] for i in range(4) ]

        # print(top4Letters)

        # Get possible keys, assuming ' ' is the most occuring character => ['g', 'l', ' ', 'v'] returns ['h', 'm', 'a', 'w']
        possibleKeys = [ shiftLetter(top4Letters[i], 1) for i in range(4) ]

        # print(possibleKeys)

        # Find key, assuming possible plaintext with most matches is original plaintext
        textMatches = 0
        plaintext = ''
        key = ''
        for possibleKey in possibleKeys:
            possibleText = caesar(fileLine, possibleKey, False)
            
            matches = 0
            for word in words:
                matches += possibleText.count(word)

            if matches >= textMatches:
                textMatches = matches
                plaintext = possibleText
                key = possibleKey

        # Output plaintext and key with most matches to a file
        outputFile = open('./output/' + selectedFile.split('.')[0] + '_plaintext.' + selectedFile.split('.')[1], 'w')
        outputFile.write('Key: ' + key + '\n')
        outputFile.write('---------------------------------------\n')
        outputFile.write(plaintext)
        outputFile.close()

        print('Plaintext and key outputted to ./output/' + selectedFile.split('.')[0] + '_plaintext.' + selectedFile.split('.')[1])