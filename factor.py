
import array
import math
import time
import sys
from random import randint

class point:
    def __init__(self,x,y):
        self.x_intercept = x
        self.y_intercept = y

class elliptic_curve:
    def __init__(self,param_a,param_b,f):
        self.a = param_a
        self.b = param_b
        self.field = f

def sec_sq(base,exp,mod):

	Q = base
	R = 1
	
	while exp > 0:
		if exp % 2 == 1:
			R = (Q*R) % mod
			exp = exp - 1
		else:
			Q = (Q*Q) % mod
			exp = exp/2
	
	return R


def is_prime(n):

	x = int((n-1)/2)
	if n%2 == 0:
		if n != 2:
			return False
		else:
			return True
	for i in range(2,12):	
		a = randint(2,n-1)
		if jacobi(a,n) == 0:
			i = i-1
		elif jacobi(a,n) != int(sec_sq(a,x,n)) and jacobi(a,n) != int(sec_sq(a,x,n)) - n:
			return False
	return True

def jacobi(top,bottem):
	ans = 0
	sign = 1
	while ans != 1 or ans != -1:
		if gcd(top,bottem) != 1:
			return 0
		elif gcd(top,bottem) == 1 and top > bottem:
			top = top % bottem
		elif top == -1:
			return sign*int(pow(-1,(bottem-1)/2))
		elif top == 2:
			if bottem%8 == 1 or bottem%8 == 7:
				return sign*1
			elif bottem%8 == 3 or bottem%8 == 5:
				return sign*-1
		elif top%2 == 1 and gcd(bottem,top) == 1:
			if bottem%4 == 3 and top%4 == 3:
				temp = bottem
				bottem = top
				top = temp
				sign = -1*sign
			else:
				temp = bottem
				bottem = top
				top = temp
				sign = 1*sign
		elif top%2 == 0 and gcd(top,bottem) == 1:
			while top%2 == 0:
				if top == 2:
					if bottem%8 == 1 or bottem%8 == 7:
						return sign*1
					elif bottem%8 == 3 or bottem%8 == 5:
						return sign*-1
				if bottem%8 == 1 or bottem%8 == 7:
					sign = sign*1
					top = top/2
				elif bottem%8 == 3 or bottem%8 == 5:
					sign = sign*-1
					top = top/2	
				
def gcd(number, mod):
	if number == 0 or mod == 0:
		return 0
	elif number % mod == 0:
		if number > mod:
	   		return mod
   		else:
   			return number 
	elif number == 1:
		return 1
	else:
		if number < mod:
	    		c = mod
	    		mod = number
	    		number = c
	
		r = number%mod

		while r != 0:
		    c = r
		    number = mod
		    mod = r
		       
		    r = number%mod
	    
		return c

def find_inverse(number,mod):

    mult = []
    rem = []

    num = number
    m = mod
    if number % mod == 0:
    		if number > mod:
			return -mod
		else:
			return - number
    elif number == 1:
		return 1
		
    else:
		if number < mod:
	    		c = mod
	    		mod = number
	    		number = c
	
	
		q = int(math.floor(number/mod))
		r = number%mod
		rem.append(number)
		rem.append(mod)
		c = r

		while r != 0:
		    mult.append(q)
		    rem.append(r)

		    c = r
		    number = mod
		    mod = r
		       
		    r = number%mod
		    q = int(math.floor(number/mod))

		if c != 1 and c != -1:
			return -c
		else:
			if len(mult) == 1:
				s = -mult[0]
				t = -mult[0]
			else:
				s = (-mult[len(mult)-1])*(-mult[len(mult)-2])+1
				t = -mult[len(mult)-1]

			for i in range(len(mult)-2,0,-1):
				temp = t
				t = s
				s = temp + s * - mult[i-1]
	
			if num > m:
				if t < 0:
					return t + m
				else:
					return t
			else:
				if s < 0:
					return s + m
				else:
					return s

def print_elliptic_curve(t):
    print "y^2 = x^3 + ", t.a , "x + " , t.b

def print_point(a):
    print "(" , a.x_intercept , " , " , a.y_intercept , ")"

