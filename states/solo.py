import pygame
from states.state import State
from poliminos import Poliminos
from states.menu_game import Menu_Game
from states.game_over import Game_Over

class Solo(State):
	def __init__(self, game, path, pieces, selected_size):
		State.__init__(self, game)
		self.block_size=30
		self.field_size_x = selected_size
		self.pieces = pieces
		self.poliminos = Poliminos(self.game, self.block_size, self.field_size_x, self.pieces, self.game.canvas_w/2)
	
	def update(self, deltatime, actions):
		if self.game.playGame==False:
			self.state_out()
			self.state_out()
			return
		if actions["Scape"]:# se scape fro pressionado vai para o menu de jogo
			new_state = Menu_Game(self.game)
			new_state.state_in()	#adiciona o estado ao topo da pilha
			self.game.reset_actions()
		if not self.poliminos.update(deltatime, actions):
			new_state = Game_Over(self.game, False)
			new_state.state_in()	#adiciona o estado ao topo da pilha
			self.poliminos = Poliminos(self.game, self.block_size, self.field_size_x, self.pieces, self.game.canvas_w/2)

	def draw(self, canvas):
		canvas.fill(pygame.Color("antiquewhite3"))
		self.poliminos.draw(canvas)