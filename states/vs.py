import pygame
from states.state import State
from poliminos import Poliminos
from states.menu_game import Menu_Game
from states.game_over import Game_Over
import numpy as np
from algorithms.q_1 import Q_learning
#from deep_q import Deep_q

class Vs(State):
	def __init__(self, game, path, pieces, selected_size):
		State.__init__(self, game)
		self.field_size_x = selected_size
		self.pieces = pieces
		self.poliminos1 = Poliminos(self.game, self.field_size_x, self.pieces, self.game.canvas_w*0.25)
		self.poliminos2 = Poliminos(self.game, self.field_size_x, self.pieces, self.game.canvas_w*0.75)
		self.Q = Q_learning(self.poliminos2, self.pieces)
		self.Q.training=False
		self.q_values = np.load("algorithms/q_4_1000.npz")['arr_0']
		self.Q.q_values = self.q_values
		self.score=[0,0]
		self.lines_score=[0,0]
	
	def update(self, deltatime, actions):
		if self.game.playGame==False:
			self.state_out()
			self.state_out()
			return
		if actions["Scape"]:# se scape fro pressionado vai para o menu de jogo
			new_state = Menu_Game(self.game)
			new_state.state_in()	#adiciona o estado ao topo da pilha
			self.game.reset_actions()
		t1=self.poliminos1.update(deltatime, actions)
		self.poliminos2.garbage+=self.poliminos1.attack	#envia o ataque do jogador para a Ai
		
		self.Q.update()
		
		t2=self.poliminos2.update(deltatime, self.Q.actions)
		self.poliminos1.garbage+=self.poliminos2.attack	#envia o ataque da AI para o jogador
		
		
		if not t1:#Se o jogador perder
			new_state = Game_Over(self.game, False)
			new_state.state_in()	#adiciona o estado ao topo da pilha
			self.lines_score[0] += self.poliminos1.total_lines_cleared
			self.lines_score[1] += self.poliminos2.total_lines_cleared
			self.poliminos1 = Poliminos(self.game, self.field_size_x, self.pieces, self.game.canvas_w*0.25)
			self.poliminos2 = Poliminos(self.game, self.field_size_x, self.pieces, self.game.canvas_w*0.75)
			self.Q = Q_learning(self.poliminos2, self.pieces)
			self.Q.training=False
			self.Q.q_values = self.q_values
			self.score[1]+=1
		elif not t2:#Se o algoritimo perder
			new_state = Game_Over(self.game, True)
			new_state.state_in()	#adiciona o estado ao topo da pilha
			self.lines_score[0] += self.poliminos1.total_lines_cleared
			self.lines_score[1] += self.poliminos2.total_lines_cleared
			self.poliminos1 = Poliminos(self.game, self.field_size_x, self.pieces, self.game.canvas_w*0.25)
			self.poliminos2 = Poliminos(self.game, self.field_size_x, self.pieces, self.game.canvas_w*0.75)
			self.Q = Q_learning(self.poliminos2, self.pieces)
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
		
		