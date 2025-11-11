from scene import *
import sound
import random
import math
import console
A = Action



class ListCompress (Node):
	def __init__(self,nlist=["yes","dot","na","dot","na","dot","na"],bicolor='#ffffff', listsize=(200,50),strokesize=7,tc='#ffffff',ap=(0,0.5),zlayer=0, *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		
		self.listn = []
		for a,b in enumerate(nlist):
			body_bg = ShapeNode(parent=self,size=(listsize[0]+strokesize,listsize[1]+strokesize),z_position=0-(a/10)+zlayer,position=(0,0),color=bicolor)
			
			body_insert = ShapeNode(parent=self,size=listsize,z_position=1-(a/10)+zlayer,color='#000000',position=(0,(0)))
			
			text = LabelNode(str(b),parent=self,font=('<System-Bold>',listsize[1]),color=tc,z_position=2-(a/10)+zlayer,anchor_point=ap,position=(-(int(listsize[0]/2-10)),0))
			if a != 0:
				text.alpha = 0
			
			self.listn.append([body_bg,body_insert,text,b,a])
		
		self.arrow = SpriteNode('iow:arrow_left_b_256',parent=self,size=(listsize[1],listsize[1]),z_position=3+zlayer,position=((listsize[0]/2-20),0))
		
			
		
		#var
		self.selected = False;
		self.touched = False;
		self.valuesize = listsize;
		self.strokesize = strokesize;
		self.psel = False
		self.value = self.listn[0][2].text
		
		
	def tbegan(a,b):
		tl = a.point_from_scene(b.location)
		
		for i in a.listn:
			if tl in i[1].frame:
				if i[4] == 0 and a.selected == False:
					i[1].color = '#ffffff'
					a.touched = True
				elif a.selected == True and i[4] != 0:
					i[1].color = '#ffffff'
					a.touched = True
					
	def tmoved(a,b):
		pass
	def tend(a,b):
		tl = a.point_from_scene(b.location)
		
		if a.touched == True:
			for i in a.listn:
				if tl in i[1].frame and a.selected == False and i[4] == 0:
					a.selected = True
					i[1].color = '#ff6262'
					break
				elif tl in i[1].frame and a.selected == True and i[4] != 0:
					a.selected = False
					store = i[3]
					a.listn[i[4]][3] = a.listn[0][3]
					a.listn[0][3] = store
					a.listn[i[4]][2].text = a.listn[i[4]][3]
					a.listn[0][2].text = a.listn[0][3]
					a.value = a.listn[0][2].text
				if tl in i[1].frame:
					a.psel = True;
				i[1].color = '#000000'
		else:
			a.selected = False
			a.listn[0][1].color = '#000000'
		
		
		if a.selected == False or (a.psel == True and a.selected == True):
			for i in a.listn:
				if i[4] != 0:
					i[0].remove_action("a")
					i[1].remove_action("a")
					i[2].remove_action("a")
					i[0].run_action(A.move_to(0,0,0,TIMING_EASE_OUT))
					i[1].run_action(A.move_to(0,0,0,TIMING_EASE_OUT))
					i[2].run_action(A.move_to(-(int(a.valuesize[0]/2-10)),0,0,TIMING_EASE_OUT))
					i[2].run_action(A.fade_to(0,0))
					a.selected == False
			#print("Removed")
		elif a.selected == True:
			for i in a.listn:
				if i[4] != 0:
					i[0].run_action(A.move_to(i[0].position[0],-(i[4]*a.valuesize[1]),0.5,TIMING_EASE_OUT),"a")
					i[1].run_action(A.move_to(i[1].position[0],-(i[4]*a.valuesize[1]),0.5,TIMING_EASE_OUT),"a")
					i[2].run_action(A.group(A.move_to(i[2].position[0],-(i[4]*a.valuesize[1]),0.5,TIMING_EASE_OUT),A.fade_to(1,0.5)),"a")
			#print("Scending")
						
		a.touched = False
		a.psel = False
		#print(a.selected)

class Togglebutton (Node):
	def __init__(self,size=(100,50),bimg=None,fontt=('<System-Bold>',20),bcolor='#000000',nc='#ff2727',pc='#5dff3b',cc='#f8fff6',showtext=True,default_txt='aeiou',use_default_text=True, *args, **kwargs):
		#bcolor = not touch color
		#nc = false/not active
		#pc = True/active
		#cc = touched color
		#showtext = show a text in the button
		#default_txt = shows text if use_default_text is set to false and showtext is True
		#use_default_text = Shows True or false button when interacting, if false, default_txt text will show
		Node.__init__(self, *args, **kwargs)
		self.body = ShapeNode(parent=self,size=(size[0]+5,size[1]+5),color=nc,z_position=0)
		self.togglebutton = SpriteNode(bimg,parent=self,size=size,color=bcolor,z_position=1)
		self.textin = LabelNode(default_txt,parent=self,z_position=2,font=fontt,alpha=int(showtext))
		
		self.touched = False;
		self.state = False
		self.bcolor = bcolor;
		self.cc = cc
		self.nc = nc
		self.pc = pc
		self.usedf = use_default_text
		self.dtxt = default_txt
		
	def touched(self,a,b):
		tl = b.point_from_scene(a.location)
		if tl in b.body.frame:
			b.touched = True
			b.togglebutton.color = b.cc
			b.textin.color = b.bcolor
			if self.usedf == True:
				b.textin.text = "touched"
			else:
				b.textin.text = str(self.dtxt)
	def end(self,a,b):
		tl = b.point_from_scene(a.location)
		if tl in b.body.frame and b.touched == True:
			b.state = (not b.state)
			b.togglebutton.color = b.bcolor;
			if b.state == True: b.body.color = b.pc;
			else: b.body.color = b.nc;
			b.touched = False
		else:
			b.togglebutton.color = b.bcolor;
			b.touched = False
		b.textin.color = b.cc
		if self.usedf == True:
			b.textin.text = str(b.state)
		else:
			b.textin.text = str(self.dtxt)

#copy paste this Slider Class to make a custom slider. The rest and value is upto you
# size, bcolor, btnsize, yaxis, buon, sc, c, anchor_point=
class Sliders (Node):
	def __init__(self, size=(20,255),bcolor='#fcfff5',btnsize=(50,50),yaxis=False,buon=True,sc="#656565",c='shp:Circle',anchor_point=(0.5,0), *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		self.body = ShapeNode(parent=self, size=size,anchor_point=anchor_point,z_position=0,color=bcolor)
		self.button = SpriteNode(c,parent=self,color='#ffffff',size=btnsize,z_position=2,alpha=int(buon))
		self.t_frame = ShapeNode(parent=self, size=btnsize,alpha=0,position=(0,0))
		self.ttext = LabelNode("0",parent=self,font=('Arial Rounded MT Bold',29),color='#000000',z_position=3)
		self.shadebody = ShapeNode(parent=self,size=(0,0),color=sc,anchor_point=anchor_point,position=(0,0),z_position=1)
		#variables
		self.yaxis = yaxis
		self.touched = False;
		self.fix = 0
		self.moved = (0,0)
		self.value = 0
		self.rsize = size
		
	def limitation(aa,b,c,d,e):
		#dont use limitation, its for repeated step from tend, tbegin and tmoved
		# aa = assgined self, b/c = assigned by tl, d = fixed, e = yaxis (auto)
		if aa.yaxis == False: a = (0,max(min(b-c+d,e),0))
		else: a = (max(min(b-c+d,e),0),0)
		return a

	def location(a):
		#dont use location as well
		# a = assigned self
		e = (a.button.position.x, a.button.position.y)
		return e

	def tend(a):
		# a = assigned self
		if a.yaxis == False: yo = 1
		else: yo = 0
		a.fix = a.moved[yo]
		a.touched = False
		a.t_frame.position = Sliders.location(a)
	
	def tmoved(a,ab,ac,ad):
		# a = assigned self, ab/ac = Assigned touch.location, ad = fixed prev
		if a.yaxis == False: yo = 1
		else: yo = 0
		if a.touched == True: a.moved = Sliders.limitation(a,ab,ac,ad,a.rsize[yo]); a.button.position = a.moved; a.value = int(a.moved[yo]/(a.rsize[yo]/100)); a.ttext.position = a.button.position; a.ttext.text = str(int(a.moved[yo]/(a.rsize[yo]/100))); a.shadebody.size = int(a.moved[0])+(yo*a.rsize[not yo]),int(a.moved[1]+((not yo)*a.rsize[not yo]))
			
	def tbegan(a,b):
		# a = assigned self, b = touch.location
		tl = b.point_from_scene(a)
		if tl in b.t_frame.frame: b.touched = True



#examlple of work
#use ( variable = Sliders() ) to begin build a slider (dont forget to add size,parent and anchor_point)

#use tbegan() tmoved() and tend() in the assigned def in order for it to woke

# use Sliders.value to get their values out of the sliders.

class MyScene (Scene):
	def setup(self):
		self.a = Sliders((7,200),parent=self,position=(200,200),anchor_point=(0.5,0),sc='#c44444')
		self.b = Sliders(size=(12,200),parent=self,position=(270,200),anchor_point=(0.5,0),c='shp:RoundRect',sc='#2dc43a')
		self.c = Sliders(size=(18,200),parent=self,position=(340,200),anchor_point=(0.5,0),sc='#2d3ac4',c='spc:TurretBaseBig')
		self.d = Sliders(size=(255,20),parent=self,position=(410,200),anchor_point=(0,0.5),yaxis=True)
		self.e = Sliders(size=(255,30),parent=self,position=(410,270),anchor_point=(0,0.5),yaxis=True)
		self.f = Sliders(size=(255,50),parent=self,position=(410,340),anchor_point=(0,0.5),yaxis=True)
		self.g = Sliders(parent=self,position=(410,410),sc='#ffeca7',c='spc:ShieldSilver',btnsize=(70,70),bcolor='#a6a8a2')
		
		self.h = Togglebutton(position=(510,410),parent=self,bimg=None,showtext=False)
		self.i = Togglebutton(position=(510,470),parent=self,bimg=None)
		self.j = Togglebutton(position=(510,530),parent=self,bimg='spc:ButtonRed',showtext=False)
		self.k = ListCompress(["1","burg","3","oi","5","ha","mama","mia","untrue"],'#959595',(100,25),2,'#ffffff',parent=self,position=(700,500))
		self.l = LabelNode(position=(800,600),parent=self,anchor_point=(0,1))
		self.m = LabelNode("yes",position=(800,630),parent=self,anchor_point=(0,1))
		
		# nlist, bicolor, listsize, strokesize, tc, ap, zlayer
	
	
	def did_change_size(self):
		pass
	
	def update(self):
		self.background_color = (self.a.value/100,self.b.value/100,self.c.value/100)
		self.i.textin.font = ('<System-Bold>',self.e.moved[0])
		self.i.textin.alpha = self.d.moved[0]/255
		
		self.l.text = str(self.a.value) + "\n"+str(self.b.value) + "\n"+str(self.c.value) + "\n"+str(self.d.value) + "\n"+str(self.e.value) + "\n"+str(self.f.value) + "\n"+str(self.g.value) + "\n"+str(self.h.state) + "\n"+str(self.i.state) + "\n"+str(self.j.state) + "\n"+str(self.k.value) + "\n"
		
	
	def touch_began(self, touch):
		tl = touch.location
		self.RY = tl.y
		self.RX = tl.x
		
		for s in [self.a,self.b,self.c,self.d,self.e,self.g]:
			Sliders.tbegan(tl,s)
			
		for i in [self.h,self.i,self.j]:
			Togglebutton.touched(i,touch,i)
		for k in [self.k]:
			ListCompress.tbegan(k,touch)
	
	def touch_moved(self, touch):
		tl = touch.location
		for i in [self.a,self.b,self.c,self.g]:
			Sliders.tmoved(i,touch.location.y,self.RY,i.fix)
		for j in [self.d,self.e]:
			Sliders.tmoved(j,touch.location.x,self.RX,j.fix)
	
	@ui.in_background
	def touch_ended(self, touch):
		for i in [self.a,self.b,self.c,self.d,self.e,self.g]:
			Sliders.tend(i)
		
		for j in [self.h,self.i,self.j]:
			Togglebutton.end(j,touch,j)
		
		for k in [self.k]:
			ListCompress.tend(k,touch)
		
		if touch.location in self.m.frame:
			a = console.input_alert("Input","",self.m.text,"⌘",hide_cancel_button=True)
			self.m.text = a

if __name__ == '__main__':
	run(MyScene(),LANDSCAPE,show_fps=True,multi_touch=True)
