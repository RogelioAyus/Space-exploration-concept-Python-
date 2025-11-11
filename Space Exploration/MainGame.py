from scene import *
import sound
import random
import math
from Interactables import ListCompress, Sliders, Togglebutton
from SolarTravelScene import SolarTravelScene
from TitleMain import TitleMain
from planets import PlanetList
A = Action

class MyScene (Scene):
	def setup(self):
		self.background_color = '#000000'
		self.bg_music = sound.Player('bg_music.m4a')
		self.bg_music.number_of_loops = -1
		self.bg_music.volume = 0
		self.bg_music.play()
		self.main_node = Node(parent=self)
		self.background = SpriteNode('IMG_3065.png',position=self.size/2,parent=self.main_node,alpha=0.5)
		self.background.run_action(A.repeat_forever(A.rotate_by(1,20)))
		self.present_modal_scene(TitleMain())
		#self.labelloading = LabelNode('Loading galaxy... no galy tho',parent=self,position=self.size/2,alpha=0)
	
	def did_change_size(self):
		pass
	
	def update(self):
		if self.t <= 3:
			self.bg_music.volume = max(min(self.t/3,1),0)
	
	def touch_began(self, touch):
		pass
	
	def touch_moved(self, touch):
		pass
	def touch_ended(self, touch):
		pass
		
		
	#---------------------------------------Custom Definitors	
	def solar_to_planetary(self):
		self.dismiss_modal_scene()
		self.present_modal_scene()
	def solardisplay(self):
		self.dismiss_modal_scene()
		self.present_modal_scene(SolarTravelScene())
	def player_new_game(self):
		self.dismiss_modal_scene()
		#self.labelloading.alpha = 1
	def stop(self):
		self.bg_music.stop()


if __name__ == '__main__':
	run(MyScene(), show_fps=False)
