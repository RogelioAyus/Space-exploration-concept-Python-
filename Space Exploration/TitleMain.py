from scene import *
import sound
import random
import math
import game_version
A = Action

class TitleMain (Scene):
	def setup(self):
		#var
		self.background_color = '#000000'
		self.started = False
		#setup sprite
		self.main_node = Node(parent=self)
		self.fader_fg = ShapeNode(color='#000000',parent=self.main_node,z_position=5,size=self.size,position=self.size/2)
		self.fader_fg.run_action(A.fade_to(0,4))
		self.titlebg = SpriteNode('SolarBg_4.png',parent=self.main_node,position=self.size/2)
		self.titlebg.run_action(A.repeat_forever(A.rotate_by(1,20)))
		self.title = SpriteNode('IMG_3066.png',parent=self.main_node,position=self.size/2,size=(1333,744))
		self.label1 = LabelNode('Press anywhere to continue',parent=self.main_node,position=(self.size.x/2,self.size.y/2-(self.size.y/3)),alpha = 0)
		self.label2 = LabelNode('Play',parent=self.main_node,position=(self.size.x/2,self.size.y/2-10),font=('<System>',30),alpha = 0)
		self.label3 = LabelNode('Load',parent=self.main_node,position=(self.size.x/2,self.size.y/2-80),font=('<System>',30),alpha = 0)
		self.label4 = LabelNode('Exit',parent=self.main_node,position=(self.size.x/2,self.size.y/2-150),font=('<System>',30),alpha = 0)
		self.gamev = LabelNode(game_version.g,parent=self.main_node,position=(self.size.x/2,100),font=('<System>',10))
		self.labelgd = LabelNode('game by RogelioAyus',parent=self.main_node,position=(self.size.x/2+160,self.size.y/2+140),font=('<System>',12),alpha = 1,z_position=4)
	
	def did_change_size(self):
		self.main_node.position = (0,0)
		self.title.position = self.size/2
		self.labelgd.position = (self.size.x/2+160,self.size.y/2+140)
		self.fader_fg.position = self.size/2
		self.gamev.position = (self.size.x/2,100)
		self.label1.position=(self.size.x/2,self.size.y/2-(self.size.y/3))
		self.label2.position = (self.size.x/2,self.size.y/2-10)
		self.label3.position = (self.size.x/2,self.size.y/2-80)
		self.label4.position = (self.size.x/2,self.size.y/2-150)
	
	def update(self):
		if self.t >= 3 and self.started == False:
			self.label1.alpha = ((max(min(self.t,5),3))-3)/2
		elif self.started == True:
			self.label1.run_action(A.fade_to(0,0.2))
			self.label2.run_action(A.sequence(A.wait(0.5),A.fade_to(1,0.2)))
			self.label3.run_action(A.sequence(A.wait(0.5),A.fade_to(1,0.2)))
			self.label4.run_action(A.sequence(A.wait(0.5),A.fade_to(1,0.2)))
			
	
	def touch_began(self, touch):
		tl = touch.location
		if self.t >= 3 and self.started == False:
			self.started = True
		if tl in self.label2.frame:
			self.presenting_scene.player_new_game()
		elif tl in self.label3.frame:
			#print('Load game here')
			pass
		elif tl in self.label4.frame:
			pass
	def touch_moved(self, touch):
		pass
	
	def touch_ended(self, touch):
		pass

if __name__ == '__main__':
	run(TitleMain(), show_fps=True, anti_alias=True)
