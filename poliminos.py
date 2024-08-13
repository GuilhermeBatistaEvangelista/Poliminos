import pygame
from piece import Piece
import random

poliminos_list={
	'monomino':['1'],
	'domino':['2'],
	'tromino':['3_I', '3_L'],
	'tetromino':['4_T', '4_O', '4_J', '4_L', '4_I', '4_S', '4_Z'],
	'pentomino':['5_1', '5_2', '5_3', '5_4', '5_5', '5_6', '5_7', '5_8', '5_9', '5_10', '5_11', '5_12', '5_13', '5_14', '5_15', '5_16', '5_17', '5_18']
}


class Poliminos():
	def __init__(self, game, block_size, field_size_x, pieces, center):
		self.game = game
		self.language()
		self.block_size=block_size
		self.field_size_x = field_size_x
		#print(field_size_x)
		self.center=center # o centro horizontal do jogo
		self.grid_left=center+(self.block_size*-field_size_x/2)#posição X do inicio da grid
		self.grid_y=self.block_size*(3+19)#posição Y do inicio da grid
		self.matrix = [[0 for y in range(40)] for x in range(field_size_x)]# field_size_x*20 são o campo jogavel e field_size_x*20 são zona de buffer
		self.bag=[]
		
		names =['monomino', 'domino', 'tromino', 'tetromino', 'pentomino']
		i=0
		#definir peças que estão na bag
		for name in names:
			if pieces[i]:
				for polimino in poliminos_list[name]:
					self.bag.append(polimino)
			i+=1
		random.shuffle(self.bag)
		
		self.bagpos=0
		self.next_piece()#pega a primeiro pepça
		self.wait_time=0			#timer de espera entre peças
		self.time=0			#timer para queda
		self.hold_time=0 # tempo segundando um botão de movimento vertical
		self.hold = None
		self.can_hold=True		#se pode-se usar a função hold
		self.falling=True		#se a peça esta caindo ou em lock down
		self.moves_while_lockdown=0		#quantidade de vazes que o contador foi reiniciado
		self.locking_timer=0
		self.lowest_falling_height=40
		#GAME OVER conditions:
		self.TOP_OUT=False		#Se o ataque de um oponente força os blocos axistentes acima da zona de buffer
		self.LOCK_OUT=False		#Se o player posiciona uma peça completamente acima do topo da matrix
		self.BLOCK_OUT=False	#Se a proxima peça esta bloqueado por um bloco existente
		#Scoring and, etc...
		self.level=1
		self.total_lines_cleared=0
		self.lines_until_next=self.level*5
		self.score=0
		self.Back_to_Back=False
		#Não tem T-spin
		self.garbage=0
		self.garbage_gap_count=0
		self.garbage_gap_pos=random.randint(0, field_size_x-1) #numero aleatoria entre 0 e 9
		self.attack=0
		self.move_rec=[]

	def update(self, deltatime, actions):
		if self.BLOCK_OUT or self.LOCK_OUT or self.BLOCK_OUT:#			if GAME OVER
			return False
		self.attack=0	#limpa o ataque
		if self.wait_time<0.2:
			self.wait_time+=deltatime
			return True
		
		temp_moves=self.moves_while_lockdown # guarda a de quantidade movimentos realizados quando em lock down
		#Movimento vertical
		move_x = actions["Right"] - actions["Left"] #recebe o valor do movimento horizontal
		if move_x==0:self.hold_time=0
		if move_x!=0:
			if self.hold_time==0 or self.hold_time>0.1:
				moved=self.piece.move([move_x,0]) # realiza o movimento vertical da peça
				self.hold_time=0
				if not self.falling and moved:
					self.moves_while_lockdown+=1
			self.hold_time += deltatime
		#Rotação
		rotation = actions["Rotate_Right"] - actions["Rotate_Left"] #recebe o valor de rotação
		if rotation!=0:
			if self.piece.rotation(rotation): # realiza a rotação da peça
				self.last_move_rotation=True
				if not self.falling:
					self.moves_while_lockdown+=1
			actions["Rotate_Right"], actions["Rotate_Left"]=False, False
		#Hold
		if actions["Hold"] and self.can_hold:
			shape=self.piece.shape
			if self.hold is not None:
				self.piece = Piece(self, self.hold.shape, [3,20])
				self.BLOCK_OUT=self.piece.collision(self.piece.blocks)#testar BLOCK OUT
				self.falling = self.piece.move([0,-1])
			else:
				self.next_piece()
			self.hold= Piece(self, shape, [-6,15])
			self.lowest_falling_height=40
			self.moves_while_lockdown=0
			self.last_move_rotation=False
			self.locking_timer=0
			self.time=0				#reseta o timer de queda
			self.can_hold=False		#trava o uso da função hold até uma peça ser colocada
			actions["Hold"]=False
		#Hard Fall
		if actions["Hard_Drop"]:
			while self.piece.move([0,-1]):
				self.score+=2		#2 pontos para cada linha percorrida em um Hard_Drop
			self.lock_piece()
			actions["Hard_Drop"]=False
		
		#Fall
		if self.piece.move([0,-1]):#se existe espaço para cair
			self.piece.move([0,1])
			self.falling = True
			if self.piece.pos[1]<self.lowest_falling_height:
				self.lowest_falling_height=self.piece.pos[1]
				self.moves_while_lockdown=0
				self.locking_timer=0
			self.last_move_rotation=False
		else:	self.falling = False
		
		if self.falling:#Falling phase
			self.time+=deltatime
			if self.time>(((0.8-((self.level - 1)*0.007))**(self.level - 1))/(1+19*actions["Soft_Drop"])):
				self.time=0
				self.piece.move([0,-1])
				self.score+=1*actions["Soft_Drop"]		#1 pontos para cada linha percorrida em um Soft_Drop
		else:#Lock phase
			if self.moves_while_lockdown<15 and temp_moves!=self.moves_while_lockdown:#se o timer de lock down for reiniciado
				self.locking_timer=0
			else:
				self.locking_timer+=deltatime
				if self.locking_timer>=0.5:#se o timer atingir o limite
					self.lock_piece()
		return True
		
		

	def draw(self, canvas):
		rect = pygame.Rect(self.grid_left-self.block_size*7, 1.5*self.block_size, self.block_size*(self.field_size_x+14), self.block_size*23)
		pygame.draw.rect(canvas, pygame.Color("gold3"), rect, 0, 15)
		pygame.draw.rect(canvas, pygame.Color("gold"), rect, 3, 15)
		#desenhar score
		self.game.text(canvas,self.words[0], 24, pygame.Color("black"), self.grid_left+self.block_size*self.field_size_x*0.15, self.block_size*2.5)
		self.game.text(canvas,str(int(self.score)), 24, pygame.Color("black"), self.grid_left+self.block_size*self.field_size_x*0.5, 2.5*self.block_size)
		#desenha Hold
		self.game.text(canvas,self.words[1], 24, pygame.Color("black"), self.grid_left-self.block_size*4, self.block_size*5.5)
		rect = pygame.Rect(self.grid_left-self.block_size*6.5, 6*self.block_size, self.block_size*6, self.block_size*5)
		pygame.draw.rect(canvas, pygame.Color("black"), rect, 0, 10)
		pygame.draw.rect(canvas, pygame.Color("gold"), rect, 3, 10)
		if self.hold is not None:
			self.hold.draw(canvas)
		for y in range(3):#hold grid
			for x in range(5):
				rect = pygame.Rect(self.grid_left-self.block_size*6+x*self.block_size, 9*self.block_size-(y*self.block_size), self.block_size, self.block_size)
				pygame.draw.rect(canvas, pygame.Color("black"), rect, 1)
				#desenha Next
		self.game.text(canvas,self.words[2], 24, pygame.Color("black"), self.grid_left+self.block_size*(self.field_size_x+2.5), self.block_size*5.5)
		rect = pygame.Rect(self.grid_left+self.block_size*(self.field_size_x+0.5), 6*self.block_size, self.block_size*6, self.block_size*5)
		pygame.draw.rect(canvas, pygame.Color("black"), rect, 0, 10)
		pygame.draw.rect(canvas, pygame.Color("gold"), rect, 3, 10)
		self.next.draw(canvas)
		for y in range(3):
			for x in range(5):
				rect = pygame.Rect(self.grid_left+self.block_size*(self.field_size_x+1)+x*self.block_size, 9*self.block_size-(y*self.block_size), self.block_size, self.block_size)
				pygame.draw.rect(canvas, pygame.Color("black"), rect, 1)
		self.game.text(canvas,"Garbage  "+str(self.garbage), 24, pygame.Color("black"), self.grid_left+self.block_size*(self.field_size_x+3.5), self.block_size*11.5)
		#desenhar level
		self.game.text(canvas,self.words[3], 24, pygame.Color("black"), self.grid_left+self.block_size*self.field_size_x*0.15, self.block_size*23.5)
		self.game.text(canvas,str(int(self.level)), 24, pygame.Color("black"), self.grid_left+self.block_size*self.field_size_x*0.3, 23.5*self.block_size)
		#desenhar lines clears
		self.game.text(canvas,self.words[4], 24, pygame.Color("black"), self.grid_left+self.block_size*self.field_size_x*0.7, self.block_size*23.5)
		self.game.text(canvas,str(int(self.total_lines_cleared)), 24, pygame.Color("black"), self.grid_left+self.block_size*self.field_size_x*0.9, 23.5*self.block_size)
		#desenha o fundo da matriz
		rect = pygame.Rect(self.grid_left, 3*self.block_size, self.block_size*self.field_size_x, self.block_size*20)
		pygame.draw.rect(canvas, pygame.Color("black"), rect, 0)
		#desenha os blocos da matriz
		for x in range(self.field_size_x):
			for y in range(20):
				if self.matrix[x][y] !=0:
					if self.matrix[x][y] !=-1:
						self.matrix[x][y].draw(canvas)
					else:
						rect = pygame.Rect(self.grid_left+x*self.block_size, self.grid_y-(y*self.block_size), self.block_size, self.block_size)
						pygame.draw.rect(canvas, pygame.Color("gray55"), rect, 0)
		#desenha a peça
		if self.piece!=0 and self.wait_time>=0.2:
			self.piece.draw(canvas)
		#desenha a matriz
		for y in range(20):
			for x in range(self.field_size_x):
				rect = pygame.Rect(self.grid_left+x*self.block_size, self.grid_y-(y*self.block_size), self.block_size, self.block_size)
				pygame.draw.rect(canvas, pygame.Color("gray"), rect, 1)
		rect = pygame.Rect(self.grid_left, self.grid_y-19*self.block_size, self.block_size*self.field_size_x, self.block_size*20)
		pygame.draw.rect(canvas, pygame.Color("gray"), rect, 2, 3)
		#desenha os movimentos realizados
		for x in range(len(self.move_rec)):
			self.game.text(canvas,self.move_rec[x], 16, pygame.Color("gray"+str(round(x*7))), self.grid_left-self.block_size*3, self.block_size*(11.5+x))
	

	def next_piece(self):
		self.piece = Piece(self, self.bag[self.bagpos], [round(int(self.field_size_x/2))-round(int(self.bag[self.bagpos][0])/2), 20])
		if self.piece.collision(self.piece.blocks): #testar BLOCK OUT
			self.BLOCK_OUT=True
			return False
		self.falling = self.piece.move([0,-1])
		self.bagpos+=1
		if self.bagpos==len(self.bag):
			self.bagpos=0
			random.shuffle(self.bag)
		self.next = Piece(self, self.bag[self.bagpos], [self.field_size_x+1,15])
		self.can_hold=True
		
		
		self.lowest_falling_height=40
		self.moves_while_lockdown=0
		self.locking_timer=0
		self.time=0
		return True

	def lock_piece(self):
		self.LOCK_OUT=True
		for block in self.piece.blocks:
			self.matrix[block.pos[0]][block.pos[1]] = block	#guarda o bloco na matriz
			if block.pos[1]<20:#testar Lock Out
				self.LOCK_OUT=False		#se algum bloco do piece estiver dentro da matriz não sera Lock Out
		if self.LOCK_OUT:
			return False
		self.pattern_recognition()
		self.next_piece()
		self.wait_time=0
	
	def pattern_recognition(self):#r
		lines=self.full_line()
		num_lines=len(lines)
		
		#Moves:
		awarded_lines=0
		if num_lines==1:#1 line clear
			self.score+=100*self.level
			awarded_lines=1
			self.attack=0
			self.Back_to_Back=False
			self.move_rec.insert(0,"Single")
		elif num_lines==2:#2 line clear
			self.score+=300*self.level
			awarded_lines=3
			self.attack=1
			self.Back_to_Back=False
			self.move_rec.insert(0,"Double")
		elif num_lines==3:#3 line clear
			self.score+=500*self.level+(500*self.level*0.5*self.Back_to_Back)
			awarded_lines=5+(5*0.5*self.Back_to_Back)
			self.attack=2+(1*self.Back_to_Back)
			self.Back_to_Back=True
			self.move_rec.insert(0,"Triple")
		elif num_lines==4:#Tetris
			self.score+=800*self.level+(800*self.level*0.5*self.Back_to_Back)
			awarded_lines=8+(8*0.5*self.Back_to_Back)
			self.attack=4+(1*self.Back_to_Back)
			self.Back_to_Back=True
			self.move_rec.insert(0,"Tetris")
		elif num_lines==5:#Petris
			self.score+=1200*self.level+(1200*self.level*0.5*self.Back_to_Back)
			awarded_lines=12+(12*0.5*self.Back_to_Back)
			self.attack=6+(1*self.Back_to_Back)
			self.Back_to_Back=True
			self.move_rec.insert(0,"Petris")
		
		if len(self.move_rec)>10:
			self.move_rec.pop()
		#Atualiza o level, linhas até o proximo level e o total de linhas
		if self.level<15:#15 é o level maximo
			self.lines_until_next-=awarded_lines
			while self.lines_until_next<=0:
				self.level+=1
				self.lines_until_next+=self.level*5
		self.total_lines_cleared+=awarded_lines
		#Ataque e contra-ataque
		self.attack_and_counter()
		if len(lines)!=0:#se alguma linha tiver sido completa, Line clear
			self.clear_lines(lines)#Apaga as linhas completadas
		self.add_garbage()
	
	def full_line(self):#indentifica as linhas completas 
		lines=[]
		for y in range(40):
			column=0
			for x in range(self.field_size_x):
				if self.matrix[x][y] !=0:
					column+=1
			if column == self.field_size_x:#se todas as colunas da linha estiverem ocupadas
				lines.append(y)
		return lines		#retorna uma lista com as linhas completas
	
	def attack_and_counter(self):
		if self.garbage!=0 and self.attack!=0:#Calcula o resultado do ataque e do garbage, se ambos existirem
			if self.garbage>self.attack:
				self.garbage -= self.attack
				self.attack=0
			elif self.garbage<self.attack:
				self.attack -= self.garbage
				self.garbage=0
			else:
				self.attack, self.garbage = 0, 0
		

	def clear_lines(self, lines):#Apaga as linhas completas
		for i in range(len(lines)):
			for x in range(self.field_size_x):
				for y in range(lines[i]+1,40):
					self.matrix[x][y-1] = self.matrix[x][y]
					if self.matrix[x][y-1]!=0 and self.matrix[x][y-1]!= -1:
						self.matrix[x][y-1].pos[1]-=1
			for j in range(i,len(lines)):
				lines[j]-=1
		for x in range(self.field_size_x):
			self.matrix[x][39]=0
	
	def add_garbage(self):#Adicionar as linhas de garbage
		for x in range(self.field_size_x):#checa top out
			if self.matrix[x][39-self.garbage]!=0:
			#se exitir um bloco na linha que saira do topo da matriz com a adição de garbage, resultara em TOP_OUT
				self.TOP_OUT=True
				return
		while self.garbage>0:#se existir garbage
			#todos os blocos da matriz 1 linha
			for x in range(self.field_size_x):
				for y in range(38, -1, -1):#de 38 até 0
					self.matrix[x][y+1] = self.matrix[x][y]
					if self.matrix[x][y+1]!=0 and self.matrix[x][y+1]!= -1:
						self.matrix[x][y+1].pos[1]+=1
			#adicionar linha no fundo da matriz
			for x in range(self.field_size_x):
				self.matrix[x][0] = -1
			self.matrix[self.garbage_gap_pos][0]=0
			self.garbage_gap_count+=1
			if self.garbage_gap_count==8:#muda a posição do espaço vazio nas linhas de garbage a cada 8 linhas
				self.garbage_gap_count=0
				self.garbage_gap_pos=random.randint(0, self.field_size_x-1)
			self.garbage-=1
	
	def language(self):
		if self.game.save["language"] == "EN":
			self.words = ["Score","Hold","Next","Level","Lines"]
			
		elif self.game.save["language"] == "PT":
			self.words = ["Pontuação","Hold","Proxima","Nível","Linhas"]
