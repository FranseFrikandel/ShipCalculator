import numpy as np
from dataclasses import dataclass

from numpy.core.numeric import moveaxis

@dataclass
class Shape():
    """
    Een losse vorm. Meerdere vormen kunnen samen een schip vormen die bestaat uit meerdere simplistische vormen.

    XY coordinaten zijn t.o.v. centroid. Voor een rechthoek dus het middelpunt, voor een driehoek op 1/3h, etc.

    X is lengte van het schip
    Y is de breedte van het schip
    length is dus de grootte in X-richting,
    width is dus de grootte in de Y-richting.

    Ondersteunde vormen:
    rect - Rechthoek.
    circle - Cirkel. Hierbij voor lengte en breedte dezelfde waarde ingeven. TODO: Vervangen met ellips
    triangle - Driehoek. WIP
    """
    sType: str
    length: float
    width: float
    height: float
    x: float
    y: float

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


class Ship():
    def __init__(self, **kwargs):
        self.shapes = []

    def addShape(self, shapeOb):
        if not isinstance(shapeOb, Shape):
            raise TypeError("Not a shape object")
        
        self.shapes.append(shapeOb)
    
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