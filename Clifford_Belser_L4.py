#importing the required modules
from turtle import *
from numpy import *
import numpy as np
from matplotlib.pyplot import *
import matplotlib.pyplot as plt

#setting global variables
#allowing an input of G and dt
G=input('Enter value for G:')
dt=input('Enter value for dt:')
potentialList=[]
energyList=[]
xlist=[]
ylist=[]
class Planet(object):

    def __init__(self, name, rad, mass, dist, color, vX, vY):

        self.name = name
        self.rad = rad
        self.mass = mass
        self.dist = dist
        self.color = color
        self.x = dist
        self.y = 0.
        self.vX = vX
        self.vY = vY
        self.data = []
        self.data_x = []
        self.data_y = []
        self.data_results = { "a":0, "b":0, "t":0, "e":0}
        self.mw = Turtle()
        self.mw.color(self.color)
        self.mw.shape("circle")


        self.mw.up()
        self.mw.goto(self.x, self.y)
        self.mw.down()


    def getName(self):
        return self.name

    def getRad(self):
        return self.rad

    def getMass(self):
        return self.mass

    def getDist(self):
        return self.dist

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def movePos(self, nX, nY):
        self.x = nX
        self.y = nY

    def getVX(self):
        return self.vX

    def getVY(self):
        return self.vY

    def setXV(self, newVX):
        self.vX = newVX

    def setYV(self, newVY):
        self.vY = newVY
    def set_data_results(self, a, b, t, e):
        self.data_results["a"] = a
        self.data_results["b"] = b
        self.data_results["t"] = t
        self.data_results["e"] = e
    def get_data_results(self):
        return(self.data_results)
#equation for potential energy
    def potential(self,sun_mass,r):
        global G
        self.U = -(G*self.mass*sun_mass)/r
        return self.U
#equation for total energy
    def energy(self,sun_mass,r,vx,vy):
        global G
        self.E = self.mass*(vx**2.0+vy**2.0)/2.0-(G*self.mass*sun_mass)/r
        return self.E

    def record_states(self, x, y):
        self.data.append((x,y))
        self.data_x.append(x)
        self.data_y.append(y)

    def get_distance_from_origin_max(self):
        return math.sqrt(amax(self.data_y) ** 2 + amax(self.data_x) ** 2)

    def get_distance_from_origin_min(self):
        return math.sqrt(amin(self.data_y) ** 2 + amin(self.data_x) ** 2)
    def get_x_y_data(self):
        return(self.data)


class Sun(object):
#setting the position and properties of the sun

    def __init__(self):
        self.name = "Sun"
        self.rad = 150.0
        self.m = 15000.0
        self.c = "yellow"
        self.x = 0
        self.y = 0


        self.mw = Turtle()
        self.mw.up()
        self.mw.goto(self.x, self.y)
        self.mw.down()
        self.mw.dot(self.rad, self.c)

    def getMass(self):
        return self.m

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def __str__(self):
        return self.name




class milkyWay(Planet):


    def __init__(self, sun):
        self.star = sun
        self.planets = []
        self.mw = Turtle()
        self.mw.ht()


    def addPlanet(self, planet):
        self.planets.append(planet)

    def rotatePlanets(self):
        #all algorithms are laid out here using the equations given in the lecture
        for p in self.planets:
            #Euler

            #p.movePos(p.getX() + p.vX*dt,p.getY() + p.vY*dt)

            #rx = self.star.getX() - p.getX()
            #ry = self.star.getY() - p.getY()
            #r = math.sqrt(rx ** 2 + ry ** 2)


            #accX = G * self.star.getMass() * rx / r ** 3
            #accY = G * self.star.getMass() * ry / r ** 3

            #p.setXV(p.getVX() + accX*dt)
            #p.setYV(p.getVY() + accY*dt)


            #Verlet

            #xlist.append(p.getX())
            #ylist.append(p.getY())

            #rx = self.star.getX() - p.getX()
            #ry = self.star.getY() - p.getY()
            #r = math.sqrt(rx ** 2 + ry ** 2)

            #accX = G * self.star.getMass() * rx / r ** 3
            #accY = G * self.star.getMass() * ry / r ** 3

            #if (len(xlist) <= 4 or len(ylist) <=4):
             #   p.movePos(p.getX() + p.getVX()*dt , p.getY() + p.getVY()*dt)
            #else :
             #   p.movePos(2*p.getX() + accX*dt**2 - xlist[-5] , 2*p.getY() + accY*dt**2 - ylist[-5])


            #Velocity Verlet
            rx = self.star.getX() - p.getX()
            ry = self.star.getY() - p.getY()
            r = math.sqrt(rx ** 2 + ry ** 2)


            accX = G * self.star.getMass() * rx / r ** 3
            accY = G * self.star.getMass() * ry / r ** 3

            p.movePos(p.getX() + p.vX*dt + (accX*dt**2)/2,p.getY() + p.vY*dt + (accY*dt**2)/2)

            rx = self.star.getX() - p.getX()
            ry = self.star.getY() - p.getY()
            r = math.sqrt(rx ** 2 + ry ** 2)

            accnewX = G * self.star.getMass() * rx / r ** 3
            accnewY = G * self.star.getMass() * ry / r ** 3

            p.setXV(p.getVX() + ((accX+accnewX)/2)*dt)
            p.setYV(p.getVY() + ((accY+accnewY)/2)*dt)




            potentialList.append(p.potential(self.star.m,r))
            energyList.append(p.energy(self.star.m,r,p.getVX(),p.getVY()))




