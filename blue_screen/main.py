import pygame
import tkinter as tk
pygame.init()


root = tk.Tk()
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
root.destroy()
fenetre = pygame.display.set_mode((w, h), pygame.FULLSCREEN)


fond = pygame.image.load(("image/blue.png"))
fond = pygame.transform.scale(fond, (w, h))

continuer = True


while continuer == True:

    fenetre.blit(fond, (0, 0))
    pygame.mouse.set_visible(False)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
            pygame.quit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_BACKSPACE]:
        continuer = False

    pygame.display.flip()





