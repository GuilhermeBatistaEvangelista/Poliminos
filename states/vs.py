import pygame
from states.state import State
from poliminos import Poliminos
from states.menu_game import Menu_Game
from states.game_over import Game_Over
import numpy as np
#from deep_q import Deep_q
import imp

class Vs(State):
	def __init__(self, game, path, pieces, selected_size):
		#import
		path="q_"+str(path)+".py"
		self.name=path[:-3]+"_"+str(selected_size)+"_("
		for i in range(5):	
			if pieces[i]:
				if self.name[-1]=="(":
					self.name +=str(i+1)
				else:
					self.name +="_"+str(i+1)
		self.name +=")"
		self.path="algorithms/"+path
		print("path",self.name)
		module = imp.load_source("Q_learning", self.path)
		self.Algorithm=module.Q_learning
		
		State.__init__(self, game)
		self.field_size_x = selected_size
		self.pieces = pieces
		if selected_size<16:
			self.block_size=30-1*(selected_size-8)
		else:
			self.block_size=22-1*(selected_size-16)
		self.poliminos1 = Poliminos(self.game, self.block_size, self.field_size_x, self.pieces, self.game.canvas_w*0.25)
		self.poliminos2 = Poliminos(self.game, self.block_size, self.field_size_x, self.pieces, self.game.canvas_w*0.75)
		self.Q = self.Algorithm(self.poliminos2, self.pieces)
		self.Q.training=False
		self.q_values = np.load("algorithms/"+self.name+"_250.npz")['arr_0']
		self.Q.q_values = self.q_values
		self.score=[0,0]
		self.lines_score=[0,0]
		self.back_button = pygame.Rect((0,0), (40,40))
		self.back_button.center=(20,20)
	
	def update(self, deltatime, actions):
		if self.game.mouse and self.back_button.collidepoint(self.game.mouse_pos):#se clicar no botão de retorno
			actions["Scape"]=True
		if self.game.playGame==False:
			self.state_out()
			self.state_out()
			return
		if actions["Scape"]:# se scape fro pressionado vai para o menu de jogo
			new_state = Menu_Game(self.game)
			new_state.state_in()	#adiciona o estado ao topo da pilha
			self.game.reset_actions()
		t1=self.poliminos1.update(deltatime, actions)
		self.poliminos2.garbage+=self.poliminos1.attack	#envia o ataque do jogador para o agente
		
		self.Q.update()
		
		t2=self.poliminos2.update(deltatime, self.Q.actions)
		self.poliminos1.garbage+=self.poliminos2.attack	#envia o ataque do agente para o jogador
		
		
		if not t1:#Se o jogador perder
			new_state = Game_Over(self.game, False)
			new_state.state_in()	#adiciona o estado ao topo da pilha
			self.lines_score[0] += self.poliminos1.total_lines_cleared
			self.lines_score[1] += self.poliminos2.total_lines_cleared
			self.poliminos1 = Poliminos(self.game, self.block_size, self.field_size_x, self.pieces, self.game.canvas_w*0.25)
			self.poliminos2 = Poliminos(self.game, self.block_size, self.field_size_x, self.pieces, self.game.canvas_w*0.75)
			self.Q = self.Algorithm(self.poliminos2, self.pieces)
			self.Q.training=False
			self.Q.q_values = self.q_values
			self.score[1]+=1
		elif not t2:#Se o algoritimo perder
			new_state = Game_Over(self.game, True)
			new_state.state_in()	#adiciona o estado ao topo da pilha
			self.lines_score[0] += self.poliminos1.total_lines_cleared
			self.lines_score[1] += self.poliminos2.total_lines_cleared
			self.poliminos1 = Poliminos(self.game, self.block_size, self.field_size_x, self.pieces, self.game.canvas_w*0.25)
			self.poliminos2 = Poliminos(self.game, self.block_size, self.field_size_x, self.pieces, self.game.canvas_w*0.75)
			self.Q = self.Algorithm(self.poliminos2, self.pieces)
			self.Q.training=False
			self.Q.q_values = self.q_values
			self.score[0]+=1

	def draw(self, canvas):
		canvas.fill(pygame.Color("gray"))
		self.poliminos1.draw(canvas)
		self.poliminos2.draw(canvas)
		
		#desenhar score
		self.game.text(canvas,f"Games:{self.score[0]+self.score[1]}", 24, pygame.Color("black"), self.game.canvas_w*0.50, 20)
		self.game.text(canvas,f"Lines:{self.lines_score[0]}", 24, pygame.Color("black"), self.game.canvas_w*0.20, 20)
		self.game.text(canvas,f"Wins:{self.score[0]}", 24, pygame.Color("black"), self.game.canvas_w*0.30, 20)
		self.game.text(canvas,f"Lines:{self.lines_score[1]}", 24, pygame.Color("black"), self.game.canvas_w*0.70, 20)
		self.game.text(canvas,f"Wins:{self.score[1]}", 24, pygame.Color("black"), self.game.canvas_w*0.80, 20)
		
		#Botão de retorno
		pygame.draw.rect(canvas, pygame.Color("black"), self.back_button, 2, 2)
		self.game.text(canvas, "<", 40, pygame.Color("black"), 20, 20)
		
		