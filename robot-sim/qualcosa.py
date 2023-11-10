from __future__ import print_function

import time
from sr.robot import *

R = Robot()

a_th = 1.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

threshold = 0.0005

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


def find_token(num,qualcosa): 
    dist = 100
    for token in R.see(): 
        if qualcosa == True:
            print("E VAI C'E L'HAI QUASI FATTA")    
            if token.dist < dist: 
                dist = token.dist 
                rot_y = token.rot_y 
        elif token.info.code is num and token.dist < dist:
            print(num)
            print(token.dist)
            if token.info.code is num and token.dist < dist:
                dist = token.dist
                rot_y = token.rot_y
                print("almeno sono qua dentro")
                                
        if dist == 100: 
            return -1,-1 
        else:
            return dist, rot_y
            
def get_together(code1,qualcosa):
   	while 1:
		dist,rot_y= find_token(code1,qualcosa)
   		if dist < threshold:
			drive(50,1)
   			R.release()
   			drive(-20,1)
   			return -1
   		elif -a_th <= rot_y <= a_th:
   			drive(50,0.5)
   		elif rot_y < -a_th:
   			turn(-5,0.5)
   		elif rot_y >a_th:
   			turn(2,0.5)


def take_marker(code, code1, qualcosa):
	while 1: 
		if code == code1:
			dist,rot_y = find_token(code1,qualcosa)
		else:
			dist,rot_y = find_token(code,qualcosa)
    		if dist==-1: 
			print("I don't see any token!!")
			turn(+10, 1)
    		elif dist <d_th:
        		print("Found it!")
        		if qualcosa == True and R.grab(): 
        			print("Gotcha!")
        			print("SPERO SIA IL PRIMO")
	    			turn(20, 3)
				drive(50,3)
				R.release()
				drive(-50,1)
				turn(-20,2)
				return -1 
			elif R.grab():
				print("ALLORA FORSE CE L'HO FATTA")
				turn(20,3)
				get_together(code1,qualcosa)
				turn(-20,2)
				#return -1
	    	elif -a_th<= rot_y <= a_th: 
		        drive(70, 0.5)
		elif rot_y < -a_th:
	       	 turn(-2, 0.5)
	   	elif rot_y > a_th:
	        	turn(+2, 0.5)
	




def main ():
    v = []
    drive(50,6)
    for i in range(6): #see all the places
        for marker in R.see():
        	v.append(marker.info.code)
        print(v)
        turn(20,0.9)
        i += 1
        
    code1 = v[0]
    search = True
    for code in v:
    	print(code1,"code 1 e' questo!!!")
        if code == code1:
            take_marker(0,code1,search)
            print("Primo preso")
            search = False
        else:
            take_marker(code, code1,search)
            print("ho appena lasciato la scatola codice", code)
    print("EUREKA!")

main() 

