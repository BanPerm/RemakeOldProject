import random
import json
import tkinter as tk
from tkinter import Button, TOP
from tkinter import filedialog
from numpy import gcd

"""
Ce programme fonctionne avec une interface graphique sous le module tkinter
Une partie des fonction à été revu par ChatGPT en cas de bug et/ou pour l'optimisation de certaines fontions qui ont poser problèmes
Il y a possibilité de charger des fichier qu'il soient en .txt ou autre
"""
screen = tk.Tk()

#Cette donction permet de changer le texte d'un élément, je l'utilise ici pour changer le texte de mon canva
def load_file_to_canvas(text):
    filename = filedialog.askopenfilename(title="Ouvrir votre document",
                                          filetypes=[('txt files', '.txt'), ('all files', '.*')])
    try:
        with open(filename, "r") as fichier:
            content = fichier.read()
            text.delete("1.0", tk.END)
            text.insert(tk.END, content)
    except FileNotFoundError:
        print("Le fichier n'a pas été sélectionné ou n'existe pas.")

#Initialisation de la fenetre et des éléments
screen.title("Encoding content")

cnv = tk.Text(screen, width=50, height=20, bg="ivory")
cnv.pack(side=TOP, padx=5, pady=5)

# Bouton pour charger le texte depuis un fichier
load_button = Button(screen, text='Charger depuis un fichier', command=lambda: load_file_to_canvas(cnv))
load_button.pack(side=tk.LEFT, padx=5, pady=5)

# Bouton pour encrypter le texte
encrypt_button = Button(screen, text='Chiffrer', command=lambda: action(0))
encrypt_button.pack(side=tk.LEFT, padx=5, pady=5)

# Bouton pour décrypter le texte
decrypt_button = Button(screen, text='Dechiffrer', command=lambda: action(1))
decrypt_button.pack(side=tk.LEFT, padx=5, pady=5)

########################################Fonction utiliser pour le RSA########################################


def random_bit(n):
    """
    Generate a random number of size n bits
    
    :param n: Number of bis
    """
    return(random.randrange(2**(n-1)+1, 2**n-1))

def sieve_eratosthene(n):
    """
    Calculate list of first prime number
    
    :param n: max number to test
    """

    prime = [True] * (n+1)
    p=2

    while p*p <= n:
        if prime[p]:
            for i in range(p*p, n+1, p):
                prime[i] = False
        p+=1
    
    res = []
    for p in range(2, n+1):
        if prime[p]:
            res.append(p)
    
    return res

first_prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383]

def primality_test(n):
    """
    Return True if n is probably prime
    
    :param n: Number we want to test
    """
    while True:
        candidate = random_bit(n)
        for divisor in first_prime_list:
            if candidate%divisor != 0 and divisor**2>=candidate:
                return candidate
            
def is_miller_rabin_passed(n, k=20):
    """
    Return True if n is probably prime
    
    :param n: Number we want to test
    :param k: Number of round (more accurate if bigger)
    """
    if n<2:
        return False

    if n == 2 or n==3:
        return True
    
    if n%2 == 0:
        return False
    
    r = 0
    s = n-1
    while s%2 == 0:
        r+=1
        s//=2
    for _ in range(k):
        a = random.randrange(2,n-1)
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


def generate_prime_number(n):
    number = primality_test(n)
    while not is_miller_rabin_passed(number):
        number = primality_test(n)
    return number

########################################Handle encode and decode########################################

def generate_keys(size=100):
    print('hello')
    p = generate_prime_number(size)
    q = generate_prime_number(size)

    print('test')

    n = p*q
    phi = (p-1)*(q-1)

    e = 2
    while e<phi and gcd(e,phi) != 1:
        e+=1

    d = 2
    while d<phi and (e*d)%phi !=1:
        d+=1

    return e,d,n


def binaire_modulo(a, e, n):
    result = 1
    while e > 0:
        if e % 2 == 1:
            result = (result * a) % n
        e //= 2
        a = (a * a) % n
    return result


def rsa_chiffre(m, e, n):
    a = m % n
    return binaire_modulo(a, e, n)

def rsa_dechiffre(c, d, n):
    a = c % n
    return binaire_modulo(a, d, n)

#----------------------------------------Fin fonction pour RSA----------------------------------------#


########################################Fonction gestion fichier avec JSON########################################

#Fonction de sauvegarde de cle priver
def save_secret_key(d, n):
    f = open('rsa_secret', 'w')
    dico = {"n": n, "d": d}
    json.dump(dico, f, indent=2)
    f.close()

#Fonction de récupération de cle priver
def load_secret_key():
    try:
        f = open('rsa_secret', 'r')
        r = json.load(f)
        return r["d"], r["n"]
    except FileNotFoundError:
        return None
    except json.decoder.JSONDecodeError:
        return None

#Fonction de sauvegarde de cle public
def save_public_key(e, n):
    f = open('rsa_public', 'w')
    dico = {"n": n, "e": e}
    json.dump(dico, f, indent=2)
    f.close()

#Fonction de récupération de cle public
def load_public_key():
    try:
        f = open('rsa_public', 'r')
        r = json.load(f)
        return r["e"], r["n"]
    except FileNotFoundError:
        return None
    except json.decoder.JSONDecodeError:
        return None

#----------------------------------------Fin fonction JSON----------------------------------------#


#Convertir les mot en nombre
def mot_to_number(m):
    return [ord(x) for x in m]

#Convertir nombre en mot
def number_to_mot(m):
    return ''.join(chr(x) for x in m)

#Chiffrer un texte
def chiffre_text_rsa(m, e, n):
    nombre = mot_to_number(m)
    resultat = []
    for p in nombre:
        resultat.append(str(rsa_chiffre(p, e, n)))
    return resultat

#Dechiffrer un texte
def dechiffre_text_rsa(m, d, n):
    m = m.split()
    resultat = []
    for p in m:
        resultat.append(rsa_dechiffre(int(p), d, n))
    lettre = number_to_mot(resultat)
    return lettre

#Gestion principale de mon programme, toute les actions passent par là
def action(type):
    m = cnv.get("1.0", tk.END)
    public_key = load_public_key()
    private_key = load_secret_key()

    #Création fichier clé public et privée en cas de fichier ou contenu de fichier manquant
    if public_key is None or private_key is None:
        e,d,n = generate_keys(100)

        public_key = e, n
        private_key = d, n

        save_secret_key(d, n)
        save_public_key(e, n)


    result = 0
    if type == 0:
        result = chiffre_text_rsa(m, public_key[0], public_key[1])
    if type == 1:
        result = dechiffre_text_rsa(m, private_key[0], private_key[1])

    cnv.delete("1.0", tk.END)
    if type ==0:
        for element in result:
            cnv.insert(tk.END, str(element) + "\n")
    else:
        cnv.insert(tk.END,str(result))

screen.resizable(False, False)

screen.mainloop()