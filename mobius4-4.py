# Dit script test de resultaten van shipCalculator tegenover de resultaten van Thierry voor mobius 4-4

import shipCalculator as sc

# Begin script Thierry
#deze opgave is met driehoek voor dus lengte ponton = lengte van schip - lengte driehoek
#dus ook oppervlakte waterlijn word berekend met driehoek

#gegevens
#torens achter
L1 = 16.2
B1 = 3.5
D1 = 25.0      #bij deze opgave geen diepgang nodig

#boeg voor (driehoek)
L2 = 30.7
B2 = 43.8
D2 = 25.0     #zelfde diepgang als torens achter

#ponton
L3 = 210.3    #als er een driehoek voor zit is het L3 - L2
B3 = 43.8
D3 = 4.54


#deel1
print('deel 1 is transit')
#transit = gehele schip boven water
#berekenen oppervlakte waterlijn Awl in transit
A_ponton = L3*B3
A_driehoek = (L2*B2)*0.5
Awl_transit = A_ponton + A_driehoek
print('Oppervlakte waterlijn transit is',Awl_transit,'in [m^2]')

#traagheidsmoment van transit waterlijn in dwarsrichting
It_transit_dwars_ponton = (L3*(B3)**3)/12
It_transit_dwars_driehoek = (L2*(B3)**3)/48
It_transit_dwars = It_transit_dwars_ponton + It_transit_dwars_driehoek
print('Traagheidsmoment transit in dwarsrichting is',It_transit_dwars,'in [m^4]')

#drukkingspunt in lengterichting vanaf kont
G_ponton = (L3*0.5)*A_ponton              #oppervalkte ponton * helft lengte ponton
G_driehoek = (L3+((1/3)*L2))*A_driehoek   #oppervalkte driehoek * lengte tot zwaartepunt driehoek vanaf kont
LCF_transit = (G_ponton + G_driehoek)/Awl_transit
print('Drukkingspunt lengte transit is',LCF_transit,'in [m]')

#traagheidsmoment van transit waterlijn in lengterichting
#werken met steiner
It_transit_lengte_ponton = (B3*(L3)**3)/12
It_transit_lengte_driehoek = (B2*(L2)**3)/36
It_steiner_ponton = A_ponton*(LCF_transit-(L3*0.5))**2             #gebruik zwaartepunt in lengterichting
It_steiner_driehoek = A_driehoek*(((L3+(1/3)*L2)-LCF_transit)**2)   #gebruik hier ook zwaartepunt in lengterichting
It_transit_lengte = It_transit_lengte_ponton + It_transit_lengte_driehoek + It_steiner_ponton + It_steiner_driehoek
print('Traagheidsmoment transit in lengterichting',It_transit_lengte,'in [m^4]')


#deel2
print('deel 2 is beladen')
#beladen = onderkant schip onderwater zodat ander schip daarop kan (ondergedompeld)
#berekenen oppervlakte waterlijn Awl in onderdompeld
A_torens = (L1*B1)*2
A_driehoek = (L2*B2)*0.5
Awl_beladen = A_torens + A_driehoek
print('Oppervlakte waterlijn beladen is',Awl_beladen,'in [m^2]')

#traagheidsmoment van beladen waterlijn in dwarsrichting
#werken met steiner
It_beladen_dwars_torens = ((L1*(B1)**3)/12)*2
It_beladen_dwars_driehoek = (L2*(B3)**3)/48

A_toren = L1*B1
I_steiner_toren_dwars = A_toren*(((B3/2)-(B1/2))**2)        #steiner van de torens met de helft van de breedte - de helft van 1 toren
I_steiner_torens_dwars = I_steiner_toren_dwars*2

It_steiner_ponton = A_ponton*((B3/2)-(L3*0.5))**2 
It_steiner_driehoek = A_driehoek*(((L3+(1/3)*L2)-(B3/2))**2)
It_beladen_dwars = It_beladen_dwars_torens + It_beladen_dwars_driehoek + I_steiner_torens_dwars
print('Traagheidsmoment beladen in dwarsrichting is',It_beladen_dwars,'in [m^4]')

#drukkingspunt in lengterichting vanaf kont
G_torens = ((L1*0.5)*A_toren)*2               #oppervalkte toren * helft lengte ponten (*2)
G_driehoek = (L3+((1/3)*L2))*A_driehoek       #oppervalkte driehoek * lengte tot zwaartepunt driehoek vanaf kont
LCF_beladen = (G_torens + G_driehoek)/Awl_beladen
print('Drukkingspunt lengte beladen is',LCF_beladen,'in [m]')

#traagheidsmoment van transit waterlijn in lengterichting
#werken met steiner
It_beladen_lengte_torens = ((B1*(L1)**3)/12)*2
It_beladen_lengte_driehoek = (B2*(L2)**3)/36
It_steiner_torens = (A_toren*(LCF_beladen-(L1*0.5))**2)*2             #gebruik zwaartepunt in lengterichting
It_steiner_driehoek = A_driehoek*(((L3+(1/3)*L2)-LCF_beladen)**2)     #gebruik hier ook zwaartepunt in lengterichting
It_beladen_lengte = It_beladen_lengte_torens + It_beladen_lengte_driehoek + It_steiner_torens + It_steiner_driehoek
print('Traagheidsmoment beladen in lengterichting',It_beladen_lengte,'in [m^4]')

# Begin deel Romain
#torens achter
L1 = 16.2 
B1 = 3.5
D1 = 25.0      #bij deze opgave geen diepgang nodig

#boeg voor (driehoek)
L2 = 30.7
B2 = 43.8
D2 = 25.0     #zelfde diepgang als torens achter

#ponton
L3 = 210.3 + L2    #als er een driehoek voor zit is het L3 - L2
B3 = 43.8
D3 = 4.54

# Voor de XYZ coordinaten nemen we 1/2 L3 als het midden.
bodem = sc.Shape("rect", L3-L2, B3, D3, -L2/2, 0, 0)
toren1 = sc.Shape("rect", L1, B1, D1, -(L3/2)+(L1/2), (B2/2) - (B1/2), D3)
toren2 = sc.Shape("rect", L1, B1, D1, -(L3/2)+(L1/2), -(B2/2) + (B1/2), D3)
boeg = sc.Shape("triangle", L2, B2, D2, (L3/2)-(2*L2/3), 0, 0)

ship = sc.Ship()

ship.addShape(bodem)
ship.addShape(toren1)
ship.addShape(toren2)
ship.addShape(boeg)

print('deel 1 is transit')
print('Oppervlakte waterlijn transit is',ship.getArea(depth=1),'in [m^2]')
print('Traagheidsmoment transit in dwarsrichting is',ship.getxMOI(depth=1),'in [m^4]')
print('Drukkingspunt lengte transit is',ship.getxCentroid(depth=1) + L3/2,'in [m]')
print('Traagheidsmoment transit in lengterichting',ship.getyMOI(depth=1),'in [m^4]')

print('deel 2 is beladen')
print('Oppervlakte waterlijn beladen is',ship.getArea(depth=6),'in [m^2]')
print('Traagheidsmoment beladen in dwarsrichting is',ship.getxMOI(depth=6),'in [m^4]')
print('Drukkingspunt lengte beladen is',ship.getxCentroid(depth=6) + L3/2,'in [m]')
print('Traagheidsmoment beladen in lengterichting',ship.getyMOI(depth=6),'in [m^4]')
