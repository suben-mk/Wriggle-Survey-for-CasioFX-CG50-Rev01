#Wriggle Survey Program for Casio FX-CG50
import math

def print_menu():
  print('TUNNEL SURVEY')
  print('1:Wriggle Survey')
  print('2:Exit')

def wriggle_survey():	
	print('Wriggle Survey')
	num = int(input('How many points?'))
	Ei = []
	Ni = []
	Zi = []
	for i in range(num):
		Ei.append(float(input('E{:n}=?'.format(i+1))))
		Ni.append(float(input('N{:n}=?'.format(i+1))))
		Zi.append(float(input('Z{:n}=?'.format(i+1))))

	#Linear Regression by Least Square
	en=[]
	e2=[]
	for i in range(num):
	  en.append(Ei[i] * Ni[i])
	  e2.append(Ei[i]**2)
	e_sum=sum(Ei)
	n_sum=sum(Ni)
	en_sum=sum(en)
	e2_sum=sum(e2) 
	m=(en_sum - (e_sum*n_sum / num)) / (e2_sum - e_sum**2/num)
	b=n_sum/num - m*e_sum/num

	#P and Q point on Linear Regression
	e_min = min(Ei) * 0.999999
	e_max = max(Ei) * 1.0000005
	EP, NP = e_min, m * e_min + b
	EQ, NQ = e_max, m * e_max + b

	#Coordinates on PQ Line and Local coordinates xi, yi
	Xi = []
	Yi = []
	for i in range(num):
		E0 = (m * Ni[i] + Ei[i] - m * b) / (m**2 + 1)
		N0 = m * ((m * Ni[i] + Ei[i] - m * b) / (m**2 + 1)) + b
		x = math.sqrt((EP - E0)**2 + (NP - N0)**2)
		y = Zi[i] + 100 #In case elevation < 0 m. 
		Xi.append(x)
		Yi.append(y)

	#Best fit Circle by Kasa Method (least square)
	x2 = []
	y2 = []
	xy = []
	xy2 = []
	x3 = []
	yx2 = []
	y3 = []
	for i in range(num):
		x2.append(Xi[i]**2)
		y2.append(Yi[i]**2)
		xy.append(Xi[i] * Yi[i])
		xy2.append(Xi[i] * Yi[i]**2)
		x3.append(Xi[i]**3)
		yx2.append(Yi[i] * Xi[i]**2)
		y3.append(Yi[i]**3)
	xi_sum = sum(Xi)
	yi_sum = sum(Yi)	
	x2_sum = sum(x2)
	y2_sum = sum(y2)
	xy_sum = sum(xy)
	xy2_sum = sum(xy2)
	x3_sum = sum(x3)
	yx2_sum = sum(yx2)
	y3_sum = sum(y3)		

	KM1 = 2 * (xi_sum**2 - num*x2_sum)
	KM2 = 2 * (xi_sum*yi_sum - num*xy_sum)
	KM3 = 2 * (yi_sum**2 - num*y2_sum)
	KM4 = x2_sum*xi_sum - num*x3_sum + xi_sum*y2_sum - num*xy2_sum
	KM5 = x2_sum*yi_sum - num*y3_sum + yi_sum*y2_sum - num*yx2_sum

	Xc = ((KM4*KM3) - (KM5*KM2)) / ((KM1*KM3) - KM2**2)
	Yc = (KM1*KM5 - KM2*KM4) / (KM1*KM3 - KM2**2)
	R = math.sqrt(Xc**2 + Yc**2 + 1/num*(x2_sum - 2*Xc*xi_sum + y2_sum - 2*Yc*yi_sum))

	#Transform center coordinates Xc, Yc to Ec, Nc, Zc
	Q = math.atan(m)
	Ec = EP + Xc * math.cos(Q)
	Nc = NP + Xc * math.sin(Q)
	Zc = Yc - 100 #Reverse elevation 

	#Standard Deviation and Root Mean Square Error of Radius
	dR2 = []
	for i in range(num):
		Ri = math.sqrt((Xi[i]-Xc)**2 + (Yi[i]-Yc)**2)
		dR2.append((Ri - R)**2)
	dR2_sum = sum(dR2)
	sd = math.sqrt(dR2_sum/(num-1))
	rmse = math.sqrt(dR2_sum/num)
	input("Press EXE key")

	print("Circle Center Result:")
	print("E= {0:.3f}".format(Ec))
	print("N= {0:.3f}".format(Nc))
	print("Z= {0:.3f}".format(Zc)) 
	print("Radius= {0:.3f}".format(R))
	print("SD,RMSE= {0:.3f} ,{0:.3f}".format(sd,rmse))
	input("Press EXE key")	

# Manu (Credit Prajuab Riabroy's Blog)
loop=True
choice=-1
ex_choice=-1
while loop:      
  print_menu()
  choice=int(input('Selection[1-2]'))  
  if (choice==2):
    loop=False
  elif (choice==1):
    loop=True
    wriggle_survey()
    ex_choice=1