"""Utility functions and classes for calculating speed.

This module provides:
- Way to generate public ans private key using RSA
"""

import json
import math
import secrets
import tkinter as tk
from pathlib import Path
from tkinter import TOP, Button, filedialog

screen = tk.Tk()

def load_file_to_canvas(text: str) -> None:
    """Allow user to open document into tkinter canva.

    Args:
        text: Text actually display in the canva

    Raises:
        FileNotFoundError: If file not found or doesn't exist.

    """
    filename = filedialog.askopenfilename(title="Ouvrir votre document",
                                          filetypes=[("txt files", ".txt"), ("all files", ".*")])
    try:
        with Path.open(filename) as fichier:
            content = fichier.read()
            text.delete("1.0", tk.END)
            text.insert(tk.END, content)
    except FileNotFoundError as e:
        msg = "Le fichier n'a pas été sélectionné ou n'existe pas."
        raise FileNotFoundError(msg) from e

#Initialisation de la fenetre et des éléments
screen.title("Encoding content")

cnv = tk.Text(screen, width=50, height=20, bg="ivory")
cnv.pack(side=TOP, padx=5, pady=5)

# Bouton pour charger le texte depuis un fichier
load_button = Button(screen, text="Charger depuis un fichier", command=lambda: load_file_to_canvas(cnv))
load_button.pack(side=tk.LEFT, padx=5, pady=5)

# Bouton pour encrypter le texte
encrypt_button = Button(screen, text="Chiffrer", command=lambda: action(0))
encrypt_button.pack(side=tk.LEFT, padx=5, pady=5)

# Bouton pour décrypter le texte
decrypt_button = Button(screen, text="Dechiffrer", command=lambda: action(1))
decrypt_button.pack(side=tk.LEFT, padx=5, pady=5)

########################################Fonction utiliser pour le RSA########################################


def random_bit(n: int) -> int:
    """Generate a random number of size n bits.

    Args:
        n: Number of bis

    Returns:
        Random number with n bits

    """
    return secrets.randbelow(2**n - 1 - (2**(n-1)+1)) + (2**(n-1)+1)

def sieve_eratosthene(n: int) -> list[int]:
    """Calculate list of first prime number.

    Args:
        n: Max number to test

    Returns:
    List of n first prime number

    """
    prime = [True] * (n+1)
    p=2

    while p*p <= n:
        if prime[p]:
            for i in range(p*p, n+1, p):
                prime[i] = False
        p+=1

    return [p for p in range(2,n+1) if prime[p]]


first_prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383]

def primality_test(n: int) -> int:
    """Test if n is probably a prime number.

    Args:
        n: Number we want to test

    Returns:
        Random number with n bits

    """
    while True:
        candidate = random_bit(n)
        is_prime = True
        for p in first_prime_list:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break

        if is_prime:
            return candidate

def is_miller_rabin_passed(n:int, k:int=20) -> int:
    """Test if n is probably a prime number.

    Args:
        n: Number we want tot test
        k: Number of round (more accurate if bigger)

    Returns:
        Random number with n bits

    """
    if n<2:
        return False

    if n in {2, 3}:
        return True

    if n%2 == 0:
        return False

    r = 0
    s = n-1
    while s%2 == 0:
        r+=1
        s//=2
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a,s,n)
        if x==1 or x==n-1:
            continue
        for _ in range(r-1):
            x = pow(x,2,n)
            if x==n-1:
                break
        else:
            return False
    return True


def generate_prime_number(n: int) -> int:
    """Generate a prime number with n bits.

    Args:
        n: Number of bits

    Returns:
        Prime number with n bits

    """
    while True:
        candidate = secrets.randbits(n)
        # force odd and highest bit at 1
        candidate |= (1 << (n - 1)) | 1
        if is_miller_rabin_passed(candidate):
            return candidate

def modinv(a: int, m: int) -> int|None:
    """Modular inverse via extended Euclidean.

    Args:
      a: The integer for which the inverse is sought.
      m: Modulo

    Returns:
        int | None: The inverse of `a` modulo `m` if it exists, otherwise None.

    """
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m

def extended_gcd(a: int, b:int ) -> tuple[int,int,int]:
    """Compute the extended Euclidean algorithm.

    Args:
      a: First Integer
      b: Second Integer

    Returns:
        tuple[int, int, int]:
            - gcd(a, b): the greatest common divisor of a and b
            - x, y: coefficients such that a*x + b*y = gcd(a, b)

    """
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


########################################Handle encode and decode########################################

def generate_keys(size:int=100) -> tuple[int,int,int]:
    """Generate public and private key using RSA.

    Args:
      size: number of bits use to generate random number

    Returns:
        tuple[int, int, int]: A tuple containing the RSA key components
            - e: The public exponent
            - d: The private exponent
            - n: The modulo for both public and private keys

    """
    while True:
        p = generate_prime_number(size)
        q = generate_prime_number(size)

        n = p*q
        phi = (p-1)*(q-1)

        e = 65537
        if math.gcd(e, phi) != 1:
            continue

        d = modinv(e, phi)
        if d is None:
            continue

        return e,d,n


