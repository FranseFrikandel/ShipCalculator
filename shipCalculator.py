import numpy as np
from dataclasses import dataclass

@dataclass
class Shape():
    """
    Een losse vorm. Meerdere vormen kunnen samen een schip vormen die bestaat uit meerdere simplistische vormen.

    Deze vormen zijn massaloos, zie de CoG class voor zwaartepunten/gewichten toe te voegen.

    XY coordinaten zijn t.o.v. centroid. Voor een rechthoek dus het middelpunt, voor een driehoek op 1/3h, etc.
    Z coordinaten zijn t.o.v. de onderkant. Z=0 is de onderkant van het schip.

    X is lengte van het schip
    Y is de breedte van het schip
    length is dus de grootte in X-richting,
    width is dus de grootte in de Y-richting.

    Ondersteunde vormen:
    rect - Rechthoek.
    circle - Cirkel. Hierbij voor lengte en breedte dezelfde waarde ingeven. TODO: Vervangen met ellips?
    triangle - Driehoek. WIP
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
        GM
        # TODO: Welke variabelen hebben we nog nodig?
        """
        self.shapes = []
        self.CoGs = []
        if "diepgang" in kwargs:
            self.T = kwargs["diepgang"]
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
    
    def getArea(self):
        a = 0
        for sh in self.shapes:
            a += sh.getArea()
        return a
    
    def getxMOI(self):
        m = 0
        for sh in self.shapes:
            m += sh.getxMOI()
        return m

    def getyMOI(self):
        m = 0
        for sh in self.shapes:
            m += sh.getyMOI()
        return m
    
    def getMass(self):
        mt = 0
        for m in self.CoGs:
            mt += m.weight
        return mt

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
    
    def getTPC(self):
        # TODO?
        return rho / (100000 * self.getArea())