def initiateGalaxy():
#assigning properties to the planets

    sun = Sun()
    mw = milkyWay(sun)

    p1 = Planet("Planet 1", 19, 10, 220, "green", 0.0, 4.0)
    mw.addPlanet(p1)

    p2 = Planet("Planet 2", 30, 60, 280, "blue", 0.0, 5)
    mw.addPlanet(p2)

    p3 = Planet("Planet 3", 40, 50, 320, "red", 0.0, 6.3)
    mw.addPlanet(p3)

    p4 = Planet("Planet 4", 60, 100, 350, "purple", 0.0, 3.)
    mw.addPlanet(p4)
#calculating time frame and number of time steps
    pi=np.pi
    totaltime=((4*pi**2)*60**3/(G*100))**0.5
    timeFrame =int((2*totaltime)/dt)
    print ('Number of itterations=',timeFrame)

    #create empty lists
    xlist=[]
    ylist=[]
    mass=[]
    for planet in mw.planets :
        mass.append(planet.mass)

    for m in range(timeFrame):
        mw.rotatePlanets()


#itterating through each planet
        if m % 10 == 0:
            #plotting
            xlistperplanet=[]
            ylistperplanet=[]
            for p in mw.planets:
                p.mw.goto(p.x,p.y)
                p.record_states(p.getX(), p.getY())
                xlistperplanet.append(p.getX())
                ylistperplanet.append(p.getY())
            xlist.append(xlistperplanet)
            ylist.append(ylistperplanet)
    xlist=array(xlist)
    ylist=array(ylist)

    #looping through to obtain values of a,b,e and t
    for planet in mw.planets :
        print("L Max " + planet.name + " -> "+ str(planet.get_distance_from_origin_max()))
        print("L Min " + planet.name + " -> "+ str(planet.get_distance_from_origin_min()))
        a=0.5*(planet.get_distance_from_origin_max() + planet.get_distance_from_origin_min())
        b=math.sqrt(planet.get_distance_from_origin_min()*planet.get_distance_from_origin_max())
        t=2*np.pi*math.sqrt(a**3/G*planet.mass)
        e=planet.dist/planet.mass
        planet.set_data_results(a,b,t,e)
        print(planet.get_data_results())
initiateGalaxy()

#plotting the potential and total energy
plt.plot(potentialList[0::4],'-b',label='Planet 1')
plt.plot(potentialList[1::4],'r',label='Planet 2')
plt.plot(potentialList[2::4], 'y',label='Planet 3')
plt.plot(potentialList[3::4],'g',label='Planet 4')
plt.legend(loc='upper right')
plt.title('Potential Energy')
plt.show()


plt.plot(energyList[0::4],'-b',label='Planet 1')
plt.plot(energyList[1::4],'r',label='Planet 2')
plt.plot(energyList[2::4], 'y',label='Planet 3')
plt.plot(energyList[3::4],'g',label='Planet 4')
plt.legend(loc='upper right')
plt.title('Total Energy')
plt.show()
