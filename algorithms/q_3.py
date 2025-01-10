import numpy as np
from algorithms.greedy import Greedy

class Q_learning():
	def __init__(self, poliminos, pieces):
		self.poliminos = poliminos
		self.actions = {"Left": False, "Right": False, "Soft_Drop": False,"Hard_Drop": False,
			"Rotate_Right": False, "Rotate_Left": False, "Hold": False } # dicionario com as ações do jogo
		
		#parametros de treinamento
		self.epsilon = 0.0 #the percentage of time when we should take the best action (instead of a random action)
		self.discount_factor = 0.9 #	𝛾(gamma)	discount factor for future rewards
		self.learning_rate = 0.1 #		α(alpha)	the rate at which the AI agent should learn
		
		self.g=Greedy(self.poliminos)#greedy search
		
		self.position=[]#armazena a posição da peça
		self.lastScore=0

	def update(self):
		#while self.poliminos
		if len(self.position)<1:#Se por algum motivo a posição não for obtida após escolher a ação
				self.get_pos()
		if self.execute_action():
			self.position=[]
		
	def get_pos(self):
		self.position=[]
		try:
			lista=self.g.update()
			#	pos, num_lines, awarded_lines,   score, attack,	holes, 	soma das alturas, alturas,	bumpiness, 	sum of well deep, 	TAI, AAINT, TNPB, stackAndAttack
			#	0,			1,				2, 		3, 		4,		5,					6,		7, 			8,					9,	10,		11,	12,		13
			#	positon = [	piece.pos[0], piece.pos[1], piece.facing, self.hold	]

			nplist=np.array(lista, dtype=list)
			#Max stackAndAttack
			self.position=lista[nplist[:,13].argmax()][0]
		except:
			print("An exception occurred")
			print("lista", lista)
			print("nplist", nplist)
			print("piece", self.poliminos.piece.shape)
			print("next", self.poliminos.next.shape)



	def execute_action(self):#	True e se for concluida
		#print('Pos', self.poliminos.piece.shape , self.poliminos.piece.pos,self.poliminos.piece.facing, self.position)
		if len(self.position)<1: return False
		if self.poliminos.score!=self.lastScore:#se a peça for posicionada
			self.lastScore=self.poliminos.score
			return True
		#print(str(self.poliminos.piece.pos)+"<"+str(self.position)+"?")
		if self.poliminos.can_hold and self.position[3]:#	HOLD
			self.actions["Hold"] = True
			return False
		if self.poliminos.piece.facing!=self.position[2]:#	rotaçionar
			self.actions["Rotate_Right"]=True
			#print("rotato")
		elif self.poliminos.piece.pos[1]<self.position[1]:
			#print("retry")
			#print(str(self.poliminos.piece.pos)+"<"+str(self.position))
			self.get_pos()
		elif self.poliminos.piece.pos[0]==self.position[0] and self.poliminos.piece.facing==self.position[2]:
			self.actions["Hard_Drop"]=True
		elif self.poliminos.piece.pos[0]>self.position[0]:
			self.actions["Left"]=True
		elif self.poliminos.piece.pos[0]<self.position[0]:
			self.actions["Right"]=True
		
		#print("now:"+str([self.poliminos.piece.pos,self.poliminos.piece.facing]))
		return False
	
		
	