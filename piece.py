import pygame

DIRECTION=["North", "East", "South", "West"]
PIECES={
	'1':{"North":[(0,0)],
		"East":[(0,0)],
		"South":[(0,0)],
		"West":[(0,0)]},
	
	'2':{"North":[(0,0), (1,0)],
		"East":[(1,0), (1,-1)],
		"South":[(0,-1), (1,-1)],
		"West":[(0,0), (0,-1)]},
	
	'3_I':{"North":[(0,0), (1,0), (2,0)],
		"East":[(2,0), (2,-1), (2,-2)],
		"South":[(0,-2), (1,-2), (2,-2)],
		"West":[(0,0), (0,-1), (0,-2)]},
	'3_L':{"North":[(0,0), (0,-1), (1,-1)],
		"East":[(0,0), (1,0), (0,-1)],
		"South":[(0,0), (1,0), (1,-1)],
		"West":[(1,0), (0,-1), (1,-1)]},
	
	'4_O':{"North":[(1,0), (2,0), (1,-1), (2,-1)],
		"East":[(1,0), (2,0), (1,-1), (2,-1)],
		"South":[(1,0), (2,0), (1,-1), (2,-1)],
		"West":[(1,0), (2,0), (1,-1), (2,-1)]},
	'4_T':{"North":[(1,0), (0,-1), (1,-1), (2,-1)],
		"East":[(1,0), (1,-1), (2,-1), (1,-2)],
		"South":[(1,-2), (0,-1), (1,-1), (2,-1)],
		"West":[(0,-1), (1,0), (1,-1), (1,-2)]},
	'4_J':{"North":[(0,0), (0,-1), (1,-1), (2,-1)],
		"East":[(1,0), (2,0), (1,-1), (1,-2)],
		"South":[(0,-1), (1,-1), (2,-1), (2,-2)],
		"West":[(0,-2), (1,0), (1,-1), (1,-2)]},
	'4_L':{"North":[(2,0), (0,-1), (1,-1), (2,-1)],
		"East":[(1,0), (1,-1), (1,-2), (2,-2)],
		"South":[(0,-1), (1,-1), (2,-1), (0,-2)],
		"West":[(0,0), (1,0), (1,-1), (1,-2)]},
	'4_I':{"North":[(0,-1), (1,-1), (2,-1), (3,-1)],
		"East":[(2,0), (2,-1), (2,-2), (2,-3)],
		"South":[(0,-2), (1,-2), (2,-2), (3,-2)],
		"West":[(1,0), (1,-1), (1,-2), (1,-3)]},
	'4_S':{"North":[(0,-1), (1,-1), (1,0), (2,0)],
		"East":[(1,0), (1,-1), (2,-1), (2,-2)],
		"South":[(0,-2), (1,-1), (1,-2), (2,-1)],
		"West":[(0,0), (0,-1), (1,-1), (1,-2)]},
	'4_Z':{"North":[(0,0), (1,0), (1,-1), (2,-1)],
		"East":[(2,0), (1,-1), (2,-1), (1,-2)],
		"South":[(0,-1), (1,-1), (1,-2), (2,-2)],
		"West":[(1,0), (0,-1), (1,-1), (0,-2)]},
	
	'5_1':{"North":[(0,-1), (1,-1), (2,-1), (3,-1), (4,-1)],
		"East":[(3,0), (3,-1), (3,-2), (3,-3), (3,-4)],
		"South":[(0,-3), (1,-3), (2,-3), (3,-3), (4,-3)],
		"West":[(1,0), (1,-1), (1,-2), (1,-3), (1,-4)]},
	'5_2':{"North":[(1,0), (0,-1), (1,-1), (2,-1), (2,-2)],
		"East":[(1,0), (1,-1), (2,-1), (0,-2), (1,-2)],
		"South":[(0,0), (0,-1), (1,-1), (2,-1), (1,-2)],
		"West":[(1,0), (2,0), (0,-1), (1,-1), (1,-2)]},
	'5_3':{"North":[(1,0), (0,-1), (1,-1), (2,-1), (0,-2)],
		"East":[(0,0), (1,0), (1,-1), (2,-1), (1,-2)],
		"South":[(2,0), (0,-1), (1,-1), (2,-1), (1,-2)],
		"West":[(1,0), (0,-1), (1,-1), (1,-2), (2,-2)]},
	'5_4':{"North":[(0,0), (0,-1), (1,-1), (2,-1), (3,-1)],
		"East":[(2,0), (3,0), (2,-1), (2,-2), (2,-3)],
		"South":[(0,-2), (1,-2), (2,-2), (3,-2), (3,-3)],
		"West":[(1,0), (1,-1), (1,-2), (1,-3), (0,-3)]},
	'5_5':{"North":[(3,0), (0,-1), (1,-1), (2,-1), (3,-1)],
		"East":[(2,0), (2,-1), (2,-2), (2,-3), (3,-3)],
		"South":[(0,-2), (1,-2), (2,-2), (3,-2), (0,-3)],
		"West":[(0,0), (1,0), (1,-1), (1,-2), (1,-3)]},
	'5_6':{"North":[(1,0), (2,0), (0,-1), (1,-1), (2,-1)],
		"East":[(1,0), (1,-1), (2,-1), (1,-2), (2,-2)],
		"South":[(0,-1), (1,-1), (2,-1), (0,-2), (1,-2)],
		"West":[(0,0), (1,0), (0,-1), (1,-1), (1,-2)]},
	'5_7':{"North":[(0,0), (1,0), (0,-1), (1,-1), (2,-1)],
		"East":[(0,0), (1,0), (0,-1), (1,-1), (0,-2)],
		"South":[(0,-1), (1,-1), (2,-1), (1,-2), (2,-2)],
		"West":[(2,0), (1,-1), (2,-1), (1,-2), (2,-2)]},
	'5_8':{"North":[(0,0), (1,0), (1,-1), (2,-1), (3,-1)],
		"East":[(3,0), (2,-1), (3,-1), (2,-2), (2,-3)],
		"South":[(0,-2), (1,-2), (2,-2), (2,-3), (3,-3)],
		"West":[(1,0), (1,-1), (0,-2), (1,-2), (0,-3)]},
	'5_9':{"North":[(2,0), (3,0), (0,-1), (1,-1), (2,-1)],
		"East":[(2,0), (2,-1), (2,-2), (3,-2), (3,-3)],
		"South":[(1,-2), (2,-2), (3,-2), (0,-3), (1,-3)],
		"West":[(0,0), (0,-1), (1,-1), (1,-2), (1,-3)]},
	'5_10':{"North":[(1,0), (1,-1), (0,-2), (1,-2), (2,-2)],
		"East":[(0,0), (0,-1), (1,-1), (2,-1), (0,-2)],
		"South":[(0,0), (1,0), (2,0), (1,-1), (1,-2)],
		"West":[(2,0), (0,-1), (1,-1), (2,-1), (2,-2)]},
	'5_11':{"North":[(0,0), (1,0), (2,0), (0,-1), (2,-1)],
		"East":[(1,0), (2,0), (2,-1), (1,-2), (2,-2)],
		"South":[(0,-1), (2,-1), (0,-2), (1,-2), (2,-2)],
		"West":[(0,0), (1,0), (0,-1), (0,-2), (1,-2)]},
	'5_12':{"North":[(0,0), (0,-1), (0,-2), (1,-2), (2,-2)],
		"East":[(0,0), (1,0), (2,0), (0,-1), (0,-2)],
		"South":[(0,0), (1,0), (2,0), (2,-1), (2,-2)],
		"West":[(2,0), (2,-1), (0,-2), (1,-2), (2,-2)]},
	'5_13':{"North":[(1,0), (2,0), (0,-1), (1,-1), (0,-2)],
		"East":[(0,0), (1,0), (1,-1), (2,-1), (2,-2)],
		"South":[(2,0), (1,-1), (2,-1), (0,-2), (1,-2)],
		"West":[(0,0), (0,-1), (1,-1), (1,-2), (2,-2)]},
	'5_14':{"North":[(1,0), (0,-1), (1,-1), (2,-1), (1,-2)],
		"East":[(1,0), (0,-1), (1,-1), (2,-1), (1,-2)],
		"South":[(1,0), (0,-1), (1,-1), (2,-1), (1,-2)],
		"West":[(1,0), (0,-1), (1,-1), (2,-1), (1,-2)]},
	'5_15':{"North":[(2,0), (0,-1), (1,-1), (2,-1), (3,-1)],
		"East":[(2,0), (2,-1), (2,-2), (3,-2), (2,-3)],
		"South":[(0,-2), (1,-2), (2,-2), (3,-2), (1,-3)],
		"West":[(1,0), (0,-1), (1,-1), (1,-2), (1,-3)]},
	'5_16':{"North":[(1,0), (0,-1), (1,-1), (2,-1), (3,-1)],
		"East":[(2,0), (2,-1), (3,-1), (2,-2), (2,-3)],
		"South":[(0,-2), (1,-2), (2,-2), (3,-2), (2,-3)],
		"West":[(1,0), (1,-1), (0,-2), (1,-2), (1,-3)]},
	'5_17':{"North":[(0,0), (0,-1), (1,-1), (2,-1), (2,-2)],
		"East":[(1,0), (2,0), (1,-1), (0,-2), (1,-2)],
		"South":[(0,0), (0,-1), (1,-1), (2,-1), (2,-2)],
		"West":[(1,0), (2,0), (1,-1), (0,-2), (1,-2)]},
	'5_18':{"North":[(2,0), (0,-1), (1,-1), (2,-1), (0,-2)],
		"East":[(0,0), (1,0), (1,-1), (1,-2), (2,-2)],
		"South":[(2,0), (0,-1), (1,-1), (2,-1), (0,-2)],
		"West":[(0,0), (1,0), (1,-1), (1,-2), (2,-2)]}
	}