def add_points(a,b,c):
    
    if a.x_intercept == 0 and a.y_intercept == 0:
    		return b
    elif b.x_intercept == 0 and b.y_intercept == 0:
    		return a
    else:
		if a == b:
			numer = 3*a.x_intercept*a.x_intercept + c.a
			denom = 2*a.y_intercept
				
			if denom < 0:
				denom = c.field + denom
			if numer < 0:
				numer = c.field + numer
			if find_inverse(denom,c.field) < 0:
				z = find_inverse(denom,c.field) 
		    		tempx = -z
				tempy = -1
		    		temp = point(tempx,tempy)
		    		return temp
			else:
			  	m = ((numer)*(find_inverse(denom,c.field))) % c.field
			   	
				tempx = (m*m - a.x_intercept - b.x_intercept) % c.field
				tempy = (m*(a.x_intercept - tempx) - a.y_intercept) % c.field
				
				if tempx < 0:
						tempx = c.field + tempx
						
				if tempy < 0:
						tempy = c.field + tempy
				
				temp = point(tempx,tempy)
				return temp

		elif a.x_intercept == b.x_intercept:
				temp = point(0,0)
				return temp
		else:
			numer = b.y_intercept - a.y_intercept
			denom = b.x_intercept - a.x_intercept
				
			if denom < 0:
				denom = c.field + denom
			if numer < 0:
				numer = c.field + numer
			if find_inverse(denom,c.field) < 0:		
		    		z = find_inverse(denom,c.field) 
		    		tempx = -z
				tempy = -1
				temp = point(tempx,tempy)
				return temp
			else:
				m = ((numer)*(find_inverse(denom,c.field))) % c.field
			
				tempx = (m*m - a.x_intercept - b.x_intercept) % c.field
				tempy = (m*(a.x_intercept - tempx) - a.y_intercept) % c.field 	
				
				if tempx < 0:
						tempx = c.field + tempx
						
				if tempy < 0:
						tempy = c.field + tempy
				
				temp = point(tempx,tempy)
		  		return temp

def on_curve(a,c):
      
	tempx = ((a.x_intercept*a.x_intercept*a.x_intercept) + (c.a*a.x_intercept) + c.b) % c.field
	tempy = (a.y_intercept*a.y_intercept) % c.field
      
	if tempx < 0:
    		tempx = c.field + tempx
	if tempy == tempx:
		return true
	else: 
		return false
     
def double_add(a, n, t): 
	Q = a
	R = point (0,0)
	check = 0
	
	while n > 0:
		if n % 2 == 1:
			R = add_points(R,Q,t)
			n = n - 1
			if R.y_intercept < 0:
				n = 0	
		Q = add_points(Q,Q,t)
		n = n/2
		if Q.y_intercept < 0:
			n = 0
			check = 1
	if check == 1:
		return Q
	else:
		return R


def generate_curve(p, a,field):
	
	b = ((p.y_intercept*p.y_intercept) - (p.x_intercept*p.x_intercept*p.x_intercept) - a*p.x_intercept)%field
	
	t = elliptic_curve(a,b,field)
	
	return t

def factor(p,a,n,b):
	t = generate_curve(p,a,n)
	print_elliptic_curve(t)
	temp = p
	print_point(temp)
	factors = []
	check = 0
	
	if is_prime(n):
		factors.append(int(n))
	while is_prime(n) == False:
		for i in range(2,b+1):
			ans = double_add(temp,i,t)
			temp = ans
			print "\r{0} %".format((float(i)/b)*100),
			if temp.y_intercept < 0:
				if (temp.x_intercept == n):
					i = 2
				elif is_prime(temp.x_intercept) == True:
					factors.append(int(temp.x_intercept))
					n = n/temp.x_intercept
					if is_prime(n) == True:
						factors.append(n)
					t = generate_curve(p,a,n)
					temp = p
					check = 1
					break
				else:
					factors.extend(factor(p,a,int(temp.x_intercept),b))
					n = n/temp.x_intercept
					t = generate_curve(p,a,n)
					temp = p
					break
		if check == 0:			
			if is_prime(n) == False:
				print "\n"
				print "factoring failed for " , b , "!"
				print factors
				check = raw_input("would you like to try again with a new point, curve, and bound? (y/n):")
				if check == "n" :
					return
				x_1 = 1
				y_1 = 5
				b = int(100000)
				d = randint(1,100)
				temp = point(x_1,y_1)
				t = generate_curve(p,d,n)
				print_elliptic_curve(t)
				print_point(temp)

	factors[len(factors)-1] = int(factors[len(factors)-1])	
	return factors
	
	
	
n = raw_input("enter a number to factor:	 ")


n = int(n)
x_1 = 1
y_1 = 3
b = int(100000)
d = randint(1,100)

p = point(x_1,y_1)	
			
fas = factor(p,d,n,b)
			
print "\nPrime factors of" , n , "are :" , fas


			
			
			
			
			
			
