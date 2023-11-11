import pygame
import json

pygame.init()

#Définir taille écran
screen_height = 500
screen_width = 870

# Gestion temps et FPS
mainClock = pygame.time.Clock()
FPS = 144

# Music
pygame.mixer.music.load("song/song.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1, 0.0, 5000)

# Variable
run = True
argent = 0

# Image de fond
colour = pygame.image.load("image/font.jpg")

# Initialisation font texte
font = pygame.font.SysFont("broadway", 50, bold=False, italic=False)
font3 = pygame.font.SysFont("broadway", 25, bold=False, italic=False)

# Initialisation fenetre
screen = pygame.display.set_mode((screen_width, screen_height))

#Liste Objet button créer
allButton = []

#Affichage argent
argent = 0
argent_joueur = font.render (f"Patate: {argent}",True, (255,255,255))

#Sauvegarde Partie
def save():
    f = open('save.txt','w')
    dico = {}
    for c in allButton:
        nom = c.nom
        valeur_a_sauvegarder = ["nbachat","prix"]
        for i in valeur_a_sauvegarder:
            cle = f"{nom}.{i}"
            valeur = getattr(c, i)  # Utilisation de getattr pour récupérer la valeur de l'attribut
            dico[cle] = valeur
    json.dump(dico, f, indent=4)
    f.close()

# Gestion affichage prix et Argent au format scientifique
def notation_scientifique(nombre, virgule):
    s = str(nombre)
    exposant = len(s)
    return '%c.%se+%d' % (s[0], s[1:virgule + 1], exposant - 1)

# Gestion affichage prix et Argent au format fixe
def format_nombre_fixe(nombre, chiffres_apres_virgule):
    return '{:.{}f}'.format(nombre, chiffres_apres_virgule)


# Affichage des fps pour optimisation
def fps_counter():
    font2 = pygame.font.SysFont("comicsans", 15, bold=False, italic=False)
    fps = mainClock
    fps_t = font2.render(f'fps:{fps}', 1, (255, 255, 0))
    screen.blit(fps_t, (20, 50))

def draw():
    for i in allButton:
        i.draw()

def update_argent():
    font.render(f"Patate: {notation_scientifique(argent, 2)}", True, (255, 255, 255))
    screen.blit(argent_joueur, (screen_width / 2 - 100,  40))

###################################Bouton classe mère######################################

class BaseButton():
    def __init__(self, x, y, width, height, color, text, nom):
        self.nom = nom
        # Gestion position
        self.x = x
        self.y = y
        # Gestion color
        self.color = color
        # Gestion Taille
        self.width = width
        self.height = height
        # Gestion contenu
        self.text = text
        # Savoir si le bouton apparaît
        self.actif = False

    # Dessiner le bouton et son contenu
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        text = font3.render(self.text, True, (0, 0, 0))
        screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    # Test si le curseur rentre en collision avec le bouton
    def on(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


###################################Button######################################

class ButtonAchat(BaseButton):
    def __init__(self, x, y, width, height, color, text, prix, mult, image, nom):
        super().__init__(x, y, width, height, color, text, nom)
        # Gestion facteur progression prix
        self.mult = mult
        # Prix initial
        self.prix = prix
        # Nombre de fois acheté
        self.nbachat = 0
        # Image associée au bouton
        self.image = pygame.image.load(image)

        # Mettre à jour le texte du bouton en fonction du prix actuel
    def update_text(self):
        self.text = f"{self.text}:{notation_scientifique(self.prix, 2)}"

        # Regarde si le joueur peut payer en cas de clic
    def a_payer(self):
        global argent
        if argent >= self.prix:
            argent -= self.prix
            self.prix = round(self.mult * self.prix)
            self.nbachat += 1
            self.update_text()

    # Dessiner l'image du bouton en fonction du nombre d'achats
    def draw_image(self):
        nb = min(self.nbachat, 10)
        for x in range(nb):
            screen.blit(self.image, (220 + (x * 60), self.y))

    # Détruire le bouton (cette méthode peut être adaptée selon les besoins)
    def destroy(self):
        del self


#Création de mes bouttons
allButton.append(ButtonAchat(10,130,200,50,(255,255,255),'Kamarade',10,3,"image/player.png",'Kamarade'))

def game():
    global argent,argent_joueur
    running = True
    while running:
        screen.blit(colour, (0, 0))
        draw()
        update_argent()
        for i in allButton:
            i.draw_image()
        fps_counter()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in allButton:
                    if i.on(pos):
                        i.a_payer()

            if event.type == pygame.MOUSEMOTION:
                for i in allButton:
                    if i.on(pos):
                        i.color = (255,0,0)
                    else:
                        i.color = (255,255,0)

        pygame.display.update()
        mainClock.tick(144)

game()

pygame.quit()
