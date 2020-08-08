import pygame
import sys

class Bolita(pygame.sprite.Sprite):
    # Los objetos que se mueven en pygame son sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('bolita.png')
        # Cargar el rectángulo de la bolita
        self.rect = self.image.get_rect()

ancho = 640
alto = 480

# Inicializando pantalla
pantalla = pygame.display.set_mode((ancho, alto))
# Adicionando título de pantalla
pygame.display.set_caption('Juego de Ladrillos')

bolita = Bolita()

while True:
    # Se revisan los eventos...
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()

    # Dibujar bolita en pantalla
    pantalla.blit(bolita.image, bolita.rect)
    pygame.display.flip()
