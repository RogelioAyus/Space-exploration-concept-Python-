import itertools
import threading
import time
import sys
from scene import *
import sound
from random import randint, choice, uniform
from Interactables import Togglebutton
import math
import ui
from console import input_alert, login_alert
A = Action
class Module (Node):
	def __init__(self, *args, **kwargs):
		Node.__init__(self, *args, **kwargs)

class ShipDesign (Scene):
	def __init__(self, ShipData = {
		'ShipSprite': {
			'Ship':'Ship_design/Ship/Ship_1.png',
			'Engine':'Ship_design/EngineType/Rogue_Engine_1.png',
			'Burn':'Ship_design/Burn/rogue_burn.png',
			'emit_color':'#ff6c6c'
		},
		'engine_position':(-450,0),
		'ShipType': 0,
		'ShipSize': (900,900),
		'ShipEngine': None,
		'ShipHousing': [
			{
				'id':0,
				'x': -150,
				'y': 0,
				'Module': None,
				'Build_in':None,
				'size': [1,'Ship_design/Slot/small_slot.png']
			},
			{
				'id':1,
				'x':150,
				'y':0,
				'Module':None,
				'Build_in': None,
				'size': [1,'Ship_design/Slot/small_slot.png']
			}
			],
		'':''
		}

	, *args, **kwargs):
		Scene.__init__(self, *args, **kwargs)
		self.ShipData = ShipData
		
	def setup(self):
		#important motdification Vars
		self.central = (1133/2,744/2)
		self.background_color = '#000000'
		self.Ship_module_list = []
		
		#Node
		self.mainblend_node = Node(parent=self)
		self.main_node = Node(parent=self,position=self.central)
		self.dot = SpriteNode('shp:Circle',parent=self.main_node,size=(2,2))
		
		#Desinging the Ship
		self.ship_main = SpriteNode(self.ShipData['ShipSprite']['Ship'],parent=self.main_node)
		self.Engine_burn = SpriteNode(self.ShipData['ShipSprite']['Burn'],parent=self.main_node,anchor_point=(0.5,1),x_scale=0.7)
		self.Engine_burn.rotation = (math.pi*1.5)
		self.Engine_main = SpriteNode(self.ShipData['ShipSprite']['Engine'],parent=self.main_node,position=self.ShipData['engine_position'])
		self.Engine_main.rotation = (math.pi*1.5)
		self.Engine_burn.position = (self.ShipData['engine_position'][0]-30,self.ShipData['engine_position'][1])
		self.Engine_emit = SpriteNode('shp:Gradient-2',parent=self.Engine_main,position=(0,-50),scale=3,blend_mode = BLEND_ADD,alpha=0.5,color=self.ShipData['ShipSprite']['emit_color'],anchor_point=(0.5,0.7))
		
		for i in self.ShipData['ShipHousing']:
			n = SpriteNode(i['size'][1],parent=self.main_node, position = (i['x'],i['y']),scale=0.4,anchor_point=(0.5,0.5))
			self.Ship_module_list.append({'id':i['id'],'module':n})
		
		#button
		self.zoom_button = Togglebutton(parent=self.mainblend_node,position=(1000,100),default_txt='Zoom',use_default_text=False,pc='#0a1fff',nc='#02073a')
		self.travel_button = Togglebutton(parent=self.mainblend_node,position=(1000,200),default_txt='Travel',use_default_text=False,pc='#0a9fff',nc='#023a24')
		#Vars
		self.module_mode = False
		self.traveling = None
		self.engine_speed = 0
		self.moved_main_x = 0
		self.moved_main_y = 0
		self.moved_end_main_x = 0
		self.moved_end_main_y = 0
	
	def did_change_size(self):
		pass
	
	def update(self):
		self.Engine_burn.y_scale = uniform(max(min(self.engine_speed-5,99),0),self.engine_speed)
		self.Engine_emit.alpha = uniform(0.4,0.6)
		self.Engine_emit.y_scale = self.Engine_burn.y_scale*3
		self.Engine_emit.x_scale = max(min(self.Engine_burn.y_scale*3,3),0)
		if self.traveling == True:
			self.travel()
			self.shakeeffect()
			self.engine_speed = 15
		else:
			self.engine_speed = 0
	def shakeeffect(self):
		if self.zoom_button.state == False:
			nx = uniform(-10,10)
			ny = uniform(-10,10)
		else:
			nx = uniform(-1,1)
			ny = uniform(-1,1)
		self.main_node.position = (self.main_node.position.x+nx,self.main_node.position.y+ny)
	def travel(self):
		y = randint(-744*5,744*5)
		n = SpriteNode(parent=self.main_node, position=(1133*5,y),z_position=-1)
		n.rotation = (math.pi*0.5)
		ne = uniform(0.1,10)
		n.alpha = 1 - (ne/12)
		if ne <= 0.5:
			n.texture= Texture('spc:LaserBlue10')
			n.size = (30,500)
		else:
			n.texture= Texture('shp:Gradient-2')
			n.size = (30,30)
		act = [A.move_by(-2266*5,0,ne),A.remove()]
		n.run_action(A.sequence(act))
		
		
	
	@ui.in_background
	def touch_began(self, touch):
		tl = touch.location
		self.prv_main = tl
		
		for i in [self.zoom_button,self.travel_button]:
			Togglebutton.touched(i,touch,i)
	
	def touch_moved(self, touch):
		tl = touch.location
		s = self.ShipData['ShipSize']
		if self.zoom_button.state == False:
			self.moved_main_x = max(min(tl.x - self.prv_main.x + self.moved_end_main_x,s[0]/2),-s[0]/2)
			self.moved_main_y = max(min(tl.y - self.prv_main.y + self.moved_end_main_y,s[1]/2),-s[1]/2)
			self.main_node.position = (self.moved_main_x+self.central[0],self.moved_main_y+self.central[1])
	
	def touch_ended(self, touch):
		tl = touch.location
		for i in [self.zoom_button,self.travel_button]:
			Togglebutton.end(i,touch,i)
			if self.zoom_button.state == False: self.main_node.run_action(A.scale_to(1,1))
			else: self.main_node.run_action(A.scale_to(0.1,1)); self.main_node.run_action(A.move_to(1133/2,744/2,1))
			if self.travel_button.state == True: self.traveling = True
			else: self.traveling = False
			
		tl = touch.location
		self.moved_end_main_x = self.moved_main_x
		self.moved_end_main_y = self.moved_main_y

if __name__ == '__main__':
	run(ShipDesign(), show_fps=True, anti_alias = True)
