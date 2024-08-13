import pygame
from states.state import State
from states.solo import Solo
from states.vs import Vs
from states.train_q import Train_Q

#Para Iteração automatica do treino
import itertools


class Choose(State):
	def __init__(self, game, entrymode):
		State.__init__(self, game)
		self.language()
		self.verifylang=False
		self.mode = entrymode#	VS 1				Train 3
		self.positionx = 0
		self.position = 0
		self.time = 0
		
		#self.pieces = {'monomino':False, 'domino':False, 'tromino':False, 'tetromino':True, 'pentomino':False}
		self.pieces = [False, False, False, True, False]

		#conjunto de peças que não são permitidas para VS, Co-op e Treino
		self.blockedPieces=[]
		self.blockedPieces.append([True, False, False, False, False])#	1
		self.blockedPieces.append([False, True, False, False, False])#	2
		self.blockedPieces.append([True, True, False, False, False])#	1,2
		self.blockedPieces.append([False, False, True, False, False])#	3
		self.blockedPieces.append([True, False, True, False, False])#	1,3
		self.blockedPieces.append([False, True, True, False, False])#	2,3

		self.warnings=[]

		#botões das peças
		self.recs_pieces= [pygame.Rect((self.game.canvas_w/2,self.game.canvas_h/2), (self.game.canvas_w/8,self.game.canvas_h/12)) for i in range(5)]
		for i in range(len(self.recs_pieces)):
			self.recs_pieces[i].center=(self.game.canvas_w*(0.2+0.15*i),self.game.canvas_h/6)
		#botões das larguras do campo
		self.recs_width= [pygame.Rect((self.game.canvas_w/2,self.game.canvas_h/2), (self.game.canvas_w/8,self.game.canvas_h/12)) for i in range(7)]
		for i in range(len(self.recs_width)):
			self.recs_width[i].center=(self.game.canvas_w*(0.08+0.14*i),self.game.canvas_h/3)
		#botões dos algoritmos
		#self.recs_alg = [pygame.Rect((self.game.canvas_w/2,self.game.canvas_h/2), (self.game.canvas_w/4,self.game.canvas_h/8)) for i in range(6)]
		self.recs_alg = [pygame.Rect((self.game.canvas_w/2,self.game.canvas_h/2), (self.game.canvas_w/4,self.game.canvas_h/8))]
		for i in range(1):
			self.recs_alg[i].center=(self.game.canvas_w*(0.25+0.25*(i+1)),self.game.canvas_h*(0.55))
		#for i in range(3,6):
		#	self.recs_alg[i].center=(self.game.canvas_w*(0.25+0.25*(i-3)),self.game.canvas_h*(0.75))
		#botões de controle
		self.recs_cont = [pygame.Rect((self.game.canvas_w/2,self.game.canvas_h/2), (self.game.canvas_w/8,self.game.canvas_h/8)) for i in range(2)]
		for i in range(len(self.recs_cont)):
			self.recs_cont[i].center=(self.game.canvas_w*(0.40+0.20*i),self.game.canvas_h*(0.90))
		
		self.selected_alg=-1
		if entrymode!=0:
			self.selected_alg=0
		self.selected_size=6
		#treino automatico
		self.combinations = [list(i) for i in itertools.product([False,True],repeat=5)]
		self.training_step=0
		
	
	def update(self, deltatime, actions):
		#Automatic training
		if self.mode==3 and self.training_step>=0:
			self.selected_alg=0
			self.position=4
			self.positionx=1
			if self.training_step >= len(self.combinations):
				self.selected_size+=1
				self.training_step=0
			if self.selected_size >= len(self.recs_width):
				actions["Scape"]=True
			else:
				actions["Confirm"]=True
				self.pieces = self.combinations[self.training_step]
				self.training_step+=1
			print("step:", self.training_step, ",	size: ", self.size[self.selected_size], ",	pieces: ",  self.pieces)
		
		movey = actions["Down"] - actions["Up"] #recebe o valor do movimento vertical
		movex = actions["Right"] - actions["Left"] #recebe o valor do movimento horizontal
		if self.time==0:
			self.position = (self.position + movey) % 5 # realiza o movimento dentre as opções
			if self.position==0:#Peças
				self.positionx = (self.positionx + movex) % len(self.recs_pieces) # realiza o movimento dentre as opções horizontais
			elif self.position==1:#larguras do campo
				self.positionx = (self.positionx + movex) % len(self.recs_width) # realiza o movimento dentre as opções horizontais
			elif self.position>3:
				self.positionx = (self.positionx + movex) % 2 # realiza o movimento dentre as opções horizontais
			else:
				self.positionx = (self.positionx + movex) % 3 # realiza o movimento dentre as opções horizontais
		if movey==0 or self.time>0.333:
			self.time=0
		else:
			self.time += deltatime
		
		
		if self.game.mouse:#se clicar
			for i in range(len(self.recs_pieces)):#Peças
				if self.recs_pieces[i].collidepoint(self.game.mouse_pos):
					actions["Confirm"]=True
					self.position=0
					self.positionx=i
			for i in range(len(self.recs_width)):#larguras do campo
				if self.recs_width[i].collidepoint(self.game.mouse_pos):
					actions["Confirm"]=True
					self.position=1
					self.positionx=i
			for i in range(len(self.recs_alg)):#algoritmos
				if self.recs_alg[i].collidepoint(self.game.mouse_pos):
					actions["Confirm"]=True
					if i<3:
						self.position=2
						self.positionx=i
					else:
						self.position=3
						self.positionx=i-3
			for i in range(2):#controle
				if self.recs_cont[i].collidepoint(self.game.mouse_pos):
					actions["Confirm"]=True
					self.position=4
					self.positionx=i
		
		if actions["Confirm"]:
			if self.position==0:#	Selecionar Peças
				self.pieces[self.positionx] = not self.pieces[self.positionx]
			if self.position==1:#	Selecionar largura do campo
				self.selected_size=self.positionx
			if self.position==2:#	Selecionar algoritmos(1-3)
				if self.selected_alg==self.positionx:
					self.selected_alg=-1
				else: 
					self.selected_alg=self.positionx
			if self.position==3:#	Selecionar algoritmos(4-6)
				self.selected_alg=self.positionx+3
			if self.position==4:#	Selecionar controle
				if self.positionx==0:
					actions["Scape"]=True
				else:#	Confirmar dados
					self.warnings=[]
					if any(self.pieces):#if exist True in self.pieces, ou seja se pelo menos 1 conjuto de peças for selecionado
						if self.selected_alg<0:#	se não houver algoritmo selecionado
							if self.mode==0:#	Solo mode
								self.game.playGame=True
								new_state = Solo(self.game, self.selected_alg+1, self.pieces, self.size[self.selected_size])
								new_state.state_in()
							else:# erro nº 2
								self.warnings.append(self.errors[1])
								print(self.errors[1])
						else:
							if self.mode==0:#	Solo mode
								self.game.playGame=True
								new_state = Solo(self.game, self.selected_alg+1, self.pieces, self.size[self.selected_size])
								new_state.state_in()
							elif (self.pieces in self.blockedPieces):#	se o conjunto de peças selecionadas for proibidos para VS, Co-op e training
								self.warnings.append(self.errors[2])
								print(self.errors[2])# erro nº 3
							else:
								self.game.playGame=True
								if self.mode==1:#	VS mode
									print(self.pieces)
								if self.mode==2:#	Co-op mode
									print(self.pieces)
								if self.mode==3:#	Train mode
									new_state = Train_Q(self.game, self.selected_alg+1, self.pieces, self.size[self.selected_size])
									new_state.state_in()
					else:# erro nº 1
						self.warnings.append(self.errors[0])
						print(self.errors[0])
		
		if actions["Scape"]:# retorna
			self.state_out()
		self.game.reset_actions()


	def draw(self, canvas):
		w,h = self.game.canvas_w, self.game.canvas_h
		canvas.fill(pygame.Color("aquamarine3"))
		
		self.game.text(canvas,self.titles[0], 36, pygame.Color("black"), w/2, h/12)
		for i in range(len(self.recs_pieces)):#					Peças
			if self.position==0 and self.positionx==i:
				pygame.draw.rect(canvas, pygame.Color("aliceblue"), self.recs_pieces[i], 0, int(h/50))
			pygame.draw.rect(canvas, pygame.Color("white"), self.recs_pieces[i],  int(h/150), int(h/50))
			self.game.text(canvas,self.pieces_names[i], 24, pygame.Color("black"), w*(0.2+0.15*i), h/6)
			if self.pieces[i]:
				pygame.draw.rect(canvas, pygame.Color("red"), self.recs_pieces[i],  int(h/150), int(h/50))
		
		self.game.text(canvas,self.titles[1], 36, pygame.Color("black"), w/2, h/4)
		for i in range(len(self.recs_width)):#					larguras do campo
			if self.position==1 and self.positionx==i:
				pygame.draw.rect(canvas, pygame.Color("aliceblue"), self.recs_width[i], 0, int(h/50))
			self.game.text(canvas, str(self.size[i])+" X 20", 24, pygame.Color("black"), w*(0.08+0.14*i), h/3)
			pygame.draw.rect(canvas, pygame.Color("white"), self.recs_width[i],  int(h/150), int(h/50))
			if self.selected_size==i:
				pygame.draw.rect(canvas, pygame.Color("red"), self.recs_width[i],  int(h/150), int(h/50))
		
		self.game.text(canvas,self.titles[2], 36, pygame.Color("black"), w/2, h*0.45)
		for i in range(1):#						algoritmos
			if self.position==2 and self.positionx==i:
				pygame.draw.rect(canvas, pygame.Color("aliceblue"), self.recs_alg[i],  0, int(h/50))
			if self.position==3 and self.positionx==(i-3):
				pygame.draw.rect(canvas, pygame.Color("aliceblue"), self.recs_alg[i],  0, int(h/50))
			pygame.draw.rect(canvas, pygame.Color("white"), self.recs_alg[i],  int(h/150), int(h/50))
			if self.selected_alg==i:
				pygame.draw.rect(canvas, pygame.Color("red"), self.recs_alg[i],  int(h/150), int(h/50))
			if i<3:
				self.game.text(canvas,self.option[i], 16, pygame.Color("black"), w*(0.25+0.25*((i+1))), h*(0.55))
			else:
				self.game.text(canvas,self.option[i], 16, pygame.Color("black"), w*(0.25+0.25*(i-3)), h*(0.75))
		
		for i in range(2):#						controle
			if self.position==4 and self.positionx==i:
				pygame.draw.rect(canvas, pygame.Color("aliceblue"), self.recs_cont[i],  0, int(h/50))
			pygame.draw.rect(canvas, pygame.Color("white"), self.recs_cont[i],  int(h/150), int(h/50))
			self.game.text(canvas, self.control[i], 24, pygame.Color("black"), w*(0.40+0.20*i), h*(0.90))
		
		#self.game.text(canvas,str(self.position)+"y", int(self.game.canvas_h/10), [200,100,255], self.game.canvas_w/4, self.game.canvas_h/2) #print posição


	def language(self):
		self.size = [8, 10, 12, 14, 16, 18, 20]
		if self.game.save["language"] == "EN":
			self.title="Algorithms"
			self.titles = {0:"Pieces",
							1:"Field Width",
							2:"Algorithms"}
			self.pieces_names = {0:"Monomino",
							1:"Domino",
							2:"Tromino",
							3:"Tetromino",
							4:"Pentomino"}
			self.option = {0:"1 - Q(Height mean, piece, 3 actions)",
							1:"2 - Q(10 x Column(Heigth/10), piece, 3 actions)"}
			self.control = {0:"Return",
							1:"Confirm"}
			self.errors = {0:"Selecione pelo menos um conjunto de peças",# erro nº1
				  			1:"Selecione um algoritimo",# erro nº2
							2:"O conjunto de peças selecionada não é valida para o modo de jogo selecionado"}# erro nº3
		elif self.game.save["language"] == "PT":
			self.title="Algoritmos"
			self.titles = {0:"Peças",
							1:"Largura do campo",
							2:"Algorítimos"}
			self.pieces_names = {0:"Monominó",
							1:"Dominó",
							2:"Triminó",
							3:"Tetraminó",
							4:"Pentaminó"}
			self.option = {0:"1 - Q(média das alturas, peças, 3 ações)",
							1:"2 - Q()",
							2:"3 - Q()",
							3:"4 - Q()",
							4:"5 - Q()",
							5:"6 - Q()"}
			self.control = {0:"Retornar",
							1:"Confirmar"}
			self.errors = {0:"Selecione pelo menos um conjunto de peças",# erro nº1
				  			1:"Selecione um algoritimo",# erro nº2
							2:"O conjunto de peças selecionada não é valida para o modo de jogo selecionado"}# erro nº3
			