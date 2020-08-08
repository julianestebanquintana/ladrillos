import sys
import time
import pygame


ancho = 640
alto = 480
color_azul = (0, 0, 64)
color_blanco = (255, 255, 255)

pygame.init()  # Es necesario para poder usar las fuentes en un juego
#  pygame.font.init()


class Bolita(pygame.sprite.Sprite):
    # Los objetos que se ven en la pantalla en pygame, son sprites
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('bolita.png')
        # Cargar el rectángulo de la bolita
        self.rect = self.image.get_rect()
        # (x,y) : Center x
        # (0,0) : Esquina superior izquierda
        # (ancho, alto) : Esquina inferior derecha
        # Se le da una posición inicial central:
        self.rect.centerx = ancho/2
        self.rect.centery = alto/2
        # Establecer velocidad inicial
        self.speed = [3, -3]

    def update(self):
        # Evitar que se salga por arriba
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        # Evitar que se salga por los lados
        if self.rect.right >= ancho or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        # Mover según posición actual y velocidad
        self.rect.move_ip(self.speed)


class Raqueta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('paleta.png')
        # Cargar el rectángulo de la raqueta
        self.rect = self.image.get_rect()
        # Se le da una posición inicial centrada en pantalla en X.
        self.rect.midbottom = (ancho/2, alto - 20)
        # Establecer velocidad inicial
        self.speed = [0, 0]

    def update(self, evento):
        # Buscar si se presionó flecha izquierda
        if evento.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-6, 0]
        # Si se presionó flecha derecha
        elif evento.key == pygame.K_RIGHT and self.rect.right < ancho:
            self.speed = [6, 0]
        else:
            self.speed = [0, 0]
        # Mover según posición actual y velocidad
        self.rect.move_ip(self.speed)


class Ladrillo(pygame.sprite.Sprite):
    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('ladrillo.png')
        # Cargar el rectángulo del ladrillo
        self.rect = self.image.get_rect()
        # Se le da una posición inicial, provista externamente
        self.rect.topleft = posicion


class Muro(pygame.sprite.Group):
    # Existe un contenedor de sprites que se llama Group
    # Group permite agregar elementos con el método .add
    # Group permite dibujar el grupo con el método .draw
    def __init__(self, cantidad_ladrillos):
        pygame.sprite.Group.__init__(self)

        pos_x = 0
        pos_y = 20
        for i in range(cantidad_ladrillos):
            ladrillo = Ladrillo((pos_x, pos_y))
            self.add(ladrillo)

            pos_x += ladrillo.rect.width
            if pos_x >= ancho:
                pos_x = 0
                pos_y += ladrillo.rect.height


# Función llamada tras dejar ir la bolita
def juego_terminado():
    #  all_fonts = pygame.font.get_fonts()
    fuente = pygame.font.SysFont('Consolas', 72)
    texto = fuente.render('Game over', True, color_blanco)
    texto_rect = texto.get_rect()
    texto_rect.center = [ancho/2, alto/2]
    pantalla.blit(texto, texto_rect)
    pygame.display.flip()
    # Pausa por tres segundos antes de salir
    time.sleep(5)
    sys.exit()


def mostrar_puntuacion():
    fuente = pygame.font.SysFont('Consolas', 20)
    texto = fuente.render(str(puntuacion).zfill(5), True, color_blanco)
    texto_rect = texto.get_rect()
    texto_rect.topleft = [0, 0]
    pantalla.blit(texto, texto_rect)


def mostrar_vidas():
    fuente = pygame.font.SysFont('Consolas', 20)
    cadena = "Vidas: " + str(vidas).zfill(2)
    texto = fuente.render(cadena, True, color_blanco)
    texto_rect = texto.get_rect()
    texto_rect.topright = [ancho, 0]
    pantalla.blit(texto, texto_rect)


# Inicializando pantalla
pantalla = pygame.display.set_mode((ancho, alto))
# Adicionando título de pantalla
pygame.display.set_caption('Juego de Ladrillos')
# Para monitorear el tiempo, pygame ofrece el objeto .Clock
reloj = pygame.time.Clock()
# Ajustar repetición de evento de tecla presionada
pygame.key.set_repeat(30)

bolita = Bolita()
jugador = Raqueta()
muro = Muro(50)
puntuacion = 0
vidas = 3

while True:
    # Establecer los FPS permite determinar la máxima velocidad a la que va
    # a correrse el juego
    reloj.tick(60)

    # Se revisan los eventos...
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            jugador.update(evento)

    # Actualizar posición de la bolita
    bolita.update()

    # Colisión bolita - jugador
    if pygame.sprite.collide_rect(bolita, jugador):
        bolita.speed[1] = -bolita.speed[1]

    # Colisión bolita - muro
    #  pygame.sprite.spritecollide(bolita, muro, True)
    # Pide un booleano: ¿Los sprites tocados deben ser destruídos?
    # Pero esta solución elimina los ladrillos, pero no cambia la dirección
    # de la bolita. A continuación, otra solución:
    lista = pygame.sprite.spritecollide(bolita, muro, False)
    if lista:
        ladrillo = lista[0]
        cx = bolita.rect.centerx
        if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
            bolita.speed[0] = -bolita.speed[0]
        else:
            bolita.speed[1] = -bolita.speed[1]
        muro.remove(ladrillo)
        puntuacion += 10

    # Revisar si la bolita sale de la pantalla
    if bolita.rect.top > alto:
        vidas -= 1
        bolita.rect.top -= alto/2

    # Se rellena el fondo
    pantalla.fill(color_azul)
    # Se muestra la puntuación y las vidas
    mostrar_puntuacion()
    mostrar_vidas()
    # Dibujar bolita en pantalla
    # La función blit dibuja una superficie sobre otra.
    pantalla.blit(bolita.image, bolita.rect)
    # Se dibuja la raqueta del jugador
    pantalla.blit(jugador.image, jugador.rect)
    # Dibujar el muro
    muro.draw(pantalla)
    # Actualizar los elementos en pantalla
    pygame.display.flip()

    if vidas <= 0:
        juego_terminado()