def rsa_chiffre(m: str, e: int, n:int) -> int:
    """Encrypt an integer message using the RSA public key.

    Args:
        m: The message to encrypt, represented as an integer.
        e: The public exponent.
        n: The modulus of the public key.

    Returns:
        int: The encrypted message as an integer.

    """
    a = m % n
    return pow(a, e, n)

def rsa_dechiffre(c: int, d: int, n: int) -> int:
    """Decrypt an integer message using the RSA private key.

    Args:
        c: The encrypted message to decrypt.
        d: The private exponent.
        n: The modulus of the private key.

    Returns:
        int: The decrypted message as an integer.

    """
    a = c % n
    return pow(a, d, n)

#----------------------------------------Fin fonction pour RSA----------------------------------------#


########################################Fonction gestion fichier avec JSON########################################

def save_secret_key(d: int, n: int) -> None:
    """Save the RSA private key to a file in JSON format.

    Args:
        d: The private exponent.
        n: The modulus of the private key.

    """
    f = Path.open("rsa_secret", "w")
    dico = {"n": n, "d": d}
    json.dump(dico, f, indent=2)
    f.close()

def load_secret_key() -> tuple[int,int]:
    """Load the RSA private key from a JSON file.

    Returns:
        A tuple containing (d, n) if the file exists and is valid, otherwise None.

    """
    try:
        f = Path.open("rsa_secret")
        r = json.load(f)
        return r["d"], r["n"]
    except FileNotFoundError:
        return None
    except json.decoder.JSONDecodeError:
        return None

def save_public_key(e: int, n: int) -> None:
    """Save the RSA public key to a file in JSON format.

    Args:
        e: The public exponent.
        n: The modulus of the public key.

    """
    f = Path.open("rsa_public", "w")
    dico = {"n": n, "e": e}
    json.dump(dico, f, indent=2)
    f.close()

#Fonction de récupération de cle public
def load_public_key() -> tuple[int,int]:
    """Load the RSA public key from a JSON file.

    Returns:
        A tuple containing (e, n) if the file exists and is valid, otherwise None.

    """
    try:
        f = Path.open("rsa_public")
        r = json.load(f)
        return r["e"], r["n"]
    except FileNotFoundError:
        return None
    except json.decoder.JSONDecodeError:
        return None

#----------------------------------------Fin fonction JSON----------------------------------------#


def mot_to_number(m: str) -> list[int]:
    """Convert a string into a list of Unicode code points.

    Args:
        m: The input string.

    Returns:
        A list of integers representing the Unicode code of each character.

    """
    return [ord(x) for x in m]

def number_to_mot(m: list[int]) -> str:
    """Convert a list of Unicode code points back into a string.

    Args:
        m: A list of integers representing Unicode codes.

    Returns:
        str: The reconstructed string.

    """
    return "".join(chr(x) for x in m)

def chiffre_text_rsa(m: str, e: int, n: int) -> list[str]:
    """Encrypt a text message using RSA, character by character.

    Args:
        m: The message to encrypt.
        e: The RSA public exponent.
        n: The RSA modulus.

    Returns:
        A list of encrypted numbers as strings, one for each character.

    """
    nombre = mot_to_number(m)
    return [str(rsa_chiffre(p, e, n)) for p in nombre]

#Dechiffrer un texte
def dechiffre_text_rsa(m: str, d: int, n: int) -> str:
    """Decrypt a text message previously encrypted with RSA.

    Args:
        m: The encrypted message, with numbers separated by spaces.
        d: The RSA private exponent.
        n: The RSA modulus.

    Returns:
        str: The decrypted text message.

    """
    m = m.split()
    return [rsa_dechiffre(int(p), d, n) for p in m]

#Gestion principale de mon programme, toute les actions passent par là
def action(type_action: int) -> None:
    """Handle the main program actions to encrypt or decrypt a message.

    Retrieve the message from the GUI, load or generate RSA keys if missing,
    and perform encryption or decryption. Display the result in the GUI.

    Args:
        type_action: The action type: 0 for encryption, 1 for decryption.

    """
    m = cnv.get("1.0", tk.END)
    public_key = load_public_key()
    private_key = load_secret_key()

    #Création fichier clé public et privée en cas de fichier ou contenu de fichier manquant
    if public_key is None or private_key is None:
        e,d,n = generate_keys(1000)

        public_key = e, n
        private_key = d, n

        save_secret_key(d, n)
        save_public_key(e, n)


    result = 0
    if type_action == 0:
        result = chiffre_text_rsa(m, public_key[0], public_key[1])
    if type_action == 1:
        result = dechiffre_text_rsa(m, private_key[0], private_key[1])

    cnv.delete("1.0", tk.END)
    if type_action ==0:
        for element in result:
            cnv.insert(tk.END, str(element) + "\n")
    else:
        cnv.insert(tk.END,str(result))

screen.resizable(width=False, height=False)

screen.mainloop()
