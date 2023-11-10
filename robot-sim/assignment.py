from __future__ import print_function

import time
from sr.robot import *

R = Robot()

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

search = True

def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_marker():
    markers = R.see()
    code = []
    print("I can see",len(markers),"markes:")
    for m in markers:
    	if m.info.marker_type in (MARKER_TOKEN_GOLD):
        	print(" - Token {0} is {1} meters away".format( m.info.offset, m.dist ))
    	code= m.info.code
    	return code

def find_token():
    dist=100
    for token in R.see():
        if token.dist < dist:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y
   	
   	
def take_first_marker(code,search):
   while 1:
   	if search == True:
   		dist,rot_y= look_code(code)
   	if dist ==-1:
   		#print("I don't see any tokens!!")
   		turn(10,1)
   	elif dist <d_th:
   		if R.grab():
   			print("Gotcha!")
   			turn(20,3)
   			drive(50,3)
   			R.release()
   			turn(-20,2)
   			return -1
   	elif -a_th <= rot_y <= a_th:
   		drive(30,0.5)
   	elif rot_y < -a_th:
   		turn(-2,0.5)
   	elif rot_y >a_th:
   		turn(2,0.5)

def look_code(num):
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.code is num:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	#print("PROBLEMI! PROBLEMI PER LA FERRARI!")
	return -1, -1
    else:
   	return dist, rot_y

def get_together(code1):
   while 1:
   	if search == True:
   		dist,rot_y= look_code(code1)
   	if dist < 2*d_th:
		drive(20,1)
   		R.release()
   		return -1
   	elif -a_th <= rot_y <= a_th:
   		drive(25,0.5)
   	elif rot_y < -a_th:
   		turn(-5,0.5)
   	elif rot_y >a_th:
   		turn(2,0.5)

def take_marker(code,code1,search):
   while 1:
   	if search == True:
   		dist,rot_y= look_code(code)
   	if dist ==-1:
   		print("I don't see any tokens!!")
   		turn(-10,1)
   	elif dist <d_th:
   		if R.grab():
   			print("Gotcha!")
   			turn(20,3)
   			get_together(code1)
   			return -1
   	elif -a_th <= rot_y <= a_th:
   		drive(50,0.5)
   	elif rot_y < -a_th:
   		turn(-2,0.5)
   	elif rot_y > a_th:
   		turn(2,0.5)

def main():
	v = []
	drive(50,6)
	for i in range(6):
		v.append(find_marker())
		print(v)
		turn(20,0.9)
		i += 1
	code1 = v[0]	
	take_first_marker(code1, search)
	for code in v[1:]:
		if search == True:
			print(code, search)
			take_marker(code, code1, search)
	print("EUREKA!")
			
main ()


    
