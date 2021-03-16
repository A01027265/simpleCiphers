from os import listdir, path


if __name__ == "__main__":
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

    letters = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z, '.split(',')
    occurrence = []
    for letter in letters:
        occurrence.append(fileLine.count(letter))

    lOccurrence = {}
    for idx, letter in enumerate(letters):
        lOccurrence.update({ letter: occurrence[int(idx)] })

    s_lOccurrence = {key: value for key, value in sorted(lOccurrence.items(), key=lambda item: item[1], reverse=True)}

    # alphaFreq = ' ,e,a,r,i,o,t,n,s,l,c,u,d,p,m,h,g,b,f,y,w,k,v,x,z,j,q'.split(',')
    alphaFreq = ' ,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,a,b,c,d,e,f,g,h,i,j'.split(',')
    s_letters = list(s_lOccurrence.keys())
    s_occurrence = list(s_lOccurrence.values())

    print(alphaFreq, len(alphaFreq))
    print(s_letters, len(s_letters))
    print(s_occurrence, len(s_occurrence))
    
    fileLine_copy = fileLine
    for idx, letter in enumerate(alphaFreq):
        fileLine_copy = fileLine_copy.replace(s_letters[idx], alphaFreq[idx])
    
    print(fileLine_copy)