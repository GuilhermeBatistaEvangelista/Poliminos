import pygame
import numpy as np
import matplotlib.pyplot
import json
from states.state import State
from poliminos import Poliminos
from states.menu_game import Menu_Game
from states.game_over import Game_Over
#from algorithms.q import Q_learning
import imp
#from deep_q import Deep_q
#import time

class Train_Q(State):
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
		module = imp.load_source("Q_learning", self.path)
		self.Algorithm=module.Q_learning
		#
		State.__init__(self, game)
		if selected_size<16:
			self.block_size=30-1*(selected_size-8)
		else:
			self.block_size=22.5-0.7*(selected_size-16)
		self.field_size_x = selected_size
		self.pieces = pieces
		self.poliminos1 = Poliminos(self.game, self.block_size, self.field_size_x, self.pieces, self.game.canvas_w*0.25)
		self.poliminos2 = Poliminos(self.game, self.block_size, self.field_size_x, self.pieces, self.game.canvas_w*0.75)
		self.Q1 = self.Algorithm(self.poliminos1, self.pieces)
		self.Q2 = self.Algorithm(self.poliminos2, self.pieces)
		self.score=[0,0]
		self.lines_score=[0,0]
		self.epsilon=0.5
		self.epsilon_increase_rate=0.00200803213
		self.total_time=0
		self.game_time=0
		#metricas de analise de resultados
		self.result_score=[]
		self.result_lines=[]
		self.attack1=0
		self.attack2=0
		self.result_attack=[]
		self.result_time=[]
		self.actions_list=[]
	
	def update(self, deltatime, actions):
		if self.game.playGame==False:
			self.state_out()
			return
		if actions["Scape"]:# se scape for pressionado vai para o menu de jogo
			new_state = Menu_Game(self.game)
			new_state.state_in()	#adiciona o estado ao topo da pilha
			self.game.reset_actions()
		
		#self.reload_graphs()
		
		self.Q1.update()
		t1=self.poliminos1.update(deltatime, self.Q1.actions)
		self.poliminos2.garbage+=self.poliminos1.attack	#envia o ataque do jogador para a Ai
		self.attack1+=self.poliminos1.attack
		
		self.Q2.update()
		t2=self.poliminos2.update(deltatime, self.Q2.actions)
		self.poliminos1.garbage+=self.poliminos2.attack	#envia o ataque da AI para o jogador
		self.attack2+=self.poliminos2.attack
		
		self.game_time+=deltatime
		if self.game_time>3600:# se o jogo durar mais de 1 hora
			if self.attack1!=self.attack2:#seleciona o que possui maior linhas de atques enviadas
				if self.attack1>self.attack2:
					t2=False
				else:
					t1=False
			else:#ou o que possuir maior pontuaçao
				if self.poliminos1.score>self.poliminos2.score:
					t2=False
				else:
					t1=False
		if not t1:#Se o algoritimo1 perder
			self.result_score.append(self.poliminos2.score)
			self.result_lines.append(self.poliminos2.total_lines_cleared)
			self.result_attack.append(self.attack2)
			self.score[1]+=1
			self.actions_list.append(np.array(self.Q2.all_actions)/sum(self.Q2.all_actions))
			self.restart(self.Q2.q_values)
			
		elif not t2:#Se o algoritimo2 perder
			self.result_score.append(self.poliminos1.score)
			self.result_lines.append(self.poliminos1.total_lines_cleared)
			self.result_attack.append(self.attack1)
			self.score[0]+=1
			self.actions_list.append(np.array(self.Q1.all_actions)/sum(self.Q1.all_actions))
			self.restart(self.Q1.q_values)

	def draw(self, canvas):
		canvas.fill(pygame.Color("gray"))
		self.poliminos1.draw(canvas)
		self.poliminos2.draw(canvas)
		
		#desenhar score
		self.game.text(canvas,f"Games:{self.score[0]+self.score[1]}", 24, pygame.Color("black"), self.game.canvas_w*0.45, 20)
		self.game.text(canvas,f"\u03B5:{round(self.epsilon,3)}", 24, pygame.Color("black"), self.game.canvas_w*0.55, 20)
		self.game.text(canvas,f"Total time: {round(self.total_time)}s", 24, pygame.Color("black"), self.game.canvas_w*0.40, self.game.canvas_h-20)
		self.game.text(canvas,f"Game time: {round(self.game_time)}s", 24, pygame.Color("black"), self.game.canvas_w*0.60, self.game.canvas_h-20)
		self.game.text(canvas,f"Lines:{self.lines_score[0]}", 24, pygame.Color("black"), self.game.canvas_w*0.20, 20)
		self.game.text(canvas,f"Wins:{self.score[0]}", 24, pygame.Color("black"), self.game.canvas_w*0.30, 20)
		self.game.text(canvas,f"Lines:{self.lines_score[1]}", 24, pygame.Color("black"), self.game.canvas_w*0.70, 20)
		self.game.text(canvas,f"Wins:{self.score[1]}", 24, pygame.Color("black"), self.game.canvas_w*0.80, 20)
		
	def restart(self,q_values):
		#save scores
		self.result_time.append(self.game_time)
		self.total_time+=self.game_time
		self.game_time=0
		self.attack1=0
		self.attack2=0
		self.lines_score[0] += self.poliminos1.total_lines_cleared
		self.lines_score[1] += self.poliminos2.total_lines_cleared
		
		#termina após 250 jogosde treino		ou após 1 jogo durar maid de 1 hora
		if ((self.score[0]+self.score[1])==250) or (self.game_time>3600):
			self.game.playGame=False
			self.fechar(q_values)
			return

		#restart
		self.poliminos1 = Poliminos(self.game, self.block_size, self.field_size_x, self.pieces, self.game.canvas_w*0.25)
		self.poliminos2 = Poliminos(self.game, self.block_size, self.field_size_x, self.pieces, self.game.canvas_w*0.75)
		self.Q1 = self.Algorithm(self.poliminos1, self.pieces)
		self.Q2 = self.Algorithm(self.poliminos2, self.pieces)
		self.Q1.q_values,self.Q2.q_values = q_values,q_values
		
		#increase epsilon
		self.epsilon +=self.epsilon_increase_rate
		self.Q1.epsilon, self.Q2.epsilon = self.epsilon, self.epsilon
	
	def fechar(self, q_values):#	Chamada ao se encerrar o treinamento
		if ((self.score[0]+self.score[1])>100):
			
			matplotlib.pyplot.figure(figsize=(12,9))
			matplotlib.pyplot.rcParams.update({'font.size': 26})
			#		grafico de pontuação
			data=np.array(self.result_score)
			matplotlib.pyplot.plot(data)
			matplotlib.pyplot.xlabel("Jogos")
			matplotlib.pyplot.ylabel("Pontuação")
			#matplotlib.pyplot.show()
			matplotlib.pyplot.savefig("results/"+self.name+"_"+str(self.score[0]+self.score[1])+"_score__𝛾"+str(self.Q1.discount_factor)+"_α"+str(self.Q1.learning_rate)+".png", format="png")
			np.save("results/"+self.name+"_"+str(self.score[0]+self.score[1])+"_score", data)
			matplotlib.pyplot.clf()
			#		grafico de linhas completas
			data=np.array(self.result_lines)
			matplotlib.pyplot.plot(data)
			matplotlib.pyplot.xlabel("Jogos")
			matplotlib.pyplot.ylabel("linhas")
			#matplotlib.pyplot.show()
			matplotlib.pyplot.savefig("results/"+self.name+"_"+str(self.score[0]+self.score[1])+"_lines__𝛾"+str(self.Q1.discount_factor)+"_α"+str(self.Q1.learning_rate)+".png", format="png")
			np.save("results/"+self.name+"_"+str(self.score[0]+self.score[1])+"_lines", data)
			matplotlib.pyplot.clf()
			#		grafico de linhas de ataque enviada
			data=np.array(self.result_attack)
			matplotlib.pyplot.plot(data)
			matplotlib.pyplot.xlabel("Jogos")
			matplotlib.pyplot.ylabel("linhas de ataque")
			#matplotlib.pyplot.show()
			matplotlib.pyplot.savefig("results/"+self.name+"_"+str(self.score[0]+self.score[1])+"_attack__𝛾"+str(self.Q1.discount_factor)+"_α"+str(self.Q1.learning_rate)+".png", format="png")
			np.save("results/"+self.name+"_"+str(self.score[0]+self.score[1])+"_attack", data)
			matplotlib.pyplot.clf()
			#		grafico de tempo de jogo
			data=np.array(self.result_time)
			matplotlib.pyplot.plot(data)
			matplotlib.pyplot.xlabel("Jogos")
			matplotlib.pyplot.ylabel("Tempo(s)")
			#matplotlib.pyplot.show()
			matplotlib.pyplot.savefig("results/"+self.name+"_"+str(self.score[0]+self.score[1])+"_time__𝛾"+str(self.Q1.discount_factor)+"_α"+str(self.Q1.learning_rate)+".png", format="png")
			np.save("results/"+self.name+"_"+str(self.score[0]+self.score[1])+"_time", data)
			matplotlib.pyplot.clf()
			#		grafico de ações tomadas
			self.actions_list=np.array(self.actions_list)
			cycle = matplotlib.pyplot.rcParams['axes.prop_cycle'].by_key()['color']
			if(len(self.actions_list[0])==3):#labels
				matplotlib.pyplot.plot([], [], color = cycle[0], label ='Minimizar Buracos')
				matplotlib.pyplot.plot([], [], color = cycle[1], label ='Minimizar Altura')
				matplotlib.pyplot.plot([], [], color = cycle[2], label ='Maximizar Linhas')
			matplotlib.pyplot.legend(loc="lower left")
			x=np.arange(0,len(self.actions_list))
			y= np.vstack((self.actions_list[:, 0], self.actions_list[:, 1]))
			for n in range(2,len(self.actions_list[0])):
				y = np.vstack((y, self.actions_list[:, n]))
			matplotlib.pyplot.stackplot(x,y,  baseline ='zero')
			matplotlib.pyplot.xlabel("Jogos")
			matplotlib.pyplot.ylabel("Ações")
			matplotlib.pyplot.xticks([])
			#matplotlib.pyplot.show()
			matplotlib.pyplot.savefig("results/"+self.name+"_"+str(self.score[0]+self.score[1])+"_actions__𝛾"+str(self.Q1.discount_factor)+"_α"+str(self.Q1.learning_rate)+".png", format="png")
			np.save("results/"+self.name+"_"+str(self.score[0]+self.score[1])+"_action", self.actions_list)
			matplotlib.pyplot.clf()
			
			np.savez("algorithms/"+self.name+"_"+str(self.score[0]+self.score[1]), q_values)
			
			
	def reload_graphs(self):
		self.game.playGame=False
		
		matplotlib.pyplot.figure(figsize=(12,9))
		matplotlib.pyplot.rcParams.update({'font.size': 26})

		#		grafico de pontuação
		data=np.load("results/"+self.name+"_250_score.npy")
		matplotlib.pyplot.plot(data)
		matplotlib.pyplot.xlabel("Jogos")
		matplotlib.pyplot.ylabel("Pontuação")
		#matplotlib.pyplot.show()
		matplotlib.pyplot.savefig("results/"+self.name+"_250_score__𝛾"+str(self.Q1.discount_factor)+"_α"+str(self.Q1.learning_rate)+".png", format="png")
		matplotlib.pyplot.clf()
		#		grafico de linhas completas
		data=np.load("results/"+self.name+"_250_lines.npy")
		matplotlib.pyplot.plot(data)
		matplotlib.pyplot.xlabel("Jogos")
		matplotlib.pyplot.ylabel("linhas")
		#matplotlib.pyplot.show()
		matplotlib.pyplot.savefig("results/"+self.name+"_250_lines__𝛾"+str(self.Q1.discount_factor)+"_α"+str(self.Q1.learning_rate)+".png", format="png")
		matplotlib.pyplot.clf()
		#		grafico de linhas de ataque enviada
		data=np.load("results/"+self.name+"_250_attack.npy")
		matplotlib.pyplot.plot(data)
		matplotlib.pyplot.xlabel("Jogos")
		matplotlib.pyplot.ylabel("linhas de ataque")
		#matplotlib.pyplot.show()
		matplotlib.pyplot.savefig("results/"+self.name+"_250_attack__𝛾"+str(self.Q1.discount_factor)+"_α"+str(self.Q1.learning_rate)+".png", format="png")
		matplotlib.pyplot.clf()
		#		grafico de tempo de jogo
		data=np.load("results/"+self.name+"_250_time.npy")
		matplotlib.pyplot.plot(data)
		matplotlib.pyplot.xlabel("Jogos")
		matplotlib.pyplot.ylabel("Tempo(s)")
		#matplotlib.pyplot.show()
		matplotlib.pyplot.savefig("results/"+self.name+"_250_time__𝛾"+str(self.Q1.discount_factor)+"_α"+str(self.Q1.learning_rate)+".png", format="png")
		matplotlib.pyplot.clf()