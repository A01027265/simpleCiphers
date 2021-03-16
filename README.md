# Simple Ciphersd
Simple cipher contains simple implementations of cryptography and cryptoanalysis on Caesar's Cipher, Vigenere's Cipher, and One Time Pads.

All three programs use the following alphabet: `'abcdefghijklmnopqrstuvwxyz '`.

`caesar.py` and `vigenere.py` both assume that the ciphertext is in english and use the following 5 words to cryptoanalyse and decipher a ciphertext with an unknown key:
```
[' the ', ' be ', ' to ', ' of ', ' and ']
```
> A list of 100 words that occur most frequently in written English is given below, based on an analysis of the Oxford English Corpus. 
[Source](https://en.wikipedia.org/wiki/Most_common_words_in_English)

## Abilities Mastered
- Enciphering and Deciphering a plaintext/ciphertext with a key using Caesar's Cipher, Vigenere's Cipher, and a One Time Pad
- Implementation of Caesar's Cipher, Vigenere's Cipher, and One Time Pad
- Decipher through cryptoanalysis a ciphertext with an unknown key enciphered with Caesar's Cipher or Vigenere's Cipher

# Caesar's Cipher
`caesar.py` can cipher a user's input plaintext with a given key, decipher a user's input ciphertext with a known given key, and find an unknown key for an input ciphertext ciphered with caesar's cipher (in this case the ciphertext is input as a `.txt` file in `./input` and chosen in the CLI).

The approach taken to cryptoanalyse and decipher an ciphertext with an unknown key is to assume that `' '` is one of the most occurrent characters in the ciphertext and proceeding to find the top most occurrent characters in the ciphertext.

# Vigenere's Cipher
`vigenere.py` can cipher a user's input plaintext with a given key, decipher a user's input ciphertext with a known given key, and find an unknown key for an input ciphertext (in this case the ciphertext is input as a `.txt` file in `./input` and chosen in the CLI).

**Note:** `vigenere.py` is made only to find unknown keys that are 4 characters in length and it assumes that the ciphertext is in english.

When finding an unknown key for an input ciphertext, `vigenere.py` assumes that the original unknown plaintext has the following alphabet: `'abcdefghijklmnopqrstuvwxyz '` and does not contain line breaks or any other characters not included in the alphabet. It finds the unknown ciphertext through the following steps:

1. Divides the ciphertext's characters into 4 groups (`'hello world'` would be divided into `[ ['h','o','r'],['e', ' ', 'l'],['l','w','d'],['l','o']`).
2. Finds the top 4 most occurrent characters in each group.
3. Assuming `' '` is one of the top 4 most occurrent characters in each group, it finds the appropriate shifts for each characacter of the top 4 most occurrent characters per group.
4. Generates all the possible 4 lettered keys that the ciphertext could have (256 possible keys).
5. Uses 4 threads that each decipher the text with 64 possible keys and count the number of appearances of the top 5 most common words in the english language (the, be, to, of, and), and each returns the key which had the most total matches of these substrings.
6. Asks the user to pick one of the top 4 most possible plain texts and outputs the plaintext and key to a `.txt` file.

# One Time Pad
`onetimepad.py` will cipher a user's input plaintext with a randomly generated key which is the length of the user's input plaintext, and given the key and the ciphertext, it can decipher the ciphertext back into a plain text. 

This program uses the function `vigenere(text, key, cipher)` and the only thing it does differently from `vigenere.py` is that it generates a completely random key which it inputs into that function to cipher the plaintext. `onetimepad.py` also uses the same function to decipher the given ciphertext with a given key.