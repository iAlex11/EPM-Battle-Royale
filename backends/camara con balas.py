import pygame, sys, time, random, math
from pygame.locals import *

velJugador = 5

def mover(B,camera_pos):
    pos_x,pos_y = camera_pos
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:

        B[1] -= velJugador
        pos_y += velJugador
    if key[pygame.K_a]:

        B[0] -= velJugador
        pos_x += velJugador
    if key[pygame.K_s]:

        B[1] += velJugador
        pos_y -= velJugador
    if key[pygame.K_d]:

        B[0] += velJugador
        pos_x -= velJugador


    if B[0] < 0:
        B[0] = 0
        pos_x = camera_pos[0]
    elif B[0] > anchoMapa-20:
        B[0] = anchoMapa-20
        pos_x = camera_pos[0]
    if B[1] < 0:
        B[1] = 0
        pos_y = camera_pos[1]
    elif B[1] > anchoMapa-20:
        B[1] = anchoMapa-20
        pos_y = camera_pos[1]

    return (pos_x,pos_y)

anchoPantalla = 800
largoPantalla = 800
anchoMapa = 2000
largoMapa = 2000
cadencia = 7

pygame.init()
mundo=pygame.Surface((anchoMapa,largoMapa))
V=pygame.display.set_mode((anchoPantalla,largoPantalla))
pygame.display.set_caption('EPM Battle Royale v1.0b2019f6')


Negro=(0,0,0)
Blanco=(255,255,255)
Rojo=(255,0,0)
Verde=(0,255,0)
Azulo=(0,0,255)
Azulc=(51,153,255)
Morado=(102,0,102)
Amarillo=(255,255,0)
Gris=(110,110,110)
Naranja=(252,152,3)

cambiox=0
cambioy=0

B=pygame.Rect(0,0,20,20)
reloj=pygame.time.Clock()
camara=((B[0]-10)+anchoPantalla//2,(B[1]-10)+largoPantalla//2)

contador=5
abajo=False
balas=[]
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
           pygame.quit()
           sys.exit()

        if event.type==MOUSEBUTTONDOWN:
            abajo=True


        if event.type==MOUSEBUTTONUP:
            abajo=False
            contador=cadencia

    if abajo and contador>0:
        contador-=1
    V.fill(Negro)
    mundo.fill(Azulc)

    while abajo and contador<=0:
        try:
            pos=pygame.mouse.get_pos()
            l=[]
            largo=(pos[0]-anchoPantalla//2)
            alto=(pos[1]-largoPantalla//2)
            hip=math.sqrt((largo**2)+(alto**2))
            v=250/hip
            l.append(B.centerx)
            l.append(B.centery)
            l.append((largo*v)/12)
            l.append((alto*v)/12)
            balas.append(l)
            contador=cadencia
        except:
            pass

    mundo.fill(Verde)


    camara=mover(B,camara)

    pygame.draw.rect(mundo,Rojo,B)










    for i in range(len(balas)):
        balas[i][0]+=balas[i][2]
        balas[i][1]+=balas[i][3]
        pygame.draw.rect(mundo,Azulo,(balas[i][0],balas[i][1],5,5))

    for x in range(len(balas)-1,0,-1):
        try:
            if balas[x][0]<=-5 or balas[x][0]>=anchoMapa or balas[x][1]<=-5 or balas[x][1]>=largoMapa:
                balas.remove(balas[x])

        except:
            pass
    V.blit(mundo,camara)
    pygame.display.update()
    reloj.tick(60)
