import pygame
import sys

ancho = 640
alto = 480

# Inicializando pantalla

pantalla = pygame.display.set_mode((ancho, alto))

while True:
    # Se revisan los eventos...
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()

    pygame.display.flip()
