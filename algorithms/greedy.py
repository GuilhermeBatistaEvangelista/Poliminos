from piece import Piece
import copy
class Greedy():
	def __init__(self, poliminos):
		self.poliminos = poliminos
		self.matrix = self.poliminos.matrix
	
	def update(self):
		self.values=[]
		self.hold=False
		self.i=0
		#print("piece:"+str([self.poliminos.piece.pos,self.poliminos.piece.facing]))
		piece = Piece(self.poliminos, self.poliminos.piece.shape, [round(int(self.poliminos.field_size_x/2))-round(int(self.poliminos.piece.shape[0])/2), 20])
		piece.rotation(self.poliminos.piece.facing)
		piece.move([0,-1])
		piece.move( [self.poliminos.piece.pos[0]-piece.pos[0], self.poliminos.piece.pos[1]-piece.pos[1]] )
		#piece.move([0,-1])
		#print("new:"+str([piece.pos,piece.facing]))
		#print(piece.shape)
		
		self.search(piece)#	busca para peça atual
		
		if self.poliminos.can_hold:#Se poder trocar dar hold na peça
			self.hold=True
			if self.poliminos.hold:#se hold Não estiver vazio
				piece = Piece(self.poliminos, self.poliminos.hold.shape, [round(int(self.poliminos.field_size_x/2))-round(int(self.poliminos.hold.shape[0])/2), 20])
			else:
				piece = Piece(self.poliminos, self.poliminos.next.shape, [round(int(self.poliminos.field_size_x/2))-round(int(self.poliminos.next.shape[0])/2), 20])
			piece.move([0,-1])
			self.search(piece)#	busca para peça atual
		
		return self.values
	
	def search(self, piece):
		#print(' ')
		#print(piece.shape)
		rotations=3
		if piece.shape=='1' or piece.shape=='4_O' or piece.shape=='5_14':
			rotations=0
		elif piece.shape=='2' or piece.shape=='3_I' or piece.shape=='4_I' or piece.shape=='4_S' or piece.shape=='4_Z' or piece.shape=='5_1' or piece.shape=='5_17' or piece.shape=='5_18':
			rotations=1
		
		#print(f'Facing:{piece.facing}')
		self.get_moves(piece)
		while rotations!=0:
			piece.rotation(1)
			#print(f'Facing:{piece.facing}')
			self.get_moves(piece)
			rotations-=1
	
	def get_moves(self, piece):#movimenta a peça por todas as colunas
		#print('move_x')
		count=0
		while piece.move([1,0]):#move para a direita até onde é possivel 
			pass
		self.drop(piece)#movimento de queda
		count=0
		#print(f'	{piece.pos}')
		i=1
		while piece.move([-1,0]):#move para a esquerda até onde é possivel 
			count-=1
			#print(piece.pos)
			self.drop(piece)#movimento de queda
			i+=1
		self.i+=i
		piece.move([count,0])#retorna a peça para o centro
	
	def drop(self, piece):
		#print("drop",piece.pos)
		count=0
		while piece.move([0,-1]):#drop piece
			count+=1
		num_lines = self.full_line(piece)
		self.save_move(piece, self.patters(num_lines, piece ), self.get_parameters(piece, num_lines) )
		piece.move([0,count])#retorna a peça para a linha inicial
		
	def save_move(self, piece, scores, parameters):
		if piece.pos[1]<=self.poliminos.piece.pos[1]:
			pos=[piece.pos[0], piece.pos[1], piece.facing, self.hold]
			self.values.append([pos, scores[0], scores[1], scores[2], scores[3], parameters[0], sum(parameters[1]), parameters[1]])
			#					pos, num_lines, awarded_lines,   score, attack,			holes, 		soma das alturas, alturas
			#					0,			1,				2, 		3, 		4,				5,						6,		7
		
	def full_line(self, piece):#conta linhas completas
		lines=[]
		matrix=self.matrix
		for y in range(40):
			column=0
			filled=False
			for x in range(self.poliminos.field_size_x):
				if matrix[x][y]!=0:
					filled=True
				for block in piece.blocks:
					if block.pos[0]==x and block.pos[1]==y:
						filled=True
				if filled:
					column+=1
					filled=False
			if column== self.poliminos.field_size_x:#se todas as colunas da linha estiverem ocupadas
				lines.append(y)
		return len(lines)		#retorna o numero de linhas completas
	
	def get_parameters(self, piece, num_lines):
		holes=0
		heights=[]
		matrix=self.matrix
		count=0
		filled=False
		empit=False
		for x in range(self.poliminos.field_size_x):
			for y in range(20):
				if matrix[x][y]!=0:
					filled=True
				for block in piece.blocks:
					if block.pos[0]==x and block.pos[1]==y:
						filled=True
				if filled:
					count = y
					filled=False
			for y in range(count):
				if matrix[x][y]==0:
					empit=True
				for block in piece.blocks:
					if block.pos[0]!=x and block.pos[1]!=y:
						empit=True
				if empit:
					holes+=1
					empit=False
			heights.append(count-num_lines)
			count=0
		return [holes, heights]
	
	def patters(self, num_lines, piece):
		#Moves:
		awarded_lines=0
		score=0
		attack=0
		if num_lines==1:#1 line clear	#Single
			score+=100*self.poliminos.level
			awarded_lines=1
			attack=0
			self.poliminos.Back_to_Back=False
		elif num_lines==2:#2 line clear	#Double
			score+=300*self.poliminos.level
			awarded_lines=3
			attack=1
			self.poliminos.Back_to_Back=False
		elif num_lines==3:#3 line clear	#Triple
			score+=500*self.poliminos.level+(500*self.poliminos.level*0.5*self.poliminos.Back_to_Back)
			awarded_lines=5+(5*0.5*self.poliminos.Back_to_Back)
			attack=2+(1*self.poliminos.Back_to_Back)
			self.poliminos.Back_to_Back=False
		elif num_lines==4:#Tetris
			score+=800*self.poliminos.level+(800*self.poliminos.level*0.5*self.poliminos.Back_to_Back)
			awarded_lines=8+(8*0.5*self.poliminos.Back_to_Back)
			attack=4+(1*self.poliminos.Back_to_Back)
			self.poliminos.Back_to_Back=True
		elif num_lines==5:#Petris
			score+=1200*self.poliminos.level+(1200*self.poliminos.level*0.5*self.poliminos.Back_to_Back)
			awarded_lines=12+(12*0.5*self.poliminos.Back_to_Back)
			attack=6+(1*self.poliminos.Back_to_Back)
			self.poliminos.Back_to_Back=True
		return [num_lines, awarded_lines, score, attack]
