import numpy as np
from dataclasses import dataclass

# TODO: Meeste functies die getArea() gebruiken houden nog geen rekening met 
# dieptegangen.

@dataclass
class Shape():
    """
    Een losse vorm. Meerdere vormen kunnen samen een schip vormen die bestaat 
    uit meerdere simplistische vormen.

    Deze vormen zijn massaloos, zie de CoG class voor zwaartepunten/gewichten 
    toe te voegen.

    XY coordinaten zijn t.o.v. centroid. Voor een rechthoek dus het middelpunt,
    voor een driehoek op 1/3h, etc.
    Z coordinaten zijn t.o.v. de onderkant. Z=0 is de onderkant van het schip.

    X is lengte van het schip
    Y is de breedte van het schip
    length is dus de grootte in X-richting,
    width is dus de grootte in de Y-richting.

    Ondersteunde vormen:
    rect - Rechthoek.
    circle - Cirkel. Hierbij voor lengte en breedte dezelfde waarde ingeven. 
    TODO: Vervangen met ellips?
    triangle - Driehoek. Gaat er van uit dat de "punt" altijd naar voor of 
    achter wijst. LET OP: Dit wil zeggen dat schepen met een driehoek vorm die 
    met de punt naar een zijkant wijst dus niet correct wordt berekend.
    """
    sType: str
    length: float
    width: float
    height: float
    x: float
    y: float
    z: float

    def __post_init__(self):
        if self.sType == "circle":
            self.width = self.length

    def getArea(self):
        if self.sType == "rect":
            return self.length * self.width * self.height
        elif self.sType == "circle":
            return np.pi * self.length**2
        elif self.sType == "triangle":
            return (self.length * self.width / 2)

    def getxMOI(self):
        """
        Berekent het MOI over de as in de lengterichting.
        """
        if self.sType == "rect":
            moi = self.width**3 * self.length / 12
            steiner = self.getArea()*self.y**2
            return moi + steiner
        elif self.sType == "circle":
            moi = 0.25*np.pi*self.width**4
            steiner = self.getArea()*self.y**2
            return moi + steiner
        elif self.sType == "triangle":
            moi = (1/48)*self.width**3*self.length
            steiner = self.getArea()*self.y**2

    def getyMOI(self):
        """
        Berekent het MOI over de as in de breedterichting.
        """
        if self.sType == "rect":
            moi = self.length**3 * self.width / 12
            steiner = self.getArea()*self.x**2
            return moi + steiner
        elif self.sType == "circle":
            moi = 0.25*np.pi*self.width**4
            steiner = self.getArea()*self.x**2
            return moi + steiner
        elif self.sType == "triangle":
            moi = (1/36)*self.length**3*self.width
            steiner = self.getArea()*self.x**2
            return moi + steiner
        
    def isAtDepth(self, depth):
        """
        Controleert of deze vorm op deze diepte bestaat
        """
        if self.z < depth < self.z + self.height:
            return True
        return False



@dataclass
class CoG():
    """
    Voegt zwaartepunten toe aan een schip.

    Gewicht ik kg
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
        
        self.shapes.append(CoGOb)
    
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
        T = 1
        # TODO: Dit kan een oneindige loop veroorzaken als de diepte kort op de
        # overgang tussen 2 dieptes ligt.
        while self.T != T:
            self.T = T
            T = m/(self.getArea(self.T)*self.rho)
        return self.T
    
    def getWeight(self):
        mt = 0
        for m in self.CoGs:
            mt += m.weight
        return mt
    
    def getxMOI(self):
        # TODO: Werkt alleen als de centerlijn in het midden ligt. Berekent 
        # anders steiner-aandeel fout.
        # TODO: Houdt nog geen rekening met dieptegang
        m = 0
        for sh in self.shapes:
            m += sh.getxMOI()
        return m

    def getyMOI(self):
        # TODO: Werkt alleen als de centerlijn in het midden ligt. Berekent 
        # anders steiner-aandeel fout.
        # TODO: Houdt nog geen rekening met dieptegang
        m = 0
        for sh in self.shapes:
            m += sh.getyMOI()
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
        y = ax / mt
        z = ax / mt
        return (x,y,z)
    
    def getCoB(self):
        # TODO: Ondersteunt alleen rechtstaand schip.
        if self.T == 0:
            raise LookupError("Depth is not yet calculated")
        
        # Format: V, Centroid (X,Y,Z)
        volumes = np.array([])
        for sh in self.shapes:
            if self.T - sh.z > 0: # Controleert of de vorm onder water zit
                v = (self.T - sh.z) * sh.getArea()
                volumes.append([v, (sh.x, sh.y, sh.z)])
        
        vt = 0
        vct = np.array([0, 0, 0])
        for vol in volumes:
            vt += vol[0]
            vct += vol[1]*vol[0]
        
        return vct/vt
        
    
    def getTPC(self):
        # TODO?
        return rho / (100000 * self.getArea())