class Block:
	def __init__(self, piece, start_pos, pos, color):
		self.piece = piece
		self.pos=[int(start_pos[0]+pos[0]), int(start_pos[1]+pos[1])]		#posição do bloco
		self.color=color					#cor do bloco
		self.size = piece.poliminos.block_size
		self.grid_start_pos_x = piece.poliminos.grid_left
		self.grid_start_pos_y = piece.poliminos.grid_y

	def draw(self, canvas):
		if self.pos[1]<20:
			rect = pygame.Rect(self.grid_start_pos_x+self.pos[0]*self.size, self.grid_start_pos_y-(self.pos[1]*self.size), self.size, self.size)
			pygame.draw.rect(canvas, pygame.Color(self.color), rect, 0)
		
class Piece:
	def __init__(self, poliminos, shape, start_pos):
		self.poliminos = poliminos
		self.shape=shape
		self.facing=0
		self.pos=start_pos
		self.blocks=[Block(self, self.pos, pos, self.poliminos.game.save["colors"][self.shape]) for pos in PIECES[self.shape][DIRECTION[self.facing]]]
	
	def update(self, actions):
		pass
	
	def move(self, direction):
		for block in self.blocks:
			block.pos[0]+=direction[0]
			block.pos[1]+=direction[1]
		self.pos[0]+=direction[0]
		self.pos[1]+=direction[1]
		if not self.is_inside(self.blocks) or self.collision(self.blocks):
			for block in self.blocks:
				block.pos[0]-=direction[0]
				block.pos[1]-=direction[1]
			self.pos[0]-=direction[0]
			self.pos[1]-=direction[1]
			return False
		return True
	
	def rotation(self, rotate):
		facing = (self.facing+rotate)%4
		new_blocks=[Block(self, self.pos, pos, self.poliminos.game.save["colors"][self.shape]) for pos in PIECES[self.shape][DIRECTION[facing]]]
		if self.is_inside(new_blocks) and (not self.collision(new_blocks)):#Se esta dentro da matriz e não existe colisão
			self.blocks=new_blocks
			self.facing=facing
			return True
		return False
	
	def is_inside(self, blocks):#verifica se o tetromino esta dentro da matriz
		for block in blocks:
			if (block.pos[0]<=-1) or (block.pos[0]>=self.poliminos.field_size_x) or (block.pos[1]<=-1):
				return False
		return True
	
	def collision(self, blocks):#verifica se a posição esta vazia
		for block in blocks:
			if self.poliminos.matrix[block.pos[0]][block.pos[1]] !=0:
				return True
		return False
	
	def draw(self, canvas):
		for block in self.blocks:
			block.draw(canvas)
	