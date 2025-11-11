from scene import *
from planets import PlanetList
import sound
from random import choice, randint, uniform
import Constellation_Name
import math
A = Action

class PlanetAsset (Node):
	def __init__(self,posit=(1333/2,744/2), *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		#All planet Assets
		#Type, TypeSize, IcePre, atmosphere, atmosPressure, Habitability, water, metal, alloy, biomass, Species, Name
		# 1/Habit,3/nbio_water,4/nbio,5/Gas, 6/Star
		#Asset
		self.posit = posit
		self.Type = choice([1,3,4,5])
		self.Sprite = choice(PlanetList[self.Type])
		
		#Size adjustment
		if self.Type == 1:
			self.TypeSize = uniform(1,1.5)
		elif self.Type == 3:
			self.TypeSize = uniform(0.6,2)
		elif self.Type == 4:
			self.TypeSize = uniform(0.3,3)
		elif self.Type == 5:
			self.TypeSize = uniform(4,7)
		self.Ts = (self.TypeSize/10) * 256
		
		#condition met
		self.glow = SpriteNode('shp:Gradient-2',position=self.posit,parent=self,size=(self.Ts+50,self.Ts+50),alpha=0.7,color='#808bff')
		self.SpriteN = SpriteNode(self.Sprite,position=self.posit,parent=self,size=(self.Ts,self.Ts))
		
		#Ice cap only exist at planet size 0.6 to 2.5
		if self.Type != 6 and 0.6 <= self.TypeSize <= 2.5:
			self.IcePre = choice([0,1,2,3,4])
			self.IcePreSprite = SpriteNode(PlanetList[2][self.IcePre],position=self.posit,parent=self,size=(self.Ts,self.Ts), alpha = 0.5)
		else:
			self.IcePre = None
		
		#cloud (only exist in Planet size 0.8 to 1.9)
		if 0.8 <= self.TypeSize <= 1.9:
			self.Ts = self.Ts *1.1
			self.Cloud = choice([0])
			self.CloudSprite = SpriteNode(PlanetList[0][self.Cloud],position=self.posit,parent=self,size=(self.Ts,self.Ts))
			self.atmosphere = True
		else:
			self.atmosphere = False
		
		#Planet Condition
		#(Habitability and AtmosPressure)
		# Habitability is according to the planet size and atmosphere
		# 1 is 100% Habitable, 0.9 to 0.5 is severe habitable (with 100%-50% decrease in species), 0.5 to 0 is inhabitable
		#Size must be 0.9 to 1.6 maintain
		if self.atmosphere == True and self.Type in [1,3]:
			self.habitability = (((((-max(min(self.TypeSize,1.1),0.6)+1) + (-1.5 +(max(min(self.TypeSize,2),1.5)))))+0.5)/0.5) * 100
			self.habitability = max(min(self.habitability,100),0)
			
		else:
			self.habitability = 0.0
		
		#AtmosPressure is how can the colony grow properly (1 is the normal pressure), anything more is bad thing. No Atmospressure is good but it makes habitability none existed
		if self.atmosphere == True:
			if 40 <= self.habitability <= 100:
				self.atmosPressure = 1
			elif self.IcePre == None:
				self.atmosPressure = self.TypeSize * 1 + (1)
			else:
				self.atmosPressure = uniform(1,5)
		elif self.Type == 5:
			self.atmosPressure = 1000
		else:
			self.atmosPressure = 0
		
		
		#Resources
		#(H2O,C,Ti,Biomass,SpeciesPop, Hydrohium)
		#Water/H2O for food and Engine 
		#Metal/C for repairs and tool upgrade
		#Alloy/Ti for Engine Upgrade
		#Biomass for Long term Low Quality Food (Common)
		#Species Population for short term High Quality Food (Rare)
		#Hydrohium for colony currency and colony growth
		# Value 0.1-1 (Very Rare), 1-5 (Rare), 5-10 (Uncommon), 10-20 (Common)
		
		
		#Set value for Water Resources
		if self.Type in [1,3]:
			if self.IcePre in [3,4]: self.water = uniform(0.1,1)
			elif self.IcePre == 2: self.water = uniform(1,4)
			elif self.IcePre == 1: self.water = uniform(5,10)
			else: self.water = uniform(10,20)
		elif self.Type == 4:
			if self.IcePre in [3,4]: self.water = uniform(1,2)
			elif self.IcePre == 2: self.water = uniform(0.5,1)
			elif self.IcePre == 1: self.water = uniform(0.1,0.5)
			else: self.water = 0.0
		else:
			self.water = 0.0
		
		#Set value for Metal
		if self.Type in [3,4]:
			if self.IcePre in [3,4]: self.metal = uniform(1,1.5)
			elif self.IcePre == 2: self.metal = uniform(1.5,2)
			elif self.IcePre == 1: self.metal = uniform(2,4)
			else: self.metal = uniform(4,8)
		elif self.Type == 1:
			if self.IcePre in [3,4]: self.metal = uniform(0,0.1)
			elif self.IcePre == 2: self.metal = uniform(0.1,0.5)
			elif self.IcePre == 1: self.metal = uniform(0.5,1)
			else: self.metal = uniform(1,2)
		else:
			self.metal = 0.0
		
		#Set value for Alloy
		if self.Type in [1,3,4]:
			if self.IcePre in [3,4]: self.alloy = uniform(0,0.1)
			elif self.IcePre == 2: self.alloy = uniform(0,1)
			elif self.IcePre == 1: self.alloy = uniform(0,2)
			else: self.alloy = uniform(0,2.5)
		else:
			self.alloy = 0.0
		
		#Set value for Biomass
		if self.Type == 1:
			if self.IcePre in [3,4]: self.biomass = uniform(1,5)
			elif self.IcePre == 2: self.biomass = uniform(1,5)
			elif self.IcePre == 1: self.biomass = uniform(5,10)
			else: self.biomass = uniform(10,30)
		else:
			self.biomass = 0.0
		
		#set species
		if self.Type in [1,3]:
			self.speciesPop = uniform(0,20)*(self.habitability/100)
		else:
			self.speciesPop = 0.0
		
		#set for Hydrohium
		if self.Type == 5:
			self.hydrohium = uniform(0,10) + ((-max(min(self.TypeSize,7),5)+5)/2) * 2.0
		else:
			self.hydrohium = 0.0
		
		#Final Condition "Hazard"
		#use in colony safety, if Hzard is above 100%, the upkeep will increase significantly
		self.hazard = 0
		if self.IcePre == 3: self.hazard += 0.10
		elif self.IcePre == 4: self.hazard += 0.25
		if 10 <= self.speciesPop: self.hazard += 0.25
		if self.biomass <= 5: self.hazard += 0.25
		elif 5.1 <= self.biomass <= 10: self.hazard += 0.10
		elif 10.1 <= self.biomass <= 20: self.hazard += 0.05
		if self.atmosphere == False: self.hazard += 0.25
		if 1 <= self.atmosPressure <= 51: self.hazard += 0.1
		elif 51 <= self.atmosPressure: self.hazard += 0.25
		if 2 <= self.TypeSize: self.hazard += 0.25
		self.hazard += (-((self.habitability)/100) + 1) * 0.4
		
		#Name the planet
		if self.habitability >= 50:
			aPl = str(randint(1,9)) + 'H-'
		else:
			aPl = 'nH' + str(randint(1,9)) + '-'
		if self.water >= 5:
			bPl = 'O' + str(randint(10,99)) + '-'
		else:
			bPl = str(randint(10,99)) + 'W-'
		cPl = str(choice(Constellation_Name.listAlpha))
		if self.Type == 1 and self.habitability >= 70:
			dPl = ' ExoPlanet'
		elif self.Type in [3,4] and self.TypeSize >= 0.8:
			dPl = ' Planet'
		elif self.TypeSize < 0.8:
			dPl = ' Dwarf Planet'
		elif self.Type == 5 and self.TypeSize >= 4:
			dPl = ' Gas Gaint'
		self.Name = aPl + bPl + cPl + dPl
			
		

class MyScene (Scene):
	def setup(self):
		self.background_color = '#000000'
		self.a = PlanetAsset(parent=self)
		self.b = LabelNode('ETETETEG',parent=self,position=(0,self.size.y/2),anchor_point=(0,1))
	
	def did_change_size(self):
		pass
	
	def update(self):
		pass
	
	def touch_began(self, touch):
		self.a.remove_from_parent()
		self.a = PlanetAsset(parent=self,posit=touch.location)
		self.b.text ='''Name: {}
Type: {}
TypeSize: {:.3g}
IcePre: {}
atmosphere: {} 
atmosPressure: {} 
Habitability: {:.3g}%
H2O: {:.3g}
C: {:.3g}
Ti: {:.3g} 
biomass: {:.3g} 
SpeciesPop: {:.3g}
Hydrohium: {:.3g}
Hazard: {:.3g}%
			'''.format(self.a.Name,self.a.Type,self.a.TypeSize,self.a.IcePre,self.a.atmosphere,self.a.atmosPressure,self.a.habitability,self.a.water,self.a.metal,self.a.alloy,self.a.biomass,self.a.speciesPop,self.a.hydrohium,self.a.hazard*100)
	
	def touch_moved(self, touch):
		pass
	
	def touch_ended(self, touch):
		pass

if __name__ == '__main__':
	run(MyScene(), show_fps=False)
