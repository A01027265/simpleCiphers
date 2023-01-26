<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
<h3 align="center">Simple Ciphers</h3>

  <p align="center">
    Simple implementations of cryptography and cryptoanalysis on Caesar's Cipher, Vigenere's Cipher, and One Time Pads.
    <br />
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#caesars-cipher">Caesar's Cipher</a></li>
        <li><a href="#vigeneres-cipher">Vigenere's Cipher</a></li>
        <li><a href="#one-time-pad">One Time Pad</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#abilities-mastered">Abilities Mastered</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Simple cipher contains simple implementations of cryptography and cryptoanalysis on Caesar's Cipher, Vigenere's Cipher, and One Time Pads.

All three programs use the following alphabet: `'abcdefghijklmnopqrstuvwxyz '`.

`caesar.py` and `vigenere.py` both assume that the ciphertext is in english and use the following 5 words to cryptoanalyse and decipher a ciphertext with an unknown key:
```
[' the ', ' be ', ' to ', ' of ', ' and ']
```
> A list of 100 words that occur most frequently in written English is given below, based on an analysis of the Oxford English Corpus. 
[Source](https://en.wikipedia.org/wiki/Most_common_words_in_English)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Caesar's Cipher
`caesar.py` can cipher a user's input plaintext with a given key, decipher a user's input ciphertext with a known given key, and find an unknown key for an input ciphertext ciphered with caesar's cipher (in this case the ciphertext is input as a `.txt` file in `./input` and chosen in the CLI).

The approach taken to cryptoanalyse and decipher an ciphertext with an unknown key is to assume that `' '` is one of the most occurrent characters in the ciphertext and proceeding to find the top most occurrent characters in the ciphertext.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Vigenere's Cipher
`vigenere.py` can cipher a user's input plaintext with a given key, decipher a user's input ciphertext with a known given key, and find an unknown key for an input ciphertext (in this case the ciphertext is input as a `.txt` file in `./input` and chosen in the CLI).

**Note:** `vigenere.py` is made only to find unknown keys that are 4 characters in length and it assumes that the ciphertext is in english.

When finding an unknown key for an input ciphertext, `vigenere.py` assumes that the original unknown plaintext has the following alphabet: `'abcdefghijklmnopqrstuvwxyz '` and does not contain line breaks or any other characters not included in the alphabet. It finds the unknown ciphertext through the following steps:

1. Divides the ciphertext's characters into 4 groups (`'hello world'` would be divided into `[ ['h','o','r'],['e', ' ', 'l'],['l','w','d'],['l','o']`).
2. Finds the top 4 most occurrent characters in each group.
3. Assuming `' '` is one of the top 4 most occurrent characters in each group, it finds the appropriate shifts for each characacter of the top 4 most occurrent characters per group.
4. Generates all the possible 4 lettered keys that the ciphertext could have (256 possible keys).
5. Uses 4 threads that each decipher the text with 64 possible keys and count the number of appearances of the top 5 most common words in the english language (the, be, to, of, and), and each returns the key which had the most total matches of these substrings.
6. Asks the user to pick one of the top 4 most possible plain texts and outputs the plaintext and key to a `.txt` file.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### One Time Pad
`onetimepad.py` will cipher a user's input plaintext with a randomly generated key which is the length of the user's input plaintext, and given the key and the ciphertext, it can decipher the ciphertext back into a plain text. 

This program uses the function `vigenere(text, key, cipher)` and the only thing it does differently from `vigenere.py` is that it generates a completely random key which it inputs into that function to cipher the plaintext. `onetimepad.py` also uses the same function to decipher the given ciphertext with a given key.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[![Python][Python]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ABILITIES MASTERED -->
## Abilities Mastered

* Enciphering and Deciphering a plaintext/ciphertext with a key using Caesar's Cipher, Vigenere's Cipher, and a One Time Pad
* Implementation of Caesar's Cipher, Vigenere's Cipher, and One Time Pad
* Decipher through cryptoanalysis a ciphertext with an unknown key enciphered with Caesar's Cipher or Vigenere's Cipher

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/empobla/simpleCiphers.git
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Caesar's Cipher
With this script, you can: 
1. Cipher a message with a key
2. Decipher a message with a key
3. Decrypt a message in a file. 

In order to decrypt a message in a file, you must save the file as a `.txt` in the `input/` directory. The output of the decrypted file will be found in `outputs/original_file_name.txt`, with the key of the cipher and the decrypted message.

In order to run this script, follow the following instructions:

1. `cd` into the project's directory
   ```sh
   cd simpleCiphers
   ```
2. Run `caesar.py`
   ```sh
   python caesar.py
   ```

### Vigenere's Cipher
With this script, you can: 
1. Cipher a message with a key
2. Decipher a message with a key
3. Decrypt a message in a file. 

In order to decrypt a message in a file, you must save the file as a `.txt` in the `input/` directory. The script will then analyze the ciphertext and will find possible keys that decipher the given text. After chosing the key that deciphers the ciphertext, the script will output the plain text as an output file. The output of the decrypted file will be found in `outputs/original_file_name.txt`, with the key of the cipher and the decrypted message.

In order to run this script, follow the following instructions:

1. `cd` into the project's directory
   ```sh
   cd simpleCiphers
   ```
2. Run `vigenere.py`
   ```sh
   python vigenere.py
   ```

### One Time Pad
With this script, you can: 
1. Cipher a message
2. Decipher a message

When enciphering a plaintext message with this script, the script will create a One Time Pad, encipher the plaintext message, and output the ciphertext and the key to the console. These outputs can be used with this script's second option, which will decipher the message.

In order to run this script, follow the following instructions:

1. `cd` into the project's directory
   ```sh
   cd simpleCiphers
   ```
2. Run `onetimepad.py`
   ```sh
   python onetimepad.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

This project is property of Emilio Popovits Blake. All rights are reserved. Modification or redistribution of this code must have _explicit_ consent from the owner.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Emilio Popovits Blake - [Contact](https://emilioppv.com/contact)

Project Link: [https://github.com/empobla/simpleCiphers](https://github.com/empobla/simpleCiphers)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Most common words in english](https://en.wikipedia.org/wiki/Most_common_words_in_English)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/emilio-popovits

[Python]: https://img.shields.io/badge/python-3776ab?style=for-the-badge&logo=python&logoColor=ffdc52
[Python-url]: https://aws.amazon.com