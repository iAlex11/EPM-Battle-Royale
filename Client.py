import pygame as pg
import random, sys, ast, json, socket, threading, time, math, pyautogui


def dibujarTexto(text, font, surface, x, y, color):
	objText = font.render(text, 1, color)
	rectText = objText.get_rect()
	rectText.center = (x, y)
	surface.blit(objText, rectText)


def WaitForKeyPress():
	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				Finish()
			if event.type == pg.KEYDOWN:
				return


def Finish():
	pg.quit()
	sys.exit()

#playerName = input('Name: ')


userList = []
passwordList = []

file = open('Logins.txt')
fileLines = file.readlines()
for x in fileLines:
	users = []
	pwds = []
	coma1Found = False
	for y in x:
		if y != ';' and y != '\n':
			if not coma1Found:
				users.append(y)
			elif coma1Found:
				pwds.append(y)

		if y == ';':
			coma1Found = True

	userList.append(''.join(users))
	passwordList.append(''.join(pwds))
print(userList)
print(passwordList)
user = 0

file.close()

uName = None

if pyautogui.confirm(text='Login or register:', title='Login', buttons=['Login', 'Register', 'Back']) == 'Login':
	while True:
		uName = pyautogui.prompt(text='Username', title='Login', default='')
		if uName in userList:
			for x in range(len(userList)):
				if userList[x] == uName:
					user = x
					while True:
						pwd = pyautogui.password(text='Password', title='Login', default='', mask='*')
						if pwd == passwordList[user]:
							pyautogui.alert(text='Done', title='Login', button='OK')
							break
						elif pwd == None:
							break

						else:
							pyautogui.alert(text='Incorrect password. Try again', title='Login error', button='OK')
		elif uName == None:
			break

		else:
			pyautogui.alert(text='Incorrect usrename. Try again', title='Login error', button='OK')
			continue
		break

if uName == None:
	Finish()

playerName = "Player " + uName
zzName = "zz" + playerName

## Inicializar pygame
pg.init()
reloj = pg.time.Clock()

## Configurar venana
dimensiones = [800, 600]
sv = pg.display.set_mode(dimensiones)
pg.display.set_caption('GameStructure')

## Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (2, 247, 18)
AZULcLARO = (0, 0, 255)
AZULoSCURO = (0, 0, 60)
NARANJA = (255, 204, 0)
GRIS = (174, 187, 186)
AMARILLO = (255, 255, 0)


class Pared(pg.sprite.Sprite):
	def __init__(self, color, x, y, largo, alto):
		super().__init__()
		self.image = pg.Surface([largo, alto])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Bala(pg.sprite.Sprite):
	def __init__(self, color, x, y, radio, velX, velY):
		super().__init__()
		self.image = pg.Surface([2*radio, 2*radio])
		self.image.fill(ROJO)
		pg.draw.circle(self.image, color, (x, y), radio)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.velX = velX
		self.velY = velY

	def update(self):
		self.rect.x += self.velX
		self.rect.y += self.velY

