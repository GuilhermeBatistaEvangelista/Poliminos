import os, json, pygame

def load_existing_save(savefile):
	with open(os.path.join(savefile), 'r+') as file:
		controls = json.load(file)
	return controls

def write_save(data):
	with open(os.path.join(os.getcwd(),'save.json'), 'w') as file:
		json.dump(data, file)

def load_save():
	try:# Se um save ja foi carregado 
		save = load_existing_save('save.json')
	except:# cria um savefile 
		save = create_save()
		write_save(save)
	return save


def create_save():
	new_save = {
	"resolution":{"W": 1366, "H": 768},
	"controls":{"Left": pygame.K_a, "Right": pygame.K_d, "Up": pygame.K_w, "Down": pygame.K_s, "Confirm": pygame.K_SPACE,
		"Soft_Drop": pygame.K_s, "Hard_Drop": pygame.K_SPACE, "Rotate_Right": pygame.K_w, "Rotate_Left": pygame.K_z,
		"Hold": pygame.K_c},
	"colors":{
		"1":list(pygame.Color("lightyellow3")),
		
		"2":list(pygame.Color("green3")),
		
		"3_I":list(pygame.Color("cadetblue2")), "3_L":list(pygame.Color("lightsalmon")),
		
		"4_I": list(pygame.Color("aqua")), "4_J": list(pygame.Color("blue3")), "4_L": list(pygame.Color("coral")),
			"4_O": list(pygame.Color("gold1")), "4_S": list(pygame.Color("limegreen")), "4_Z": list(pygame.Color("red2")), "4_T": list(pygame.Color("orchid3")),
		
		"5_1":list(pygame.Color("rosybrown1")), "5_2":list(pygame.Color("tan")), "5_3":list(pygame.Color("tan")), "5_4":list(pygame.Color("khaki2")), "5_5":list(pygame.Color("khaki2")),
		"5_6":list(pygame.Color("darkolivegreen3")), "5_7":list(pygame.Color("darkolivegreen3")), "5_8":list(pygame.Color("darkseagreen2")), "5_9":list(pygame.Color("darkseagreen2")),
		"5_10":list(pygame.Color("mediumaquamarine")), "5_11":list(pygame.Color("skyblue")), "5_12":list(pygame.Color("skyblue2")), "5_13":list(pygame.Color("mediumpurple")),
		"5_14":list(pygame.Color("mediumpurple1")), "5_15":list(pygame.Color("mediumorchid")), "5_16":list(pygame.Color("mediumorchid")), "5_17":list(pygame.Color("pink2")), "5_18":list(pygame.Color("pink2"))
		},
	"language":"EN"}

	return new_save

def reset_keys(actions):
	for action in actions:
		actions[action] = False
	return actions