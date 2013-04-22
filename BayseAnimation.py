#!/usr/bin/env Python

# This module develops an animation to illustrate how the 
# Net-VISA software works on a simple one-dimentional problem
# There is one source to detect by two stations.
# The velocity is constant.
# The arrival time distributions (shown in the same color as the 
# stations) are Laplacian with two different decay rate.
# The x space along the line is sampled randomly 
# The animation stop when the source is detected and 
# graphically represented after it passes the score 
# threshold three times.
# The score for each position is shown in white on the blue bottom canvas
# The hit number is shown in purple at the top of the blue bottom canvas.
# Ronan Le Bras
# Copyright Gydatos LLC March 2013
# GNU license

import math as m
import numpy as np
from Tkinter import *
from random import randint

def dist(x,xm,dx):
  d1=0.5*m.exp(-1.*abs(x-xm)/dx)/dx
	return d1

def covariance(x0,x00,x1,dx):
	Sum  = 0.
	cov0 = 0.
	for i in range(1000):
		x = i
		cov = dist(x,abs(x1-x00),dx)*dist(x,abs(x1-x0),dx) 
		Sum += 0.5*(cov+cov0)
		cov0 = cov
	return 4.*dx*Sum

root=Tk()
root.title=("Wave fronts")
cw=1000
ch=200
#logo=PhotoImage(file="logo_gydatos_wave.gif")
chart_1=Canvas(root,width=cw,height=ch,background="white")
chart_3=Canvas(root,width=cw,height=ch,background="white")
chart_4=Canvas(root,width=cw,height=ch,background="white")
label=Label(chart_3,text="Hello World",bg="white",font=("Times roman","22"))
#label.image=logo
label.pack()
label_rg=Label(chart_3,text="\n                               Copyright Gydatos LLC, 2013.                                 \n\n\n\n\n\n",bg="white")
label_rg.pack()
textvar="\n Animation to illustrate how\
 an extreme simplification of the Net-VISA software working on a simple one-dimentional problem.\n\
 There is one source to detect by two stations.\
 The velocity is constant.\n\
 The arrival time distributions (shown in the same color as the\
 stations) are Laplacian with two different decay rates.\n\
 The X space along the line is sampled randomly.\n\
 The animation stops when the source is detected and graphically represented after it passes the score\
 threshold three times.\n\
 The score for each position is shown in white on the blue bottom canvas. A score of one is the maximum\n\
 The hit number is shown in purple at the top of the blue bottom canvas.\n"
label_text=Label(chart_4,bg="white",text=textvar,wraplength=450,justify=LEFT)
label_text.text=textvar
label_text.pack()

chart_2=Canvas(root,width=cw, height=ch,background="blue")
chart_1.grid(row=0,column=0)
chart_2.grid(row=1,column=0)
chart_3.grid(row=0,column=1)
chart_4.grid(row=1,column=1)
lap1=np.arange(0,1000,10, dtype="float")
lap2=np.arange(0,1000,10, dtype="float")
score=np.arange(0.,1000,10, dtype="float")
hits=np.arange(0,1000,10,dtype="int")
for i in range(100):
	lap1[i]=8.*dist(float(10*i),300.,10.)
	lap2[i]=8.*dist(float(10*i),700.,20.)
	score[i]=0.
	hits[i]=0
max_score=0.
high_score=0
x00=500
for j in range(1000):
	x0=10*randint(0,99)	
	p1=covariance(x0,x00,300.,10.)
	p2=covariance(x0,x00,700.,20.)

#	print p1,p2
	y0=100
	circle_radius=10
	dr = 20
	pause=5
	if hits[x0/10] > 0 : 
		continue
	hits[x0/10] += 1
	score[x0/10]=p1*p2
	if(score[x0/10] > 1.):
		high_score += 1
	if(high_score>2):
		chart_2.after(10000)
		chart_1.after(10000)
		chart_2.create_rectangle(10*k-5,0,10*k+5,20*hits[k],width=3,fill="orange",outline="")
		chart_2.create_rectangle(10*k-5,200,10*k+5,int(200.-100*score[k]),width=3,fill="white",outline="")
		chart_2.update()
		break
		
	if(score[x0/10] > max_score):
		max_score=score[x0/10]
	for i in range(25):
		rad=circle_radius+i*dr
		chart_1.create_line(0,100,1000,100,width=3,fill="black")
		for k in range(99):
			chart_1.create_line(10*k,int(200.*(1.-lap1[k])),10*(k+1),int(200.*(1.-lap1[k+1])),width=2,fill="red")
			chart_1.create_line(10*k,int(200.*(1.-lap2[k])),10*(k+1),int(200.*(1.-lap2[k+1])),width=2,fill="blue")
		chart_1.create_oval(x0-rad,y0-rad,x0+rad,y0+rad,outline="violet",width=3)
		chart_1.create_rectangle(290,90,310,110,fill="red")
		chart_1.create_text(300,80,text="Station 1",fill="black",font=("Times Roman","16"))
		if(max_score > 0.6):
			chart_1.create_oval(490,90,510,110,fill="yellow")
			chart_1.create_text(500,80,text="Source",fill="black",font=("Times Roman","16"))
		chart_1.create_rectangle(690,90,710,110,fill="blue")
		chart_1.create_text(700,80,text="Station 2",fill="black",font=("Times Roman","16"))
		chart_1.create_oval(x0-10,y0-10,x0+10,y0+10,fill="violet")				
		for k in range(99):
			chart_2.create_rectangle(10*k-5,200,10*k+5,int(200.-200*score[k]),width=3,fill="white",outline="")
			if(high_score<2):
				chart_2.create_rectangle(10*k-5,0,10*k+5,20*hits[k],width=3,fill="violet",outline="")
			elif (high_score == 2):
				chart_2.create_rectangle(10*k-5,0,10*k+5,20*hits[k],width=3,fill="orange",outline="")
				high_score=3
			
			
		chart_1.update()
		chart_1.after(pause)
		chart_1.delete(ALL)
		chart_2.delete(ALL)

root.mainloop()
