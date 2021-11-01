import numpy as np
from dataclasses import dataclass

# TODO: Meeste functies die getArea() gebruiken houden nog geen rekening met 
# dieptegangen.

class Shape():
    """
    args:
    size - Een tuple in (length, width, height)
    coord - Een tuple in (x, y, z)

    XY coordinaten zijn t.o.v. centroid. Voor een rechthoek dus het middelpunt,
    voor een driehoek op 1/3h, etc.
    Z coordinaten zijn t.o.v. de onderkant. Z=0 is de onderkant van het schip.

    Deze vormen zijn massaloos, zie de CoG class voor zwaartepunten/gewichten 
    toe te voegen.

    X is lengte van het schip
    Y is de breedte van het schip
    length is dus de grootte in X-richting,
    width de grootte in de Y-richting.
    """
    def __init__(self, size, coord):
        self.size = size
        self.coord = coord

    def isAtDepth(self, depth):
        """
        Controleert of deze vorm op deze diepte bestaat
        """
        if self.coord[2] < depth < self.coord[2] + self.size[2]:
            return True
        return False


class Rectangle(Shape):
    def getArea(self):
        return self.size[0] * self.size[1]

    def getxMOI(self, offset):
        """
        Berekent het MOI over de as in de lengterichting.
        """
        steiner = self.getArea()*(self.coord[1]-offset)**2
        moi = self.size[1]**3 * self.size[0]/12
        return moi + steiner

    def getyMOI(self, offset):
        """
        Berekent het MOI over de as in de breedterichting.
        """
        steiner = self.getArea()*(self.coord[0]-offset)**2
        moi = self.size[0]**3 * self.size[1]/12
        return moi + steiner


class Triangle(Shape):
    def getArea(self):
        return self.size[0] * self.size[1] / 2

    def getxMOI(self, offset):
        """
        Berekent het MOI over de as in de lengterichting.
        """
        steiner = self.getArea()*(self.coord[1]-offset)**2
        moi = self.size[1]**3 * self.size[0]/48
        return moi + steiner

    def getyMOI(self, offset):
        """
        Berekent het MOI over de as in de breedterichting.
        """
        steiner = self.getArea()*(self.coord[0]-offset)**2
        moi = self.size[0]**3 * self.size[1]/36
        return moi + steiner


class Circle(Shape):
    def getArea(self):
        return (self.size[0]/2)**2 * np.pi

    def getxMOI(self, offset):
        """
        Berekent het MOI over de as in de lengterichting.
        """
        steiner = self.getArea()*(self.coord[1]-offset)**2
        moi = 0.25*np.pi*self.size[0]**4
        return moi + steiner

    def getyMOI(self, offset):
        """
        Berekent het MOI over de as in de breedterichting.
        """
        steiner = self.getArea()*(self.coord[0]-offset)**2
        moi = 0.25*np.pi*self.size[0]**4
        return moi + steiner


class ComplexShape(Shape):
    """Speciale klasse voor complexe vormen.
    moi: een tuple in vorm (xMOI, yMOI)
    area: totale oppervlakte
    Let op: ongetest!"""
    def __init__(self, size, coord, moi, area):
        self.size = size
        self.coord = coord
        self.moi = moi
        self.area = area

    def getArea(self):
        return self.area

    def getxMOI(self, offset):
        """
        Berekent het MOI over de as in de lengterichting.
        """
        steiner = self.area*(self.coord[1]-offset)**2
        return self.moi[0] + steiner

    def getyMOI(self, offset):
        """
        Berekent het MOI over de as in de breedterichting.
        """
        steiner = self.area*(self.coord[0]-offset)**2
        return self.moi[1] + steiner


@dataclass
class CoG():
    """
    Voegt zwaartepunten toe aan een schip.

    Gewicht in kg
    """
    weight: float
    x: float
    y: float
    z: float


@dataclass
class LiqCont():
    """Een vloeistofcontainer. Nog niet geimplementeerd."""
    #TODO: Niet geimplementeerd.
    length: float
    width: float
    height: float


