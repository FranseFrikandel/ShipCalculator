

if __name__ == "__main__":
    errMargin = 1.005 # Foutmarge van 0,5% vanwege float rounding errors

    import shipCalculator as sc
    
    vorm = sc.Shape("rect", 50, 50, 10, 0, 0)
    ship = sc.Ship()
    ship.addShape(vorm)

    moi = 50**3 * 50 / 12
    assert (moi/errMargin) <= ship.getxMOI() <= (moi*errMargin)