class Player(pg.sprite.Sprite):
	def __init__(self, color, largo, alto, x, y):
		super().__init__()
		self.image = pg.Surface([largo, alto])#self.image = pg.image.load('[path]').convert() /n self.image.set_colorkey(NEGRO)
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.velX = 0
		self.velY = 0
		self.paredes = None

		self.largo = largo
		self.alto = alto

	def cambioVel(self, x, y):
		self.velX += x
		self.velY += y


	def shoot(self):

		self.targetCenter = (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
		self.catetoX = self.targetCenter[0]-self.rect.x
		self.catetoY = self.targetCenter[1]-self.rect.y
		self.hipotenusa = math.sqrt(self.catetoX**2 + self.catetoY**2)

		self.relCatX_CatY = math.ceil(self.catetoX/self.catetoY)
		self.relHipOrg_HipNueva = self.hipotenusa/2000

		self.proyVelX = self.catetoX/self.relHipOrg_HipNueva
		self.proyVelY = self.catetoY/self.relHipOrg_HipNueva


		bala = Bala(ROJO, self.rect.x, self.rect.y, 3, self.proyVelX/200, self.proyVelY/200)
		listaBalas.add(bala)
		bullets.append([ROJO, self.rect.x, self.rect.y, 3, 0])

		#parsed[playerName][1].append({"c": ROJO, "x": self.rect.x, "y": self.rect.y, "r": 3})


		'''loopCount = 0

		for item in parsed[playerName][1]:
			item["c"] = bullets[loopCount][0]
			item["x"] = bullets[loopCount][1]
			item["y"] = bullets[loopCount][2]
			item["r"] = bullets[loopCount][3]
			loopCount += 1'''


	def updateOnNetwork(self):
		parsed[playerName]["x"] = self.rect.x
		parsed[playerName]["y"] = self.rect.y

		#for item in parsed[playerName]


	def update(self):
		self.rect.x += self.velX

		listaImpactos = pg.sprite.spritecollide(self, self.paredes, False)
		for bloque in listaImpactos:
			if self.velX > 0:
				self.rect.right = bloque.rect.left
			elif self.velX < 0:
				self.rect.left = bloque.rect.right


		self.rect.y += self.velY

		listaImpactos = pg.sprite.spritecollide(self, self.paredes, False)
		for bloque in listaImpactos:
			if self.velY > 0:
				self.rect.bottom = bloque.rect.top
			elif self.velY < 0:
				self.rect.top = bloque.rect.bottom

class Habitacion():
	def __init__(self):
		self.paredList = pg.sprite.Group()

class Hab1(Habitacion):
	def __init__(self):
		super().__init__()
		paredes = [[AZULcLARO, 0, 0, 10, 600],
				   [AZULcLARO, 0, 0, 800, 10],
				   [AZULcLARO, 0, 590, 800, 10],
				   [AZULcLARO, 790, 0, 10, 800]]#Paredes
		for item in paredes:
			pared = Pared(item[0], item[1], item[2],item[3],item[4])
			self.paredList.add(pared)


class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def sendMsg(self):
		while True:
			if parsedCreated:
				self.sock.send(bytes(str(parsed), 'utf-8'))
			else:
				self.sock.send(bytes('Hola', 'utf-8'))
			time.sleep(1/60)

	def __init__(self, address, name):
		self.sock.connect((address, 10000))
		self.sock.send(bytes(zzName, 'utf-8'))
		time.sleep(1)

		iThread = threading.Thread(target=self.sendMsg)
		iThread.daemon = True
		iThread.start()



## ----------------------------------------

##pg.mixer.music.load('musicaDeFondo.mid')
##pg.mixer.music.play(-1)

dibujarTexto('The   Final   Game', pg.font.SysFont('ZenzaiItacha', 80), sv, 250, 150, BLANCO)
dibujarTexto('Press start to continue', pg.font.SysFont('ZenzaiItacha', 60), sv, 250, 350, BLANCO)

pg.display.update()

WaitForKeyPress()

parsedCreated = False

client = Client(sys.argv[1], sys.argv[2])

while True:

	parsed = {playerName: {"x": 100, "y": 100}}
	parsedCreated = True


	listaSprites = pg.sprite.Group()
	listaParedes = pg.sprite.Group()
	playersGroup = pg.sprite.Group()
	listaBalas = pg.sprite.Group()
	bullets = []

	player = Player(BLANCO, 20, 20, 100, 100)
	playersGroup.add(player)
	listaSprites.add(player)


	hab1 = Hab1()
	player.paredes = hab1.paredList
	listaSprites.add(hab1.paredList)
	listaParedes.add(hab1.paredList)

	habActual = hab1


	hecho = False

	## Game loop
	while not hecho:

		sv.fill(NEGRO)

		data = client.sock.recv(1024)

		dataDict = {}
		dataProcessed = str(data, 'utf-8')

		if '}{' in str(data, 'utf-8'):
			dataProcessed = str(data, 'utf-8').split('}{')[0]
			dataProcessed = dataProcessed + '}'


		try:
			dataDict = ast.literal_eval(str(dataProcessed))
		except:
			pass

		if data:
			#print('Server --> ' + dataProcessed)
			print(dataDict)

		try:
			for item in dataDict["Players"]:
				if list(item.keys())[0] != playerName:
					xPos = item[list(item.keys())[0]]["x"]
					yPos = item[list(item.keys())[0]]["y"]
					pg.draw.rect(sv, ROJO, (xPos, yPos, 30, 30))

					'''for bullet in item[list(item.keys())[0]][1]:
						bulletX = bullet["x"]
						bulletY = bullet["y"]
						bulletW = bullet["r"]
						bulletH = bullet["r"]

						pg.draw.rect(sv, VERDE, (bulletX, bulletY, bulletW, bulletH))
		'''
		except:
			pass

		for item in bullets:
			item[4] += 1

			if item[4] >= 60:
				bullets.pop(bullets.index(item))



		#client.sock.send(bytes(parsed, 'utf-8'))


		for event in pg.event.get():
			if event.type == pg.QUIT:
				hecho = True

			if event.type == pg.KEYDOWN:
				if event.key == pg.K_UP:
					player.cambioVel(0, -5)
				if event.key == pg.K_DOWN:
					player.cambioVel(0, 5)
				if event.key == pg.K_RIGHT:
					player.cambioVel(5, 0)
				if event.key == pg.K_LEFT:
					player.cambioVel(-5, 0)

			if event.type == pg.KEYUP:
				if event.key == pg.K_UP:
					player.cambioVel(0, 5)
				if event.key == pg.K_DOWN:
					player.cambioVel(0, -5)
				if event.key == pg.K_RIGHT:
					player.cambioVel(-5, 0)
				if event.key == pg.K_LEFT:
					player.cambioVel(5,  0)

			if event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 1:
					player.shoot()

		player.updateOnNetwork()

		for item in listaBalas:
			item.update()

		player.update()
		playersGroup.draw(sv)
		habActual.paredList.draw(sv)
		listaBalas.draw(sv)

		reloj.tick(60)
		pg.display.update()

	dibujarTexto('Game', pg.font.SysFont('ZenzaiItacha', 80), sv, 250, 150, BLANCO)
	dibujarTexto('Over', pg.font.SysFont('ZenzaiItacha', 80), sv, 250, 250, BLANCO)
	pg.display.update()
	WaitForKeyPress()