class Ship():
    """
    Een schip-class. Bewaard alle variabelen en berekent vanalles.
    TODO: Consistentie in of diepgang een functieparameter of een variabelen
    in het object is.
    """
    def __init__(self, **kwargs):
        """
        kwargs:
        diepgang
        rho
        # TODO: Welke variabelen hebben we nog nodig?
        """
        self.shapes = []
        self.CoGs = []
        if "diepgang" in kwargs:
            self.T = kwargs["diepgang"]
        else:
            self.T = -1
        if "rho" in kwargs:
            self.rho = kwargs["rho"]
        else:
            self.rho = 1025 # kg/m^2

    def addShape(self, shapeOb):
        if not isinstance(shapeOb, Shape):
            raise TypeError("Not a shape object")
        
        self.shapes.append(shapeOb)

    def addCoG(self, CoGOb):
        if not isinstance(CoGOb, CoG):
            raise TypeError("Not a CoG object")
        
        self.CoGs.append(CoGOb)
    
    def getArea(self, depth=-1):
        # Berekent de waterlijnoppervalkte op een bepaalde diepgang
        checkDepth = True
        if depth == -1:
            checkDepth = False

        a = 0
        for sh in self.shapes:
            if checkDepth and not sh.isAtDepth(depth):
                continue
            a += sh.getArea()
        return a

    def getDepth(self):
        """Berekent dieptegang. Gaat er van uit dat het schip vlak staat.
        Gaat ook vanuit dat alle vormen op dezelfde diepte beginnen"""
        # TODO: Ondersteuning voor schepen onder een hoek.
        m = self.getWeight()
        T = 0.01
        # TODO: Dit kan een oneindige loop veroorzaken als de diepte kort op de
        # overgang tussen 2 vormen ligt.
        while self.T != T:
            self.T = T
            T = m/(self.getArea(depth=self.T)*self.rho)
        return self.T
    
    def getWeight(self):
        mt = 0
        for m in self.CoGs:
            mt += m.weight
        return mt

    def getxCentroid(self, depth=-1):
        """
        Berekent de offset tussen de werkelijke centroid en de coordinaat 
        nulpunt
        """
        checkDepth = True
        if depth == -1:
            checkDepth = False
        
        a = 0
        ad = 0
        for sh in self.shapes:
            if checkDepth and not sh.isAtDepth(depth):
                continue

            a += sh.getArea()
            ad += sh.coord[0] * sh.getArea()
        return ad / a
    
    def getyCentroid(self, depth=-1):
        checkDepth = True
        if depth == -1:
            checkDepth = False
        
        a = 0
        ad = 0
        for sh in self.shapes:
            if checkDepth and not sh.isAtDepth(depth):
                continue

            a += sh.getArea()
            ad += sh.coord[1] * sh.getArea()
        return ad / a

    def getxMOI(self, depth=-1):
        # TODO: Werkt alleen als de centerlijn in het midden ligt. Berekent 
        # anders steiner-aandeel fout.
        checkDepth = True
        if depth == -1:
            checkDepth = False

        centr = self.getyCentroid(depth=depth)
        m = 0
        for sh in self.shapes:
            if checkDepth and not sh.isAtDepth(depth):
                continue
            m += sh.getxMOI(centr)
        return m

    def getyMOI(self, depth=-1):
        # TODO: Werkt alleen als de centerlijn in het midden ligt. Berekent 
        # anders steiner-aandeel fout.
        checkDepth = True
        if depth == -1:
            checkDepth = False

        centr = self.getxCentroid(depth=depth)
        m = 0
        for sh in self.shapes:
            if checkDepth and not sh.isAtDepth(depth):
                continue
            m += sh.getyMOI(centr)
        return m

    def getCoG(self):
        """
        Berekent het zwaartepunt en geeft het terug als een X,Y,Z tuple
        """
        mt = 0
        ax = 0
        ay = 0
        az = 0
        for m in self.CoGs:
            mt += m.weight
            ax += m.weight * m.x
            ay += m.weight * m.y
            az += m.weight * m.z
        x = ax / mt
        y = ay / mt
        z = az / mt
        return (x,y,z)
    
    def getNabla(self):
        # TODO: Ondersteunt alleen rechtstaand schip.
        if self.T == -1:
            raise LookupError("Depth is not yet calculated")
        
        # Format: V, Centroid (X,Y,Z)
        volume = 0
        for sh in self.shapes:
            if self.T - sh.coord[2] > 0: # Controleert of de vorm onder water zit
                v = (self.T - sh.coord[2]) * sh.getArea()
                volume += v
        
        return v

    def getCoB(self):
        # TODO: Ondersteunt alleen rechtstaand schip.
        if self.T == -1:
            raise LookupError("Depth is not yet calculated")
        
        # Format: V, Centroid (X,Y,Z)
        volumes = np.array([])
        for sh in self.shapes:
            if self.T - sh.coord[2] > 0: # Controleert of de vorm onder water zit
                v = (self.T - sh.coord[2]) * sh.getArea()
                volumes.append([v, sh.coord])
        
        vt = 0
        vct = np.array([0, 0, 0])
        for vol in volumes:
            vt += vol[0]
            vct += vol[1]*vol[0]
        
        return vct/vt
    
    def getBM(self):
        return self.getxMOI(depth=self.T) / self.getNabla()
    
    def getTPC(self):
        return self.rho / (100000 * self.getArea())
