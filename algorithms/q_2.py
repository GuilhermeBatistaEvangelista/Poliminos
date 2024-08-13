import numpy as np
from algorithms.greedy import Greedy

TETROMINO = {'T':0, 'O':1, 'J':2, 'L':3, 'I':4, 'S':5, 'Z':6}
poliminos_list={
	'monomino':['1'],
	'domino':['2'],
	'tromino':['3_I', '3_L'],
	'tetromino':['4_T', '4_O', '4_J', '4_L', '4_I', '4_S', '4_Z'],
	'pentomino':['5_1', '5_2', '5_3', '5_4', '5_5', '5_6', '5_7', '5_8', '5_9', '5_10', '5_11', '5_12', '5_13', '5_14', '5_15', '5_16', '5_17', '5_18']
}

class Q_learning():
	def __init__(self, poliminos, pieces):
		self.poliminos = poliminos
		self.actions = {"Left": False, "Right": False, "Soft_Drop": False,"Hard_Drop": False,
			"Rotate_Right": False, "Rotate_Left": False, "Hold": False } # dicionario com as ações do jogo
		
		self.piece_list=[]
		names =['monomino', 'domino', 'tromino', 'tetromino', 'pentomino']
		i=0
		#definir peças que estão na lista de peças
		for name in names:
			if pieces[i]:
				for polimino in poliminos_list[name]:
					self.piece_list.append(polimino)
			i+=1
		
		#				Q(N x Coluna esta acima de 10, piece, 3 actions)
		#							 											3 ações(Minimizar  buracos, Minimizar altura, Maximizar linhas)
		if self.poliminos.field_size_x==8:
			self.q_values = np.zeros((2,2,2,2,  2,2,2,2, len(self.piece_list), 3))
		elif self.poliminos.field_size_x==10:
			self.q_values = np.zeros((2,2,2,2,  2,2,2,2,  2,2, len(self.piece_list), 3))
		elif self.poliminos.field_size_x==12:
			self.q_values = np.zeros((2,2,2,2,  2,2,2,2,  2,2,2,2, len(self.piece_list), 3))
		elif self.poliminos.field_size_x==14:
			self.q_values = np.zeros((2,2,2,2,  2,2,2,2,  2,2,2,2,  2,2, len(self.piece_list), 3))
		elif self.poliminos.field_size_x==16:
			self.q_values = np.zeros((2,2,2,2,  2,2,2,2,  2,2,2,2,  2,2,2,2, len(self.piece_list), 3))
		elif self.poliminos.field_size_x==18:
			self.q_values = np.zeros((2,2,2,2,  2,2,2,2,  2,2,2,2,  2,2,2,2,  2,2, len(self.piece_list), 3))
		elif self.poliminos.field_size_x==20:
			self.q_values = np.zeros((2,2,2,2,  2,2,2,2,  2,2,2,2,  2,2,2,2,  2,2,2,2, len(self.piece_list), 3))
		
		self.column=[]
		for i in range(self.poliminos.field_size_x):
			self.column.append(0)
		
		#parametros de treinamento
		self.epsilon = 0.0 #the percentage of time when we should take the best action (instead of a random action)
		self.discount_factor = 0.9 #discount factor for future rewards
		self.learning_rate = 0.1 #the rate at which the AI agent should learn
		
		self.g=Greedy(self.poliminos)#greedy search
		
		self.old_garbage=0
		self.height_mean=0
		self.total_lines_cleared=0
		self.current_piece = self.piece_list.index(self.poliminos.piece.shape)
		self.position=0#armazena a posição da peça
		self.old_action =-1
		self.all_actions = [ 0, 0, 0]#	lista de ações tomadas
		self.current_action =self.get_next_action()
		self.training=True

	def update(self):
		#while self.poliminos
		if self.current_action==-1:
			if self.training:
				self.update_q_value()
			#print("new action")
			self.current_action = self.get_next_action()
		if self.execute_action():
			self.old_action = self.current_action
			self.current_action=-1	
		

	def get_next_action(self):
		if np.random.random() < self.epsilon:
			#return np.argmax(self.q_values[self.heights[0], self.heights[1], self.heights[2], self.heights[3], self.heights[4], self.heights[5], self.heights[6], self.heights[7], self.heights[8], self.heights[9], self.current_piece])
			if self.poliminos.field_size_x==8:
				action = np.argmax(self.q_values[self.column[0],self.column[1],self.column[2],self.column[3],  self.column[4],self.column[5],self.column[6],self.column[7], self.current_piece])
			elif self.poliminos.field_size_x==10:
				action = np.argmax(self.q_values[self.column[0],self.column[1],self.column[2],self.column[3],  self.column[4],self.column[5],self.column[6],self.column[7],  self.column[8],self.column[9], self.current_piece])
			elif self.poliminos.field_size_x==12:
				action = np.argmax(self.q_values[self.column[0],self.column[1],self.column[2],self.column[3],  self.column[4],self.column[5],self.column[6],self.column[7],  self.column[8],self.column[9],self.column[10],self.column[11], self.current_piece])
			elif self.poliminos.field_size_x==14:
				action = np.argmax(self.q_values[self.column[0],self.column[1],self.column[2],self.column[3],  self.column[4],self.column[5],self.column[6],self.column[7],  self.column[8],self.column[9],self.column[10],self.column[11],  self.column[12],self.column[13], self.current_piece])
			elif self.poliminos.field_size_x==16:
				action = np.argmax(self.q_values[self.column[0],self.column[1],self.column[2],self.column[3],  self.column[4],self.column[5],self.column[6],self.column[7],  self.column[8],self.column[9],self.column[10],self.column[11],  self.column[12],self.column[13],self.column[14],self.column[15], self.current_piece])
			elif self.poliminos.field_size_x==18:
				action = np.argmax(self.q_values[self.column[0],self.column[1],self.column[2],self.column[3],  self.column[4],self.column[5],self.column[6],self.column[7],  self.column[8],self.column[9],self.column[10],self.column[11],  self.column[12],self.column[13],self.column[14],self.column[15],  self.column[16],self.column[17], self.current_piece])
			elif self.poliminos.field_size_x==20:
				action = np.argmax(self.q_values[self.column[0],self.column[1],self.column[2],self.column[3],  self.column[4],self.column[5],self.column[6],self.column[7],  self.column[8],self.column[9],self.column[10],self.column[11],  self.column[12],self.column[13],self.column[14],self.column[15],  self.column[16],self.column[17],self.column[18],self.column[19], self.current_piece])
			#action = np.argmax(self.q_values[self.height_mean, self.current_piece])
		else: #choose a random action
			action = np.random.randint(3)
		
		#print("got_action")
		self.get_pos(action)
		self.all_actions[action]+=1 
		return action

	def get_pos(self, action):
		lista=self.g.update()
		#	pos, num_lines, awarded_lines,   score, attack,			holes, 		soma das alturas, alturas
		#	0,			1,				2, 		3, 		4,				5,						6,		7
		#	positon = [	piece.pos[0], piece.pos[1], piece.facing, self.hold	]

		#print(lista)
		nplist=np.array(lista, dtype=list)
		#print(nplist)
		if action==0:#Minimizar  buracos
			#print("holes")#holes
			#print(nplist[:,5])#holes list
			#print(nplist[:,5].argmin())#Minimizar  buracos
			self.position=lista[nplist[:,5].argmin()][0]
		elif action==1:#Minimizar altura
			#print("heigths")#altura
			#print(nplist[:,6])#altura list
			#print(nplist[:,6].argmin())#Minimizar  altura
			self.position=lista[nplist[:,6].argmin()][0]
		else:#Maximizar linhas
			#print("full lines")#altura
			#print(nplist[:,1])#altura list
			#print(nplist[:,1].argmax())#Maximizar linhas completadas
			#print("awarded lines")#altura
			#print(nplist[:,2])#altura list
			#print(nplist[:,2].argmax())#Maximizar linhas recompensadas
			self.position=lista[nplist[:,2].argmax()][0]
		#print("got_pos:")
		#print(self.position)
		self.poliminos.wait_time=0.000000001


	def execute_action(self):#	True e se for concluida
		if self.poliminos.wait_time==0:#se a peça for posicionada
			self.actions["Left"]=False
			self.actions["Right"]=False
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
			self.get_pos(self.current_action)
		elif self.poliminos.piece.pos[0]==self.position[0] and self.poliminos.piece.facing==self.position[2]:
			self.actions["Hard_Drop"]=True
			self.actions["Left"]=False
			self.actions["Right"]=False
		elif self.poliminos.piece.pos[0]>self.position[0]:
			self.actions["Right"]=False
			if self.actions["Left"]:
				self.actions["Left"]=False
			else:
				self.actions["Left"]=True
		elif self.poliminos.piece.pos[0]<self.position[0]:
			self.actions["Left"]=False
			if self.actions["Right"]:
				self.actions["Right"]=False
			else:
				self.actions["Right"]=True
		
		#print("now:"+str([self.poliminos.piece.pos,self.poliminos.piece.facing]))
		return False
	
	def update_q_value(self):
		#h =[self.heights[0], self.heights[1], self.heights[2], self.heights[3], self.heights[4], self.heights[5], self.heights[6], self.heights[7], self.heights[8], self.heights[9]]
		old_column=self.column[:]
		#old_h_mean=self.height_mean
		old_piece = self.current_piece
		self.current_piece = self.piece_list.index(self.poliminos.piece.shape)
		reward = self.get_reward()
		
		#Valor Q atual
		if self.poliminos.field_size_x==8:
			old_q_value = self.q_values[old_column[0],old_column[1],old_column[2],old_column[3],  old_column[4],old_column[5],old_column[6],old_column[7], old_piece, self.old_action]
		elif self.poliminos.field_size_x==10:
			old_q_value = self.q_values[old_column[0],old_column[1],old_column[2],old_column[3],  old_column[4],old_column[5],old_column[6],old_column[7],  old_column[8],old_column[9], old_piece, self.old_action]
		elif self.poliminos.field_size_x==12:
			old_q_value = self.q_values[old_column[0],old_column[1],old_column[2],old_column[3],  old_column[4],old_column[5],old_column[6],old_column[7],  old_column[8],old_column[9],old_column[10],old_column[11], old_piece, self.old_action]
		elif self.poliminos.field_size_x==14:
			old_q_value = self.q_values[old_column[0],old_column[1],old_column[2],old_column[3],  old_column[4],old_column[5],old_column[6],old_column[7],  old_column[8],old_column[9],old_column[10],old_column[11],  old_column[12],old_column[13], old_piece, self.old_action]
		elif self.poliminos.field_size_x==16:
			old_q_value = self.q_values[old_column[0],old_column[1],old_column[2],old_column[3],  old_column[4],old_column[5],old_column[6],old_column[7],  old_column[8],old_column[9],old_column[10],old_column[11],  old_column[12],old_column[13],old_column[14],old_column[15], old_piece, self.old_action]
		elif self.poliminos.field_size_x==18:
			old_q_value = self.q_values[old_column[0],old_column[1],old_column[2],old_column[3],  old_column[4],old_column[5],old_column[6],old_column[7],  old_column[8],old_column[9],old_column[10],old_column[11],  old_column[12],old_column[13],old_column[14],old_column[15],  old_column[16],old_column[17], old_piece, self.old_action]
		elif self.poliminos.field_size_x==20:
			old_q_value = self.q_values[old_column[0],old_column[1],old_column[2],old_column[3],  old_column[4],old_column[5],old_column[6],old_column[7],  old_column[8],old_column[9],old_column[10],old_column[11],  old_column[12],old_column[13],old_column[14],old_column[15],  old_column[16],old_column[17],old_column[18],old_column[19], old_piece, self.old_action]
		#old_q_value=self.q_values[old_h_mean, old_piece, self.old_action]
		
		#deferença temporal = reward + (discount_factor * maxima recompensa futura) - old_q_value
		if self.poliminos.field_size_x==8:
			temporal_difference = reward +(self.discount_factor * np.max(self.q_values[self.column[0],self.column[1],self.column[2],self.column[3],  self.column[4],self.column[5],self.column[6],self.column[7], self.current_piece])) - old_q_value
		elif self.poliminos.field_size_x==10:
			temporal_difference = reward +(self.discount_factor * np.max(self.q_values[self.column[0],self.column[1],self.column[2],self.column[3],  self.column[4],self.column[5],self.column[6],self.column[7],  self.column[8],self.column[9], self.current_piece])) - old_q_value
		elif self.poliminos.field_size_x==12:
			temporal_difference = reward +(self.discount_factor * np.max(self.q_values[self.column[0],self.column[1],self.column[2],self.column[3],  self.column[4],self.column[5],self.column[6],self.column[7],  self.column[8],self.column[9],self.column[10],self.column[11], self.current_piece])) - old_q_value
		elif self.poliminos.field_size_x==14:
			temporal_difference = reward +(self.discount_factor * np.max(self.q_values[self.column[0],self.column[1],self.column[2],self.column[3],  self.column[4],self.column[5],self.column[6],self.column[7],  self.column[8],self.column[9],self.column[10],self.column[11],  self.column[12],self.column[13], self.current_piece])) - old_q_value
		elif self.poliminos.field_size_x==16:
			temporal_difference = reward +(self.discount_factor * np.max(self.q_values[self.column[0],self.column[1],self.column[2],self.column[3],  self.column[4],self.column[5],self.column[6],self.column[7],  self.column[8],self.column[9],self.column[10],self.column[11],  self.column[12],self.column[13],self.column[14],self.column[15], self.current_piece])) - old_q_value
		elif self.poliminos.field_size_x==18:
			temporal_difference = reward +(self.discount_factor * np.max(self.q_values[self.column[0],self.column[1],self.column[2],self.column[3],  self.column[4],self.column[5],self.column[6],self.column[7],  self.column[8],self.column[9],self.column[10],self.column[11],  self.column[12],self.column[13],self.column[14],self.column[15],  self.column[16],self.column[17], self.current_piece])) - old_q_value
		elif self.poliminos.field_size_x==20:
			temporal_difference = reward +(self.discount_factor * np.max(self.q_values[self.column[0],self.column[1],self.column[2],self.column[3],  self.column[4],self.column[5],self.column[6],self.column[7],  self.column[8],self.column[9],self.column[10],self.column[11],  self.column[12],self.column[13],self.column[14],self.column[15],  self.column[16],self.column[17],self.column[18],self.column[19], self.current_piece])) - old_q_value
		#temporal_difference = reward +(self.discount_factor * np.max(self.q_values[self.height_mean, self.current_piece])) - old_q_value
		
		#Novo valor Q
		new_q_value = old_q_value + (self.learning_rate * temporal_difference)
		
		if self.poliminos.field_size_x==8:
			self.q_values[old_column[0],old_column[1],old_column[2],old_column[3],  old_column[4],old_column[5],old_column[6],old_column[7], old_piece, self.old_action] = new_q_value
		elif self.poliminos.field_size_x==10:
			self.q_values[old_column[0],old_column[1],old_column[2],old_column[3],  old_column[4],old_column[5],old_column[6],old_column[7],  old_column[8],old_column[9], old_piece, self.old_action] = new_q_value
		elif self.poliminos.field_size_x==12:
			self.q_values[old_column[0],old_column[1],old_column[2],old_column[3],  old_column[4],old_column[5],old_column[6],old_column[7],  old_column[8],old_column[9],old_column[10],old_column[11], old_piece, self.old_action] = new_q_value
		elif self.poliminos.field_size_x==14:
			self.q_values[old_column[0],old_column[1],old_column[2],old_column[3],  old_column[4],old_column[5],old_column[6],old_column[7],  old_column[8],old_column[9],old_column[10],old_column[11],  old_column[12],old_column[13], old_piece, self.old_action] = new_q_value
		elif self.poliminos.field_size_x==16:
			self.q_values[old_column[0],old_column[1],old_column[2],old_column[3],  old_column[4],old_column[5],old_column[6],old_column[7],  old_column[8],old_column[9],old_column[10],old_column[11],  old_column[12],old_column[13],old_column[14],old_column[15], old_piece, self.old_action] = new_q_value
		elif self.poliminos.field_size_x==18:
			self.q_values[old_column[0],old_column[1],old_column[2],old_column[3],  old_column[4],old_column[5],old_column[6],old_column[7],  old_column[8],old_column[9],old_column[10],old_column[11],  old_column[12],old_column[13],old_column[14],old_column[15],  old_column[16],old_column[17], old_piece, self.old_action] = new_q_value
		elif self.poliminos.field_size_x==20:
			self.q_values[old_column[0],old_column[1],old_column[2],old_column[3],  old_column[4],old_column[5],old_column[6],old_column[7],  old_column[8],old_column[9],old_column[10],old_column[11],  old_column[12],old_column[13],old_column[14],old_column[15],  old_column[16],old_column[17],old_column[18],old_column[19], old_piece, self.old_action] = new_q_value
		#self.q_values[old_h_mean, old_piece, self.old_action] = new_q_value
		
		#print(f"old {old_q_value}	new {new_q_value}")
	
	def get_reward(self):
		over_10, holes = self.update_parameters()
		reward=0
		if self.old_garbage>self.poliminos.garbage:
			reward = 100*(self.old_garbage-self.poliminos.garbage)
			self.old_garbage=0
		reward += 1000*self.poliminos.attack+(1000*self.poliminos.Back_to_Back)
		reward += 100*(self.poliminos.total_lines_cleared-self.total_lines_cleared) - 100*over_10 - 10*holes
		self.total_lines_cleared=self.poliminos.total_lines_cleared
		return reward
		
	
	def update_parameters(self):
		h=[]
		count=0
		over_10 =0
		holes=0
		for x in range(self.poliminos.field_size_x):
			for y in range(20):#conta a altura das linhas
				if self.poliminos.matrix[x][y]!=0:
					count = y
			h.append(count)#alturas
			for y in range(count):
				if self.poliminos.matrix[x][y]==0:
					holes+=1
			if count>10:
				over_10+=1
				self.column[x]=1
			else:
				self.column[x]=0
			count=0
		#self.heights=h
		#self.height_mean=int(sum(h)/self.poliminos.field_size_x)
		return over_10, holes
		
	