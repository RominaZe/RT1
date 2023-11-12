from __future__ import print_function

import time
from sr.robot import *

R = Robot()

a_th = 1.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""


def drive(speed, seconds):
	""" 
	Function for setting a linear velocity. 
	Args: speed (int): the speed of the wheels 
	      seconds (int): the time interval  
	"""
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

def turn(speed, seconds):
	""" 
	Function for setting an angular velocity.
	Args: speed (int): the speed of the wheels 
	      seconds (int): the time interval  
	"""
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = -speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0
    

def search_token(v_token,search):
	""" 
	Function that find the list of token seen
	If the code of the marker is not in the list then put the new 
	value in the list
	Arg:  v_token : array that contains the lis of seen token
	"""
	while search == True:
		for i in range(6): # is 6 for the 360 degree turn
			for marker in R.see():
				if marker.info.code in v_token:
					print("There is no new token")
				else: 
					v_token.append(marker.info.code)
					print("I find a new token",marker.info.code)
			turn(20,0.9)
			i += 1
		search = not search
		
		
def look_code(num):
	""" 
	Function to find the markes that are in the list
	Args: num: contain the code of the token that we have to search
	Returns:
	dist (float): distance of the maker in the list with the first 
	token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token 
	is detected) 
	"""
	dist = 100
	for token in R.see():
		if token.dist < dist and token.info.code is num:
			dist = token.dist
			rot_y = token.rot_y
	if dist == 100:
		return -1,-1
	else:
		return dist, rot_y
   	

def see_list(v_token):
	""" 
	Function that check in the list of the token that have been seen if 
	there is a new token. If so then append the value of the token that 
	is new in the list
	Args: v_token: array that contains the list of seen token  
	"""
	turn(20,1)
	for marker in R.see():
		if marker.info.code in v_token:
			print("I don't see a new token")
		else:
			v_token.append(marker.info.code)
	turn(-20,1)

		
def primo_token(code,v,search):
	"""
	Function that is run when we have the first token and release in some 
	point of the arena (without the coordinate of the center is the approximate 
	center but only in my pc)
	Args: code: contain the code of the token 
	        v: is the array of all the token seen
	"""
	while 1:
		if search == True:
			dist,rot_y= look_code(code)
		if dist ==-1:
			turn(10,1)
		elif dist <d_th:
			if R.grab(): # if we are close to the token, we grab it.
				print("Gotcha!")
				turn(20,3)
				see_list(v) # see if there are token that he did not see in the first check around
				drive(50,3)
				R.release()
				drive(-20,1)
				turn(-20,2)
				return -1
		elif -a_th <= rot_y <= a_th: # if the robot is well aligned with the token, we go forward 
			drive(50,0.5)#30
		elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			turn(-2,0.5)
		elif rot_y >a_th:
			turn(2,0.5)


def get_together(code1,search):
	"""
	Function that is run when we have get together the token and release next 
	to the first token that was took in the program (without the coordinate 
	of the center is the approximate center but only in my pc) 
	Args: code1: is the code of the first token that we saw previously
	"""
	while 1:
		if search == True:
			dist,rot_y= look_code(code1)
		if dist < 2*d_th: # If the robot is close enought to the first token then release the token that is in the gripper
			drive(20,1)
			R.release() # this release the token next to the first one 
			drive(-20,1)
			return -1
		elif -a_th <= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
			drive(25,0.5)
		elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			turn(-5,0.5)
		elif rot_y >a_th:
	   		turn(2,0.5)
   		

def take_token(code,code1,v,search):
	"""
	This function is run when is no more the first token. First check the distance 
	and the angle of the token we wnat to reach, then grab token, then check 
	if there is other token that were not saw in the previous check, then the 
	token that is grab is release beside the first token that was grab (without the 
	coordinate of the center is the approximate center but only in my pc)
	Arg : code: is the code of the token we have to pick 
	    code1: is the code of the first token were we have then to reach and release
	    v: is the array of all the token seen
	"""
	while 1:
		if search == True:
			dist,rot_y= look_code(code) # we look for markers
		if dist == -1:
			turn(-10,1)
		elif dist <d_th:
			if R.grab():
				print("Gotcha!")
				turn(20,3)
				see_list(v) # see if there are token that he did not see in the first check around	
				get_together(code1,search) # put the tokens together
				return -1
		elif -a_th <= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
			drive(75,0.5)
		elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			turn(-2,0.5)
		elif rot_y > a_th:
   			turn(2,0.5)
	

def main():
	"""Assignment Research Track 1
		The code should make the robot:
	     	- 1) Go to the center of the arena
	     	- 2) See the markers that are in the area
	     	- 3) Pick the first marker that he saw in the point before and release 
	     	it in the center
     		- 4) Pick the other markers and release it beside the first one 
     	"""
	v = [] #list of token 
	p = [] #list of grab token
	search = True
	primo = True
	drive(50,6)
	search_token(v,search)
	print(v)
	code1 = v[0] # define the first token that have to be pick
	if len(v) == 0: # If there are no token then the program finish 
		print("There are no token")
		search = not search
	while search == True:
		if primo == True: # If is the first token then run the program primo_token
			primo_token(code1,v,search)
			p.append(code1) # append the first value of the token that he grab
			primo = not primo # for now on there is not more a first token
		else:
			for code in v[1:]: # this start from the second token because the first is the  clause of the if
				take_token(code,code1,v,search)
				p.append(code)
		if len(p) == len(v): # when the list of token in the arena is equal to the one that have been grab then the task is finish
			search = not search
	print("EUREKA!")

main()
