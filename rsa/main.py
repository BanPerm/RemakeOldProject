import random
import json
import tkinter as tk
from tkinter import *
from tkinter import filedialog

"""
Ce programme fonctionne avec une interface graphique sous le module tkinter
Une partie des fonction à été revu par ChatGPT en cas de bug et/ou pour l'optimisation de certaines qontions qui ont poser problèmes
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
screen.title("Une appli sympa")

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

# 100% sur de fonctionner
def EuclideEtendue(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        (c, v, g) = EuclideEtendue(b, a % b)
        (a, z, e) = (c, g, v - (a // b) * g)
    return (a, z, e)


# 100% fonctionnel
def premier_entre_eux(n, a):
    if n <= 1:
        return 0
    if n % a == 0:
        return 0
    if pow(a, n - 1, n) == 1:
        return 1
    else:
        return 0


# 100% fonctionnel
def my_random(a, b):
    return random.randint(a, b)


# 100% fonctionnel
def nombre_premier(longueur):
    a = my_random(2 ** (longueur - 1), 2 ** longueur)
    while not premier_entre_eux(a, 2) or not premier_entre_eux(a, 3):
        a = my_random(2 ** (longueur - 1), 2 ** longueur)
    return a


# 100% fonctionnel
def find_e(total):
    e = my_random(2, total)
    while not (e < total and premier_entre_eux(e, total)):
        e = my_random(2, total)
    return e


# 100% fonctionnel
def find_d(total, e):
    a, b, c = EuclideEtendue(total, e)
    return c % total


# 100% sur de fonctionner
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
    l = binaire_modulo(a, e, n)
    return l


def rsa_dechiffre(c, d, n):
    a = c % n
    l = binaire_modulo(a, d, n)
    return l

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
        p = nombre_premier(500)
        q = nombre_premier(500)

        n = p * q

        total = (q - 1) * (p - 1)

        e = find_e(total)
        d = find_d(total, e)

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
