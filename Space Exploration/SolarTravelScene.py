
import time
import sys
from scene import *
import sound
from random import randint,uniform,choice
import math
from planets import Solar
import Constellation_Name
import Interactables
from PlanetAsset import PlanetAsset
A = Action

class SolarTravelScene (Scene):
	def __init__(self,
	SolarData={'playername':'aeiou',
	'ship_sprite':'Ship_design/Ship/Ship_1.png',
	'generated':False,
	'SolarQuantity':50,
	'SolarSize':(3450,2250),
	'SolarIndep':[],
	'PlayerPrevPos': [0,0]
	},
	*args, 
	**kwargs):
		Scene.__init__(self)
		self.playername = SolarData['playername']
		self.ship_data = SolarData['ship_sprite']
		self.haveGenerated = SolarData['generated']
		self.SolarQuantity = SolarData['SolarQuantity']
		self.SolarSize = SolarData['SolarSize']
		self.SolarIndep = SolarData['SolarIndep']
		self.PlayerPrevPos = SolarData['PlayerPrevPos']
	def setup(self):
		#vars
		self.background_color = '#000000'
		self.central_pos = (1133/2,744/2)
		self.fixpth = (0,0)
		self.selectedsolarpos = self.PlayerPrevPos
		self.valuex = 0
		self.valuey = 0
		self.dis = 0.1
		self.pspx = 0
		self.pspy = 0
		self.insolar = False
		self.selected_solar_list = []
		self.scroll = False
		self.doubleclick = False
		self.solarselected = False
		self.dlist = []
		#All main nodes for moving maps at main node and menus for menu node
		self.main_node = Node(parent=self, position=self.central_pos,z_position=2)
		self.menu_node = Node(parent=self, position=self.bounds,z_position=3)
		#centeral dot
		self.dot = SpriteNode('shp:Circle',size=(1,1),parent=self.main_node)
		#player ship
		self.playership = SpriteNode(self.ship_data,scale=0.03,parent=self.main_node,position=self.PlayerPrevPos)
		#select sprites
		self.select = SpriteNode('iow:code_256',size=(40,40),parent=self.main_node,color='#800000',scale=2,alpha=0)
		self.select2 = SpriteNode('iow:code_256',size=(30,30),parent=self.main_node,color='#ff0000',scale=1.5,alpha=0)
		self.selectLabel = LabelNode('YourShip',parent=self.menu_node,font=('<System>',20),anchor_point=(0.5,0),position=(self.size.x/2,self.size.y/50),alpha=0)
		#Background parallax
		self.bg1 = SpriteNode('SolarBg_1.png',parent=self,position=self.central_pos,alpha=1)
		self.bg2 = SpriteNode('SolarBg_2.png',parent=self,position=self.central_pos,alpha=0.8)
		self.bg3 = SpriteNode('SolarBg_3.png',parent=self,position=self.central_pos,alpha=0.5)
		self.bg4 = SpriteNode('SolarBg_4.png',parent=self,position=self.central_pos,alpha=0.5,size=self.size)
		#spawn zoom effect
		self.bg1.run_action(
			A.sequence(
				A.scale_to(20,0),A.scale_to(1,1,TIMING_EASE_OUT)
			))
		self.bg2.run_action(
			A.sequence(
				A.scale_to(30,0),A.scale_to(1,1,TIMING_EASE_OUT)
			))
		self.bg3.run_action(
			A.sequence(
				A.scale_to(40,0),A.scale_to(1,1,TIMING_EASE_OUT)
			))
		self.bg4.run_action(
			A.sequence(
				A.scale_to(50,0),A.scale_to(1,1,TIMING_EASE_OUT)
			))
		self.main_node.run_action(
			A.sequence(
				A.scale_to(100,0),A.scale_to(1,1,TIMING_EASE_OUT)
			))
		#Generating SolarIndep
		if self.haveGenerated == False:
			for i in range(1,self.SolarQuantity):
				nglow = SpriteNode('shp:aura',parent=self.main_node,scale=uniform(0.2,0.3),alpha=0.3)
				n = SpriteNode(Solar[0],parent=self.main_node,scale=uniform(0.1,0.2))
				n.position = (uniform(-self.SolarSize[0]/2,self.SolarSize[0]/2),
						uniform(-self.SolarSize[1]/2,self.SolarSize[1]/2))
						
				#proccess the solar to be 1 light years apart
				ac = False
				while ac == False:
					ac = True
					for i2 in self.SolarIndep:
						if (math.sqrt( (n.position.x - i2['solar'].position.x)**2+(n.position.y - i2['solar'].position.y)**2) ) >= 150:
							pass
						else:
							ac = False
					if ac == False:
						n.position = (uniform(-self.SolarSize[0]/2,self.SolarSize[0]/2),
						uniform(-self.SolarSize[1]/2,self.SolarSize[1]/2))
					else:
						#print('Solar no.' + str(i) + ' succeed.\n\n')
						break
						
				nglow.position = (n.position.x,n.position.y+2)
				nam = choice(Constellation_Name.list)
				Name = str(nam['name']) +" " + str(randint(10,99)) + str(nam['abbr']) + str(randint(1,9)) + choice(Constellation_Name.listAlpha)
				self.SolarIndep.append({'id':i,
				'StarName':Name,
				'solar':n,
				'glow':nglow,
				'color':None,
				'explored':False})
				#print(i)
			self.haveGenerated = True
		self.fade = ShapeNode(color='#ffffff',size=self.size,z_position=101,parent=self,position=self.size/2)
		self.fade.run_action(A.fade_to(0,0.5))
		
		#buttons in Self.menu_node group
		self.travel_button = Interactables.Togglebutton(parent=self.menu_node,bimg=None,showtext=True,default_txt='Travel',position=(80,80),use_default_text=False)
		self.SolarTravel_button = Interactables.Togglebutton(parent=self.menu_node,bimg=None,showtext=True,default_txt='SolarTravel',position=(1050,80),use_default_text=False)
	def did_change_size(self):
		pass
	
	def update(self):
		self.select.rotation = (self.t)*4
		self.select2.rotation = self.t*10
		self.SolarTraveling()
		self.travel_update()
	def touch_began(self, touch):
		self.pth = touch.location
		
		for a in [self.travel_button,self.SolarTravel_button]:
			Interactables.Togglebutton.touched(a,touch,a)
			
		
	
	def touch_moved(self, touch):
		self.doubleclick = False
		self.scroll = True
		tl = touch.location
		ss = self.SolarSize
		cn = self.central_pos
		self.valuex = max(min(tl.x-self.pth.x+self.fixpth[0],ss[0]/2),-ss[0]/2)
		self.valuey = max(min(tl.y-self.pth.y+self.fixpth[1],ss[1]/2),-ss[1]/2)
		self.main_node.position = (
			cn[0] + self.valuex,
			cn[1] + self.valuey
			)
			
		self.bg1.position = (cn[0] + self.valuex/3,cn[1] + self.valuey/3)
		self.bg2.position = (cn[0] + self.valuex/5,cn[1] + self.valuey/8)
		self.bg3.position = (cn[0] + self.valuex/10,cn[1] + self.valuey/10)
		self.bg3.position = (cn[0] + self.valuex/10,cn[1] + self.valuey/15)
		#print(self.main_node.position.x)
	
	def touch_ended(self, touch):
		cn = self.central_pos
		tl = touch.location
		mainpoint = self.main_node.point_from_scene(tl)
		self.fixpth = (self.valuex,self.valuey)
		#print(self.fixpth)
		
		#button
		for i in [self.travel_button,self.SolarTravel_button]:
			Interactables.Togglebutton.end(i,touch,i)
		
		#Constant travel
		if self.travel_button.state == True:
			self.pspx = (self.PlayerPrevPos[0] - self.selectedsolarpos[0])*(1/(500 * self.dis/150))
			self.pspy = (self.PlayerPrevPos[1] - self.selectedsolarpos[1])*(1/(500 * self.dis/150))
			#print(str(self.pspx + self.pspy))
		else:
			self.pspx = 0
			self.pspy = 0
		if self.travel_button.state == False and self.insolar == False:
			self.selected_solar_list = []
		#important definitors
		self.selector(mainpoint)		
		self.line_maker()
		self.selector_effect()
		#end set
		self.scroll = False
		#print(self.PlayerPrevPos)
		#print(self.selectedsolarpos)
		
	def line_maker(self):
		#create line effect
		if self.scroll == False and self.travel_button.touched == False and self.travel_button.state == False and self.travel_button.touched == False:
			#clean line
			for i in self.dlist:
				i.remove_from_parent()
				while i.parent:
					if not i.parent:
						self.dlist.remove(i)
			#create line effect
			if self.selected_solar_list != [] and not self.travel_button == False:
				for j in range(0,int(self.dis)):
					d = SpriteNode('shp:Circle',parent=self.main_node,size=(1,1),z_position=5,color='#ff7676')
					self.posx = [self.PlayerPrevPos[0],self.selectedsolarpos[0]]
					self.posy = [self.PlayerPrevPos[1],self.selectedsolarpos[1]]
					self.pfix = self.posx[1] - (self.posx[1]-self.posx[0])*(j/self.dis)
					self.pfiy = self.posy[1] - (self.posy[1]-self.posy[0])*(j/self.dis)
					d.position = (self.pfix,self.pfiy)
					self.dlist.append(d)
	def selector(self,mainpoint):
		if self.scroll == False and self.travel_button.touched == False and self.travel_button.state == False and self.SolarTravel_button.touched == False:
			for a in self.SolarIndep:
				if mainpoint in a['solar'].frame:
					sound.play_effect('ui:click1')
					self.selectedsolarpos = (a['solar'].position.x,a['solar'].position.y)
					self.select.position = a['solar'].position
					self.select2.position = a['solar'].position
					self.dis = math.sqrt( (self.PlayerPrevPos[0]-self.selectedsolarpos[0])**2+(self.PlayerPrevPos[1]-self.selectedsolarpos[1])**2)
					self.selectLabel.text = str(a['StarName']) + '\nLightyears: {:.3g}'.format((self.dis/150)) + '\n' + ('Discovered' if a['explored'] == True else 'Undiscovered')
					#print(self.dis)
					self.doubleclick = True
					self.selected_solar_list.append(a)
					self.playership.rotation = -(math.atan2(self.PlayerPrevPos[0]-self.selectedsolarpos[0],self.PlayerPrevPos[1]-self.selectedsolarpos[1])) + (math.pi*1.5)
			#cancel selection
		if self.selected_solar_list == [] and self.scroll == False and self.travel_button.touched == False and self.travel_button.state == False and self.SolarTravel_button.touched == False:
			self.playership.rotation = 0
			self.select.position = self.PlayerPrevPos
			self.select2.position = self.PlayerPrevPos
			self.selectLabel.text = 'Shipname: ' + self.playername 
	def selector_effect(self):
		if self.scroll == False:
			self.select.run_action(A.sequence(
				A.group(
					A.fade_to(0,0),
					A.scale_to(5,0)
					),
				A.group(
					A.fade_to(1,0.3),
					A.scale_to(2,1,TIMING_BOUNCE_OUT))
			))
			self.select2.run_action(A.sequence(
				A.group(
					A.fade_to(0,0),
					A.scale_to(7,0)
					),
				A.group(
					A.fade_to(1,0.3),
					A.scale_to(1.5,0.5,TIMING_EASE_OUT))
			))
			self.selectLabel.run_action(
				A.sequence(
					A.fade_to(0,0),
					A.fade_to(1,1)))
	def travel_update(self):
		if self.travel_button.state == True:
			if math.sqrt(
				(self.PlayerPrevPos[0] - self.selectedsolarpos[0])**2 +
				(self.PlayerPrevPos[1] - self.selectedsolarpos[1])**2
				) <= 10:
					self.selector_effect()
					try:
						self.insolar = True
						self.dis = self.td_a_to_b(self.PlayerPrevPos[0],self.selectedsolarpos[0],self.PlayerPrevPos[1],self.selectedsolarpos[1])
						self.selectLabel.text = str(self.selected_solar_list[0]['StarName']) + '\nLightyears: {:.3g}'.format((self.dis/150)) + '\n' + ('Discovered' if self.selected_solar_list[0]['explored'] == True else 'Undiscovered')
					except:
						self.selectLabel.text = 'Shipname: ' + self.playername
					self.travel_button.state = False
					self.travel_button.body.color = self.travel_button.nc
			else:
				self.insolar = False
				self.PlayerPrevPos[0] -= self.pspx
				self.PlayerPrevPos[1] -= self.pspy
				self.playership.position = (self.PlayerPrevPos[0],self.PlayerPrevPos[1])
				self.selectLabel.text = 'Traveling: {:.3g}'.format(math.sqrt( (self.PlayerPrevPos[0]-self.selectedsolarpos[0])**2+(self.PlayerPrevPos[1]-self.selectedsolarpos[1])**2)/150) + ' LY'
	
	def SolarTraveling(self):
		if self.SolarTravel_button.state == True:
			if (self.dis/150) >= 0.1:
				#print(self.dis/150)
				print('Too far')
				self.SolarTravel_button.state = False
				self.SolarTravel_button.body.color = self.travel_button.nc
			elif not self.selected_solar_list == []:
				#print(self.selected_solar_list)
				#print(self.dis/150)
				print('Traveling')
				self.SolarTravel_button.state = False
				self.SolarTravel_button.body.color = self.travel_button.nc
			else:
				#print(self.dis/150)
				#print(self.selected_solar_list)
				print('Solar not selected')
				self.SolarTravel_button.state = False
				self.SolarTravel_button.body.color = self.travel_button.nc
	
	def td_a_to_b(self,x1,x2,y1,y2):
		a = math.sqrt((x1-x2)**2+(y1-y2)**2)
		return a
	def stop(self):
		pass


if __name__ == '__main__':
	run(SolarTravelScene(), show_fps=True, anti_alias=True)
